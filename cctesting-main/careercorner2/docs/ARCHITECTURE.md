# Career Corner - Architecture Documentation

---

## Problem Statement & Project Overview 

Career Corner is an AI-powered career guidance platform designed for high school students navigating university admissions and professionals seeking job market advancement. Students struggle with vague psychotechnical tests, scattered degree information, and disconnected final grade calculations, while professionals face challenges tailoring CVs and preparing for interviews without clear skill path mappings. As former high school students and aspiring data scientists, the creators of Career Corner aimed to bridge these gaps by combining adaptive conversational AI, real Portuguese education data (DGES catalogs, IAVE exams, CIF formulas), built-in research tools, and practical features into dual student/professional dashboards, delivering personalized sector matches (i.e. Healthcare), university finders with interactive maps, CV parsing, mock interviews, and final reports that connect interests, grades, and actionable career paths far beyond generic advice.

---

## Architecture Decisions

### Why Streamlit?

Streamlit was used for the frontend framework because it was taught in class and therefore there was higher familiarity with it, allowing us to deploy our application faster through a cloud, without the need to spend extra valuable time learning a different frontend option. This made it so that we could focus our time working on the concrete app features.
Although streamlit is very convenient, since it is natively integrated to python and has built-in session management, the UI customization is very limited. We used CSS styling (styles.py) to bypass some of the limitations, allowing for some more personalization and colorfulness.


### Why Google Gemini?
Decision: Google Gemini 2.5 Flash as the primary LLM.
For similar reasons as stated above, Google Gemini was the LLM preferred since it was used in class and differentiates itself from other LLMs like OpenAI GPT-4 (cost prohibitive), Claude (lower free tier limits), by a very generous free tier. It also handles both text and images so we could process CVs and grade reports (images, pdfs), and its large context window let us send entire documents to the AI without complex RAG setups.


### Why No RAG/Vector Database?

Following the above rationale, Google Gemini has a large context window, so we opted for direct context injection instead of RAG, mainly since the files our application would ingest (Cvs and grades) fit within Gemini's 200K context window. Gemini's architecture is also simpler, so there are fewer failure points. Additionally, there is no semantic search requirement (students ask specific questions, not "find similar")


### Why Langfuse?

We used Langfuse because it was taught in class and the free tier worked for our project. Langfuse was used to track AI generation so we could understand the functioning behind the AI and check if everything was working correctly. We logged user thumbs-up/down feedback to improve prompts over time, but later removed it from the final deployment version.

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


---

## Technology Stack

### Backend
- Language: Python 3.13
- LLM Provider: Google Gemini 2.5 Flash (used for all features and tools)
- Database: SQLite (lightweight, file-based) to store user reports and saved universities in the temp directory so data persisted across Streamlit sessions
- Authentication: Custom implementation with werkzeug password hashing


### Frontend
- Framework: Streamlit 1.40+
- UI Components: Native Streamlit widgets

Streamlit handled all UI components including tabs, chat interfaces, progress bars, and sliders. Custom CSS was used to implement DM Sans typography, button hover and text animations, and a consistent yellow and green design across both student and professional dashboards.


### Stack Overview

- Package Manager: pip with virtual environment (venv) managing dependencies including streamlit 1.40+, google.genai, langfuse v3.11.1, reportlab, werkzeug-security, doc2text, PyPDF2, folium (streamlit folium).
- Version Control: Git with GitHub repository following modular folder structure (pages/services/utils)
- Environment Management: .env files for local development with dotenv, Streamlit Cloud secrets for production (GOOGLE_API_KEY, LANGFUSE credentials, GOOGLE_CLIENT(ID/SECRET) optional, for Google OAuth login feature)
- Database: SQLite in tempdir with automatic init_database() call handling users, professional_reports, saved_universities, user_cvs tables
- Deployment: Streamlit Cloud with automatic GitHub integration, zero-downtime deploys from main branch
- Debugging: Langfuse dashboard for tracing AI generations
- File Organization: 24 Python files structured as pages/ (14 UI), services/ (5), utils/ (2), scripts(1), top-level helpers (styles.py, zapp.py)
- Static Assets: data/ folder with images for CSS backgrounds and branding
- Documentation: root README.md file with project details and instructions, docs/ folder with ARCHITECTURE.md (architecture decisions and technical choices) and TOOLS.md (documenting each tool)


### AI & Monitoring

- **LLM Provider:** Google Gemini (`gemini-2.5-flash`)
- **Observability:** Langfuse v3.11.1
- **Function Calling:** 8 built-in tools + 9 custom function calling tools

#### Built-In Tools (8)
Built-in tools use Google's native capabilities (Google Search & URL Context) to retrieve real-time web data:

1. **get_study_resources_web** - Finds free online courses, video tutorials, practice websites, and community resources for any subject
2. **get_career_options** - Discovers career paths, job titles, and salary ranges for specific degrees
3. **get_wage_info** - Retrieves salary information by experience level (entry/mid/senior) for job titles in any country
4. **get_job_search_results** - Returns direct links to job postings from LinkedIn, Indeed, Glassdoor, and company career pages
5. **get_course_recommendations** - Finds online courses from Coursera, Udemy, edX, LinkedIn Learning, and YouTube for specific skills
6. **get_linkedin_profile_optimization** - Provides headline options, About section rewrites, skill recommendations, and profile improvement tips
7. **get_company_research** - Delivers company culture, reviews, news, benefits, and salary information
8. **fetch_job_description_from_url** - Extracts job descriptions from URLs using Gemini's URL context tool

#### Custom Function Calling Tools (9)
Function calling tools access user-specific data from CareerCorner's SQLite database:

**Student Tools (4):**
1. **search_saved_universities** - Searches through user's bookmarked universities and programs by degree name and country
2. **calculate_admission_grade** - Calculates student's CIF admission average from stored grades
3. **search_dges_database** - Queries Portuguese university database (DGES) for degrees, admission grades, and vacancies
4. **get_student_profile** - Retrieves complete student profile including grades, saved universities, and degree reports

**Professional Tools (5):**
1. **get_cv_analysis** - Accesses stored CV analysis with skills, experience, education, and recommendations
2. **get_career_quiz_results** - Retrieves career quiz results including personality type, interests, and recommended paths
3. **analyze_skill_gaps** - Compares current CV skills against target role requirements and identifies missing competencies
4. **get_career_roadmap** - Generates phased career roadmaps (6 months / 1 year / 2 years) based on stored profile data
5. **get_professional_profile** - Aggregates all professional data including CVs, quizzes, and career assessments

#### Tool Usage & Monitoring

Langfuse wraps all Gemini calls to track prompts, responses, and token usage. Function calls in `student_resources.py` and `resources.py` are monitored using the `@observe` decorator rather than wrapped directly.

**Distribution:**
- **Student Resources:** 4 custom function calling tools (support chat) + 3 built-in tools (main page: study resources, career options, wage info)
- **Professional Resources:** 5 custom function calling tools (support chat) + 5 built-in tools (4 on main page: job search, courses, LinkedIn optimizer, company research + 1 in CV Builder cover letter page: fetch_job_description_from_url)

All function calling tools implement 3-attempt retry logic for resilience against database locks and transient errors.


### Deployment
- Platform: Streamlit Cloud
- Environment Management: .env files (local), Streamlit secrets (production)
We deployed to Streamlit Cloud which worked perfectly for our GitHub based workflow. SQLite tempdir was used for persistence without external databases. Environment variables were used to secure our API keys in Streamlit Secrets.


---

## System Architecture

Career Corner follows a modular layered architecture with clear separation of concerns. The application routes users between student and professional dashboards (`student_dashboard.py` vs `professional_dashboard.py`) based on account type, with each dashboard providing access to specialized tools.

### High-Level Overview

**Student Pipeline:**
- `student_career_quiz.py` - 10-question adaptive personality assessment
- `degree_picker.py` - AI-guided degree recommendations via yes/no questions
- `grades_analysis.py` - CIF calculator with multimodal grade extraction
- `university_finder.py` - DGES database search with interactive maps
- `student_resources.py` - Quick search tools + AI support chat with function calling

**Professional Pipeline:**
- `cv_analysis.py` - Multimodal CV parser extracting structured JSON
- `career_growth_quiz.py` - CV-aware 12-question career assessment
- `interview_simulator.py` - Mock interviews with STAR method feedback
- `cv_builder.py` - 3-mode CV toolkit (build/tailor/cover letter)
- `resources.py` - Job search + course finder + AI support chat

**Shared Infrastructure:**
- `authentication.py` - User management (local + Google OAuth)
- `langfuse_helper.py` - LangfuseGeminiWrapper for AI observability
- `database.py` - SQLite operations across 4 tables
- `reports.py` - "My Reports" interface for saved data
- `styles.py` - Consistent CSS branding

---
```
careercorner2/
├── pages/ # User-facing pages
│ ├── career_growth_quiz.py
│ ├── cv_analysis.py
│ ├── cv_builder.py
│ ├── degree_picker.py
│ ├── grades_analysis.py
│ ├── interview_simulator.py
│ ├── professional_chat.py
│ ├── professional_dashboard.py
│ ├── resources.py
│ ├── student_career_quiz.py
│ ├── student_chat.py
│ ├── student_dashboard.py
│ ├── student_resources.py
│ └── university_finder.py
├── services/ # business logic + external integrations
│ ├── __init__.py
│ ├── authentication.py  # manual and Google Login/session helpers
│ ├── langfuse_helper.py  # Langfuse + Gemini wrappers
│ ├── professional_tools.py
│ ├── student_tools.py
│ └── tools.py
├── utils/ # shared helpers and data access
│ ├── __init__.py
│ ├── database.py
│ └── reports.py
├── scripts/ 
│ ├── __init__.py
│ └── build_dges_universities.py
├── data/ # static files
│ ├── bg1.png
│ ├── bg2.png
│ ├── careercornerlogo2.png
│ ├── careercornermini.png
│ ├── crumpledpaper2.jpg
│ ├── crumpledpaper3.avif
│ └── universities_2025_1f.csv
├── docs/
│ ├── ARCHITECTURE.md
│ └── TOOLS.md
├── zapp.py # Main Streamlit entry
└── styles.py # Custom CSS styling functions
├── README.md
├── requirements.txt
└── .env.example
```

### Component Breakdown
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


## File Overview and Responsibilities

| File | Purpose |
|------|---------|
| `zapp.py` | **Main Streamlit entry point** with student/professional dashboard routing and sidebar navigation |
| `styles.py` | **Custom CSS styling** with DM Sans fonts, lime/yellow gradients, animations, and responsive components |
| `langfuse_helper.py` | **LangfuseGeminiWrapper** for all Gemini calls with v3 tracing, user_id/session_id tracking, feedback logging) |
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

---

## Data Flow

### Example: Career Discovery Quiz

1. User Input: Student answers adaptive personality question
2. Service Layer: gemini_service sends prompt to Gemini with conversation history
3. AI Generation: Gemini generates next adaptive question based on previous answers
4. Observability: Langfuse logs trace
5. UI Update: Streamlit displays next question
6. Repeat: 10 questions total
7. Final Analysis: Gemini analyzes all answers, generates career sector matches
8. Storage: Report saved to SQLite via database.py, accesible in "My reports" section
9. Display: Results shown with sector percentages and recommended degrees

---

## AI Integration

### LLM Configuration

#### Temperature Guide

| Temperature | Use Case | Files |
|-------------|----------|-------|
| 0.1 | Extraction, parsing | CV extraction, grades extraction |
| 0.2 | Structured output | Degree questions |
| 0.3 | Analysis with facts | CV feedback, career quiz analysis |
| 0.4 | Conversational | Dashboard chats, polish CV |
| 0.5 | Search/recommendations | University search, interview questions |
| 0.6 | Reports | Interview feedback, career reports |
| 0.7 | Creative + function calling | Cover letters, resource chats |
| 0.9 | Adaptive/creative | Student career quiz questions |

---

#### Common Patterns

#### Standard LangfuseGeminiWrapper setup:
```python
from config import ModelConfig

CLIENT = LangfuseGeminiWrapper(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model=ModelConfig.MODULE_CONFIG["model"],
)
```

#### Standard prompt call:
```python
from config import ModulePrompts

prompt = ModulePrompts.PROMPT_NAME.format(
    param1=value1,
    param2=value2
)

response = CLIENT.generate_content(
    prompt=prompt,
    system_instruction=ModulePrompts.SYSTEM_INSTRUCTION,
    temperature=ModelConfig.MODULE_CONFIG["temp"],
    user_id=get_user_id(),
    session_id=get_session_id()
)
```

#### Standard fallback pattern:
```python
from config import FallbackQuestions

try:
    # AI generation
    questions = generate_questions_ai()
except Exception as e:
    st.error(f"Using fallback: {e}")
    questions = FallbackQuestions.FALLBACK_NAME
```


#### Prompt Engineering Strategy

Structured Outputs: Using markdown formatting for parseable reports
System Instructions: Persona definitions and clear prompts for consistent tone
Example: "You are a creative career counselor for Portuguese students. Ask unexpected questions that reveal thinking styles, not direct career preferences."

**Client Prompts**:
- accessible at config/prompts.py

---

## Function Calling & Tools

### Available Tools

**Built-In Tools**
1.
2.
3.
4.
5.
6.
7.
8.

**Custom Function Calling Tools**
1.
2.
3.
4.
5.
6.
7.
8.

- For in depth information about tools, access TOOLS.md file.

---

## Multimodal Processing

### CV Analysis Feature

Capability: Upload PDF/image of grade report -> AI extracts CV information -> Writes a detailed report listing your strenghts and observations -> Saves it to database

Implementation:
1. Multimodal Input: Gemini's vision capabilities process image/PDF directly
2. Structured Extraction: Prompt engineered to output JSON
3. Use: Use CV in other tabs (Interview Prep, CV Builder, Your Next Steps)

Why This Approach:
- No OCR library needed (Gemini handles it)
- Works with varied formats (flexibility)
- Directly integrated with other feature logic


### Grades Analysis Feature

write here


---

## Observability & Monitoring

### Langfuse Integration

Implementation: Custom wrapper (LangfuseGeminiWrapper) around Gemini API calls

What We Track:
- All LLM generations (prompts, outputs, token usage)
- User sessions and conversation flows
- Quiz question generation patterns
- Error rates and failure patterns

Why:
- Debug adaptive quiz logic (why certain questions generated)
- Monitor costs (token usage per feature)
- Improve prompts based on output quality
- Track user engagement patterns

---

## Deployment

### Platform: Streamlit Cloud

Why Streamlit Cloud:
- Free tier sufficient for our project
- Native Streamlit support
- Automatic deployment from GitHub
- Built-in secrets management

### Environment Variables

Required:
- GOOGLE_API_KEY: Gemini API access
- LANGFUSE_PUBLIC_KEY: Observability
- LANGFUSE_SECRET_KEY: Observability
- LANGFUSE_HOST: cloud.langfuse.com

Optional:
GOOGLE_CLIENT_ID; GOOGLE_CLIENT_SECRET: For google login

---

## Future Enhancements

### Potential Additions

1. RAG Implementation: If degree database grows beyond context limits (mentioned below)
2. Mobile Optimization: Responsive design for phone usage, different interface choice
3. Advanced Analytics: Career trend predictions, for example
4. More robust database implementation for scalability (mentioned below)


### Scalability Considerations

Our current architecture supports hundreds of concurrent users (Streamlit Cloud limits) and SQLite is sufficient for thousands of user records.
If scaling was needed we could migrate to PostgreSQL (relational data), add Redis for session caching and deploy to AWS/GCP for higher throughput
RAG implementation could support thousands of university programs via vector similarity matching beyond Gemini's context window. Advanced analytics could integrate salary trends and employment statistics.

---

End of Architecture Documentation
