/*
Generates the next segment of the story with an LLM, 
providing both known and unknown words as guidance.
*/
MERGE INTO educational_technology.mvp_project.user_story_segments AS t
USING(
    with
    
    review_words as (
    
        select word
        from educational_technology.mvp_project.flashcards
        where user_name = '{user_name}'
        order by next_review_scheduled_at_utc asc
        limit 3
    
    ),
    
    known_words as (
    
        select word
        from educational_technology.mvp_project.flashcards
        where user_name = '{user_name}'
        order by next_review_scheduled_at_utc desc, length(word) desc
        limit 10
    
    ),
    
    num_story_segments_read as (
    
        select max(story_segment_number) as num_preexisting_segments
        from educational_technology.mvp_project.user_story_segments
        where user_name = '{user_name}'
            and story_name = '{story_name}'
    
    ),
    
    original_story_segment as (
    
        select story_segment_text
        from educational_technology.mvp_project.original_story_segments
        where story_segment_number = (select num_preexisting_segments from num_story_segments_read) + 1
            and story_name = '{story_name}'
    
    ),
    
    combined as (
    
        select
            original_story_segment.story_segment_text,
            (select array_agg(word) from review_words) as review_words,
            (select array_agg(word) from known_words) as known_words
        from original_story_segment
        
    ),
    
    rewritten as (
    
        select
            story_segment_text,
            review_words,
            known_words,
            concat(
                'Please rewrite a story excerpt. Your rewrite should include at least one instance of the words: ',
                array_to_string(review_words, ', '),
                '. If any of those words are already in the story excerpt, you do not have to include them an additional time. ',
                'This rewrite should strive for clarity and cater towards a student whose current vocabulary is on par with the complexity of these words: ',
                array_to_string(known_words, ', '),
                '. Do not preface your response in any way. Only include the rewritten passage and rewrite the passage in the original language of the text. ',
                'It is also essential that you preserve the narrative thread of the passage. Change the text as little as possible to meet the requirements above, but if in doubt, lean towards adding content rather than taking any away. ',
                'The excerpt is: ',
                story_segment_text
            ) as prompt,
            snowflake.cortex.complete('llama3-70b', prompt) as next_story_segment
        from combined
    
    ),
    
    final as (
    
        select
            '{user_name}' as user_name,
            '{story_name}' as story_name,
            rewritten.next_story_segment as story_segment_text,
            ((select num_preexisting_segments from num_story_segments_read) + 1) as story_segment_number
        from rewritten
    
    )
    
    select * from final

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
