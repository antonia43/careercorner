import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Raw client for built-in tools
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_study_resources_web(subject: str) -> dict:
    """Web search for study resources using Google Search built-in tool"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Find the best free study resources for: {subject}. Include courses, tutorials, practice sites, and community resources.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        # Extract sources
        sources = []
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.grounding_chunks:
            sources = [{"title": c.web.title, "url": c.web.uri} for c in metadata.grounding_chunks]
        
        return {"success": True, "answer": response.text, "sources": sources}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_career_options(course_name: str) -> dict:
    """Get career paths using Google Search"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"What are the top career options and job positions for someone with a degree in {course_name}? Include entry-level and senior roles.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        sources = []
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.grounding_chunks:
            sources = [{"title": c.web.title, "url": c.web.uri} for c in metadata.grounding_chunks[:5]]
        
        return {"success": True, "answer": response.text, "sources": sources}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_wage_info(job_title: str, country: str = "Portugal") -> dict:
    """Get salary information using Google Search"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"What is the typical salary range for {job_title} in {country}? Provide entry-level, mid-level, and senior-level salaries with monthly and annual figures.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        sources = []
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.grounding_chunks:
            sources = [{"title": c.web.title, "url": c.web.uri} for c in metadata.grounding_chunks[:3]]
        
        return {"success": True, "answer": response.text, "sources": sources}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_job_search_results(role: str, location: str = "Portugal") -> dict:
    """Job search using Google Search built-in tool"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Find current job opportunities for {role} in {location}. Include company names, job boards, and search tips.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        sources = []
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.grounding_chunks:
            sources = [{"title": c.web.title, "url": c.web.uri} for c in metadata.grounding_chunks]
        
        return {"success": True, "answer": response.text, "sources": sources}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_course_recommendations(skill: str) -> dict:
    """Course search using Google Search"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Find the best online courses to learn {skill}. Include free and paid options from Coursera, Udemy, edX, and other platforms.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        sources = []
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.grounding_chunks:
            sources = [{"title": c.web.title, "url": c.web.uri} for c in metadata.grounding_chunks]
        
        return {"success": True, "answer": response.text, "sources": sources}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_networking_tips(industry: str = "general") -> dict:
    """Networking strategies using Google Search"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"What are effective networking strategies for professionals in {industry}? Include online platforms, events, and community tips.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        sources = []
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.grounding_chunks:
            sources = [{"title": c.web.title, "url": c.web.uri} for c in metadata.grounding_chunks[:5]]
        
        return {"success": True, "answer": response.text, "sources": sources}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_interview_prep(role: str) -> dict:
    """Interview prep using Google Search"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"What are common interview questions and preparation tips for {role} positions? Include behavioral and technical questions.",
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            )
        )
        
        sources = []
        metadata = response.candidates[0].grounding_metadata
        if metadata and metadata.grounding_chunks:
            sources = [{"title": c.web.title, "url": c.web.uri} for c in metadata.grounding_chunks[:5]]
        
        return {"success": True, "answer": response.text, "sources": sources}
    except Exception as e:
        return {"success": False, "error": str(e)}


# UI Render Functions

def render_exam_papers_tool():
    """IAVE exam papers - direct links only"""
    st.subheader("Past Exam Papers")
    st.info("Access official IAVE nacional exam papers from previous years")
    
    st.markdown("---")
    
    st.markdown("### Current Year Exams")
    st.caption("Browse the latest nacional exams")
    st.link_button(
        "Open IAVE Current Exams",
        "https://iave.pt/provas-e-exames/provas-e-exames/provas-e-exames-finais-nacionais-es/",
        use_container_width=True,
        type="primary"
    )
    
    st.markdown("---")
    
    st.markdown("### Complete Archive (All Years)")
    st.caption("Access past papers from all previous years")
    st.link_button(
        "Open IAVE Archive",
        "https://iave.pt/provas-e-exames/arquivo/arquivo-provas-e-exames-finais-nacionais-es/",
        use_container_width=True,
        type="primary"
    )
    
    st.markdown("---")
    st.caption("Tip: Practice with past papers to improve your exam technique")


def render_scholarships_tool():
    """Scholarship links"""
    st.subheader("Scholarships & Financial Aid")
    st.info("Find scholarships from DGES, FCT, Erasmus+, and more")
    
    scholarships = [
        {
            "name": "DGES Scholarships",
            "description": "Portuguese government scholarships for higher education",
            "url": "https://www.dges.gov.pt/pt/pagina/bolsas-de-estudo"
        },
        {
            "name": "FCT Research Grants",
            "description": "Funding for research and postgraduate studies",
            "url": "https://www.fct.pt/apoios/bolsas/"
        },
        {
            "name": "Erasmus+ Mobility",
            "description": "Study abroad opportunities in Europe",
            "url": "https://erasmus-plus.ec.europa.eu/opportunities/opportunities-for-individuals/students"
        }
    ]
    
    for scholarship in scholarships:
        with st.container():
            st.markdown(f"**{scholarship['name']}**")
            st.caption(scholarship['description'])
            st.link_button(
                f"Visit {scholarship['name']}",
                scholarship['url'],
                use_container_width=True
            )
            st.divider()


def render_study_resources_tool():
    """Study resources with Google Search"""
    st.subheader("Study Resources")
    st.info("Find the best learning materials for any subject")
    
    subject = st.text_input(
        "What subject do you want to study?",
        placeholder="e.g., Python, Biology, Calculus, History...",
        key="study_resources_subject"
    )
    
    if st.button("Search Study Resources", use_container_width=True, type="primary"):
        if subject.strip():
            with st.spinner(f"Finding resources for {subject}..."):
                results = get_study_resources_web(subject.strip())
                if results["success"]:
                    st.success("Found resources")
                    st.markdown(results["answer"])
                    
                    if results["sources"]:
                        with st.expander("View Sources"):
                            for source in results["sources"]:
                                st.markdown(f"[{source['title']}]({source['url']})")
                else:
                    st.error(f"Error: {results.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter a subject")


def render_career_options_tool():
    """Career options using Google Search"""
    st.subheader("Career Options Explorer")
    st.info("Discover what careers you can pursue with your degree")
    
    course = st.text_input(
        "What degree/course are you interested in?",
        placeholder="e.g., Computer Science, Medicine, Psychology...",
        key="career_options_course"
    )
    
    if st.button("Explore Career Options", use_container_width=True, type="primary"):
        if course.strip():
            with st.spinner(f"Finding careers for {course}..."):
                results = get_career_options(course.strip())
                if results["success"]:
                    st.success("Career paths found")
                    st.markdown(results["answer"])
                    
                    if results["sources"]:
                        with st.expander("View Sources"):
                            for source in results["sources"]:
                                st.markdown(f"[{source['title']}]({source['url']})")
                else:
                    st.error(f"Error: {results.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter a course name")


def render_wage_finder_tool():
    """Salary information using Google Search"""
    st.subheader("Wage Finder")
    st.info("Find salary ranges for different job positions")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        job_title = st.text_input(
            "Job title:",
            placeholder="e.g., Software Engineer, Nurse, Teacher...",
            key="wage_finder_job"
        )
    
    with col2:
        country = st.selectbox(
            "Country:",
            ["Portugal", "Spain", "UK", "USA", "Germany", "France", "Other"],
            key="wage_finder_country"
        )
    
    if st.button("Search Salaries", use_container_width=True, type="primary"):
        if job_title.strip():
            with st.spinner(f"Finding salary data for {job_title}..."):
                results = get_wage_info(job_title.strip(), country)
                if results["success"]:
                    st.success("Salary information found")
                    st.markdown(results["answer"])
                    
                    if results["sources"]:
                        with st.expander("View Sources"):
                            for source in results["sources"]:
                                st.markdown(f"[{source['title']}]({source['url']})")
                else:
                    st.error(f"Error: {results.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter a job title")


def render_job_search_tool():
    """Job search with Google Search"""
    st.subheader("Job Search")
    st.info("Find job opportunities in your field")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        role = st.text_input(
            "Job role or company:",
            placeholder="e.g., Software Engineer, Nurse, Zara...",
            key="job_search_role"
        )
    
    with col2:
        location = st.selectbox(
            "Location:",
            ["Portugal", "Lisbon", "Porto", "Remote", "Spain", "UK"],
            key="job_search_location"
        )
    
    if st.button("Search Jobs", use_container_width=True, type="primary"):
        if role.strip():
            with st.spinner(f"Searching for {role} jobs in {location}..."):
                results = get_job_search_results(role.strip(), location)
                if results["success"]:
                    st.success("Found job opportunities")
                    st.markdown(results["answer"])
                    
                    if results["sources"]:
                        with st.expander("View Sources"):
                            for source in results["sources"]:
                                st.markdown(f"[{source['title']}]({source['url']})")
                else:
                    st.error(f"Error: {results.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter a job role or company name")


def render_course_finder_tool():
    """Course finder with Google Search"""
    st.subheader("Course Finder")
    st.info("Discover courses to learn new skills")
    
    skill = st.text_input(
        "What skill do you want to learn?",
        placeholder="e.g., Python, Data Analysis, Project Management...",
        key="course_finder_skill"
    )
    
    if st.button("Find Courses", use_container_width=True, type="primary"):
        if skill.strip():
            with st.spinner(f"Finding courses for {skill}..."):
                results = get_course_recommendations(skill.strip())
                if results["success"]:
                    st.success("Found learning resources")
                    st.markdown(results["answer"])
                    
                    if results["sources"]:
                        with st.expander("View Sources"):
                            for source in results["sources"]:
                                st.markdown(f"[{source['title']}]({source['url']})")
                else:
                    st.error(f"Error: {results.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter a skill to learn")


def render_networking_tool():
    """Networking tips using Google Search"""
    st.subheader("Networking Guide")
    st.info("Build professional connections in your industry")
    
    industry = st.text_input(
        "Your industry (optional):",
        placeholder="e.g., Tech, Healthcare, Finance...",
        key="networking_industry"
    )
    
    if st.button("Get Networking Tips", use_container_width=True, type="primary"):
        industry_value = industry.strip() if industry.strip() else "general"
        with st.spinner("Generating networking strategies..."):
            results = get_networking_tips(industry_value)
            if results["success"]:
                st.success("Networking strategies ready")
                st.markdown(results["answer"])
                
                if results["sources"]:
                    with st.expander("View Sources"):
                        for source in results["sources"]:
                            st.markdown(f"[{source['title']}]({source['url']})")
            else:
                st.error(f"Error: {results.get('error', 'Unknown error')}")


def render_interview_prep_tool():
    """Interview prep using Google Search"""
    st.subheader("Interview Preparation")
    st.info("Prepare for interviews with role-specific guidance")
    
    role = st.text_input(
        "Job role you're interviewing for:",
        placeholder="e.g., Software Developer, Marketing Manager...",
        key="interview_prep_role"
    )
    
    if st.button("Generate Interview Prep", use_container_width=True, type="primary"):
        if role.strip():
            with st.spinner(f"Creating interview guide for {role}..."):
                results = get_interview_prep(role.strip())
                if results["success"]:
                    st.success("Interview preparation ready")
                    st.markdown(results["answer"])
                    
                    if results["sources"]:
                        with st.expander("View Sources"):
                            for source in results["sources"]:
                                st.markdown(f"[{source['title']}]({source['url']})")
                else:
                    st.error(f"Error: {results.get('error', 'Unknown error')}")
        else:
            st.warning("Please enter a job role")
