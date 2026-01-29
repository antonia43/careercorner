# CareerCorner Tools Documentation

## Overview

This document provides comprehensive documentation for all tools and functions used in the CareerCorner application. The tools leverage Google's Gemini AI with built-in search capabilities to provide career guidance, job search assistance, and educational resources.

## Table of Contents

1. [Tool Types Overview](#tool-types-overview)
   - [Built-in Tools (Google Search & URL Context)](#1-built-in-tools-google-search--url-context)
   - [Function Calling Tools (Custom Python Functions)](#2-function-calling-tools-custom-python-functions)
   - [Comparison at a Glance](#comparison-at-a-glance)
   - [How They Work Together](#how-they-work-together)
2. [Setup and Configuration](#setup-and-configuration)
3. [Built-in Tools: Core Functions](#built-in-tools-core-functions)
4. [Built-in Tools: UI Rendering Functions](#built-in-tools-ui-rendering-functions)
5. [Helper Functions](#helper-functions)
6. [Function Calling Tools](#function-calling-tools)
   - [Student Tools](#student-tools)
   - [Professional Tools](#professional-tools)
   - [Function Calling vs Built-in Tools](#function-calling-vs-built-in-tools)
7. [Usage Examples](#usage-examples)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)


---

## Tool Types Overview

CareerCorner uses **two distinct types of AI tools** to provide comprehensive career guidance:

### 1. Built-in Tools (Google Search & URL Context)

**What they are**: Native Google Gemini capabilities that access external web data in real-time.

**Tools available**:
- 🌐 **Google Search** (`types.GoogleSearch()`) - Real-time web search with grounding
- 🔗 **URL Context** (`types.UrlContext()`) - Extract content from specific URLs

**Purpose**: Retrieve current information from the internet
- Study resources (courses, tutorials, videos)
- Career paths and job options
- Salary information by country
- Company research and reviews
- Job postings and opportunities
- LinkedIn optimization tips
- Online course recommendations
- Job description URL extractor 

**Data source**: Public internet, updated in real-time

**When to use**: Need current, general information that's publicly available online

**Sections in this document**:
- [Built-in Tools: Core Functions](#built-in-tools-core-functions)
- [Built-in Tools: UI Rendering Functions](#built-in-tools-ui-rendering-functions)

---

### 2. Function Calling Tools (Custom Python Functions)

**What they are**: Custom Python functions that Gemini can invoke to access CareerCorner's database and user-specific data.

**Tools available**:
- **Student Tools** (4 functions) - Grades, saved universities, DGES database
- **Professional Tools** (5 functions) - CV analysis, career quiz, skill gaps, roadmaps

**Purpose**: Access user-specific data and perform personalized calculations
- User's admission grades (CIF)
- Saved universities and programs
- CV analysis and work history
- Career quiz results
- Skill gap analysis
- Personalized career roadmaps

**Data source**: CareerCorner application database (SQLite)

**When to use**: Need user-specific, personalized information that's stored in the application

**Sections in this document**:
- [Function Calling Tools](#function-calling-tools)

---

### Comparison at a Glance

| Aspect | Built-in Tools | Function Calling Tools |
|--------|----------------|----------------------|
| **Type** | Google's native tools | Custom Python functions |
| **Data Source** | Public internet | Application database |
| **Information** | General, current | User-specific, personalized |
| **Examples** | Course search, job search | User grades, saved data |
| **Latency** | Higher (web search) | Lower (local database) |
| **Requires** | Internet connection | Database access |
| **Updates** | Real-time | Based on user actions |
| **Monitoring** | Google's infrastructure | Langfuse observability |

---

### How They Work Together

CareerCorner uses **both tool types in combination** to provide the best experience:

**Example 1: Personalized University Search**
```
User: "Find me universities I can get into with my grade"

Workflow:
1. 🔧 Function Calling: calculate_admission_grade(user_id) 
   → Gets user's grade: 17.85/20

2. 🔧 Function Calling: search_dges_database("Engineering", "Lisbon")
   → Finds programs with requirements

3. 🌐 Google Search: "University of Lisbon Engineering program reviews"
   → Gets current student reviews and rankings

4. 🤖 Gemini combines all data:
   → Personalized recommendations with web context
```

**Example 2: Career Transition Planning**
```
User: "I want to become a Data Scientist. What should I do?"

Workflow:
1. 🔧 Function Calling: get_professional_profile(user_id)
   → Gets user's CV and career quiz data

2. 🔧 Function Calling: analyze_skill_gaps(user_id, "Data Scientist")
   → Identifies missing skills (ML, Statistics)

3. 🌐 Google Search: "Machine Learning online courses"
   → Finds Coursera, Udemy courses

4. 🔧 Function Calling: get_career_roadmap(user_id, "Data Scientist", "1 year")
   → Creates personalized timeline

5. 🤖 Gemini delivers:
   → Complete transition plan with specific resources
```

---



## Setup and Configuration

### Dependencies

```python
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
```

### Environment Variables

Required environment variables in `.env` file:
- `GOOGLE_API_KEY`: Your Google Gemini API key

### Client Initialization

```python
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
```

The client is initialized as a raw client to access Google's built-in tools including:
- Google Search (`GoogleSearch()`)
- URL Context (`UrlContext()`)

---

## Built-in Tools: Core Functions

### 1. `get_study_resources_web(subject: str) -> dict`

**Purpose**: Searches for free study resources on a specific subject using Google Search.

**Parameters**:
- `subject` (str): The academic subject or topic to search for (e.g., "Python", "Biology", "Calculus")

**Returns**:
- `dict` with keys:
  - `success` (bool): Whether the operation succeeded
  - `answer` (str): Formatted markdown response with resources and links
  - `sources` (list): List of dicts with `title` and `url` for each source
  - `error` (str): Error message if `success` is False

**Features**:
- Searches for free online courses (Coursera, edX, Khan Academy)
- Finds video tutorials and YouTube playlists
- Locates practice websites and tools
- Identifies community resources (Discord, Reddit, forums)
- Provides direct clickable links to 8-10+ resources

**Model Configuration**:
- Model: `gemini-2.5-flash`
- Tools: Google Search

**Example**:
```python
result = get_study_resources_web("Machine Learning")
if result["success"]:
    print(result["answer"])  # Markdown formatted resource list
    print(result["sources"])  # Source metadata
```

---

### 2. `get_career_options(course_name: str) -> dict`

**Purpose**: Discovers career paths and job positions for a specific degree or course.

**Parameters**:
- `course_name` (str): Name of the degree or course (e.g., "Computer Science", "Medicine")

**Returns**:
- `dict` with keys:
  - `success` (bool): Operation status
  - `answer` (str): Markdown formatted career information
  - `sources` (list): Up to 5 source citations
  - `error` (str): Error message if applicable

**Features**:
- Entry-level position titles
- Mid-level career progression paths
- Senior/leadership roles
- Average salary ranges for each level
- Industry sectors that hire graduates with this degree

**Model Configuration**:
- Model: `gemini-2.5-flash`
- Tools: Google Search
- Output: Clean markdown (no code blocks)

**Example**:
```python
result = get_career_options("Data Science")
# Returns career paths from junior analyst to chief data officer
```

---

### 3. `get_wage_info(job_title: str, country: str = "Portugal") -> dict`

**Purpose**: Retrieves salary information for a specific job title in a given country.

**Parameters**:
- `job_title` (str): The job position (e.g., "Software Engineer", "Nurse")
- `country` (str, optional): Country for salary data. Default: "Portugal"

**Returns**:
- `dict` with standard format (success, answer, sources, error)

**Features**:
- Entry-level salary (annual and monthly)
- Mid-level salary (annual and monthly)
- Senior-level salary (annual and monthly)
- Clean markdown formatting
- Plain text numbers (e.g., "$85,000", not code blocks)

**Model Configuration**:
- Model: `gemini-2.5-flash`
- Tools: Google Search
- Sources: Limited to top 3

**Example**:
```python
result = get_wage_info("Data Analyst", "United States")
# Returns salary breakdown by experience level
```

---

### 4. `get_job_search_results(role: str, location: str = "Portugal") -> dict`

**Purpose**: Finds current job openings for a specific role and location.

**Parameters**:
- `role` (str): Job role or position title
- `location` (str, optional): Geographic location. Default: "Portugal"

**Returns**:
- `dict` with standard format

**Features**:
- Direct links to job postings (LinkedIn, Indeed, Glassdoor)
- Company career pages
- Recruitment agencies specializing in the field
- Location-specific job platforms
- At least 10 direct job links with company names and titles

**Model Configuration**:
- Model: `gemini-2.5-flash`
- Tools: Google Search
- Sources: All grounding chunks included

**Example**:
```python
result = get_job_search_results("Product Manager", "London")
# Returns 10+ direct job posting links
```

---

### 5. `get_course_recommendations(skill: str) -> dict`

**Purpose**: Finds online courses for learning a specific skill.

**Parameters**:
- `skill` (str): The skill to learn (e.g., "Python", "Project Management")

**Returns**:
- `dict` with standard format

**Features**:
- Courses from major platforms:
  - Coursera
  - Udemy
  - edX
  - Udacity
  - LinkedIn Learning
  - FreeCodeCamp
  - YouTube playlists
- Both free and paid options
- Direct clickable course links

**Model Configuration**:
- Model: `gemini-2.5-flash`
- Tools: Google Search

**Example**:
```python
result = get_course_recommendations("React.js")
# Returns course links from multiple platforms
```

---


### 6. `get_linkedin_profile_optimization(...) -> dict`

**Purpose**: Optimizes LinkedIn profiles for specific target roles using AI and research.

**Parameters**:
- `current_headline` (str): Current LinkedIn headline
- `current_about` (str): Current About/Summary section
- `target_role` (str): Desired job role
- `industry` (str): Target industry
- `skills` (str): Current skill list

**Returns**:
- `dict` with standard format (up to 5 sources)

**Features**:
1. 3-5 optimized headline options (keyword-rich, ATS-friendly)
2. Rewritten About section with impact statements
3. Recommended skills to add
4. Profile improvement checklist (photo, banner, featured section)
5. Engagement strategy (posting tips, networking advice)

**Model Configuration**:
- Model: `gemini-2.5-flash`
- Tools: Google Search
- Researches best practices for specific roles

**Example**:
```python
result = get_linkedin_profile_optimization(
    current_headline="Student at University",
    current_about="Passionate about technology...",
    target_role="Data Scientist",
    industry="Technology",
    skills="Python, SQL, Machine Learning"
)
# Returns comprehensive profile optimization advice
```

---

### 7. `get_company_research(company_name: str) -> dict`

**Purpose**: Provides comprehensive research on a company for job application preparation.

**Parameters**:
- `company_name` (str): Name of the company to research

**Returns**:
- `dict` with standard format (up to 8 sources)

**Features**:
- Company culture and values
- Recent news and developments
- Employee reviews and ratings (Glassdoor, Indeed)
- Work environment and benefits
- Career growth opportunities
- Salary information
- Both positive and negative aspects

**Model Configuration**:
- Model: `gemini-2.5-flash`
- Tools: Google Search

**Example**:
```python
result = get_company_research("Microsoft")
# Returns detailed company information from multiple sources
```

---

### 8. `fetch_job_description_from_url(url: str) -> dict`

**Purpose**: Extracts job description from a URL using Gemini's URL context tool.

**Parameters**:
- `url` (str): URL of the job posting

**Returns**:
- `dict` with keys:
  - `success` (bool): Operation status
  - `job_description` (str): Extracted job details
  - `source_url` (str): Original URL
  - `error` (str): Error message if applicable

**Features**:
- Extracts job title, company name, responsibilities, requirements
- Formats as clean text
- Uses URL context tool (not Google Search)

**Model Configuration**:
- Model: `gemini-2.5-flash`
- Tools: URL Context

**Example**:
```python
result = fetch_job_description_from_url("https://careers.google.com/jobs/...")
if result["success"]:
    print(result["job_description"])
```

---

## Built-in Tools: UI Rendering Functions

### 1. `render_exam_papers_tool()`

**Purpose**: Displays direct links to IAVE nacional exam papers.

**Features**:
- Link to current year exams
- Link to complete archive (all years)
- Clean UI with buttons and captions
- No API calls (static links only)

**UI Components**:
- `st.subheader()`: Section title
- `st.info()`: Description
- `st.link_button()`: Direct links to IAVE website
- `st.caption()`: Usage tips

---

### 2. `render_scholarships_tool()`

**Purpose**: Displays scholarship and financial aid resources.

**Features**:
- DGES Scholarships (Portuguese government)
- FCT Research Grants (research funding)
- Erasmus+ Mobility (study abroad)
- Direct links with descriptions

**UI Components**:
- Container blocks for each scholarship
- Link buttons with descriptions
- Dividers between sections

---

### 3. `render_study_resources_tool()`

**Purpose**: Interactive tool for finding study resources with Google Search.

**Features**:
- Text input for subject
- Search button triggers `get_study_resources_web()`
- Displays markdown-formatted results
- Expandable sources section

**UI Components**:
- `st.text_input()`: Subject input
- `st.button()`: Trigger search
- `st.spinner()`: Loading indicator
- `st.markdown()`: Display results
- `st.expander()`: Show/hide sources

---

### 4. `render_career_options_tool()`

**Purpose**: Interactive career exploration tool.

**Features**:
- Text input for course/degree name
- Calls `get_career_options()`
- Displays career paths and salary info
- Source citations

**UI Components**:
- Similar structure to study resources tool
- Error handling with `st.error()`
- Warning for empty inputs

---

### 5. `render_wage_finder_tool()`

**Purpose**: Salary information lookup tool with country selection.

**Features**:
- Two-column layout (job title, country)
- Custom country selector with "Other" option
- Calls `get_wage_info()`
- Displays salary breakdown by experience level

**UI Components**:
- `st.columns()`: Layout structure
- `render_country_selector()`: Country dropdown
- Standard result display pattern

---

### 6. `render_job_search_tool()`

**Purpose**: Job search interface with location options.

**Features**:
- Role/company input
- Location selector (cities + countries + remote)
- Custom location option
- Calls `get_job_search_results()`
- Displays direct job posting links

**UI Components**:
- Two-column layout
- Custom location dropdown with cities and countries
- "Other" option for custom locations

---

### 7. `render_course_finder_tool()`

**Purpose**: Course discovery tool for skill learning.

**Features**:
- Skill input field
- Calls `get_course_recommendations()`
- Displays course links from multiple platforms
- Free and paid options

**UI Components**:
- Simple single-input layout
- Standard button and result display

---


### 8. `render_linkedin_optimizer_tool()`

**Purpose**: Comprehensive LinkedIn profile optimization interface.

**Features**:
- Multiple input fields:
  - Current headline
  - Current about section (text area)
  - Target role
  - Industry dropdown
  - Skills list
- Calls `get_linkedin_profile_optimization()`
- Displays optimization suggestions

**UI Components**:
- Section headers for organization
- Two-column layout for target info
- `st.text_area()` for longer text input
- `st.selectbox()` for industry
- Validation for required fields

---

### 9. `render_company_research_tool()`

**Purpose**: Company research and analysis tool.

**Features**:
- Company name input
- Calls `get_company_research()`
- Displays comprehensive company information
- Up to 8 source citations

**UI Components**:
- Simple input and button layout
- Extensive result display with sources

---

## Helper Functions

### `render_country_selector(key_prefix: str, label: str = "Country:", default: str = "Portugal") -> str`

**Purpose**: Creates a reusable country dropdown with "Other" option for custom input.

**Parameters**:
- `key_prefix` (str): Unique prefix for Streamlit widget keys
- `label` (str, optional): Label text for dropdown. Default: "Country:"
- `default` (str, optional): Default selected country. Default: "Portugal"

**Returns**:
- `str`: Selected country name

**Features**:
- 24 predefined countries including:
  - European countries (Portugal, Spain, UK, Germany, France, etc.)
  - North America (US, Canada)
  - Asia-Pacific (Japan, Singapore, Australia)
  - Middle East (UAE)
  - Latin America (Brazil)
  - "Other" option for custom input
- Custom text input appears when "Other" is selected
- Fallback to "Portugal" if custom input is empty
- Unique keys prevent Streamlit widget conflicts

**Usage**:
```python
country = render_country_selector("wage_finder", "Country:", "Portugal")
# Returns selected country name for use in API calls
```

---

## Usage Examples

### Example 1: Complete Study Resources Workflow

```python
# In Streamlit app
def main():
    render_study_resources_tool()

# User enters "Python" -> clicks search
# get_study_resources_web("Python") is called
# Results displayed with sources
```

### Example 2: Job Search with Custom Location

```python
# User flow:
# 1. Enters "Software Engineer" as role
# 2. Selects "Other" from location dropdown
# 3. Types "Singapore" in custom location field
# 4. Clicks "Search Jobs"
# Result: get_job_search_results("Software Engineer", "Singapore")
```

### Example 3: LinkedIn Profile Optimization

```python
# Complete optimization workflow
result = get_linkedin_profile_optimization(
    current_headline="Computer Science Student",
    current_about="I am passionate about coding and problem solving...",
    target_role="Machine Learning Engineer",
    industry="Technology",
    skills="Python, TensorFlow, Deep Learning, NLP"
)

# Result includes:
# - 3-5 ATS-optimized headlines
# - Rewritten about section with impact metrics
# - Additional skills to add (MLOps, PyTorch, etc.)
# - Profile checklist (professional photo, custom banner)
# - Engagement strategy (post frequency, content ideas)
```

### Example 4: Error Handling Pattern

```python
# All core functions follow this pattern
result = get_career_options("Business Administration")

if result["success"]:
    # Display answer
    st.markdown(result["answer"])

    # Show sources
    if result["sources"]:
        with st.expander("View Sources"):
            for source in result["sources"]:
                st.markdown(f"[{source['title']}]({source['url']})")
else:
    # Handle error
    st.error(f"Error: {result.get('error', 'Unknown error')}")
```

---

## Error Handling

### Try-Catch Pattern

All core functions use consistent error handling:

```python
try:
    response = client.models.generate_content(...)
    # Process response
    return {"success": True, "answer": ..., "sources": ...}
except Exception as e:
    return {"success": False, "error": str(e)}
```

### Common Error Scenarios

1. **API Key Missing**: Environment variable not set
   - Solution: Check `.env` file and `GOOGLE_API_KEY`

2. **Rate Limiting**: Too many API calls
   - Solution: Implement retry logic or rate limiting

3. **Invalid Input**: Empty strings or malformed data
   - Solution: Input validation in UI functions (warnings)

4. **Network Errors**: Connection issues
   - Solution: Try-catch returns error dict for graceful handling

5. **Model Errors**: Gemini API errors
   - Solution: Error message displayed to user via `st.error()`

### Input Validation

UI functions validate user input before API calls:

```python
if subject.strip():
    # Proceed with search
    results = get_study_resources_web(subject.strip())
else:
    # Show warning
    st.warning("Please enter a subject")
```

---

## Best Practices

### 1. API Usage

- Use `gemini-2.5-flash` for fast, cost-effective responses
- Limit sources to relevant number (3-8 depending on use case)
- Strip whitespace from user inputs
- Provide clear, specific prompts to the model

### 2. UI Design

- Use consistent button styling (`use_container_width=True`, `type="primary"`)
- Show loading indicators with `st.spinner()`
- Organize with `st.columns()` for multi-field inputs
- Use `st.expander()` for optional information (sources)
- Add helpful `st.caption()` for usage tips

### 3. Response Formatting

- Request clean markdown (no code blocks) for readability
- Ask for direct links in responses
- Specify minimum number of resources (8-10 for study resources)
- Request structured output (headers, bullet points)

### 4. Key Management

- Use unique `key` parameter for all Streamlit widgets
- Follow naming pattern: `{tool_name}_{field_name}`
- Use `key_prefix` in helper functions to avoid conflicts

### 5. Error Messages

- Display user-friendly errors with `st.error()`
- Show warnings for empty inputs with `st.warning()`
- Include error details from API for debugging

---

## Configuration Summary

### Model: `gemini-2.5-flash`

**Reasons for Selection**:
- Fast response times
- Cost-effective for high-volume usage
- Sufficient capability for search and summarization tasks
- Supports built-in tools (Google Search, URL Context)

### Built-in Tools

1. **Google Search** (`types.GoogleSearch()`):
   - Real-time web search results
   - Grounding chunks with source attribution
   - Used by most functions

2. **URL Context** (`types.UrlContext(url=url)`):
   - Extract content from specific URLs
   - Used by `fetch_job_description_from_url()`
   - Requires exact URL

### Response Structure

All core functions return consistent dict format:
```python
{
    "success": bool,
    "answer": str,           # Markdown formatted
    "sources": [             # List of source dicts
        {"title": str, "url": str},
        ...
    ],
    "error": str             # Only if success=False
}
```

---

## Integration Notes

### Streamlit Cloud Deployment

- Store API key in Streamlit secrets
- Update client initialization:
  ```python
  api_key = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]
  client = genai.Client(api_key=api_key)
  ```

### Database Integration

Functions can be extended to log:
- User queries
- Search results
- Popular searches
- Error rates

### Caching Considerations

Consider caching for:
- Common searches (e.g., "Python" study resources)
- Static data (salary ranges update infrequently)
- Use `@st.cache_data` with TTL

Example:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_study_resources_web_cached(subject: str) -> dict:
    return get_study_resources_web(subject)
```

---

## Future Enhancements

### Potential Improvements

1. **Search Refinement**: Add filters (free only, specific platforms, language)
2. **Personalization**: Remember user preferences and past searches
3. **Analytics**: Track most searched topics and resources
4. **Bookmarking**: Save favorite resources
5. **Comparison Tools**: Side-by-side course comparisons
6. **Progress Tracking**: Track learning goals and applications
7. **Notifications**: Alert for new jobs matching criteria
8. **Multi-language**: Support for Portuguese and other languages

### Advanced Features

1. **Resume Parsing**: Extract experience from resumes
2. **Cover Letter Generator**: Based on job description
3. **Interview Prep**: Company-specific interview questions
4. **Skill Gap Analysis**: Compare current vs. required skills
5. **Learning Path**: Personalized course sequences
6. **Salary Negotiation**: Data-driven negotiation tips

---

## Troubleshooting

### Common Issues

**Issue**: "API key not found"
- **Solution**: Check `.env` file exists and contains `GOOGLE_API_KEY=your_key`

**Issue**: Empty sources list
- **Solution**: Some queries may not return grounding chunks. This is normal.

**Issue**: Markdown not rendering
- **Solution**: Ensure using `st.markdown()`, not `st.write()` for formatted text

**Issue**: Widget key errors
- **Solution**: Ensure all widgets have unique keys with proper prefixes

**Issue**: Slow responses
- **Solution**: Check internet connection; Gemini API may have latency

---

## Contact & Support

For issues with this codebase:
1. Check error messages in Streamlit UI
2. Review API key configuration
3. Verify Google Gemini API status
4. Check rate limits and quotas

---



---

## Function Calling Tools

### Overview

CareerCorner uses custom Python functions as tools that Gemini can invoke to access user-specific data and application features.

**Key difference from Built-in Tools**: While Google Search retrieves general web information, Function Calling Tools access your personal data stored in CareerCorner's database.

---

## Function Calling Tools Architecture

### Components

Function calling tools consist of three parts:

1. **Function Declaration** - Tells Gemini what functions exist and their parameters
2. **Function Implementation** - Actual Python code that executes with retry logic
3. **Function Dispatcher** - Routes Gemini's calls to the correct implementation

```python
# 1. Declaration (what Gemini sees)
tool = types.FunctionDeclaration(
    name="search_saved_universities",
    description="Search user's saved universities",
    parameters={...}
)

# 2. Implementation (what actually runs)
@observe(name="search_saved_universities")
def search_saved_universities(degree_name, country="All"):
    # Database query logic with retry
    pass

# 3. Dispatcher (routing)
FUNCTION_HANDLERS = {
    "search_saved_universities": search_saved_universities
}
```

### Monitoring with Langfuse

All functions use `@observe` decorator for:
- Performance tracking
- Error monitoring
- Usage analytics
- Debugging support

---

## Student Tools

Tools for students to access grades, saved universities, and DGES database.

### Configuration

```python
STUDENT_TOOLS = types.Tool(function_declarations=[
    search_universities_tool,
    calculate_admission_grade_tool,
    search_dges_database_tool,
    get_student_data_tool
])
```

---

### 1. search_saved_universities

**Type**: Function Calling Tool

**Purpose**: Search through user's saved universities and programs

**When Gemini calls**: User asks about saved universities, wants to compare programs, needs info about saved degrees

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `degree_name` | string | Yes | - | Degree to search (e.g., "Computer Science") |
| `country` | string | No | "All" | Filter: "Portugal", "International", "All" |

#### Returns

```python
{
    "success": True,
    "universities": [
        {
            "university": "University of Lisbon",
            "program": "Computer Science Engineering",
            "location": "Lisbon",
            "type": "Public",
            "grade_required": "17.5/20",
            "duration": "3 years"
        }
    ],
    "total_saved": 5,
    "matching_count": 1
}
```

#### Use Cases

- "Show me all Computer Science programs I saved"
- "What engineering degrees did I save in Portugal?"
- "Which universities did I bookmark for Medicine?"

#### Example

```
User: "What Computer Science programs did I save?"

Gemini calls: search_saved_universities("Computer Science", "All")

Response: "You have 3 Computer Science programs saved:
- University of Lisbon: CS Engineering (17.5/20)
- University of Porto: Informatics Engineering (16.8/20)
- IST: Computer Science (18.0/20)"
```

---

### 2. calculate_admission_grade

**Type**: Function Calling Tool

**Purpose**: Calculate student's admission average (CIF) from grades

**When Gemini calls**: User asks about chances, admission average, university qualification

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID to fetch grades |

#### Returns

```python
{
    "success": True,
    "has_grades": True,
    "cif_200_scale": 178.5,
    "cif_20_scale": 17.85,
    "weights_used": {
        "exam_weight": 0.5,
        "coursework_weight": 0.5
    },
    "message": "Student's admission average: 17.85/20"
}
```

#### Use Cases

- "What's my admission average?"
- "Can I get into this university?"
- "Do I meet the grade requirement?"

---

### 3. search_dges_database

**Type**: Function Calling Tool

**Purpose**: Search Portuguese university database (DGES) for degrees

**When Gemini calls**: User wants to find Portuguese universities for a specific degree

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `degree_name` | string | Yes | - | Degree in Portuguese (e.g., "Engenharia Informática") |
| `location` | string | No | "All of Portugal" | Region: "Lisbon", "Porto", "Coimbra", etc. |
| `max_results` | integer | No | 10 | Max results (1-50) |

#### Returns

```python
{
    "success": True,
    "universities": [
        {
            "university": "Instituto Superior Técnico",
            "program": "Engenharia Informática e de Computadores",
            "location": "Lisbon",
            "type": "Public",
            "last_grade": "18.2/20",
            "vacancies": 180
        }
    ],
    "total_found": 15
}
```

#### Use Cases

- "Show me Computer Engineering programs in Lisbon"
- "What's the grade needed for Medicine in Porto?"
- "List all Engineering programs in Portugal"

---

### 4. get_student_profile

**Type**: Function Calling Tool

**Purpose**: Get complete student profile (grades, saved universities, preferences)

**When Gemini calls**: Needs context about student for personalized advice

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID |

#### Returns

```python
{
    "success": True,
    "profile": {
        "user_id": "student123",
        "has_grades": True,
        "has_degree_reports": True,
        "has_saved_universities": True,
        "admission_average": 17.85,
        "saved_universities_count": 5,
        "degree_reports_count": 2
    }
}
```

#### Use Cases

- "What should I do next in my university search?"
- "What information am I missing?"
- Context gathering for personalized advice

---

## Professional Tools

Tools for professionals to access CV, career quiz, and career planning features.

### Configuration

```python
PROFESSIONAL_TOOLS = types.Tool(function_declarations=[
    get_cv_analysis_tool,
    get_career_quiz_results_tool,
    analyze_skill_gaps_tool,
    get_career_roadmap_tool,
    get_professional_profile_tool
])
```

---

### 5. get_cv_analysis

**Type**: Function Calling Tool

**Purpose**: Get professional's CV analysis (skills, experience, recommendations)

**When Gemini calls**: Needs to reference background, skills, work history

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID |

#### Returns

```python
{
    "success": True,
    "has_cv": True,
    "cv_title": "Software Engineer CV",
    "cv_data": {
        "skills": ["Python", "React", "AWS"],
        "experience": [...],
        "education": [...]
    },
    "total_cvs": 3
}
```

#### Use Cases

- "Does my CV match this job description?"
- "What skills are on my CV?"
- "Summarize my work history"

---

### 6. get_career_quiz_results

**Type**: Function Calling Tool

**Purpose**: Get career quiz results (personality, interests, career paths)

**When Gemini calls**: Advising on career direction or job fit

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID |

#### Returns

```python
{
    "success": True,
    "has_quiz": True,
    "quiz_data": {
        "personality_type": "INTJ",
        "interests": ["Technology", "Problem-solving"],
        "recommended_paths": ["Data Science", "Software Architecture"]
    }
}
```

#### Use Cases

- "Is this job a good fit for me?"
- "Should I transition to data science?"
- "What are my career strengths?"

---

### 7. analyze_skill_gaps

**Type**: Function Calling Tool

**Purpose**: Analyze skill gaps between current CV and target role

**When Gemini calls**: Advising on career transitions or upskilling

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID |
| `target_role` | string | Yes | Target role (e.g., "Data Scientist") |

#### Returns

```python
{
    "success": True,
    "target_role": "Data Scientist",
    "required_skills": ["Python", "ML", "SQL", "Statistics"],
    "existing_skills": ["Python", "SQL"],
    "missing_skills": ["ML", "Statistics"],
    "gap_percentage": 50.0,
    "recommendations": [...]
}
```

#### Supported Roles

| Role | Key Skills |
|------|-----------|
| Data Scientist | Python, ML, SQL, Statistics, Data Viz, Deep Learning |
| Software Engineer | Programming, Algorithms, System Design, Git, Testing |
| Product Manager | Strategy, Roadmapping, Analytics, UX/UI, Agile |
| Marketing Manager | Digital Marketing, SEO/SEM, Analytics, Social Media |
| Data Analyst | SQL, Excel, Data Viz, Statistics, Python/R, BI |
| UX Designer | User Research, Wireframing, Prototyping, Usability |

#### Use Cases

- "What skills do I need to become a Data Scientist?"
- "What am I missing for a Product Manager role?"
- "What should I learn next?"

---

### 8. get_career_roadmap

**Type**: Function Calling Tool

**Purpose**: Generate personalized career roadmap

**When Gemini calls**: User asks about career progression or next steps

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `user_id` | string | Yes | - | User ID |
| `target_role` | string | Yes | - | Target role |
| `timeframe` | string | No | "1 year" | "6 months", "1 year", "2 years" |

#### Roadmap Templates

**6 Months:**
1. Months 1-2: Skill Assessment & Learning
2. Months 3-4: Skill Development
3. Months 5-6: Job Search & Application

**1 Year:**
1. Months 1-3: Skill Assessment
2. Months 4-6: Building Experience
3. Months 7-9: Career Positioning
4. Months 10-12: Job Search

**2 Years:**
1. Months 1-6: Foundation Building
2. Months 7-12: Intermediate Growth
3. Months 13-18: Advanced Development
4. Months 19-24: Transition

#### Use Cases

- "How do I become a Senior Engineer?"
- "Timeline to switch to Product Management?"
- "What should I do each month?"

---

### 9. get_professional_profile

**Type**: Function Calling Tool

**Purpose**: Get complete professional profile

**When Gemini calls**: Needs comprehensive context about the professional

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `user_id` | string | Yes | User ID |

#### Returns

```python
{
    "success": True,
    "profile": {
        "user_id": "prof456",
        "has_cv": True,
        "has_quiz": True,
        "cv_count": 3,
        "quiz_count": 2,
        "cv_summary": "Senior Software Engineer CV",
        "quiz_summary": "Career Direction Assessment"
    }
}
```

---

## Function Calling vs Built-in Tools: Detailed Comparison

### When to Use Each Type

**Use Built-in Tools (Google Search):**
✅ Finding online courses and resources  
✅ Researching companies  
✅ Getting salary data by country  
✅ Finding job postings  
✅ Getting career advice from web  
✅ Current news and trends  

**Use Function Calling Tools:**
✅ Accessing user's saved data  
✅ Calculating user's grades  
✅ Analyzing user's CV  
✅ Personalized recommendations  
✅ Tracking user progress  
✅ Database queries  

### Hybrid Usage Example

```
User: "Find Data Science programs I can get into"

Step 1: 🔧 calculate_admission_grade(user_id)
→ Result: 17.85/20

Step 2: 🔧 search_dges_database("Data Science", "Portugal")
→ Result: 15 programs found

Step 3: Filter by user's grade
→ Result: 8 programs user qualifies for

Step 4: 🌐 Google Search top programs for reviews
→ Result: Student reviews, rankings

Step 5: 🤖 Gemini combines everything
→ "You qualify for 8 programs. Top 3 based on reviews..."
```

---

## Error Handling & Retry Logic

### Retry Pattern

All function calling tools implement 3-attempt retry:

```python
def function_implementation(params, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = perform_operation()
            return {"success": True, "data": result}
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(0.5)
                continue
            return {"success": False, "error": str(e)}
```

### Why Retry?

1. **Database locks** - SQLite temporary locks
2. **Race conditions** - Multiple simultaneous requests
3. **Transient errors** - Network/session issues
4. **Resilience** - No user intervention needed

### Error Format

```python
{
    "success": False,
    "error": "Descriptive error message"
}
```

---

## Langfuse Monitoring

### What It Tracks

- ⏱️ Function execution times
- ✅ Success/failure rates
- 📊 Input/output data
- 🐛 Error messages
- 📈 Usage patterns

### Benefits

1. **Performance** - Identify slow functions
2. **Reliability** - Track failure patterns
3. **Analytics** - Understand feature usage
4. **Debugging** - Replay failed calls
5. **Costs** - Monitor API usage

---

## Integration with Gemini

### Basic Flow

```python
# 1. Create chat with tools
chat = client.chats.create(
    model="gemini-2.0-flash-exp",
    config={"tools": [STUDENT_TOOLS]}
)

# 2. Send message
response = chat.send_message("What's my admission average?")

# 3. Handle function call
if has_function_call(response):
    result = execute_function_call(func_name, func_args)
    response = chat.send_message(function_response(result))

# 4. Get final answer
answer = response.text
```

---

## Function Dispatchers

### Student Tools

```python
FUNCTION_HANDLERS = {
    "search_saved_universities": search_saved_universities,
    "calculate_admission_grade": calculate_admission_grade,
    "search_dges_database": search_dges_database,
    "get_student_profile": get_student_profile
}
```

### Professional Tools

```python
FUNCTION_HANDLERS = {
    "get_cv_analysis": get_cv_analysis,
    "get_career_quiz_results": get_career_quiz_results,
    "analyze_skill_gaps": analyze_skill_gaps,
    "get_career_roadmap": get_career_roadmap,
    "get_professional_profile": get_professional_profile
}
```

---

*Function Calling Tools Documentation - Updated January 2026*


*Documentation generated for CareerCorner v1.0*  
*Last updated: January 2026*
