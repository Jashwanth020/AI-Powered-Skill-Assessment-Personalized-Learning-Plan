"""
Catalyst - Streamlit Web Application
AI-Powered Skill Assessment & Personalized Learning Plan Agent
"""

import streamlit as st
import json
from datetime import datetime
from agent_engine import CatalystAgent
import os
from io import StringIO

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

st.set_page_config(
    page_title="Catalyst - Skill Assessment Agent",
    page_icon="",
    layout="wide"
)

SAMPLE_JD = """
Software Engineer - Machine Learning

Requirements:
- 3+ years Python development experience
- Experience with ML frameworks (TensorFlow, PyTorch)
- Strong SQL and database design skills
- Cloud platforms experience (AWS or GCP)
- Experience with REST APIs and microservices
- Strong problem-solving skills
- Excellent communication skills
- BS/MS in Computer Science or related field
"""

SAMPLE_RESUME = """
John Smith - Senior Software Developer

Experience:
- 5 years Python development (Django, Flask, FastAPI)
- Built REST APIs serving 1M+ requests/day for e-commerce
- MySQL and PostgreSQL database design and optimization
- AWS certified Solutions Architect
- Led team of 4 developers at TechCorp
- Computer Science degree from State University

Skills: Python, Django, Flask, SQL, MySQL, PostgreSQL, AWS, REST APIs, Git
"""


def init_session():
    if "catalyst_agent" not in st.session_state:
        api_key = os.environ.get("GROQ_API_KEY", st.session_state.get("api_key", ""))
        if api_key:
            st.session_state.catalyst_agent = CatalystAgent(api_key)
    
    if "results" not in st.session_state:
        st.session_state.results = None


def read_uploaded_file(uploaded_file):
    """Read text from uploaded file (txt or pdf)"""
    if uploaded_file is None:
        return ""
    
    file_type = uploaded_file.name.lower()
    
    if file_type.endswith('.pdf') and PyPDF2:
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
    elif file_type.endswith('.txt'):
        return uploaded_file.read().decode('utf-8')
    else:
        try:
            return uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            try:
                return uploaded_file.read().decode('latin-1')
            except:
                return uploaded_file.read().decode('utf-8', errors='ignore')


def get_score_color(score):
    if score >= 70:
        return "green"
    elif score >= 45:
        return "orange"
    else:
        return "red"


def get_score_label(score):
    if score >= 81:
        return "Expert"
    elif score >= 61:
        return "Advanced"
    elif score >= 41:
        return "Intermediate"
    elif score >= 21:
        return "Beginner"
    else:
        return "Novice"


def main():
    init_session()
    
    st.title("Catalyst")
    st.markdown("### AI-Powered Skill Assessment & Personalized Learning Plan")
    
    with st.sidebar:
        st.header("Configuration")
        
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Enter your Groq API key",
            key="api_key_input"
        )
        
        if api_key and not hasattr(st.session_state, "catalyst_agent"):
            st.session_state.catalyst_agent = CatalystAgent(api_key)
            st.success("API Key configured!")
        
        st.divider()
        
        st.subheader("Sample Data")
        if st.button("Load Sample JD + Resume"):
            st.session_state["sample_jd"] = SAMPLE_JD
            st.session_state["sample_resume"] = SAMPLE_RESUME
            st.rerun()
        
        if st.button("Clear Results"):
            st.session_state.results = None
            st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Job Description")
        jd_file = st.file_uploader("Upload JD (PDF/TXT)", type=['pdf', 'txt'], key="jd_file")
        if jd_file:
            job_description = read_uploaded_file(jd_file)
            st.success(f"Loaded: {jd_file.name}")
        else:
            job_description = st.text_area(
                "Or paste job description",
                height=250,
                key="job_desc",
                placeholder="Paste job description here..."
            )
    
    with col2:
        st.subheader("Resume")
        resume_file = st.file_uploader("Upload Resume (PDF/TXT)", type=['pdf', 'txt'], key="resume_file")
        if resume_file:
            resume = read_uploaded_file(resume_file)
            st.success(f"Loaded: {resume_file.name}")
        else:
            resume = st.text_area(
                "Or paste resume",
                height=250,
                key="resume_input",
                placeholder="Paste resume here..."
            )
    
    if st.button("Analyze Skills", type="primary", use_container_width=True):
        if not job_description or not resume:
            st.error("Please provide both job description and resume")
        elif not hasattr(st.session_state, "catalyst_agent"):
            st.error("Please configure your Groq API key")
        else:
            with st.spinner("Analyzing skills..."):
                try:
                    results = st.session_state.catalyst_agent.assess(job_description, resume)
                    st.session_state.results = results
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    if st.session_state.results:
        results = st.session_state.results
        
        st.divider()
        st.header("Assessment Results")
        
        summary = results.get("summary", {})
        
        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Skills Required", summary.get("total_skills_required", 0))
        col_b.metric("Skills Strong", summary.get("skills_strong", 0), delta_color="normal")
        col_c.metric("Skills Gapped", summary.get("skills_gapped", 0), delta_color="inverse")
        col_d.metric("Learning Hours", f"{summary.get('total_learning_hours', 0)}h")
        
        tab1, tab2, tab3 = st.tabs(["Skill Assessment", "Gap Analysis", "Learning Plan"])
        
        with tab1:
            st.subheader("Skill Proficiency Scores")
            
            for assessment in results.get("assessments", []):
                skill = assessment.get("skill", "")
                score = assessment.get("score", 0)
                level = assessment.get("level", "")
                evidence = assessment.get("evidence", "")
                reasoning = assessment.get("reasoning", "")
                
                color = get_score_color(score)
                
                with st.container():
                    col_s1, col_s2 = st.columns([1, 4])
                    
                    with col_s1:
                        st.markdown(f"**{skill}**")
                        st.markdown(f":{color}[{score}/100]")
                        st.caption(level)
                    
                    with col_s2:
                        st.caption(evidence)
                        if reasoning:
                            st.caption(f"*{reasoning}*")
                    
                    st.divider()
        
        with tab2:
            gap_analysis = results.get("gap_analysis", {})
            
            st.subheader("Critical Gaps")
            critical = gap_analysis.get("critical_gaps", [])
            if critical:
                for gap in critical:
                    with st.container():
                        st.markdown(f"**{gap['skill']}**")
                        st.progress(gap["gap_size"] / 100)
                        st.caption(f"Gap: {gap['gap_size']} points | Learnability: {gap.get('learnability_score', 'N/A')}/100")
            else:
                st.success("No critical gaps found!")
            
            st.subheader("Adjacent Opportunities")
            adjacent = gap_analysis.get("adjacent_opportunities", [])
            if adjacent:
                for opp in adjacent:
                    st.markdown(f"**{opp['current_skill']}** -> **{opp['adjacent_skill']}**")
                    st.caption(f"Correlation: {opp.get('correlation', '')}")
            else:
                st.info("No adjacent opportunities identified")
        
        with tab3:
            learning_plan = results.get("learning_plan", [])
            
            if learning_plan:
                for item in learning_plan:
                    with st.expander(f"Priority {item.get('priority', '')}: {item.get('skill', '')}", expanded=True):
                        st.markdown(f"**Timeline:** {item.get('weeks', '')} ({item.get('total_hours', 0)} hours)")
                        st.markdown(f"**Target:** {item.get('target_proficiency', '')}")
                        st.markdown(f"**First Step:** {item.get('actionable_first_step', '')}")
                        
                        st.markdown("**Resources:**")
                        for resource in item.get("resources", []):
                            cost_badge = "Free" if resource.get("cost") == "free" else "Paid"
                            st.markdown(f"- {resource.get('name')} ({resource.get('type', '')}) {cost_badge} - {resource.get('hours', 0)}h")
                        
                        st.markdown("**Milestones:**")
                        for milestone in item.get("milestones", []):
                            st.markdown(f"- {milestone}")
            else:
                st.info("No learning plan generated")
        
        with st.expander("View Raw JSON"):
            st.json(results)


if __name__ == "__main__":
    main()