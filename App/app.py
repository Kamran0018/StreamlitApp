import streamlit as st
from openai import OpenAI

st.title("ProfessorGPT with Deepseek")
st.divider()

# Initialize the OpenRouter / Deepseek client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# User input
prompt = st.text_input("What concept do you want to learn about?")

# Session state to store responses
if 'full_lesson' not in st.session_state:
    st.session_state.full_lesson = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'hindi' not in st.session_state:
    st.session_state.hindi = None

# Step 1: Generate full lesson
if st.button("Teach Me"):
    if not prompt.strip():
        st.warning("Please enter a topic or concept first!")
    else:
        with st.spinner("Preparing your lesson..."):
            try:
                completion = client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3.1:free",
                    messages=[{"role": "user", "content": f"Teach me the following concept in detail: {prompt}"}]
                )
                st.session_state.full_lesson = completion.choices[0].message.content
                # Reset summary and Hindi for new topic
                st.session_state.summary = None
                st.session_state.hindi = None
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Step 2: Display full lesson if available
if st.session_state.full_lesson:
    st.success("Here's your lesson:")
    st.write(st.session_state.full_lesson)

    # Buttons for Summary and Hindi (Romanized)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Summary"):
            if not st.session_state.summary:
                with st.spinner("Generating summary..."):
                    try:
                        completion = client.chat.completions.create(
                            model="deepseek/deepseek-chat-v3.1:free",
                            messages=[{"role": "user", "content": f"Summarize the following text in easy English words: {st.session_state.full_lesson}"}]
                        )
                        st.session_state.summary = completion.choices[0].message.content
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            if st.session_state.summary:
                st.success("Summary (Easy English):")
                st.write(st.session_state.summary)

    with col2:
        if st.button("Hindi (Romanized)"):
            if not st.session_state.hindi:
                with st.spinner("Generating Romanized Hindi..."):
                    try:
                        completion = client.chat.completions.create(
                            model="deepseek/deepseek-chat-v3.1:free",
                            messages=[{"role": "user", "content": f"Translate the following text to Hindi, but write it in English letters (Romanized Hindi) only, do not use any English words except letters: {st.session_state.full_lesson}"}]
                        )
                        st.session_state.hindi = completion.choices[0].message.content
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            if st.session_state.hindi:
                st.success("Hindi Explanation (Romanized):")
                st.write(st.session_state.hindi)
