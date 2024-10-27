import google.generativeai as genai
import streamlit as st
import time


# Configure the Gemini API
genai.configure(api_key="AIzaSyD9oeJ_5I26O4SX4v2KjNwNtMElj-dYvBM")

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

# Function to get responses from the Gemini model
def gemini(prompt):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            convo = model.start_chat(history=[])
            convo.send_message(prompt)
            return convo.last.text
        except Exception as e:
            # Log the error for debugging
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if "429" in str(e):  # Check for rate limit errors
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
                time.sleep(wait_time)  # Wait before retrying
            else:
                st.error("Error while generating response. Please try again later.")
                return None

    st.error("Max retries exceeded. Please try again later.")
    return None

def leo_ai():
    st.title("Leo - Your AI Assistant")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message['role'] == 'user':
            st.chat_message("User").markdown(message['content'])
        else:
            st.chat_message("Leo").markdown(message['content'])

    prompt = st.chat_input("I'm all ears... Leo is here...")
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        result = gemini(prompt)
        
        if result:
            st.session_state.messages.append({"role": "leo", "content": result})

        # Clear the input box after submission
        st.rerun()  # Rerun to update the UI

def home():
        st.title(":rainbow[Mood Journal] 🎨 🖌")
        st.caption("Your Personal Growth Canvas: Log your daily moods and receive tailored suggestions to enhance your soft skills. Transform your emotional insights into a masterpiece of personal development!")
        st.write("")
        st.write("")
        st.sidebar.caption("An AF's Endeavour, developed with 💡 and 🥤.!")        

def about():
    st.write("About")

def settings():
    st.write("Settings")


def moodjournal():
    page_1_home = st.Page(
        home,
        title="Home",
        icon=":material/home:",
        default=True,
    )
                
    page_2_about = st.Page(
        about,
        title="About",
        icon=":material/person:",
    )
    page_3 = st.Page(
        leo_ai,
        title="MoodCanvas Assistant",
        icon=":material/smart_toy:"
    )
    page_4 = st.Page(
        settings,
        title="Settings",
        icon=":material/manage_accounts:"
    )

    # NAVIGATION SETUP
    #if st.session_state.get('authentication_status'):
    book = st.navigation(
        {   "": [page_1_home],
            "Info": [page_2_about, page_4],
            "Your Canvas Space": [page_3],
        }
    )
    book.run()

if __name__ == '__main__':
    moodjournal()
