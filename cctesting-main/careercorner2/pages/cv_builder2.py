import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from services.langfuse_helper import LangfuseGeminiWrapper, get_user_id, get_session_id
from utils.database import save_report, load_reports
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors

load_dotenv()
GEMINI = LangfuseGeminiWrapper(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash",
)


def render_cv_builder():
    st.markdown('<div class="cc-fade-in">', unsafe_allow_html=True)
    st.header("✂ CV and Cover Letter Builder")
    st.markdown("</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
        ["Build CV Quiz", "Tailor CV to Job", "Cover Letter"]
    )

    with tab1:
        render_cv_quiz_builder()

    with tab2:
        render_cv_tailor_to_job()

    with tab3:
        render_cover_letter()


# ---------------- Tab 1: CV quiz ----------------


def render_cv_quiz_builder():
    st.subheader("Build Your CV Through a Quick Quiz")

    if "cv_quiz_step" not in st.session_state:
        st.session_state.cv_quiz_step = 0
        st.session_state.cv_quiz_data = {}

    steps = ["personal_info", "education", "experience", "skills", "achievements"]
    step = steps[st.session_state.cv_quiz_step]

    if step == "personal_info":
        st.markdown("### Step 1/5: Personal Info")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", key="cv_name")
        with col2:
            email = st.text_input("Email", key="cv_email")
        phone = st.text_input("Phone (optional)", key="cv_phone")
        location = st.text_input("Location (City, Country)", key="cv_location")

        if st.button("Next: Education", width='stretch', key="next_edu"):
            st.session_state.cv_quiz_data.update(
                {"name": name, "email": email, "phone": phone, "location": location}
            )
            st.session_state.cv_quiz_step += 1
            st.rerun()

    elif step == "education":
        st.markdown("### Step 2/5: Education")
        degree = st.selectbox(
            "Highest Degree:", ["Bachelor", "Master", "PhD", "High School"], key="cv_degree"
        )
        field = st.text_input("Field of Study:", key="cv_field")
        school = st.text_input("University/School:", key="cv_school")
        years = st.text_input("Years (e.g., 2020–2024):", key="cv_edu_years")

        if st.button("Next: Experience", width='stretch', key="next_exp"):
            st.session_state.cv_quiz_data.setdefault("education", []).append(
                {"degree": degree, "field": field, "school": school, "years": years}
            )
            st.session_state.cv_quiz_step += 1
            st.rerun()

    elif step == "experience":
        st.markdown("### Step 3/5: Work Experience")
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Job Title:", key="cv_job_title")
            company = st.text_input("Company:", key="cv_company")
        with col2:
            years = st.text_input("Years (e.g., 2022–Present):", key="cv_exp_years")

        description = st.text_area(
            "Key responsibilities (3 bullet points):", height=120, key="cv_desc"
        )

        if st.button("Next: Skills", width='stretch', key="next_skills"):
            st.session_state.cv_quiz_data.setdefault("work_experience", []).append(
                {
                    "title": job_title,
                    "company": company,
                    "years": years,
                    "description": description,
                }
            )
            st.session_state.cv_quiz_step += 1
            st.rerun()

    elif step == "skills":
        st.markdown("### Step 4/5: Top Skills")
        skills_input = st.text_input(
            "Skills (comma separated):",
            placeholder="Python, SQL, AWS, Leadership",
            key="cv_skills"
        )

        if st.button("Next: Achievements", width='stretch', key="next_achieve"):
            skills = [s.strip() for s in skills_input.split(",") if s.strip()]
            st.session_state.cv_quiz_data["skills"] = skills
            st.session_state.cv_quiz_step += 1
            st.rerun()

    elif step == "achievements":
        st.markdown("### Step 5/5: Key Achievements")
        achievements = st.text_area(
            "3 biggest wins (one per line, with numbers):", height=150, key="cv_achievements"
        )

        col1, col2 = st.columns(2)
        with col1:
            target_job = st.text_input("Target job title:", key="cv_target_job")
        with col2:
            industry = st.selectbox(
                "Industry:", ["Tech", "Finance", "Marketing", "Healthcare", "", "Other"], key="cv_industry"
            )
            
        if st.button("Generate My CV", width='stretch', type="primary", key="gen_cv"):
            st.session_state.cv_quiz_data.update(
                {
                    "achievements": [
                        a.strip()
                        for a in achievements.split("\n")
                        if a.strip()
                    ],
                    "target_job": target_job,
                    "industry": industry,
                }
            )

            with st.spinner("Polishing your CV..."):
                polished_cv = polish_quiz_cv(st.session_state.cv_quiz_data)
                st.session_state.cv_data = polished_cv
                st.session_state.cv_quiz_step = 0

            st.success("✓ CV ready! Saved to My Reports.")
            
            # autosaving to database
            if "username" in st.session_state and st.session_state.username:
                try:
                    cv_summary = f"Built from CV Builder quiz for {target_job} in {industry}"
                    
                    save_report(
                        user_id=st.session_state.username,
                        report_type="professional_cv",
                        title=f"CV Builder - {st.session_state.cv_quiz_data.get('name', 'Unnamed')} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                        content=cv_summary,
                        cv_data=polished_cv
                    )
                    
                    st.info("🗂️ Automatically saved to My Reports!")
                except Exception as e:
                    st.warning(f"Could not auto-save: {e}")
            
            # show cv data
            st.divider()
            st.subheader("Your CV")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # pretty PDF download
                pdf_bytes = generate_pretty_cv_pdf(polished_cv)
                st.download_button(
                    "➜] Download CV (PDF)",
                    data=pdf_bytes,
                    file_name=f"cv_{st.session_state.cv_quiz_data.get('name', 'resume').replace(' ', '_').lower()}.pdf",
                    mime="application/pdf",
                    width='stretch'
                )
            
            with col2:
                # JSON backup download
                cv_json = generate_cv_json(polished_cv)
                st.download_button(
                    "➜] Download CV (JSON)",
                    data=cv_json,
                    file_name=f"cv_{st.session_state.cv_quiz_data.get('name', 'resume').replace(' ', '_').lower()}.json",
                    mime="application/json",
                    width='stretch'
                )
            
            with st.expander("Preview CV Data"):
                st.json(polished_cv)


# ---------------- Tab 2: Tailor CV to Job ----------------

def render_cv_tailor_to_job():
    st.subheader("Tailor Your CV to a Specific Job")

    # getting saved CVs from database
    if "username" not in st.session_state or not st.session_state.username:
        st.warning("⚠︎ Please log in to use CV tailoring.")
        return
    
    user_id = st.session_state.username
    reports = load_reports(user_id, "professional_cv")

    if not reports:
        st.warning(
            "To tailor your CV, you first need to upload or analyze it in **CV Analysis**."
        )
        if st.button("↩ Go to CV Analysis", width='stretch'):
            st.session_state.redirect_to = "CV Analysis"
            st.rerun()
        return

    # pick which saved CV to use
    titles = [r["title"] for r in reports]
    selected_title = st.selectbox(
        "Choose which saved CV to tailor:", titles, key="tailor_cv_selector"
    )

    selected_report = next(r for r in reports if r["title"] == selected_title)
    base_cv = selected_report.get("cv_data") or {}

    if not base_cv:
        st.error("This saved report has no structured CV data attached.")
        return

    # keeping current CV synced
    st.session_state.cv_data = base_cv

    # tailoring inputs
    col1, col2 = st.columns(2)
    with col1:
        target_job = st.text_input(
            "Target job title:", placeholder="e.g., Data Scientist", key="tailor_job"
        )
    with col2:
        company = st.text_input(
            "Company (optional):", placeholder="e.g., Spotify", key="tailor_company"
        )

    job_desc = st.text_area(
        "Paste job description (optional but recommended):",
        height=180,
        placeholder="Paste the full job ad here for better tailoring.",
        key="tailor_desc"
    )

    if st.button("✎ Tailor My CV", width='stretch', type="primary", key="tailor_btn") and target_job.strip():
        with st.spinner("Tailoring your CV for this role..."):
            tailored = tailor_cv_to_job(
                base_cv=base_cv,
                target_job=target_job,
                company=company,
                job_description=job_desc,
            )
            st.session_state.tailored_cv = tailored

        st.success(f"✓ CV tailored for {target_job}!")
        
        # autosave tailored to cv
        try:
            company_name = f" at {company}" if company else ""
            tailored_summary = f"Tailored for {target_job}{company_name}"
            
            save_report(
                user_id=user_id,
                report_type="professional_cv",
                title=f"Tailored CV - {target_job} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                content=tailored_summary,
                cv_data=tailored
            )
            
            st.info("🗂️ Automatically saved to My Reports!")
        except Exception as e:
            st.warning(f"Could not auto-save: {e}")
        
        st.divider()
        st.subheader("Tailored CV")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # pretty PDF
            pdf_bytes = generate_pretty_cv_pdf(tailored)
            company_slug = company.replace(' ', '_').lower() if company else 'tailored'
            st.download_button(
                "➜] Download Tailored CV (PDF)",
                data=pdf_bytes,
                file_name=f"cv_{target_job.replace(' ', '_').lower()}_{company_slug}.pdf",
                mime="application/pdf",
                width='stretch'
            )
        
        with col2:
            # json
            cv_text = json.dumps(tailored, indent=2, ensure_ascii=False)
            st.download_button(
                "➜] Download Tailored CV (JSON)",
                data=cv_text.encode("utf-8"),
                file_name=f"cv_{target_job.replace(' ', '_').lower()}_{company_slug}.json",
                mime="application/json",
                width='stretch'
            )
        
        with st.expander("Preview Tailored CV Data"):
            st.json(tailored)


# ---------------- Tab 3: Cover Letter ----------------

def render_cover_letter():
    st.subheader("Cover Letter Builder")

    base_cv = st.session_state.get("cv_data") or {}
    has_cv = bool(base_cv)
    use_cv = False
    if has_cv:
        use_cv = st.checkbox("Use my CV information", value=True, key="use_cv_cover")
    else:
        st.caption("No CV on file yet – you can still generate a letter from the job ad.")

    profile = base_cv if use_cv else {}

    job_desc = st.text_area("Paste job description:", height=150, key="cover_job_desc")
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("Tone:", ["Professional", "Enthusiastic"], key="cover_tone")
    with col2:
        length = st.selectbox(
            "Length:", ["Short (200 words)", "Standard (350 words)"], key="cover_length"
        )

    if st.button("✍︎ Generate Cover Letter", width='stretch', type="primary", key="gen_cover") and job_desc.strip():
        with st.spinner("Writing your letter..."):
            cover_letter = generate_cover_letter(profile, job_desc, tone, length)
            st.session_state.cover_letter = cover_letter

        content = cover_letter["content"]
        job_title = cover_letter.get("job_title", "role")
        
        st.success("✓ Cover letter generated!")
        
        st.divider()
        st.subheader("Your Cover Letter")
        st.markdown(content)
        
        st.download_button(
            "➜] Download Cover Letter (TXT)",
            data=content,
            file_name=f"{job_title.replace(' ', '_').lower()}_cover_letter.txt",
            mime="text/plain",
            width='stretch'
        )
        

def polish_quiz_cv(quiz_data: dict) -> dict:
    prompt = {
        "task": "Turn this quiz data into a structured, recruiter-friendly CV JSON with keys: name, email, phone, location, education (list), work_experience (list), skills (list), achievements (list), summary (string).",
        "cv_quiz_data": quiz_data,
    }
    try:
        resp = GEMINI.generate_content(
            prompt=json.dumps(prompt),
            temperature=0.4,
            user_id=get_user_id(),
            session_id=get_session_id(),
        )
        cleaned = resp.strip().replace("``````", "").strip()
        return json.loads(cleaned)
    except Exception as e:
        st.warning(f"Polish CV error: {e}")
        return quiz_data


def tailor_cv_to_job(base_cv: dict, target_job: str, company: str, job_description: str) -> dict:
    prompt = {
        "task": (
            "Tailor this CV for a specific job. "
            "Rewrite or reorder bullets, highlight the most relevant experience, "
            "and add missing but reasonable keywords from the job description. "
            "Return JSON with similar structure to the input CV."
        ),
        "base_cv": base_cv,
        "target_job": target_job,
        "company": company,
        "job_description": job_description,
    }
    try:
        resp = GEMINI.generate_content(
            prompt=json.dumps(prompt),
            temperature=0.4,
            user_id=get_user_id(),
            session_id=get_session_id(),
        )
        cleaned = resp.strip().replace("``````", "").strip()
        return json.loads(cleaned)
    except Exception:
        fallback = dict(base_cv)
        fallback["note"] = f"Could not tailor automatically for {target_job}."
        return fallback


def generate_cover_letter(cv_data: dict, job_desc: str, tone: str, length: str) -> dict:
    prompt = {
        "task": (
            "Write a tailored cover letter. Return JSON with keys "
            "`job_title` and `content` (plain text letter)."
        ),
        "cv_data": cv_data,
        "job_description": job_desc,
        "tone": tone,
        "length": length,
    }
    try:
        resp = GEMINI.generate_content(
            prompt=json.dumps(prompt),
            temperature=0.7,
            user_id=get_user_id(),
            session_id=get_session_id(),
        )
        cleaned = resp.strip().replace("``````", "").strip()
        return json.loads(cleaned)
    except Exception:
        name = cv_data.get("name", "Your Name")
        return {
            "job_title": "Role",
            "content": f"Dear Hiring Manager,\n\n[Cover letter based on the job ad goes here.]\n\nBest regards,\n{name}",
        }


def generate_cv_json(cv_data: dict) -> bytes:
    return json.dumps(cv_data, indent=2, ensure_ascii=False).encode("utf-8")


def generate_pretty_cv_pdf(cv_data: dict) -> bytes:
    """Generating a beautiful PDF CV using report lab"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E86AB'),
        spaceAfter=6,
        alignment=1 #center
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#A23B72'),
        spaceAfter=6,
        spaceBefore=12
    )
    normal_bold = ParagraphStyle(
        'NormalBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    name = cv_data.get('full_name') or cv_data.get('name', 'Your Name')
    story.append(Paragraph(name, title_style))
    story.append(Spacer(1, 0.1*inch))
    
    contact = []
    if cv_data.get('email'):
        contact.append(cv_data['email'])
    if cv_data.get('phone'):
        contact.append(cv_data['phone'])
    if cv_data.get('location'):
        contact.append(cv_data['location'])
    
    contact_text = " | ".join(contact)
    story.append(Paragraph(contact_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    summary = cv_data.get('summary') or cv_data.get('achievements', [])
    if summary:
        story.append(Paragraph("Professional Summary", heading_style))
        if isinstance(summary, list):
            summary_text = " ".join(summary)
        else:
            summary_text = str(summary)
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
    
    edu = cv_data.get('education', [])
    if edu:
        story.append(Paragraph("Education", heading_style))
        if isinstance(edu, list):
            for item in edu:
                if isinstance(item, dict):
                    edu_text = f"<b>{item.get('degree', '')} in {item.get('field', '')}</b><br/>{item.get('school', '')} | {item.get('years', '')}"
                    story.append(Paragraph(edu_text, styles['Normal']))
                    story.append(Spacer(1, 0.08*inch))
                else:
                    story.append(Paragraph(str(item), styles['Normal']))
                    story.append(Spacer(1, 0.08*inch))
        else:
            story.append(Paragraph(str(edu), styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
    
    exp = cv_data.get('work_experience') or cv_data.get('experience_summary')
    if exp:
        story.append(Paragraph("Work Experience", heading_style))
        if isinstance(exp, list):
            for item in exp:
                if isinstance(item, dict):
                    exp_text = f"<b>{item.get('title', '')}</b> at {item.get('company', '')}<br/>{item.get('years', '')}"
                    story.append(Paragraph(exp_text, normal_bold))
                    story.append(Spacer(1, 0.05*inch))
                    
                    desc = item.get('description', '')
                    if desc:
                        story.append(Paragraph(desc, styles['Normal']))
                    story.append(Spacer(1, 0.12*inch))
        else:
            story.append(Paragraph(str(exp), styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
    
    skills = cv_data.get('skills', [])
    if skills:
        story.append(Paragraph("Skills", heading_style))
        if isinstance(skills, list):
            skills_text = " • ".join(skills)
        else:
            skills_text = str(skills)
        story.append(Paragraph(skills_text, styles['Normal']))
        story.append(Spacer(1, 0.15*inch))
    
    # building pdf file
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
