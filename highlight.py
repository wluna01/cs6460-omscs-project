import streamlit as st
import streamlit.components.v1 as components

# HTML and JavaScript for word interaction
def generate_text_with_js(text):
    words = text.split()
    html_words = ' '.join([f'<span class="hoverable">{word}</span>' for word in words])
    custom_html = f"""
    <html>
    <head>
        <style>
            .hoverable {{
                cursor: pointer;
                display: inline-block;
            }}
            .hoverable:hover {{
                background-color: yellow;
            }}
        </style>
    </head>
    <body>
        <div>{html_words}</div>
    </body>
    </html>
    """
    return custom_html

# Streamlit UI
st.title("Highlight on Hover")

text = "This is a sample passage where each word can be hovered over."

# Display text with custom JavaScript
html_content = generate_text_with_js(text)
components.html(html_content, height=200)
