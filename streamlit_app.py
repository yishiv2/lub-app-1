import requests
import streamlit as st

# Set page configuration
st.set_page_config(page_title="関係性イメージアプリ", layout="centered")

# Add custom CSS
st.markdown(
    """
<style>
    body {
        font-family: 'Arial', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        color: #4CAF50;
        margin-bottom: 20px;
    }
    .date-selector {
        text-align: center;
        margin: 20px 0;
    }
    .question-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 10px 0;
    }
    .question-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        margin: 10px;
        background-color: #f9f9f9;
        text-align: center;
        width: 200px;
        height: 60px;
        position: relative;
    }
    .line {
        position: absolute;
        top: 50%;
        left: 100%;
        width: 30px;
        height: 1px;
        background-color: #4CAF50;
        transform: translateY(-50%);
    }
    .word {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
    }
    .answer {
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #f0f0f0;
        text-align: center;
        margin-top: 10px;
        color: #555;
    }
    .spacer {
        height: 50px;
    }
    .number {
        font-size: 1.2em;
        margin-right: 10px;
        align-self: center;
    }
</style>
""",
    unsafe_allow_html=True,
)

BASE_URL = "http://127.0.0.1:8000"

st.markdown('<div class="title">関係性イメージアプリ</div>', unsafe_allow_html=True)


# Step 1: Cache the API call to get available dates
@st.cache_data
def fetch_available_dates():
    response = requests.get(f"{BASE_URL}/word_sets/dates/")
    return response.json().get("available_dates", [])


# Step 2: Cache the API call to get word sets for the selected date
@st.cache_data
def fetch_word_sets_for_date(selected_date):
    response = requests.get(f"{BASE_URL}/word_sets/?date={selected_date}")
    return response.json()


# Fetch available dates
available_dates = fetch_available_dates()
available_dates.sort(reverse=True)

# Let the user select a date
selected_date = st.selectbox(
    "日付を選択してください",
    available_dates,
    key="date_selector",
    index=0,
)

# Fetch word sets if a date is selected
if selected_date:
    st.write(f"### 作成日: {selected_date}", unsafe_allow_html=True)

    daily_word_sets = fetch_word_sets_for_date(selected_date)

    if daily_word_sets:
        total_questions = len(daily_word_sets)
        st.write(f"全{total_questions}問")

        # Step 4: Display question cards with answer button
        for i in range(total_questions):
            selected_set = daily_word_sets[i]

            # Question container with number outside
            question_container = f"""
            <div class="question-container">
                <div class="number">{i + 1}</div>
                <div class="question-card">
                    <div class="word">{selected_set['word1']}</div>
                    <div class="line"></div>
                </div>
                <div class="question-card">
                    <div class="word">{selected_set['word2']}</div>
                </div>
            </div>
            """
            st.markdown(question_container, unsafe_allow_html=True)

            # Manage answer visibility
            answer_key = f"answer-{i}"
            if answer_key not in st.session_state:
                st.session_state[answer_key] = False  # Initial state is hidden

            # Answer button
            if st.button("答えを表示", key=f"answer-button-{i}"):
                st.session_state[answer_key] = not st.session_state[
                    answer_key
                ]  # Toggle visibility

            # Display answer if visible
            if st.session_state[answer_key]:
                st.markdown(
                    f"<div class='answer'>{selected_set['commonality']}</div>",
                    unsafe_allow_html=True,
                )

    # Extra space at the bottom
    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
