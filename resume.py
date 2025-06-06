import os
import streamlit as st
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# --- Load GitHub Token ---
load_dotenv()
token = os.getenv("GITHUB_TOKEN")

# --- Setup DeepSeek AI Client ---
endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# --- DeepSeek ask function ---
def ask_deepseek(prompt: str) -> str:
    try:
        response = client.complete(
            messages=[
                SystemMessage("You are a professional resume reviewer and builder AI."),
                UserMessage(prompt),
            ],
            temperature=0.7,
            top_p=0.9,
            max_tokens=1024,
            model=model,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# --- Streamlit App Starts ---
st.set_page_config(page_title="🧠 Smart Resume Checker & Builder", layout="wide")

st.title("📝 AI-Powered Resume Checker & Builder")
st.write("Upload, Review, Improve, and Download your Resume securely with AI Agents! 🚀")

# --- Upload Section ---
st.header("📤 Upload Your Resume (TXT format)")

uploaded_file = st.file_uploader("Choose a TXT file with your resume content", type=["txt"])

if uploaded_file:
    resume_text = uploaded_file.read().decode("utf-8")
    st.subheader("🧾 Uploaded Resume Preview:")
    st.text(resume_text)

    # Save uploaded resume into session state
    st.session_state["uploaded_resume"] = resume_text

# --- Actions Section ---
if "uploaded_resume" in st.session_state:

    st.markdown("---")
    st.header("⚡ AI Actions for Your Resume")

    col1, col2, col3 = st.columns(3)

    # --- Fraud Detection ---
    with col1:
        if st.button("🚨 Check for Fraud / Fake Claims"):
            with st.spinner("Analyzing for potential fraud..."):
                fraud_prompt = f"""
                Carefully review the following resume for any fraudulent claims, inconsistencies, unrealistic achievements, or exaggerations. 
                Mark them clearly and suggest corrections. Resume:\n\n{st.session_state['uploaded_resume']}
                """
                fraud_report = ask_deepseek(fraud_prompt)
                st.subheader("🚨 Fraud Detection Report:")
                st.write(fraud_report)
                st.session_state["fraud_report"] = fraud_report

    # --- Resume Improvement ---
    with col2:
        if st.button("✨ Improve My Resume"):
            with st.spinner("Polishing and optimizing your resume..."):
                improve_prompt = f"""
                Rewrite and professionally improve this resume.
                Focus on clarity, impact, formatting, and keywords (ATS friendly).
                Make it truthful, concise, and appealing for recruiters.\n\nResume:\n\n{st.session_state['uploaded_resume']}
                """
                improved_resume = ask_deepseek(improve_prompt)
                st.subheader("✨ Improved Resume:")
                st.text(improved_resume)
                st.session_state["improved_resume"] = improved_resume

    # --- Create New Resume from Scratch ---
    with col3:
        if st.button("🛠️ Create New Resume (AI)"):
            with st.spinner("Building a fresh professional resume..."):
                create_prompt = """
                Create a modern, professional resume template suitable for data science, tech, or business roles.
                Leave placeholders for name, experience, education, and skills.
                """
                new_resume = ask_deepseek(create_prompt)
                st.subheader("🛠️ New AI-Generated Resume Template:")
                st.text(new_resume)
                st.session_state["new_resume"] = new_resume

# --- Download Section ---
st.markdown("---")
st.header("📥 Download Your Resume")

if "improved_resume" in st.session_state:
    st.download_button(
        label="Download Improved Resume",
        data=st.session_state["improved_resume"],
        file_name="Improved_Resume.txt",
        mime="text/plain",
    )

if "new_resume" in st.session_state:
    st.download_button(
        label="Download New Resume Template",
        data=st.session_state["new_resume"],
        file_name="New_Resume_Template.txt",
        mime="text/plain",
    )

# --- Live Chatbot for Resume Advice ---
st.markdown("---")
st.header("💬 Resume Advisor Chatbot")
st.write("Ask anything about resumes, job applications, or interviews!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Your question about resumes or job hunting...")

if st.button("Ask Advisor"):
    if user_query:
        with st.spinner("Thinking..."):
            chat_prompt = f"You are a career and resume advisor AI. User asks: {user_query}"
            bot_reply = ask_deepseek(chat_prompt)
            st.session_state.chat_history.append(("You", user_query))
            st.session_state.chat_history.append(("AI", bot_reply))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 AI:** {message}")