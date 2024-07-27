[![Open in Streamlit Cloud](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cs6460-omscs-project.streamlit.app/)

# GRALE
### Graded Reading through an Adaptive Language Environment

![UI Intro](readme_image.png)

### Description
Application that presents novels and short stories with optional read-along transcriptions.

As the reader looks up unknown vocabulary with the built-in dictionary, the application builds a model of their vocabulary. This vocabulary model then informs an LLM which rewrites subsequent passages to cater to the reader's current level. Unknown words are added into subsequent passages following a Spaced Repetition Scheduler (SRS) to cement those words in long-term memory.

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

### Secrets Management
GRALE requires secrets from Snowflake, Merriam Webster, and Google Cloud. See the `example_secrets.toml` file for details.
