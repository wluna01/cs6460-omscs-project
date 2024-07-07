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

combined as (

    select
        original_story_segment.story_segment_text,
        (select word from review_word) as review_word,
        (select array_agg(word) from known_words) as known_words
    from original_story_segment
    
),

rewritten as (

    select
        story_segment_text,
        review_word,
        'Please rewrite a story excerpt to fulfill these criteria: ' AS intro_instruction,
        concat(
            '1. Simplify the excerpt to be easily read by a someone who is reading in their second language. ',
            'To give you a sense of how much the excerpt needs to be simplified, these words represent the upper limit of the student''s vocabulary: ',
            array_to_string(known_words, ', ')
        ) AS simplification_instruction,
        concat(
            '2. Include the following word in the excerpt: ',
            review_word
        ) AS review_instruction,
        'Do not preface your response in any way, only include the rewritten excerpt. Rewrite the excerpt in the original language of the text. Preserve the narrative in the excerpt. The excerpt is: ' as concluding_instruction,
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
