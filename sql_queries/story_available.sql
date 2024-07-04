/*
Determines if a story is available to a user based on the story_name's presence in the stories table
*/
SELECT story_name
FROM educational_technology.mvp_project.stories
WHERE story_name = '{story_name}'
LIMIT 1
