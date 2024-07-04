/*
Get the read user story segments
*/
SELECT
    story_segment_number,
    story_segment_text
FROM educational_technology.mvp_project.user_story_segments
WHERE user_name = '{user_name}'
    AND story_name = '{story_name}'
ORDER BY story_segment_number ASC
