WITH
    
review_word AS (

    SELECT word
    FROM educational_technology.mvp_project.flashcards
    WHERE user_name = '{user_name}'
        AND next_review_scheduled_at_utc <= current_timestamp() -- new
    ORDER BY next_review_scheduled_at_utc ASC
    LIMIT 1

),

known_words AS (

    SELECT word
    FROM educational_technology.mvp_project.flashcards
    WHERE user_name = '{user_name}'
        -- review being at least three months out as proxy for knowing the word -- new
        AND next_review_scheduled_at_utc > dateadd(day, 90, current_date()) -- new
    ORDER BY
        next_review_scheduled_at_utc DESC,
        --and using word length as proxy for complexity -- new
        LENGTH(word) DESC
    LIMIT 10

),

num_story_segments_read AS (

    SELECT max(story_segment_number) AS num_preexisting_segments
    FROM educational_technology.mvp_project.user_story_segments
    WHERE user_name = '{user_name}'
        AND story_name = '{story_name}'

),

original_story_segment AS (

    SELECT story_segment_text
    FROM educational_technology.mvp_project.original_story_segments
    WHERE story_segment_number = (SELECT num_preexisting_segments FROM num_story_segments_read) + 1
        AND story_name = '{story_name}'

),

combined AS (

    SELECT
        original_story_segment.story_segment_text,
        (SELECT word FROM review_word) AS review_word,
        (SELECT array_agg(word) FROM known_words) AS known_words
    FROM original_story_segment
    
),

rewritten AS (

    SELECT
        story_segment_text,
        review_word,
        'Por favor reescribe un fragmento de historia para cumplir con estos criterios: ' AS intro_instruction,
        concat(
            '1. Simplifica el fragmento para que sea fácilmente leído por alguien que está leyendo en su segundo idioma. ',
            'Para darte una idea de cuánto debe simplificarse el fragmento, estas palabras representan el límite superior del vocabulario del estudiante: ',
            array_to_string(known_words, ', ')
        ) AS simplification_instruction,
        concat(
            ' 2. Incluye la siguiente palabra en el fragmento: ',
            review_word
        ) AS review_instruction,
        '. No antepongas tu respuesta de ninguna manera, solo incluye el fragmento reescrito. Por favor, conserva tanto como sea posible del lenguaje y la narrativa original. El fragmento es: ' AS concluding_instruction,
        iff(
            contains(story_segment_text, review_word), -- if review word isn't already in the excerpt
            concat(
                intro_instruction,
                simplification_instruction,
                concluding_instruction,
                story_segment_text
            ),
            concat(
                intro_instruction,
                simplification_instruction,
                review_instruction, -- include instructions to add it
                concluding_instruction,
                story_segment_text
            )
        ) AS prompt,
        iff(
            review_word IS NULL, -- if student has no reviews
            story_segment_text, -- they are capable of reading original text
            snowflake.cortex.complete('llama3-70b', prompt)
        ) AS next_story_segment
    FROM combined

),

final AS (

    SELECT
        '{user_name}' AS user_name,
        '{story_name}' AS story_name,
        rewritten.next_story_segment AS story_segment_text,
        ((SELECT num_preexisting_segments FROM num_story_segments_read) + 1) AS story_segment_number
    FROM rewritten

)

SELECT * FROM final
