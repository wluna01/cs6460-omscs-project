/*
Determines if the user has already started reading a story
by virtue of whether the story user pair is present in the user_started_stories table
*/
SELECT user_name
FROM educational_technology.mvp_project.user_story_segments
WHERE user_name = '{user_name}'
    AND story_name = '{story_name}'
LIMIT 1
