from claude_api import Client
import streamlit as st
from st_pages import show_pages_from_config, add_page_title
show_pages_from_config()
claude_cookie = st.secrets["claude_cookie"]

st.set_page_config(
    page_title="Blog Post Generator",
    page_icon="📝",
)


st.title("📝 Blog Post Generator")

claude_api = Client(cookie=claude_cookie)

initial_prompt = """I would like you to write me a series of blogs mimicking my style, tone and language of writing, and also using my previously written content as a knowledge base where possible.
I have 22 blogs scraped to provide as examples. This is the perfect representation of my writing and also contain a good amount of knowledge. I can send this to you in a file.
I also have an e-book in txt. This is a good representation but it is not written in blog format, so not perfect. It does contain my general style of writing and a lot of knowledge.
You may also use your own knowledge where knowledge is not contained within my blogs or ebook.
Can you think through this step by step and come up with the best plan on how to achieve this. I would like the blogs to sound exactly like my writing and delivery quality content to my audience. The blog is for my company which is a garment design and development company that helps small and medium businesses with their garment manufacturing requirements in China.
"""

blog_title = st.text_area("Blog Title", placeholder="Enter blog title here")
submit = st.button("Generate")

if submit:
    if blog_title:
        with st.status("Generating blog...", expanded=True):
            conversation_id = claude_api.create_new_chat()['uuid']
            st.write("Sending initial prompt...")
            response = claude_api.send_message(initial_prompt, conversation_id)    
            st.write("Prompting file attachemnts...")
            response = claude_api.send_message("This is a great plan, which file would you like me to attach first?", conversation_id)
            st.write("Sending example blogs as reference...")
            response = claude_api.send_message("Here are the 22 example blogs that represent my writing:", conversation_id, attachment="rickblogs/Blog content.docx",timeout=600)
            st.write("Sending ebook as knowledge base...")
            response = claude_api.send_message("Make sure to use this ebook in txt format as a knowledge base as well, but don't use it as a basis for the writing style and tone.", conversation_id, attachment="rickblogs/ebook - garment manufacturing.txt", timeout=600)
            st.write("Writing comprehensive guide on writing style and tone...")
            response = claude_api.send_message("Okay sounds good. Write me a comprehensive guide on my writing style and any additional insights you noticed on the way I write and how my tone is.", conversation_id)
            st.write("Writing initial draft...")
            response = claude_api.send_message(f'Sounds good. Write me an initial draft that I could review, while keeping the analysis in mind. Here is your first blog title: "{blog_title}"', conversation_id)
            st.write("Incorporating anecdotes...")
            response = claude_api.send_message("Looks good! Make sure to incorporate anecdotes as well, and keep my writing style and tone as well from the given example blogs.", conversation_id)
            st.write("Writing final draft...")
            response = claude_api.send_message("Looks good! Now write me a final blog post that would be ready for posting", conversation_id)
            st.write("Blog post generated! 🎉")
        
        st.write(response)
        # prompt = st.text_input("Enter prompt here", placeholder="Enter modifications (shorten, elaborate, lengthen, etc.) here")
        # submit_prompt = st.button("Modify")
        # if submit_prompt:
        #     if prompt:
        #         respone = claude_api.send_message(prompt, conversation_id)
        #         st.write(response)
        #     else:
        #         st.error("Please enter a prompt")
    else: 
        st.error("Please enter a blog title")

