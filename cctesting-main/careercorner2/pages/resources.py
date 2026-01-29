import streamlit as st
import os
from dotenv import load_dotenv
from google.genai import types
from services.langfuse_helper import LangfuseGeminiWrapper
from utils.database import load_reports
from services.tools import (
    render_job_search_tool,
    render_course_finder_tool,
    render_wage_finder_tool,
    render_linkedin_optimizer_tool,
    render_company_research_tool
)

from services.professional_tools import PROFESSIONAL_TOOLS, execute_function_call

load_dotenv()

GEMINI_CHAT = LangfuseGeminiWrapper(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash"
)

def render_main_resources():
    """Main professional resource hub"""
    st.header("Career Resources")
    st.markdown("Tools and resources to advance your professional journey")
    
    user_id = st.session_state.get("username", "demo_user")
    
    # Optional data check (not mandatory)
    has_cv = bool(st.session_state.get("cv_data"))
    has_quiz = bool(st.session_state.get("quiz_result"))
    
    if has_cv or has_quiz:
        st.success("Loaded your CV and career data for personalized support!")
    else:
        st.info("ⓘ Complete CV Analysis or Career Quiz for more personalized guidance!")
    
    st.divider()
    
    # Tool selection buttons
    st.subheader("Choose a Tool:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Job Search", width="stretch", type="primary"):
            st.session_state.active_pro_tool = "jobs"
            st.rerun()
        
        if st.button("LinkedIn Optimizer", width="stretch", type="primary"):  # Changed
            st.session_state.active_pro_tool = "linkedin"  # Changed
            st.rerun()
            
    with col2:
        if st.button("Course Finder", width="stretch", type="primary"):
            st.session_state.active_pro_tool = "courses"
            st.rerun()
        
        if st.button("Company Research", width="stretch", type="primary"):  # Changed
            st.session_state.active_pro_tool = "company"  # Changed
            st.rerun()
    
    with col3:
        if st.button("Wage Finder", width="stretch", type="primary"):
            st.session_state.active_pro_tool = "wages"
            st.rerun()
        
        if st.button("❤︎ Career Support Chat", width="stretch"):
            st.session_state.resources_mode = "chat"
            st.rerun()
    
    st.divider()
    
    # display selected tool
    if "active_pro_tool" in st.session_state:
        

        
        if st.session_state.active_pro_tool == "jobs":
            render_job_search_tool()
        elif st.session_state.active_pro_tool == "courses":
            render_course_finder_tool()
        elif st.session_state.active_pro_tool == "wages":
            render_wage_finder_tool()
        elif st.session_state.active_pro_tool == "linkedin":  # Changed
            render_linkedin_optimizer_tool()  # Changed
        elif st.session_state.active_pro_tool == "company":
            render_company_research_tool()



def render_resources_chat():
    """Career support chat WITH function calling for skill gaps and roadmaps"""
    st.header("❤︎ Career Support Chat")

    user_id = st.session_state.get("username", "demo_user")
    
    cv_reports = load_reports(user_id, "professional_cv")
    quiz_reports = load_reports(user_id, "professional_career_quiz")
    
    col1, col2 = st.columns(2)
    with col1:
        if cv_reports:
            cv_options = {f"CV: {r.get('title', 'Untitled')}": r for r in cv_reports}
            selected_cv = st.selectbox(
                "☰ Select CV:", 
                options=list(cv_options.keys()), 
                index=0,
                key="selected_cv"
            )
            selected_cv_data = cv_options[selected_cv]
        else:
            selected_cv_data = None
            st.info("⚠︎ No CV analysis")
    
    with col2:
        if quiz_reports:
            quiz_options = {f"Quiz: {r.get('title', 'Untitled')}": r for r in quiz_reports}
            selected_quiz = st.selectbox(
                "☰ Select Quiz:", 
                options=list(quiz_options.keys()), 
                index=0,
                key="selected_quiz"
            )
            selected_quiz_data = quiz_options[selected_quiz]
        else:
            selected_quiz_data = None
            st.info("⚠︎ No career quiz")
    
    # data summary
    data_summary = f"""Professional Data ({user_id}):
• CVs: {len(cv_reports)} available
• Quizzes: {len(quiz_reports)} available"""
    
    # internal context for the ai
    internal_context = f"""You have access to this professional's data:

SELECTED CV: {selected_cv_data.get('title', 'None') if selected_cv_data else 'None'}
CV Content: {selected_cv_data.get('content', 'No CV uploaded') if selected_cv_data else 'No CV uploaded'}

SELECTED CAREER QUIZ: {selected_quiz_data.get('title', 'None') if selected_quiz_data else 'None'}
Quiz Content: {selected_quiz_data.get('content', 'No quiz completed') if selected_quiz_data else 'No quiz completed'}"""
    
    welcome_message = f"""Hi! I'm here to support you on your career journey!

{data_summary}

I can help you with:  
✦ **Career decisions** based on your CV and quiz results  
✦ **Skill gap analysis** and career roadmaps  
✦ **Emotional support** and encouragement  
✦ **Course suggestions** (names/topics - search for links in Quick Search)  
✦ **Next steps** and action planning  

What's on your mind today?"""
    
    if "resources_chat_history" not in st.session_state:
        st.session_state.resources_chat_history = [
            {"role": "assistant", "content": welcome_message}
        ]
    
    for msg in st.session_state.resources_chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("Ask for advice, support, or guidance..."):
        st.session_state.resources_chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("𖦹 Thinking..."):
                # NEW: Function calling setup
                contents = [types.Content(role="user", parts=[types.Part(text=f"""{internal_context}

User question: {prompt}

INSTRUCTIONS:
- Be supportive, empathetic, and encouraging
- Reference their CV/quiz data specifically when relevant
- Use tools (get_cv_analysis, analyze_skill_gaps, get_career_roadmap) when helpful
- Suggest courses/skills by NAME only (e.g., "Consider learning Python" not links)
- Help them make decisions based on their profile
- If they ask for job/course links, tell them to go back and use the Quick Search feature
- Focus on guidance and support, not direct job searches""")])]
                
                config = types.GenerateContentConfig(
                    tools=[PROFESSIONAL_TOOLS],
                    temperature=0.7
                )
                
                response = GEMINI_CHAT.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=config
                )
                
                # Handle function calls
                if response.candidates[0].content.parts and hasattr(response.candidates[0].content.parts[0], 'function_call'):
                    function_responses = []
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'function_call'):
                            fn_call = part.function_call
                            st.caption(f"🔧 Using: {fn_call.name}")
                            result = execute_function_call(fn_call.name, dict(fn_call.args))
                            function_responses.append(
                                types.Part.from_function_response(
                                    name=fn_call.name,
                                    response={"result": result}
                                )
                            )
                    
                    contents.append(response.candidates[0].content)
                    contents.append(types.Content(role="user", parts=function_responses))
                    
                    final_response = GEMINI_CHAT.client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=contents,
                        config=config
                    )
                    
                    response_text = final_response.text
                else:
                    response_text = response.text
                
                st.markdown(response_text)
        
        st.session_state.resources_chat_history.append({"role": "assistant", "content": response_text})
    
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("⟲ Restart Chat", width='stretch'):
            st.session_state.resources_chat_history = [
                {"role": "assistant", "content": welcome_message}
            ]
            st.rerun()
    
    with col2:
        if st.button("← Back to Quick Search", width='stretch'):
            st.session_state.resources_mode = "tools"
            st.rerun()
