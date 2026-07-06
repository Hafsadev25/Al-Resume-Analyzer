import streamlit as st
import os
import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Personal Career Coach")
st.subheader("Upload Your Resume and Get Instant AI Feedback")

# SIDEBAR: API Key Input
st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("Enter Your Gemini API Key", type="password", help="Get free key: https://aistudio.google.com/app/apikey")

if api_key:
    genai.configure(api_key=api_key)
    st.sidebar.success("API Key Loaded ✅")
else:
    st.sidebar.warning("Demo Mode: You will get Demo Feedback without Key")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_ai_feedback(resume_text, job_role="General"):
    prompt = f"""
    You are an expert Career Coach and HR. Analyze the following resume for the role of '{job_role}'.
    Give feedback in this exact format:
    
    **1. Overall Score:** /100
    **2. Strengths:** 3 bullet points
    **3. Weaknesses:** 3 bullet points 
    **4. Suggestions for Improvement:** 5 actionable points
    **5. ATS Keywords to Add:** 10 keywords for this role
    
    Resume:
    {resume_text}
    """
    
    # TRY: Real API Call
    try:
        if not api_key:
            raise Exception("No API Key")
            
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
        
    # CATCH: If API fails or Quota ends - Show Demo
    except Exception as e:
        st.warning("⚠️ API Quota Exceeded or No Key. Showing Demo Feedback below.")
        
        demo_feedback = f"""
        **1. Overall Score: 78/100**
        
        **2. Strengths:**
        - Strong projects in Python and AI
        - Experience with Streamlit is in high demand
        - Clean resume structure
        
        **3. Weaknesses:**
        - Achievements are not quantified with numbers
        - Missing keywords from Job Description
        - Summary section is missing
        
        **4. Suggestions for Improvement:**
        - Start each point with an Action Verb like "Developed", "Built"
        - Add numbers like "Increased sales by 40%"
        - Add keywords from the job you are applying for
        - Add GitHub and LinkedIn link at the top
        - Keep it to 1 Page maximum
        
        **5. ATS Keywords to Add:**
        Python, Streamlit, FastAPI, REST API, Git, GitHub, AI, Machine Learning, Data Analysis, Problem Solving
        
        *Note: This is Demo Feedback. Enter API Key above for Real AI feedback.*
        """
        return demo_feedback

# MAIN APP
col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    job_role = st.text_input("Which Job Role to check for?", "Software Engineer")

with col2:
    st.header("2. AI Feedback")
    if st.button("🔍 Analyze Resume", type="primary"):
        if uploaded_file is not None:
            with st.spinner("AI is reading your Resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                feedback = get_ai_feedback(resume_text, job_role)
                
            st.success("Analysis Complete!")
            st.markdown(feedback)
        else:
            st.error("Please upload a PDF file first")

st.divider()
st.caption("Note: Get your free API Key from https://aistudio.google.com/app/apikey. 50 free requests per day.")