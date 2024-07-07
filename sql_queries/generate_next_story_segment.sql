/*
Generates the next segment of the story with an LLM, 
providing both known and unknown words as guidance.
*/
MERGE INTO educational_technology.mvp_project.user_story_segments AS t
USING(
    {query}
) AS s
    ON t.story_name = s.story_name
        AND t.user_name = s.user_name
        AND t.story_segment_number = s.story_segment_number
WHEN MATCHED THEN
    UPDATE SET
        t.story_segment_text = s.story_segment_text
WHEN NOT MATCHED THEN
    INSERT (
        user_name,
        story_name,
        story_segment_text,
        story_segment_number
    )
    VALUES (
        s.user_name,
        s.story_name,
        s.story_segment_text,
        s.story_segment_number
    )
