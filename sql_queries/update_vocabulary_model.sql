WITH

updated_vocab AS (
    
    SELECT word
    FROM (VALUES {cte_values}) AS T(word)

),

existing_vocab AS (

    SELECT *
    FROM educational_technology.mvp_project.flashcards
    WHERE user_name = '{user_name}'

),

joined AS (

    SELECT
       '{user_name}' AS user_name,
       updated_vocab.word,
        -- determines if the word is new
        iff(
            existing_vocab.word IS NULL,
            True,
            False
        ) AS is_new,
        -- if the word is new, set the number of consecutive successful reviews to 10
        -- to indicate being cemented in long-term memory
        iff(
            is_new, -- if the word is new
            10, -- set the number of consecutive successful reviews to 10 (simulate long-term memory)
            existing_vocab.num_consecutive_successful_reviews + 1 -- if the word is not new, increment the number of consecutive successful reviews
        ) AS num_consecutive_successful_reviews,
        iff(
            is_new, -- if the word is new
            CURRENT_TIMESTAMP()::TIMESTAMP_NTZ, -- simulate this review as just in time
            existing_vocab.next_review_scheduled_at_utc -- otherwise use existing scheduled review time
        ) as next_review_scheduled_at_utc,
        CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS last_reviewed_at_utc
    FROM updated_vocab
    LEFT JOIN existing_vocab
        ON updated_vocab.word = existing_vocab.word

),

final AS (

    SELECT
        * exclude (next_review_scheduled_at_utc),
        -- next review is replaced by naive exponential scheduling
        DATEADD(
            minute,
            POWER(num_consecutive_successful_reviews, 3),
            next_review_scheduled_at_utc
        ) AS next_review_scheduled_at_utc
    FROM joined

)

SELECT
    user_name,
    word,
    num_consecutive_successful_reviews,
    last_reviewed_at_utc,
    next_review_scheduled_at_utc
FROM final
