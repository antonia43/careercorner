import os
import json
import streamlit as st
import io
from dotenv import load_dotenv
from services.langfuse_helper import LangfuseGeminiWrapper, get_user_id, get_session_id
from datetime import datetime
from utils.database import save_report, save_user_cv, load_reports
load_dotenv()

CV_SCHEMA = {
    "full_name": "What is the full name of the candidate?",
    "email": "What is the candidate's email address?",
    "phone": "What is the candidate's phone number?",
    "education": "List the candidate's education background.",
    "experience": "Summarize the candidate's professional experience.",
    "skills": "List the key technical and soft skills mentioned.",
    "languages": "Which languages does the candidate know?",
    "summary": "Summarize this CV in 3 sentences."
}

def _process_any_document(cv_text: str, prompt: str) -> str:
    """Processing CV text with Langfuse Gemini (no file upload needed)"""
    GEMINI = LangfuseGeminiWrapper(
        api_key=os.getenv("GOOGLE_API_KEY"), 
        model="gemini-2.5-flash"
    )
    
    full_prompt = f"{prompt}\n\nCV DATA:\n{cv_text[:8000]}"
    
    response = GEMINI.generate_content(
        prompt=full_prompt,
        temperature=0.3,
        user_id=get_user_id(),
        session_id=get_session_id(),
        metadata={"type": "cv_feedback"}
    )
    return response.strip()

def _extract_structured_from_document(uploaded_file, schema: dict):
    """Extracting structured CV data using Langfuse Gemini (BytesIO compatible)"""
    GEMINI = LangfuseGeminiWrapper(
        api_key=os.getenv("GOOGLE_API_KEY"), 
        model="gemini-2.5-flash"
    )
    
    # converting BytesIO/PDF to text (first 4000 chars)
    if hasattr(uploaded_file, 'getvalue'):
        file_content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
    else:
        file_content = str(uploaded_file)
    
    results = {}
    for key, question in schema.items():
        try:
            prompt = f"""
Extract ONLY this information from the CV below:
"{question}"

CV CONTENT:
{file_content[:4000]}

Return ONLY the extracted value, nothing else.
"""
            
            response = GEMINI.generate_content(
                prompt=prompt,
                temperature=0.1,
                user_id=get_user_id(),
                session_id=get_session_id(),
                metadata={"type": "cv_extraction", "field": key}
            )
            results[key] = response.strip()
            
        except Exception as e:
            results[key] = f"Error: {str(e)[:100]}"
    
    return {"success": True, "data": results}

def render_cv_analysis():
    st.header("⛶ CV Analysis")
    
    # LOGIN CHECK
    # if "username" not in st.session_state:
        #st.warning("⚠︎ Please log in first!")
        #return
    
    user_id = st.session_state.username
    
    # loading CV reports
    if "reports" not in st.session_state:
        st.session_state.reports = {}
    st.session_state.reports["professional_cv"] = load_reports(user_id, "professional_cv")
    
    cv_sources = ["Upload New CV"] + [r["title"] for r in st.session_state.reports["professional_cv"]]
    source_choice = st.selectbox(
        "Choose CV source:", 
        cv_sources,
        key="cv_analysis_source_choice"
    )
    
    # case 1 is using existing CV from reports
    if source_choice != "Upload New CV":
        cv_report = next((r for r in st.session_state.reports["professional_cv"] if r["title"] == source_choice), None)
        if cv_report:
            st.session_state.cv_data = cv_report["cv_data"]
            st.success(f"Loaded CV from: **{source_choice}**")
            st.subheader("CV Data")
            for key, value in st.session_state.cv_data.items():
                st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        else:
            st.error("CV not found!")
            return
    
    # case 2 is uploading new CV
    else:
        uploaded = st.file_uploader(
            "Upload your CV (PDF or DOCX)", 
            type=["pdf", "docx"],
            key="cv_upload_file"
        )
        if not uploaded:
            st.info("Upload your CV to get structured analysis and feedback.")
            return
        
        st.success(f"Uploaded: {uploaded.name}")
        
        #processing uploaded file
        file_buffer = io.BytesIO(uploaded.read())
        results = _extract_structured_from_document(file_buffer, CV_SCHEMA)
        
        if not results.get("success"):
            st.error("Could not process CV.")
            return
        
        # storing new CV data
        st.session_state.cv_data = {
            "full_name": results["data"].get("full_name", ""),
            "experience_summary": results["data"].get("experience", ""),
            "skills": results["data"].get("skills", ""),
            "education": results["data"].get("education", ""),
            "languages": results["data"].get("languages", ""),
            "summary": results["data"].get("summary", ""),
        }
        
        save_user_cv(user_id, st.session_state.cv_data)
        
        st.subheader("Extracted information")
        for key, value in st.session_state.cv_data.items():
            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # generating feedback for the CV
    st.subheader("✪ Summary & Feedback")
    if st.button("⏻ Generate Analysis", use_container_width=True, key="cv_generate_analysis"):
        cv_text = json.dumps(st.session_state.cv_data, indent=2)
        feedback = _process_any_document(
            cv_text,
            "Analyze this CV data for a professional and provide clear, constructive feedback on strengths and areas for improvement."
        )
        
        st.session_state.current_feedback = feedback
        st.markdown(feedback)
    
    # showing previous feedback if exists
    if hasattr(st.session_state, 'current_feedback'):
        st.markdown("---")
        st.info("**Previous analysis:**")
        st.markdown(st.session_state.current_feedback)
    
    # saving to reports
    if hasattr(st.session_state, 'current_feedback'):
        if st.button("🗂️ Save this analysis to My Reports", use_container_width=True, key="cv_save_report"):
            report_id = save_report(
                user_id=user_id,
                report_type="professional_cv",
                title=f"CV Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                content=st.session_state.current_feedback,
                cv_data=st.session_state.cv_data
            )
            st.success("✓ Saved to My Reports!")
            st.balloons()
            st.rerun()
