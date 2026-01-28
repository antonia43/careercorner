# README

# Career Corner

Helping you build your career, every step of the way.

## Overview

Career Corner is an AI-powered application designed to help high-school students and professionals make informed career decisions. Whether you're a high-school student preparing for exams and struggling to pick a degree, or a professional seeking a career change or job opportunities based on your skills, Career Corner provides comprehensive support through two dedicated interfaces: one for high-school students and another for university students and professionals.
As former high-school students and aspiring data scientists themselves, the creators of Career Corner have experienced firsthand the lack of clear guidance during critical career processes: vague psychotechnical tests at school that fail to reveal true interests, scattered information making degree selection overwhelming, and lack of helpful information for professionals who are trying to identify transferable skills or navigating daily job struggles.

Career Corner aims to solve these challenges by combining conversational AI, real Portuguese educational data, and practical career tools to deliver personalized guidance far superior to traditional generic advice. Portuguese high school students benefit from adaptive career quizzes, CIF grade calculators, degree/university matchers with interactive maps, and study resources including IAVE exam archives and DGES degree data. Professionals access CV parsing, CV-aware career growth quizzes and tailored mock interview simulators with STAR feedback. 
Both user types can enjoy smart chat interfaces that route them to optimal tools and have the ability to save all results to "My Reports" for usage in other tools and persistent access across sessions, connecting school performance and career pathways in one cohesive platform.


**Target Audience:**
- **High school students** (Career and degree discovery, Grade caculation/preparing for university admission)
- **University students & professionals** (CV analysis, Career Recommendations, Interview preparation)
- **Focus (student section):** Portuguese education system (DGES degrees, National exams); Although tools are also available for international students.

---

## The Problem

### For Students:

Students face psycotechnical tests at school that don't connect interests to real university options, yielding vague results that don't help in decision making. Grades exist in isolation requiring manual calculation of the final highschool grade in order to find suitable degrees.

- Vague school career tests lacking personalization
- Confusion about degree choices and university options
- No real time connection between grades, interests, and real admission data
- Information scattered across multiple platforms (DGES, university sites)


### For Professionals:

Professionals send CVs everyday but get no structured skill analysis or interview practice catered to their needs, which might be beneficial if they want to succeed. Additionally, some professionals might want a career change but don't know what skills they can explore.

- Difficulty identifying transferable skills for career changes
- Generic job search tools without personalized insights
- No structured way to connect CV strengths to career paths
- Overwhelming job market navigation


## Our Solution

Career Corner delivers personalized guidance through conversational AI that adapts to user responses. 
Students can answer 10 creative questions to get sector matches (i.e. Healthcare 60%, Technology 40%), use the sector match results to explore suitable degrees, upload grade reports (or manually input grades) for final score calculation and get matched to real DGES degrees/universities based on school performance, quiz results and location. 
Professionals can upload their CVs (that get parsed into structured JSON) to get feedback, play CV-aware career quizzes, practice mock interviews tailored by job offer (with feedback) and generate tailored cover letters. 
All results persist in a SQLite database, being easily accessible through a "My Reports" tab and reusable throughout all of Career Corner's features.

1. **Conversational AI:** Interactive quizzes that adapt to user responses (not static multiple-choice)
2. **Real Data Integration:** Uses DGES university data, admission grades, and Portuguese scholarship info
3. **Personalization:** Connects quiz results -> grades -> degree recommendations -> university matches
4. **Actionable and Interactive Tools:** for example, CV analysis, grades analysis, university search, career path recommendations
5. **Observability:** Langfuse tracking of AI interactions for quality assurance during app testing


## Features
Shared for all users:
- **Data Persistence:** SQLite database stores quiz reports, grades, saved universities, CVs.
- **Google OAuth Login:** Secure login with Google accounts.
- **Local Login:** Secure login with accounts created directly on the platform and stored in the database.
- **Dashboard:** A dashboard with an AI career assistant chatbot that interacts with users that aren't sure about how to nagivate the app, asking ~5 genuine questions about their situation and redirecting them to the most suitable starting tool after understanding their needs. The chatbot never mentions tool names during the first 5 turns, building context through casual dialogue like "What challenges are you facing with your studies?" or "What's frustrating about your job search?" On turn 6+, it confidently recommends a feature (i.e. "Career Quiz would suit you best because...") with clear reasoning. Both student and professional dashboards use separate chat histories with dedicated trace IDs in Langfuse for observability.
- **Reports Section** A section where all results from quizzes and analyses can be accessed and deleted by the user.
- **Custom CSS styling** Custom green and yellow UI with animations.


### For students:

#### **Career Discovery Quiz**
- Career Discovery Quiz - an interactive quiz operated through AI, to help students figure out their most valuable skills and biggest interests. The quiz asks the students creative/philosophical questions that aren't related to school or studies (i.e. "If you found a hidden path, would you explore it, observe, or do nothing?"), in order to understand the students real personality. At the end, a sector, or a mix of sectors (such as Technology, Health, Business) is attributed to the student based on their answers. Aditionally, a report is delivered, highlighting possible career paths based on the student's answers.

- **What it does:** Interactive conversational quiz (10 questions) to understand user's personality
- **Output:** 
  - Career sector match (Technology, Health, Business, Arts, etc.)
  - Top 3-5 degree recommendations with fit scores
  - Detailed report with reasoning
- **Tech:** Multi-turn chat with Gemini 2.5-flash, response validation

#### **Grades Analysis**
- Grades Analysis - A guided tool that collects school grades (through manual input or file ingestion) and calculates Portuguese final grades, helping students understand their academic profile, how far they are from getting into a certain university, and use this grade to find a university that they can get in.

- **What it does:** Calculates CIF using the official Portuguese formula or other formulas the student may want to use. The user can either manually input their grades or upload a grade report image for the AI to extract subjects and grades automatically, and enter their planned or completed exam scores to see their final score. Four options are available: Portuguese (Manual Input/Uplaod) and International (Manual Input/Upload).
- **Output:** 
  - Final CIF score (e.g., 15.8/20)
  - Comparison to saved university thresholds from University Finder (Portuguese Students)
 
- **Tech:** Gemini multimodal vision for PDF/image parsing if upload option is selected

#### **Degree Picker**
An interactive assistant that uses the students sector of interest (results from career quiz if applicable) to suggest concrete degree programs, narrowing the search down to a shortlist of degrees that best fit the student. A portuguese (DGES only degrees) and international options are available.
- **What it does:** AI assistant that asks 5-7 yes or no questions based on the sector of interest and narrows down degree choices through conversation
- **Input:** Career quiz results (if available), student preference (manually picked from a dropdown list)
- **Output:**
- Portuguese Students:
  - Top 3 DGES degrees with:
    - Fit percentage
    - Curriculum overview
    - Career paths in Portugal
    - Entry requirements
- Internatinal Students:
  - Top 3 degrees with:
    - Fit percentage
    - Curriculum overview
    - Career paths
- **Tech:** RAG-style retrieval from DGES data, Gemini reasoning

#### **University Finder**
A university search tool by degree name and location. Two options are available:

- **Portuguese**: university search uses real Portuguese real DGES admission data from 2024-2025 to show universities offering the chosen degree (can be chosen from the results of **Degree Picker**), including entry grades, location and an interactive map so students can explore their options. Favorite universities can be saved to compare later or match against **Grades Analysis** score to see which are realistic targets.
- **International**: more "search" based interface, where students can input degree names and search for universities offering that degree in the country of their choice.

- **What it does:** Search and filter Portuguese universities by degree program using live DGES data
- **Features:**
  - **Location Filter:** Lisbon, Porto, Coimbra, or nationwide search
  - **Public/Private Toggle:** Filter tuition types
  - **Interactive Map:** Folium map with university markers, click to see admission grades and additional info
  - **Save System:** Store favorite universities with timestamps, access in My Reports
  - **Individual Delete:** Remove saved universities one-by-one
  - **Transferable result** Saved universities can be used in Grades Analysis
- **Output:** University cards showing institution name, program name, location, admission grade, duration
- **Tech:** DGES dataset (20+ universities), Folium map, SQLite saved_universities table with user_id tracking

#### **Student Resources**
Dual-mode feature combining five quick search options and support chat. Quick search mode uses 5 tools with function calling: get study resources for any subject (returns Khan Academy, Coursera, YouTube, Quizlet, Reddit links), get Portugal scholarships (Portuguese Only - DGES, FCT, Erasmus+ opportunities), get IAVE exam past papers (Portuguese Only - latest + archive), ............................................................................ Support chat mode allows natural guidance conversations where you can select degree/grades reports from dropdowns and ask for more personal and catered advice.

- **Quick Search Features:**
  - Study resources: Khan Academy, Coursera, YouTube tutorials, Quizlet flashcards for any subject (mudarrrrrrrrrr)
  - Scholarships: DGES bolsas, FCT grants, Erasmus+ programs
  - Exam papers: IAVE nacional exam archives (all subjects, past years)
  - sdfghjk
  - sdfghjkl
- **Support Chat Mode:**
  - Select saved degree/grades reports from dropdowns for personalization
  - AI references your specific data for personalized advice
  - Ask: "Help me understand my final score", "Should I apply to Nova with 15.2?", ADD OTHER QUESTIONS
- **Tech:** Gemini 2.5 Flash function calling (5 tools) for quick search purposes, Gemini 2.5 Flash (temp 0.7) for support chat


### For Professionals:

#### **CV Analysis**
Upload any PDF or DOCX CV and the AI extracts structured data: skills (technical like Python/SQL + soft like leadership), work experience (roles, companies, years, achievements), education background, and hidden strengths. Saved CVs auto-load on login via My Reports. The parsed JSON feeds directly into Career Growth Quiz for personalized questions and CV Builder for tailoring. Get benchmarking against job market standards and actionable optimization tips like "Add metrics to your achievements" or "Highlight AWS experience more prominently."
- CV Analysis - A CV document parser that scans uploaded CVs (can be auto-reloaded from database on login), extracting skills, experience, achievements, and strenghts into structured insights. It highlights what makes your profile stand out, benchmarks afainst job market standards, siggests optimizations and feeds directly into the Career Growth Quiz for hyper-personalizer recommendations, or into the CV editor to enhance it or cater it to a specific job offering and position.

- **What it does:** Multimodal CV parser using Gemini vision to handle any PDF/DOCX/image format
- **Extracts:**
  - Technical skills (programming languages, tools, certifications)
  - Soft skills (leadership, communication, problem-solving)
  - Work experience (job titles, companies, duration, bullet achievements)
  - Education (degrees, institutions, graduation years)
  - Strengths (what makes profile stand out)
  - Gaps (missing keywords or experience for target roles)
- **Features:**
  - Auto-reload: Saved CVs appear in My Reports CV selector dropdown
  - Benchmarking: Compares your profile to industry standards
  - Optimization tips: "Add quantified achievements" or "Strengthen technical section"
  - Integration: Parsed JSON flows to Career Quiz + CV Builder
- **Tech:** Gemini 2.5 Flash multimodal (handles scanned PDFs, images, any format), JSON storage in professional_reports table

#### **Career Growth Quiz**
An immersive 12-question conversational quiz designed for professionals and university students seeking career advancement or transitions. If you've uploaded a CV, questions adapt to your experience (e.g., "Given your 3 years in data analysis, how do you handle ambiguous stakeholder requests?"). Without a CV, questions focus on work preferences and soft skills. The quiz covers two phases: Experience & Preferences (6Q about teamwork, pressure, autonomy) and Soft Skills (6Q about leadership, communication, adaptability). Final report provides career sector match, growth paths (management track vs technical specialist vs entrepreneurship), skills to develop next, and 3-month action plan.
- Career growth quiz - an interactive, immersive quiz operated through a conversational AI interface, made for professionals find possible  figure out their most valuable skills and biggest interests. At the end, a sector (such as technology, health, business) is attributed to the student. Aditionally, a report is delivered, highlighting possible career paths based on the student's answers.

- **What it does:** CV-aware conversational assessment across experience preferences and soft skills dimensions
- **Input:** Parsed CV data (optional), work history, professional goals
- **Output:** 
  - Career sector match with reasoning
  - Growth path recommendations (management, technical deepening, lateral moves, entrepreneurship)
  - Top 3 skills to develop with concrete next steps
  - 3-month action plan with resources
  - Profile summary describing your work style
- **Tech:** Gemini 2.5 Flash, CV JSON integration, auto-saves to professional_reports

#### **CV Builder**
Three AI-powered tools in one interface. Build CV from scratch using a 5-step quiz (personal info -> education -> experience -> skills -> achievements) that generates a polished CV with your target job/industry. Tailor existing CV by selecting a saved CV from My Reports, pasting a job description, and letting AI reorder bullets and inject relevant keywords. Generate cover letters by combining your CV data with a job posting into personalized 200-350 word letters. All outputs export as pretty PDFs using ReportLab (custom fonts, colors, professional layouts) plus JSON backups.

- **What it does:** Three modes in one tabbed interface
  1. **Build CV Quiz (Tab 1):** 5-step guided quiz collecting name/email, education, work experience, skills, achievements -> AI polishes into complete CV JSON
  2. **Tailor CV to Job (Tab 2):** Select saved CV from dropdown, enter target job + company, paste job description -> AI reorders bullets and adds missing keywords
  3. **Cover Letter (Tab 3):** Uses CV data + job description -> generates 200-350 word letter in professional/enthusiastic tone
- **Output:** 
  - Pretty PDF CVs with custom ReportLab styling (DM Sans font, lime/yellow branding)
  - JSON backup downloads for editing
  - TXT cover letters ready to paste
- **Tech:** Gemini 2.5 Flash, ReportLab PDF generation, auto-saves to professional_reports

#### **Interview Simulator**
Practice job interviews with AI-generated questions tailored to your CV and target role. Quick Practice mode (10-15 mins) lets you select focus areas (Behavioral, Technical, Situational) for 3-6 questions with instant per-answer feedback. Mock Interview mode (30 mins) generates 10 role-specific questions for full interview simulation with comprehensive feedback report including overall score (1-10), best answer, answer that needs work, STAR method analysis, and recommended practice areas. Upload cover letter for even more personalized questions.

- **What it does:** Two modes for interview practice with AI feedback
  - **Quick Practice:** Select focus areas (Behavioral/Technical/Situational/Strengths-Weaknesses/Career Goals) -> 3-6 questions -> instant feedback per answer
  - **Mock Interview:** Enter target role + company -> 10 comprehensive questions -> full feedback report
- **Features:**
  - CV-aware questions (references your experience if CV uploaded)
  - Cover letter upload for additional personalization
  - Progress tracking (Question 3 of 10)
  - Back/Next/Skip navigation
  - Text area for typed answers (1-3 minute responses)
- **Output:** 
  - Per-answer feedback (Quick Practice)
  - Comprehensive report (Mock Interview): overall score 1-10, strengths, areas for improvement, best answer analysis, answer that needs work with fixes, key takeaways, recommended practice
  - STAR method evaluation (Situation, Task, Action, Result)
- **Tech:** Gemini 2.5 Flash, CV JSON integration, session state for multi-question flow

#### **Professional Resources - Your Next Steps**
Job search and course recommendation tools with conversational chat. Quick search returns real LinkedIn job links (Portugal-focused, recent postings) and Coursera/Udemy courses for skill development. Chat mode lets you select CV/quiz reports from dropdowns so AI references your specific profile when answering questions like "Find data science jobs matching my skills" or "Show me Python courses to fill my gaps." No function calling in chat mode to prevent link spam, just natural career guidance.

- **What it does:** Two-mode professional resource finder
  - **Quick Search:** Function calling tools return LinkedIn jobs + Coursera/Udemy courses
  - **Chat Mode:** AI advisor with CV/quiz report dropdown selection for personalized guidance
- **Features:**
  - Job search: LinkedIn links filtered to Portugal, recent postings, matches your sector
  - Course recommendations: Coursera, Udemy, skill-specific
  - Report selection: Choose which CV/quiz to reference in chat
  - Context-aware answers: AI knows your parsed CV skills + quiz sector
- **Tech:** Gemini 2.5 Flash function calling (2 tools: get_jobs, get_courses), Gemini 2.5 Flash chat (temp 0.7), report dropdown integration


## Tech Stack

### Backend
- **Python 3.13** powers all files with clean separation (pages/services/utils)
- **Google Gemini API**
  - `gemini-2.5-flash`
- **SQLite** lightweight tempdir database (`/tmp/career_corner.db`) with 4 tables:
  - `professional_reports` (CV/quiz/grades results with cv_json)
  - `saved_universities` (user favorites with admission data)
  - `user_cvs` (parsed CV JSON with timestamps)
  - `users` (authentication with hashed passwords)
- **Langfuse v3.11.1** traces every Gemini call through `LangfuseGeminiWrapper`

### Frontend
- **Streamlit 1.40+** native Python web framework handles all UI:
  - Session_state for 10Q quizzes, mock interviews, multi-step workflows
  - Progress bars, tabs, expanders, chat interfaces, file uploaders
  - Back/Next navigation with `st.rerun()` for smooth UX
- **ReportLab 4.2.2** generates professional PDF CVs with custom DM Sans typography and lime/yellow branding

### Database
- **SQLite tempdir** (`/tmp/career_corner.db`) provides zero-config persistence:
  - **Why perfect:** No external hosting, survives Streamlit restarts, automatic `init_database()` creates all tables
  - **Handy for production:** Works instantly on Streamlit Cloud, no connection strings/secrets needed
  - **Scales to 1000s:** Handles thousands of user reports/universities with indexes on user_id/report_type
  - **Structured data:** CV JSON, university data, timestamps enable My Reports dropdowns

### Authentication
- **Werkzeug 3.0.4** secure password hashing (`generate_password_hash/check_password_hash`)
- **Google OAuth 2.0** via native client credentials with localhost/production redirect URIs
- **Session management** through `st.session_state.logged_in` + `st.session_state.username`

### AI/ML
- **Langfuse** production observability wrapping 95% of Gemini calls:
  - Traces prompts/responses/tokens/temperature/metadata per generation
  - User feedback scoring (thumbs up/down -> 0.0-1.0)
  - Conversation turn tracking (5Q chat routing validation)
- **Function Calling** 8 Gemini-native tools total:
  - **6 Student tools** (student_resources.py): study links, DGES scholarships, IAVE exams, CIF tips
  - **2 Pro tools** (resources.py): LinkedIn jobs, Coursera/Udemy courses
- **Multimodal AI** Gemini vision processes:
  - CV parsing (PDF/DOCX -> skills/work/education JSON)
  - Grade reports (images -> subject scores -> CIF calculation)

### Data Sources
- **DGES** Portuguese higher education (degrees, universities, 2024-2025 admission grades)
- **IAVE** national exam archives (past papers, all subjects/years)
- **Scholarships** DGES/FCT/Erasmus+ direct program links
- **No external APIs** - all resources retrieved via URLs + built-in google tools + function calling



## Architecture

### Layer Structure

**Presentation Layer** (`zapp.py`, `pages/`)
14 modular UI files, one per feature: `student_career_quiz.py` (10Q adaptive quiz), `cv_analysis.py` (PDF parsing), `interview_simulator.py` (mock interviews), etc. Each handles its own session_state, progress bars, back/next navigation, and auto-save confirmations. Streamlit widgets (tabs, expanders, chat, sliders) create intuitive multi-step workflows.

**Service Layer** (`services/`)
`authentication.py` manages SQLite users + Google OAuth. `langfuse_helper.py` provides `LangfuseGeminiWrapper` class wrapping 95% of Gemini calls with v3 tracing (prompts, responses, tokens, user feedback). Centralized services prevent code duplication across 14 UI files.
Built-in tools defined in `tools.py` (for both students and professionals, as some tools work for both). Function calling tools defined in `student_tools.py` and `professional_tools.py`. Gemini function calling in both student and professional resources support chat routes directly to these functions.

**Data Layer** (`utils/`)
`database.py` handles all SQLite CRUD across 4 tables (professional_reports, saved_universities, user_cvs, users) with tempdir persistence. `reports.py` renders tabbed My Reports with CV selectors and delete functionality. Zero external database configuration.

**Configuration Layer** (`config/`)
Centralizes all AI settings and prompts in three files: `models.py` (model names and temperature presets per feature), `prompts.py` (30+ reusable prompt templates grouped by module) and `schemas.py` (CV schemas, fallback questions, dropdown options).

**Styling Layer** (`styles.py`)
Centralized CSS with DM Sans typography, lime/yellow gradients, fade/slide animations, hover effects, and responsive components. `apply_custom_css()` called from `zapp.py` ensures consistent branding.


### Key Design Decisions

1. **Dual Dashboard Architecture:** Separate `student_dashboard.py` vs `professional_dashboard.py` prevents feature overload while sharing common services/database. Onboarding gates confirm user type before access.

2. **LangfuseGeminiWrapper Pattern:** Single wrapper handles 95% of Gemini calls with automatic tracing (user_id, session_id, temperature, metadata). Raw Gemini client used only for function calling in resources. Graceful fallback if Langfuse unavailable.

3. **Database-First Persistence:** SQLite tempdir stores everything (reports, CVs, universities) enabling dropdown selection in chats ("Select CV: My Resume - 2025-12-21"). No data loss across Streamlit reruns/sessions.

4. **One File Per Feature:** 14 UI files (`student_career_quiz.py`, `cv_builder.py`, etc.) = modular development, each file self-contained with session_state management.

5. **5-Question Chat Routing:** Dashboard chatbots (`student_chat.py`, `professional_chat.py`) ask 5 natural questions before recommending tools ("Career Quiz would suit you best because..."). Prevents premature tool spam, builds context and helps users navigate the app with ease.

6. **Streamlit-Native Workflows:** No FastAPI/React. Session_state + `st.rerun()` handles complex multi-step flows (10Q quizzes, 10Q interviews). Progress bars + back/next navigation prevent user frustration.

7. **Zero External Dependencies:** SQLite tempdir + standard library (json/re/os/datetime) = instant deployment. Only 6 pip packages needed. Works offline except Gemini API calls.

**Why This Works:** All files are production-ready, so zero configurations are needed to deploy to Streamlit Cloud. The project relies only on a small, well-defined set of Python dependencies and the built-in SQLite database, which means there is no need to provision external services, containers, or complex infrastructure. The folder structure is clear and consistent, with each major feature living in its own file, so the application can be understood and modified quickly even by someone new joining the project.

The use of a single Gemini wrapper with integrated tracing ensures that every AI interaction is automatically logged with the same pattern, instead of each page having its own fragile API logic. This makes it much easier to debug quizzes, CV analysis, or interview feedback without hunting through different files or logging systems. Observability becomes a built-in part of the architecture rather than an afterthought, so prompt iterations and quality improvements can be done with confidence.

Because each feature is encapsulated in its own Streamlit page file, the codebase scales very naturally: new tools can be added as new files, and existing ones can be refactored in isolation. At the same time, the shared services and database utilities keep repeated logic in one place, so the overall complexity stays low. The result is a system that is modular enough to support team development—different people can own different feature files—but still simple enough that a single maintainer can understand, debug, and extend the whole application without feeling overwhelmed.



## Installation & Setup

### Prerequisites
### **Prerequisites**
- **Python 3.10+**
- **Google Gemini API Key:** [Get it here](https://ai.google.dev)
- **Langfuse Account (Optional):** [Sign up](https://langfuse.com)
- **Google OAuth Credentials (Optional):** [Google Cloud Console](https://console.cloud.google.com)

### Installation Steps

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [careercorner1]
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (use your keys):
```bash
cp .env.example .env

```

### **Step 4: Run the Application**

4. Run the application:
```bash
streamlit run zapp.py  
```

**App will open at:** `http://localhost:8501`


**Required Packages:**
streamlit>=1.40.0
google-generativeai>=0.8.3
langfuse>=3.11.1
python-dotenv>=1.0.1
reportlab>=4.2.2
werkzeug>=3.0.4
sqlite3

**Required environment variables:**
```

- GOOGLE_API_KEY: "yourapikey"
- LANGFUSE_PUBLIC_KEY: "yourkey"
- LANGFUSE_SECRET_KEY: "yourkey"
- LANGFUSE_HOST: "https://cloud.langfuse.com"

```
**Optional environment variables:**
```
- GOOGLE_CLIENT_ID="yourkey"
- GOOGLE_CLIENT_SECRET="yourkey"

```

### How to set up GoogleOAuth login (optional):
## Google OAuth Setup (Optional)

### **1. Create Credentials**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project → **"Career Corner"**
3. Enable **Google+ API**
4. **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
   - App type: **Web application**
   - Name: **Career Corner Streamlit**

### **2. Add Redirect URIs**
```
  https://your-app.streamlit.app
  http://localhost:8501
```
2. **Add to Secrets:**
```
- GOOGLE_API_KEY: "yourapikey"
- LANGFUSE_PUBLIC_KEY: "yourkey"
- LANGFUSE_SECRET_KEY: "yourkey"
- LANGFUSE_HOST: "https://cloud.langfuse.com"
- GOOGLE_CLIENT_ID="yourkey"
- GOOGLE_CLIENT_SECRET="yourkey"
```

**Security Note:** 
- **NEVER commit `.env` to Git!** It's already in `.gitignore`
- For deployment, use Streamlit Secrets (see [Deployment](#deployment))


---

## Usage Guide

### First-Time Setup
1. **Launch App:** Run `streamlit run zapp.py` (opens http://localhost:8501)
2. **Choose Dashboard:** 
   - **Student Dashboard** -> high school students planning university
   - **Professional Dashboard** -> university students/professionals job hunting
3. **Onboarding:** Confirm your user type (student gate prevents pro tool access)
4. **Start Chat:** AI asks 5 natural questions before recommending tools
5. **Start Chat:** Have fun! The app is very intuitive, it tells you all you need to know to properly navigate it.


---
**Example Workflow (Student):**

```
1. Dashboard Chat (2 mins)
├─ AI: "What challenges are you facing with your studies?"
├─ You: "I'm confused about what degree to pick"
└─ AI: "Career Quiz would suit you best because you're exploring options"
```

```
2. Career Discovery Quiz (10 mins)
├─ Answer 10 adaptive questions ("Perfect day starts with what sound?")
├─ Results: "Healthcare 60%, Education 40%"
└─ Auto-saves to My Reports
```

```
3. Degree Picker (5 mins)
├─ Select sector from quiz (Healthcare -> Nursing/Physiotherapy)
├─ Top 3 DGES degrees with entry requirements/CIF needed
└─ Auto-saves recommendations
```

```
4. Grades Analysis (10 mins)
├─ Enter your portuguese grades manually
├─ CIF calculation: School 65% + Exams 35% = 15.8/20
└─ Search for Course grades and compare them to yours, get your chances of getting in

```

```
5. University Finder (10 mins)
├─ Search "Nursing" universities matching your CIF 15.8
├─ Filter: Lisbon, public unis, 14.0-16.0 admission range
├─ Interactive map -> click Nova marker -> "CIF required: 15.2"
└─ Save favorite universities (accessible at the top of the page)
```

```
6. Student Resources (Chat Mode)
├─ Click "Need personalized help?"
├─ Select degree/grades from dropdowns
└─ Ask: Please help me decipher me results, i wasn't expecting them.
```

**Example Workflow (Professional):**
```
1. Dashboard Chat (2 mins)
├─ AI: "What's frustrating about your job search?"
├─ You: "My CV isn't getting responses"
└─ AI: "CV Analysis would suit you best"
```

```
2. CV Analysis (5 mins)
├─ Upload CV (PDF/image)
├─ AI extracts skills, experience, strengths
├─ Get benchmarking + optimization tips
└─ JSON saved to My Reports
```
```
3. Career Growth Quiz (10 mins)
├─ CV-aware questions: "Given your data analysis exp, prefer teams or solo?
├─ 2 phases: Experience prefs (6Q) + Soft skills (6Q)
└─ Results: Receive personalized report (auto saved)
```

```
4. Interview Prep (30 mins)
├─ Mock Interview: "Senior Data Analyst @ Nova"
├─ 10 questions -> type answers (Situation/Task/Action/Result)
└─ Feedback: "Score 7.5/10, Best answer: Q3 leadership, Improve: Q7 metrics"
```
```
5. CV Builder (10 mins)
├─ Tab 1: Build new CV from quiz (5-step: info/education/exp/skills)
├─ Tab 2: Tailor saved CV -> "Data Scientist @ Google" + job desc
├─ Tab 3: Cover letter (350 words, enthusiastic tone)
└─ Download PDF CV + JSON backup and Branded ReportLab styling
```
```
6. Professional Resources (Short Mode)
└─ Ask: "Find data science jobs" or "Python courses"
```


### **Key Features to Highlight**

#### **Data Persistence**
- All reports saved in SQLite database
- Reload past quizzes, CVs, grades, degrees
- Delete individual saved universities

#### **Auto-saving results**
- Avoids data loss

#### **Interactive Map (University Finder for Portuguese Students)**
- Click university markers on Folium map
- See admission grades, location, website
- Filter by CIF range

#### **Document Upload**
- Supports PDF and images (JPG, PNG)
- Multimodal Gemini extracts text from any format
- Works with messy/scanned documents

#### **Dropdown Selection in Resources Chat**
- Both student and professional chat modes have dropdowns
- Select which report to reference (e.g., "CV: My Resume - 2025-12-11")
- AI uses selected report content for personalized answers



## Deployment

**Live Application:** https://careercorner.streamlit.app

**Deployment Platform:** Streamlit Cloud

### **Streamlit Cloud**
1. **Push Code to GitHub:**
```
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Select your GitHub repo (career-corner)
- Set main file: `zapp.py`

3. **Add Secrets:**
- In Streamlit Cloud dashboard -> "Settings" -> "Secrets"
- Paste your `.env` content:

4. **Deploy:**
- Click "Deploy"
- App will be live at your preferred https address

Note: ensure imports are using the right structure (e.g. from utils.database import load_report; not from database import load_report)


### **Local Deployment (Testing)**

Run with custom port
streamlit run zapp.py --server.port 8502

Run with network access
streamlit run zapp.py --server.address 0.0.0.0

Run with production-like settings
streamlit run zapp.py --server.headless true

Note: imports with structure `from utils.database import load_report` may yield errors. If thats the case, you can use directly `from database import load_report`.


| File | Purpose |
|------|---------|
| `zapp.py` | **Main Streamlit entry point** with student/professional dashboard routing and sidebar navigation |
| `styles.py` | **Custom CSS styling** with DM Sans fonts, lime/yellow gradients, animations, and responsive components |
| `langfuse_helper.py` | **LangfuseGeminiWrapper** for all Gemini calls with v3 tracing, user_id/session_id tracking, feedback logging (95% of AI calls) |
| `database.py` | **SQLite CRUD** for professional_reports (CV/quiz results), saved_universities, user_cvs tables with tempdir persistence |
| `reports.py` | **Tabbed My Reports interface** with CV selectors, delete buttons, student/pro separate tabs |
| `authentication.py` | **Local login/register** with Werkzeug password hashing and session management |
| `student_dashboard.py` | **Student tool routing** (Career Quiz, Grades, Degree Picker, University Finder, Resources) |
| `professional_dashboard.py` | **Professional tool routing** (CV Analysis, Career Growth, Interview Prep, CV Builder, Your Next Steps) |
| `student_career_quiz.py` | **Adaptive 10Q career quiz** → sector matches (Healthcare 60%) + degree paths, auto-saves |
| `career_growth_quiz.py` | **CV-aware professional quiz** (Experience + Soft Skills phases) → growth paths, uses parsed CV JSON |
| `grades_analysis.py` | **Grades extractor and CIF calculator** → Portuguese/international transcript parsing, DGES admission comparison |
| `cv_analysis.py` | **Multimodal PDF/DOCX parser** → structured CV JSON (skills/experience/education) |
| `cv_builder.py` | **2-tab CV toolkit** (quiz→ build CV, cover letters) → ReportLab PDF + JSON export |
| `university_finder.py` | **University degree search** (Portugal DGES + International Gemini search) → save favorites, grade comparison |
| `interview_simulator.py` | **Mock interviews** (Quick Practice 3-5Q + Mock 10Q) with STAR feedback scoring (1-10) |
| `student_resources.py` | **Student support tools** (exam papers, scholarships, study resources, wage finder) + function calling chat |
| `resources.py` | **Professional support tools** (job search, courses, LinkedIn optimizer, company research) + function calling chat |
| `student_chat.py` | **Student dashboard AI** (5Q rule → tool recs: "Career Quiz would suit you best") |
| `professional_chat.py` | **Professional dashboard AI** (5Q rule → "CV Analysis would suit you best") |
| `tools.py` | **Built-in tool definitions** (shared search tools for both student and professional resources) |
| `student_tools.py` | **Function calling tool definitions** for student support chat (get_saved_universities, get_user_profile, etc.) |
| `professional_tools.py` | **Function calling tool definitions** for professional support chat (analyze_cv, generate_roadmap, etc.) |
| `models.py` | **Model configurations** (gemini-2.5-flash settings, temperature presets per feature: 0.1–0.9) |
| `prompts.py` | **Centralized prompt templates** (30+ prompts organized by module with .format() placeholders) |
| `schemas.py` | **Schemas and fallbacks** (CV extraction schema, fallback questions, dropdown options for UI) |
| `.env` | **API secrets** (Gemini/Langfuse keys) - **do not commit to Git!** (.gitignore protected) |
| `requirements.txt` | **Core dependencies** for pip install (streamlit, google-generativeai, langfuse, etc.) |


# License

MIT License

Copyright (c) 2025 Antónia Lemos (antonia43 on github) and Matilde Maximiano

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Team

- **Antónia Lemos** - Core development (student + professional features)
- **Matilde Maximiano** - Core development (student + professional features)


**Both contributed equally across all aspects of the project including:**
- Architecture design and modular file structure
- Langfuse observability implementation
- Gemini API wrapper and prompt engineering
- Authentication (Google OAuth + local login)
- Production deployment to Streamlit Cloud
- Documentation (README, ARCHITECTURE.md)

**Institution:** Nova IMS, Universidade Nova de Lisboa  
**Course:** BSc in Data Science 
**Project:** Capstone Project (February 2026)


Career Corner by Matilde Maximiano and Antónia Lemos (Nova IMS, February 2026)
GitHub: https://github.com/antonia43/careercorner1

---
