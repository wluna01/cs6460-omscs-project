/*
Retrieves the word that the user should review next.
*/
SELECT word
FROM educational_technology.mvp_project.flashcards
WHERE user_name = '{user_name}'
ORDER BY next_review_scheduled_at_utc DESC
LIMIT 1
