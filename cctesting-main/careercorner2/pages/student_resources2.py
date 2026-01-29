import streamlit as st
import os
from dotenv import load_dotenv
from utils.database import get_saved_universities, load_reports
from services.tools import (
    render_exam_papers_tool,
    render_scholarships_tool,
    render_study_resources_tool,
    render_career_options_tool,
    render_wage_finder_tool,
    render_city_guide_tool
)

load_dotenv()

def render_student_main_resources():
    """Main resource hub with tool buttons"""
    st.header("✄ Student Resources")
    st.markdown("Explore tools and resources to help with your academic journey!")
    
    user_id = st.session_state.get("username", "demo_user")
    
    # Check if user has data
    has_data = False
    try:
        degree_reports = load_reports(user_id, "degree")
        grades_reports = load_reports(user_id, "grades")
        saved_unis = get_saved_universities(user_id)
        
        has_degree = len(degree_reports) > 0
        has_grades = len(grades_reports) > 0
        has_unis = len(saved_unis) > 0
        
        has_data = has_degree or has_grades or has_unis
        
        if has_data:
            st.success(f"✓ Loaded {len(degree_reports)} degrees, {len(grades_reports)} grades, {len(saved_unis)} unis")
        else:
            st.info("ⓘ Tip: For better results, try Degree Picker or Grades Analysis first!")
    except:
        pass
    
    st.divider()
    
    # Tool selection
    st.subheader("Choose a Tool:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Past Exam Papers", width="stretch", type="primary"):
            st.session_state.active_tool = "exams"
            st.rerun()
        
        if st.button("Study Resources", width="stretch", type="primary"):
            st.session_state.active_tool = "study"
            st.rerun()
    
    with col2:
        if st.button("Scholarships", width="stretch", type="primary"):
            st.session_state.active_tool = "scholarships"
            st.rerun()
        
        if st.button("Career Options", width="stretch", type="primary"):
            st.session_state.active_tool = "careers"
            st.rerun()
    
    with col3:
        if st.button("Wage Finder", width="stretch", type="primary"):
            st.session_state.active_tool = "wages"
            st.rerun()
        
        if st.button("City Guide", width="stretch", type="primary"):
            st.session_state.active_tool = "city"
            st.rerun()
    
    st.divider()
    
    # Display selected tool
    if "active_tool" in st.session_state:
        if st.session_state.active_tool == "exams":
            render_exam_papers_tool()
        elif st.session_state.active_tool == "scholarships":
            render_scholarships_tool()
        elif st.session_state.active_tool == "study":
            render_study_resources_tool()
        elif st.session_state.active_tool == "careers":
            render_career_options_tool()
        elif st.session_state.active_tool == "wages":
            render_wage_finder_tool()
        elif st.session_state.active_tool == "city":
            render_city_guide_tool()


def render_student_resources():
    """Main entry point"""
    render_student_main_resources()