# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
from datetime import datetime, timedelta
import nltk
from nltk.tokenize import word_tokenize

# Get the current credentials
session = get_active_session()

# Write directly to the app
st.title("La Tortuga Gigante")

#pull down text data
if 'stored_data' not in st.session_state:
    sql = f"select * from educational_technology.stories.la_tortuga_gigante"
    data = session.sql(sql).to_pandas()
    st.session_state.stored_data = data
    st.session_state.num_total_segments = len(data)

#initialize UI
if 'segment_number' not in st.session_state:
    st.session_state.segment_number = 0
if 'segments_displayed' not in st.session_state:
    st.session_state.segments_displayed = []
    first_segment = st.session_state.stored_data.iloc[st.session_state.segment_number]['SEGMENT_TEXT']
    st.session_state.segments_displayed.append(first_segment)
    st.session_state.segment_number += 1
if 'definition' not in st.session_state:
    st.session_state.definition = ""

def add_flashcard(): 
    current_time = datetime.now()
    next_review = current_time + timedelta(minutes=1)
    sql = f"""
        MERGE INTO vocabulary.wluna as t 
        USING (select '{unknown_word}' as word, 0 as num_consecutive_successful_reviews, '{current_time}' as last_reviewed_at_utc, '{next_review}' as next_review_due_at_utc) as s
        ON t.word = s.word
        WHEN MATCHED THEN
            UPDATE SET
                t.num_consecutive_successful_reviews = s.num_consecutive_successful_reviews,
                t.last_reviewed_at_utc = s.last_reviewed_at_utc,
                t.next_review_due_at_utc = s.next_review_due_at_utc
        WHEN NOT MATCHED THEN
            INSERT (word, num_consecutive_successful_reviews, last_reviewed_at_utc, next_review_due_at_utc)
            VALUES (s.word, s.num_consecutive_successful_reviews, s.last_reviewed_at_utc, s.next_review_due_at_utc)
    """
    #sql = f"""INSERT INTO vocabulary.wluna (word, num_consecutive_successful_reviews, last_reviewed_at_utc, next_review_due_at_utc) 
    #VALUES ('{unknown_word}', 0, '{current_time}', '{next_review}');"""
    #cursor = conn.cursor()
    #session.sql(sql)
    #cursor.execute(sql)
    session.sql(sql).collect()

def get_review_word():
    sql = f"""select word from vocabulary.wluna order by next_review_due_at_utc desc limit 1"""
    return session.sql(sql).collect()[0][0]

def on_click_continue():
    if st.session_state.segment_number < st.session_state.num_total_segments:
        #update flashcard model based on words read
        #tokens = word_tokenize(text)
        #then merge into the vocabulary table, doing nothing if no match found

        #generate next segment
        text = st.session_state.stored_data.iloc[st.session_state.segment_number]['SEGMENT_TEXT']
        review_word = get_review_word()
        prompt = f"""Please rewrite a story excerpt. Your rewrite should include at least one instance of the word: {review_word}. Do not preface your response in any way, only include the rewritten passage, and rewrite the passage in the original language of the text. The excerpt is: {text}"""
        sql = f"""select snowflake.cortex.complete('llama3-70b', '{prompt}')"""
        response = session.sql(sql).collect()[0][0]
        st.session_state.segments_displayed.append(response)
        st.session_state.segment_number += 1

def on_click_dictionary_lookup():
    if unknown_word:
        word_to_translate = unknown_word
        source_language = "es"
        target_language = "en"
        sql = f"""select snowflake.cortex.translate('{word_to_translate}', '{source_language}', '{target_language}')"""
        translation = session.sql(sql).collect()[0][0]
        st.session_state.definition = translation
        add_flashcard()
    else:
        st.session_state.definition = ""

i = 1
for segment in st.session_state.segments_displayed:
    st.write(i)   
    st.write(segment)
    i+=1

if st.session_state.segment_number < st.session_state.num_total_segments:
    st.button("Continuar", on_click=on_click_continue)
else:
    st.title("Fin")

unknown_word = st.text_input("Palabra Desconocida :thinking_face:", max_chars=20)
st.button("Buscar", on_click=on_click_dictionary_lookup)
definition_text = st.text(st.session_state.definition)
