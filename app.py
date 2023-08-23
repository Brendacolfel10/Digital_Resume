from pathlib import Path
import openai
import streamlit as st
from PIL import Image
import os

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles"/ "main.css"
resume_file = current_dir / "assets" / "cv.pdf"
profile_pic = current_dir / "assets" / "profile-pic.png"


#--- GENERAL SETTINGS ---
PAGE_TITLE = "Digital CV | Brenda Colorado Felix"
PAGE_ICON = ":wave:"
NAME = "Brenda Colorado Felix"
DESCRIPTION = """
Highly skilled Office Administrator with an impressive background specializing in administrative work and office support
"""
EMAIL = "Brenda.colfel10@gmail.com"
SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/brenda-colorado-felix-b28413263/",
    "Github": "https://github.com/Brendacolfel10",
    "Replit": "https://replit.com/@BrendaColorado",
}


st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


#---LOAD CSS, PDF & PORFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
with open(resume_file, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
        profile_pic = Image.open(profile_pic)      


# --- hero section ---
col1, col2 = st.columns(2, gap="small")
with col1:
      st.image(profile_pic,caption="Support Engineer", width=230)

with col2:
      st.title(NAME)
      st.write(DESCRIPTION)
      st.download_button(
            label=" 📄 Download Resume",
            data=PDFbyte,
            file_name=resume_file.name,
            mime="application/octet-sistem",
      )
      st.write("📫", EMAIL)


#---SOCIAL LINKS---
st.write("#")
cols = st.columns(len(SOCIAL_MEDIA))
for index, (plataform, link) in enumerate(SOCIAL_MEDIA.items()):
      cols[index].write(f"[{plataform}]({link})")

#--- EXPERIENCE & QUALIFICATIONS ---
st.write("#")
st.subheader("Experience & Qualifications")
st.write(
      """
 - ✔️ Excellent team-player and displaying strong sense of initiative on tasks
 - ✔️ Experience and knowledge in python and excel
 - ✔️ Good understending of satisfacial principles and their respective applications
 - ✔️ Experience extracting actionable insigths from data
 - ✔️ Able to handle multiple customer inquiries simultaneously without compromising on the quality of support
 - ✔️ Willingness to share knowledge and best practices within the support team for continuous improvement 
 - ✔️ Strong desire to learn and stay updated with the latest technologies and industry trends
 - ✔️ Experienced in conducting product training sessions to enhance customer understanding and self-sufficiency
 - ✔️ Proficient in conflict resolution and maintaining professionalism during challenging situations
"""
)


# --- SKILLS ---

st.write("#")
st.subheader("Hard Skills")
st.write(
      """
 - 👩‍💻 Programing: python (Scikit-learn, Pandas), SQL, VBA  
 - 📊 Data Visualization: powerBi, MS Excel, Plotly
 - 📚 Modeling: Logistic regression, linear regression, decition trees
 - 🗄️ Databases: Postgres, MongoDB, MySQL
 - 🚧 Troubleshooting and issue resolution
"""
)



#--- chatGPT ---



st.title("ChatGPT-like clone")

openai.api_key = st.secrets["OPENAI_API_KEY"]
st.write(
    "Has environment variables been set:",
    os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"],
)
print(f'OS ENVIRON: {os.environ["OPENAI_API_KEY"]}\nSTREAMLIT SECRET: {st.secrets["OPENAI_API_KEY"]}')
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})