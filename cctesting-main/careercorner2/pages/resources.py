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
