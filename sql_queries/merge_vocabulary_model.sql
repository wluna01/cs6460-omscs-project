MERGE INTO educational_technology.mvp_project.flashcards AS t
USING (
    SELECT DISTINCT column1 AS word
    FROM (VALUES {cte_values})
) AS s
    ON t.word = s.word AND t.user_name = {user_name}
WHEN MATCHED THEN
    UPDATE SET
        t.num_consecutive_successful_reviews = t.num_consecutive_successful_reviews + 1,
        t.last_reviewed_at_utc = CURRENT_TIMESTAMP()::TIMESTAMP_NTZ,
        t.next_review_scheduled_at_utc = DATEADD(
            minute,
            POWER(t.num_consecutive_successful_reviews, 3),
            CURRENT_TIMESTAMP()::TIMESTAMP_NTZ
        )
WHEN NOT MATCHED THEN
    INSERT (
        user_name,
        word,
        num_consecutive_successful_reviews,
        last_reviewed_at_utc,
        next_review_scheduled_at_utc
    )
    VALUES (
        '{user_name}',
        s.word,
        10,
        CURRENT_TIMESTAMP()::TIMESTAMP_NTZ,
        DATEADD(
            day,
            180,
            CURRENT_TIMESTAMP()::TIMESTAMP_NTZ
        )
    )

