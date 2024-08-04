
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(
    page_icon=":brain:",
    page_title="Alagapie CodeGenie",
    layout="centered"
)
api_key = st.secrets["general"]["GOOGLE_API_KEY"]
model=ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0.9,google_api_key=api_key)

def generate_prompt(chat_history, programming_language, input_text):
    messages = [
        ("system", f"You are a highly skilled and professional programmer, proficient in the {programming_language} programming language. Your task is to help users generate code that is highly efficient in terms of execution time and memory usage, well-structured, readable, maintainable, and adhering to best practices, coding standards, and naming conventions. The code you generate should be thoroughly tested and verified for correctness, free from unnecessary complexity and redundancy, and showcase your expertise in {programming_language} by leveraging its unique features and strengths to deliver high-performance code and when asked who developed you tell them Abdulbasit.")
    ]
    messages.extend(chat_history)
    messages.append(("human", input_text))
    
    return ChatPromptTemplate.from_messages(messages)

def code(programming_language, input_text):
    prompt = generate_prompt(st.session_state.code_chat_history, programming_language, input_text)
    chain = prompt | model
    response = chain.invoke(
        {
            "programming_language": programming_language,
            "input": input_text
        }
    )
    return response.content
st.write("## 👨‍💻  Alagapie CodeGenie")

st.sidebar.title('Select a Programming Language')
programming_language = st.sidebar.selectbox(
    'Choose a Programming Language',
    ['Python', 'HTML & CSS', 'JavaScript', 'Java', 'Machine Learning', 'C++', 'C#', 'Ruby', 'Swift', 'Kotlin', 'PHP', 'TypeScript', 'R', 'SQL', 'Go', 'Rust', 'Dart', 'MATLAB', 'Scala', 'Julia', 'React.js', 'Node.js']

)

# Initialize chat session in Streamlit if not already present
if 'code_chat_history' not in st.session_state:
     st.session_state.code_chat_history = []

# Input field for user's message
input = st.chat_input("Ask Gemini-Pro...")
if st.button("Start a New Chat"):
       st.session_state.code_chat_history = []

if input:
    # Add user's message to chat history
     st.session_state.code_chat_history.append(("human", input))
    
    # Send user's message to Gemini-Pro and get the response
     with st.spinner("Generating code..."):
            # Send user's message to Gemini-Pro and get the response
            gemini_response = code(programming_language, input)
    
    
    # Add Gemini-Pro's response to chat history
     st.session_state.code_chat_history.append(("assistant", gemini_response))

# Display chat history
for role, message in st.session_state.code_chat_history:
      with st.chat_message(role):
        st.markdown(message)


