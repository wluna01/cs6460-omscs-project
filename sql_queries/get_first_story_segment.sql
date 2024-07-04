/*
Gets the first segment of the story
and writes it the user_story_segments table
*/

SELECT story_segment_text
FROM educational_technology.mvp_project.story_segments
WHERE story_name = '{story_name}'
ORDER BY story_segment_number ASC
LIMIT 1
