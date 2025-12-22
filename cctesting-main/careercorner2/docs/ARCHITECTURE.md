# Career Corner - Architecture Documentation

---

## Problem Statement & Project Overview 

Career Corner is an AI-powered career guidance platform designed for Portuguese high school students navigating university admissions and international professionals seeking job market advancement. Students struggle with vague psychotechnical tests, scattered DGES degree requirements, and disconnected CIF grade calculations, while professionals face challenges tailoring CVs and preparing for interviews without clear skill-path mappings. As former high school students and aspiring data scientists ourselves, we built Career Corner to bridge these gaps by combining adaptive conversational AI, real Portuguese education data (DGES catalogs, IAVE exams, CIF formulas), and practical tools into dual student/professional dashboards—delivering personalized sector matches, university finders with interactive maps, CV parsing, mock interviews, and auto-saved reports that connect interests, grades, and actionable career paths far beyond generic advice.

---

## Architecture Decisions

### Why Streamlit?

Streamlit was used for the frontend framework because it was taught in class and therefore there was higher familiarity with it, allowing us to deploy our application faster through a cloud, without the need to spend extra valuable time learning a different frontend option. This made it so that we could focus our time working on the concrete app features.
Although streamlit is very convenient, since it is natively integrated to python and has built-in session management, the UI customization is very limited, but acceptable for our use case, where we used CSS styling to bypass some of the limitations, allowing for some more personalization and colorfulness.


### Why Google Gemini?
Decision: Google Gemini 2.5 Flash as the primary LLM.
For similar reasons as stated above, Google Gemini was the LLM preferred since it was used in class and differentiates itself from other LLMs like OpenAI GPT-4 (cost prohibitive), Claude (lower free tier limits), by a very generous free tier. It also handles both text and images so we could process CV PDFs, and its large context window let us send entire documents to the AI without complex RAG setups.
Aditionally, Google Gemini 2.0 Flash 001 was used for function calling for compatibility.


### Why No RAG/Vector Database?

Following the above rationale, Google Gemini has a large context window, so we opted for direct context injection instead of RAG, mainly since the files our application would ingest (Cvs) fit within Gemini's 200K context window. Gemini's architecture is also simpler, so there are fewer failure points. Additionally, there is no semantic search requirement (students ask specific questions, not "find similar")

When We Would Use RAG: If expanding to thousands of international university programs requiring similarity matching.


### Why Langfuse?

We used Langfuse because it was taught in class and the free tier worked for our project. Langfuse tracked every AI generation so we could debug why quizzes generated certain questions and see if our chat routing worked correctly. We logged user thumbs-up/down feedback to improve prompts over time, which was removed from the final deployment version for aesthetic reasons.

---

## Technology Stack

### Backend
- Language: Python 3.13
- Main LLM Provider: Google Gemini 2.5 Flash (chats, question and report generation, cv analysis)
- Secondary LLM Provider: Google Gemini 2.0 Flash 001 (funtion calling)
- Database: SQLite (lightweight, file-based) to store user reports and saved universities in the temp directory so data persisted across Streamlit sessions
- Authentication (2 types): Custom implementation with werkzeug password hasing + Google Login (with Google OAuth support)


### Frontend
- Framework: Streamlit 1.40+
- UI Components: Native Streamlit widgets

Streamlit 1.40+ handled all UI components including tabs, chat interfaces, progress bars, and sliders. We used ReportLab to generate professional PDF CVs with custom fonts and colors. Custom CSS gave us DM Sans typography, hover animations, and a consistent lime/yellow design across both student and professional dashboards.

### Stack Overview

- Package Manager: pip with virtual environment (venv) managing dependencies including streamlit 1.40+, google-generativeai, langfuse v3.11.1, reportlab, werkzeug-security, doc2text, PyPDF2, folium (also streamlit folium).
- Version Control: Git with GitHub repository following modular folder structure (pages/services/utils) for clean feature branching
- Environment Management: .env files for local development with dotenv, Streamlit Cloud secrets for production (GOOGLE_API_KEY, LANGFUSE credentials, GOOGLE_CLIENT(ID/SECRET) optional, for Google OAuth login feature)
- Database: SQLite in tempdir with automatic init_database() call handling users, professional_reports, saved_universities, user_cvs tables
- Deployment: Streamlit Cloud with automatic GitHub integration, zero-downtime deploys from main branch
- Debugging: Langfuse dashboard for tracing AI generations
- File Organization: 22 Python files structured as pages/ (14 UI), services/ (2), utils/ (2), scripts(1), top-level helpers (styles.py, zapp.py)
- Static Assets: data/ folder with 6 images for CSS backgrounds and branding
- Documentation: ARCHITECTURE.md and inline docstrings following Google Python style, README.md file with project details and instructions

### AI & Monitoring
- LLM Provider: Google Gemini (`gemini-2.5-flash`) and Google Gemini (`gemini-2.0-flash-001`)
- Observability: Langfuse v3.11.1
- Function Calling: 6 custom Portuguese education tools (get_job_listings,get_learning_resources, get_cif_improvement_tips, get_study_resources, get_exam_past_papers,get_portugal_scholarships)

Langfuse v3.11.1 wrapped all Gemini calls to track prompts, responses, and user feedback. Exceptionally, function calls in student_resources.py and resources.py were not wrapped, using @observe method. We created six custom tools for Portuguese students including study resource links, scholarship info, IAVE exam papers, and CIF improvement tips. For professionals, they can ask to retrieve courses (e.e. pyhton courses) and job openings from LinkedIn. Gemini's multimodal capabilities processed PDF/DOCX/image uploads directly.


### Deployment
- Platform: Streamlit Cloud
- Environment Management: .env files (local), Streamlit secrets (production)
We deployed to Streamlit Cloud which worked perfectly for our GitHub-based workflow. SQLite tempdir handled persistence without external databases. Environment variables secured our API keys in Streamlit Secrets.


---

## System Architecture

We organized the app with zapp.py routing between student_dashboard.py and professional_dashboard.py based on user type. Student features include student_career_quiz.py (adaptive open style questions), degree_picker.py (adaptive yes or no questions), grades_analysis.py (grade calculator), university_finder.py and student_resources.py (quick search with fucntion calling + AI chat). Professional features include cv_analysis.py (PDF parsing), career_growth_quiz.py (CV-aware), interview_simulator.py (CV aware), cv_builder.py (creating a CV, creating a cover letter) and resources.py (quick search with function calling + AI chatbot)

The services folder contains authentication.py and langfuse_helper.py. The utils folder contains database.py and reports.py: database.py handles all SQLite operations across reports, universities, and CVs; reports.py shows saved results in tabbed interfaces (both student and professional). Styles.py provides consistent CSS styling components everywhere.

```
careercorner2/
├── pages/ # User-facing pages
│ ├── student_dashboard.py
│ ├── student_chat.py
│ ├── degree_picker.py
│ ├── grades_analysis.py
│ ├── university_finder.py
│ ├── student_resources.py
│ ├── professional_dashboard.py
│ ├── professional_chat.py
│ ├── career_growth_quiz.py
│ ├── cv_analysis.py
│ ├── interview_simulator.py
│ ├── cv_builder.py
│ └── resources.py
├── services/ # business logic + external integrations
│ ├── __init__.py
│ ├── authentication.py  # manual and Google Login/session helpers
│ └── langfuse_helper.py  # Langfuse + Gemini wrappers
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
│ └── ARCHITECTURE.md
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
- Professional pages (6 files): professional_dashboard.py, professional_chat.py, career_growth_quiz.py (CV-aware), cv_analysis.py (PDF parsing), interview_simulator.py (mock interviews), cv_builder.py (quiz to PDF)
- All pages include progress bars, back/next navigation, and auto-save confirmations

**Service Layer** (`services/`)
- authentication.py handles SQLite users, Google OAuth, and login/register UIs
- langfuse_helper.py provides LangfuseGeminiWrapper for all Gemini calls with tracing
- Both services imported across pages for consistent authentication and observability

**Data Layer** (`utils/`)
- database.py manages SQLite CRUD operations for reports, universities, and CVs with tempdir persistence
- reports.py renders tabbed My Reports interfaces with CV selectors and delete functionality
- Auto-saves all results with timestamps and user tracking

**Styling Layer** (`styles.py`)
- Custom CSS with DM Sans typography, lime/yellow color scheme, and animations
- Hover effects, stat cards, and progress bars applied consistently
- apply_custom_css called from zapp.py across all pages

**Assets Layer** (`data/`)
- Background images (bg1.png, bg2.png), logo (careercornerlogo2.png)
- DGES data (result from running scripts/build_dges_universities.py)
- Sidebar textures (crumpledpaper2.jpg, crumpledpaper3.avif)

**Scripts Layer** (`scripts/`)
- build_dges_universities.py for one-off DGES data imports (commented out)
- Empty __init__.py maintains folder structure

**Structure Benefits**
- 18 modular files for clean Git management
- Clear separation between UI, services, and data layers
- No circular imports with services -> utils -> pages flow
- Streamlit-native deployment ready

---

## Data Flow

### Example: Career Discovery Quiz

1. User Input: Student answers adaptive personality question
2. Service Layer: gemini_service sends prompt to Gemini with conversation history
3. AI Generation: Gemini generates next adaptive question based on previous answers
4. Observability: Langfuse logs trace (prompt, response, metadata)
5. UI Update: Streamlit displays next question
6. Repeat: 10 questions total
7. Final Analysis: Gemini analyzes all answers, generates career sector matches
8. Storage: Report saved to SQLite via database.py, accesible in "My reports" section
9. Display: Results shown with sector percentages and recommended degrees

---

## AI Integration

### LLM Configuration

**Primary Client** (`gemini-2.5-flash`):
-  Career Quiz Questions: 0.9
- Dashboard Chats: 0.5 
- Degree Picker -0.2
- CV builder -0.4
- Career Growth Quiz; CV analysis- 0.3
- Interview prep -0.5
- Extracting info - 0.1


### Prompt Engineering Strategy

Structured Outputs: Using markdown formatting for parseable reports
System Instructions: Persona definitions for consistent tone
Example: "You are a creative career counselor for Portuguese students. Ask unexpected questions that reveal thinking styles, not direct career preferences."

---

## Function Calling & Tools

### Available Tools

1. get_job_listings(role, location): LinkedIn job search links for Portugal (recent postings + senior roles)
2. get_learning_resources(skill, career_field): Coursera/Khan Academy courses (Python, Data Science, ML, Nursing + dynamic search)
3. get_study_resources(subject): Dynamic study links (Khan Academy, Coursera, YouTube, Quizlet, Reddit for any subject)
4. get_portugal_scholarships(degree): DGES Bolsas, FCT, Erasmus+ opportunities
5. get_exam_past_papers(subject): IAVE nacional exams (current year + full archive)
6. get_cif_improvement_tips(cif_score): Personalized +2 point CIF improvement plans by score tier (under 14, 14-16, 16-18, 18+)


### Tool Implementation Approach
Gemini's native function calling extracts parameters from user queries and routes to appropriate tools. Each tool returns structured JSON that the AI converts into natural language responses.

---

## Document Processing

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
- Native Streamlit support (zero config)
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

1. RAG Implementation: If degree database grows beyond context limits
2. Mobile Optimization: Responsive design for phone usage
3. International Grades Analysis and University Finder, in addition to the Portuguese one already implemented; possible document ingestion for grades analysis to be possible in different countries (report cards, for example)
4. Advanced Analytics: Career trend predictions, salary data integration
5. Mobile App friendly development, different interface choice

### Scalability Considerations

Our current architecture supports hundreds of concurrent users (Streamlit Cloud limits) and SQLite is sufficient for thousands of user records.
If scaling was needed we could migrate to PostgreSQL (relational data), add Redis for session caching and deploy to AWS/GCP for higher throughput
RAG implementation would support thousands of university programs via vector similarity matching beyond Gemini's context window. Advanced analytics could integrate salary trends and employment statistics.

---


### Bonus Features Implemented

Multimodal document processing handles real CVs natively. 
Real-time CIF optimization provides actionable +2 point strategies leveraging exam weighting. Polished UI delivers custom animations, progress tracking, and intuitive cross-tool navigation.
Auto-saving reports with CV selectors create persistent user portfolios.
CV-aware adaptive quizzes personalize professional assessments using parsed experience data.
---

End of Architecture Documentation