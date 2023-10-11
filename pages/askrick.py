from claude_api import Client
import streamlit as st

claude_cookie = st.secrets["claude_cookie"]

st.set_page_config(
    page_title="Blog Post Generator",
    page_icon="📝",
)

st.title("❓ Ask Rick Anything!") 
st.write("---")
claude_api = Client(cookie=claude_cookie)
with st.chat_message("ai", avatar="👨"):
    st.write("Hi! I'm Rick! 👋")
    st.write("I'm a garment design and development expert. I can help you with your garment manufacturing requirements in China.")

initial_prompt = """Throughout the duration of our conversation, pretend you are Rick. Try mimicking my style, tone and language of writing, and also using my previously written content as a knowledge base where possible. Make sure that the answers are short and concise as well.

I will provide 22 example blogs which perfectly represent my writing.

I will also be providing an ebook, use it as a knowledge base as well, but don't use it as a basis for the writing style and tone.

Rick, also known as Richard Ward has a garment design and development company that helps small and medium businesses with their garment manufacturing requirements in China."""

prompt = st.chat_input("Ask a question!")
if prompt:
    with st.chat_message("human"):
        st.write(prompt)
    conversation_id = claude_api.create_new_chat()['uuid']
    with st.spinner('Processing...'):
            response = claude_api.send_message(initial_prompt, conversation_id, attachment="rickblogs/Blog content.docx", timeout=600)   
            response = claude_api.send_message("Here's the ebook, use it solely as a knowledge base, and don't use it as a basis for the writing style and tone. Now, pretend you are Rick.", conversation_id, attachment="rickblogs/ebook - garment manufacturing.txt", timeout=600)
            response = claude_api.send_message(prompt, conversation_id) 
    with st.chat_message("ai", avatar="👨"):
            st.write(response)