/*
Query to add a flashcard to the flashcards table.
If the word already exists, it will reset its study progress.
*/
MERGE INTO educational_technology.mvp_project.flashcards AS t
USING (
    SELECT
        '{user_name}' AS user_name,
        '{word}' AS word,
        0 AS num_consecutive_successful_reviews,
        '{current_time}' AS last_reviewed_at_utc,
        '{next_review}' AS next_review_scheduled_at_utc
) AS s
    ON t.word = s.word AND t.user_name = s.user_name
WHEN MATCHED THEN
    UPDATE SET
        t.num_consecutive_successful_reviews = s.num_consecutive_successful_reviews,
        t.last_reviewed_at_utc = s.last_reviewed_at_utc,
        t.next_review_scheduled_at_utc = s.next_review_scheduled_at_utc
WHEN NOT MATCHED THEN
    INSERT (
        user_name,
        word,
        num_consecutive_successful_reviews,
        last_reviewed_at_utc,
        next_review_scheduled_at_utc
    )
    VALUES (
        s.user_name,
        s.word,
        s.num_consecutive_successful_reviews,
        s.last_reviewed_at_utc,
        s.next_review_scheduled_at_utc
    )
