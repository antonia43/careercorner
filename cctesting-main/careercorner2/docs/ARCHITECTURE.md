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

- LLM Provider: Google Gemini (`gemini-2.5-flash`)
- Observability: Langfuse v3.11.1
- Function Calling: 8 built-in tools (get_study_resources_web, get_career_options, get_wage_info, get_job_search_results, get_course_recommendations, get_linkedin_profile_optimization, get_company_research, fetch_job_description_from_url) and NUMBER function calling tools (search_universities_tool, calculate_admission_grade_tool, search_dges_database_tool, get_student_data_tool, get_cv_analysis_tool, get_career_quiz_results_tool, analyze_skill_gaps_tool, get_career_roadmap_tool, get_professional_profile_tool)

Langfuse v3.11.1 wrapped all Gemini calls to track prompts and responses. Exceptionally, function calls in student_resources.py and resources.py were not wrapped, but were still monitored using the @observe method. For Portuguese students, we used 4 custom tools (accesible via student_resources support chat) and 3 built-in tools (accessible via student_resources main page). For professionals, we used 4 custom tools (accessible via resources.py support chat) and 5 built-in tools (4 accessible via resources main page and 1 accessible via cv_builder cover letter building page [fetch_job_description_from_url]).


### Deployment
- Platform: Streamlit Cloud
- Environment Management: .env files (local), Streamlit secrets (production)
We deployed to Streamlit Cloud which worked perfectly for our GitHub based workflow. SQLite tempdir was used for persistence without external databases. Environment variables were used to secure our API keys in Streamlit Secrets.


---

## System Architecture

We organized the app with zapp.py routing between student_dashboard.py and professional_dashboard.py based on user type. Student features include student_career_quiz.py (adaptive open style questions), degree_picker.py (adaptive yes or no questions), grades_analysis.py (grade calculator), university_finder.py and student_resources.py (quick search with fucntion calling + AI chat). Professional features include cv_analysis.py (PDF parsing), career_growth_quiz.py (CV-aware), interview_simulator.py (CV aware), cv_builder.py (creating a CV, creating a cover letter) and resources.py (quick search with function calling + AI chatbot)

The services folder contains authentication.py and langfuse_helper.py. The utils folder contains database.py and reports.py: database.py handles all SQLite operations across reports, universities, and CVs; reports.py shows saved results in tabbed interfaces (both student and professional). Styles.py provides consistent CSS styling components everywhere.

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

**Presentation Layer** (`zapp.py`, `pages/`)
- zapp.py routes between student and professional dashboards based on user type
- Student pages (7 files): student_dashboard.py (onboarding gate), student_career_quiz.py (10Q sector matching), student_chat.py (5Q tool recommendations), student_resources.py (Khan/IAVE links), grades_analysis.py, degree_picker.py, university_finder.py
- Professional pages (7 files): professional_dashboard.py, professional_chat.py, career_growth_quiz.py (CV-aware), cv_analysis.py (PDF parsing), interview_simulator.py (mock interviews), cv_builder.py (quiz to CV PDF, description/url to cover letter), resources.py.

**Service Layer** (`services/`)
- authentication.py handles SQLite users, Google OAuth, and login/register UIs
- langfuse_helper.py provides LangfuseGeminiWrapper for all Gemini calls with tracing
- tools.py - file with built-in tools used in both student and professional resources pages
- student_tools.py - separated file with custom function declarations for function calling in the student resources support chat
- professional_tools.py - separated file with custom function declarations for function calling in the professional resources support chat

**Data Layer** (`utils/`)
- database.py manages SQLite CRUD operations for reports, universities, and CVs with tempdir persistence
- reports.py renders tabbed My Reports interfaces with CV selectors and delete functionality
- Auto-saves with user tracking

**Styling Layer** (`styles.py`)
- Custom CSS with DM Sans font, yellow and green color scheme, and button/text animations
- Hover effects, stat cards, and progress bars
- apply_custom_css called from zapp.py across all pages

**Assets Layer** (`data/`)
- Background images (bg1.png, bg2.png), logo (careercornerlogo2.png)
- DGES data (result from running scripts/build_dges_universities.py)
- Sidebar textures (crumpledpaper2.jpg, crumpledpaper3.avif)

**Scripts Layer** (`scripts/`)
- build_dges_universities.py - script used to scrape the DGES website in order to get course information used in university_finder.py


**Configuration Layer** ()

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
