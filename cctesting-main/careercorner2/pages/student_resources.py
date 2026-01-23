import streamlit as st
import os
from dotenv import load_dotenv
from services.langfuse_helper import LangfuseGeminiWrapper
from utils.database import get_saved_universities, load_reports
from utils.tools import (
    render_exam_papers_tool,
    render_scholarships_tool,
    render_study_resources_tool,
    render_career_options_tool,
    render_wage_finder_tool
)

load_dotenv()

# Gemini 2.5 Flash for chat mode
GEMINI_CHAT = LangfuseGeminiWrapper(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash"
)

def render_student_main_resources():
    """Main resource hub with tool buttons"""
    st.header("✄ Student Resources")
    st.markdown("Explore tools and resources to help with your academic journey")
    
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
            st.info("ⓘ Tip: For better personalized advice, try Degree Picker or Grades Analysis first!")
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
        
        if st.button("Study Resources", width="stretch"):
            st.session_state.active_tool = "study"
            st.rerun()
    
    with col2:
        if st.button("Scholarships",width="stretch", type="primary"):
            st.session_state.active_tool = "scholarships"
            st.rerun()
        
        if st.button("Career Options", width="stretch", type="primary"):
            st.session_state.active_tool = "careers"
            st.rerun()
    
    with col3:
        if st.button("Wage Finder", width="stretch", type="primary"):
            st.session_state.active_tool = "wages"
            st.rerun()
        
        if st.button("❤︎ Support Chat", width="stretch", type="primary"):
            st.session_state.resources_mode = "chat"
            st.rerun()
    
    st.divider()
    
    # Display selected tool
    if "active_tool" in st.session_state:
        
        st.markdown("---")
        
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


def render_student_resources_chat():
    """Supportive student advisor chat"""
    st.header("❤︎ Student Support Chat")
    st.info("Get personalized guidance, emotional support, and advice on study planning, degree selection, and academic improvement")
    
    user_id = st.session_state.get("username", "demo_user")
    
    degree_reports = load_reports(user_id, "degree")
    grades_reports = load_reports(user_id, "grades")
    
    col1, col2 = st.columns(2)
    with col1:
        if degree_reports:
            degree_options = {f"Degree: {r.get('title', 'Untitled')}": r for r in degree_reports}
            selected_degree = st.selectbox(
                "☰ Select Degree:", 
                options=list(degree_options.keys()), 
                index=0,
                key="selected_degree"
            )
            selected_degree_data = degree_options[selected_degree]
        else:
            selected_degree_data = None
            st.info("⚠︎ No degree recommendations")
    
    with col2:
        if grades_reports:
            grades_options = {f"Grades: {r.get('title', 'Untitled')}": r for r in grades_reports}
            selected_grades = st.selectbox(
                "☰ Select Grades:", 
                options=list(grades_options.keys()), 
                index=0,
                key="selected_grades"
            )
            selected_grades_data = grades_options[selected_grades]
        else:
            selected_grades_data = None
            st.info("⚠︎ No grades analysis")
    
    # Data summary
    data_summary = f"""Student Data ({user_id}):
• Degrees: {len(degree_reports)} available
• Grades: {len(grades_reports)} available"""
    
    # Internal context for AI
    internal_context = f"""You have access to this student's data:

SELECTED DEGREE: {selected_degree_data.get('title', 'None') if selected_degree_data else 'None'}
Degree Content: {selected_degree_data.get('content', 'No degree recommendations yet') if selected_degree_data else 'No degree recommendations yet'}

SELECTED GRADES: {selected_grades_data.get('title', 'None') if selected_grades_data else 'None'}
Grades Content: {selected_grades_data.get('content', 'No grades uploaded yet') if selected_grades_data else 'No grades uploaded yet'}"""
    
    welcome_message = f"""Hi! I'm here to support you on your academic journey!

{data_summary}

I can help you with:  
✦ **Study planning** based on your grades and goals  
✦ **Degree selection advice** using your recommendations  
✦ **Academic improvement strategies** personalized to your level  
✦ **Emotional support** and motivation  
✦ **Career guidance** and university choices  

What's on your mind today?"""
    
    if "student_resources_chat_history" not in st.session_state:
        st.session_state.student_resources_chat_history = [
            {"role": "assistant", "content": welcome_message}
        ]
    
    for msg in st.session_state.student_resources_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Ask for advice, support, or guidance..."):
        st.session_state.student_resources_chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("𖦹 Thinking..."):
                enriched_prompt = f"""{internal_context}

User question: {prompt}

INSTRUCTIONS:
- Be supportive, empathetic, and encouraging
- Reference their degree recommendations and grades specifically when relevant
- Help them make decisions about degrees, study plans, academic improvement
- Provide actionable advice and motivation
- Focus on guidance and emotional support
- For Portuguese students: consider DGES system, nacional exams, CIF scores"""
                
                response_text = GEMINI_CHAT.generate_content(
                    enriched_prompt,
                    user_id=user_id,
                    session_id="student_support_chat",
                    temperature=0.7
                )
                st.markdown(response_text)
        
        st.session_state.student_resources_chat_history.append({"role": "assistant", "content": response_text})
    
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⟲ Restart Chat", width='stretch'):
            st.session_state.student_resources_chat_history = [
                {"role": "assistant", "content": welcome_message}
            ]
            st.rerun()
    
    with col2:
        if st.button("← Back to Tools", width='stretch'):
            if "resources_mode" in st.session_state:
                del st.session_state.resources_mode
            st.rerun()


def render_student_resources():
    """Main entry point - toggle between tools and chat"""
    if st.session_state.get("resources_mode") == "chat":
        render_student_resources_chat()
    else:
        render_student_main_resources()
