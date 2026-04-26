# Catalyst - AI-Powered Skill Assessment & Personalized Learning Plan Agent

## 1. Project Overview

**Project Name:** Catalyst

**Type:** AI Agent / Web Application

**Core Functionality:** An agent that takes a Job Description and a candidate's resume, conversationally assesses real proficiency on each required skill, identifies gaps, and generates a personalized learning plan focused on adjacent skills the candidate can realistically acquire — with curated resources and time estimates.

**Target Users:** 
- Job seekers looking to understand their skill gaps for specific roles
- Recruiters assessing candidate fit
- Career coaches providing personalized development plans

---

## 2. Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                 │
│  (Streamlit Web App - streamlit_app.py)                        │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐     │
│  │ Job Desc   │  │ Resume      │  │ Assessment Results │     │
│  │ Input      │  │ Input       │  │ + Learning Plan    │     │
│  └─────────────┘  └──────────────┘  └─────────────────────┘     │
└────────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND                                  │
│  (agent_engine.py - Core Logic)                                │
│  ┌────────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │ Skill Parser  │  │ Assessor    │  │ Learning Plan   │    │
│  │ (LLM-based)   │  │ (Convo)    │  │ Generator       │    │
│  └────────────────┘  └──────────────┘  └──────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     LLM INTEGRATION                             │
│  (OpenAI GPT-4 / Anthropic Claude)                             │
│  - Skill Extraction from JD                                    │
│  - Conversational Assessment Questions                         │
│  - Proficiency Scoring                                         │
│  - Learning Plan Generation                                    │
└───────────────────────────────────────────────────────────���─────┘
```

### Key Modules

#### 1. `skill_parser.py`
- Extracts required skills from job descriptions
- Categorizes skills: Technical, Soft, Domain, Tools
- Identifies proficiency levels (Entry, Mid, Senior, Expert)

#### 2. `assessor.py`
- Generates conversational assessment questions
- Analyzes resume for skill evidence
- Scores proficiency (0-100 scale)
- Provides reasoning for scores

#### 3. `gap_analyzer.py`
- Compares required vs. demonstrated skills
- Identifies critical gaps vs. nice-to-have gaps
- Ranks gaps by impact and learnability

#### 4. `learning_plan_generator.py`
- Creates personalized learning paths
- Suggests adjacent skills (realistically acquire-able)
- Curates resources (courses, projects, certifications)
- Estimates time to proficiency

---

## 3. Assessment Scoring Logic

### Proficiency Scale (0-100)
| Score Range | Level | Description |
|------------|-------|-------------|
| 0-20 | Novice | No evidence of skill |
| 21-40 | Beginner | Limited awareness, basic concepts |
| 41-60 | Intermediate | Can perform with guidance |
| 61-80 | Advanced | Can perform independently |
| 81-100 | Expert | Can teach/mentor others |

### Scoring Factors
1. **Resume Evidence (40%)** - Keywords, projects, certifications listed
2. **Depth of Experience (30%)** - Years, complexity of work
3. **Proof of Application (30%)** - Quantifiable outcomes, leadership

### Learnability Index
- Adjacent skills score higher (related to existing skills)
- Time to learn scales with gap size and complexity
- Resources availability factor

---

## 4. User Interface

### Input Panel
- Job Description (text area or file upload)
- Resume (text area or file upload - PDF/DOCX support via PyPDF2)
- Target Role (optional - for context)

### Output Panel
- **Skills Assessment Card**
  - Each skill with score (0-100)
  - Color-coded: Red (0-40), Yellow (41-60), Green (61-100)
  - Evidence supporting score

- **Gap Analysis**
  - Critical gaps (must-have skills)
  - Secondary gaps (nice-to-have)
  - Adjacent opportunities

- **Learning Plan**
  - Prioritized skill list
  - Weekly milestones
  - Resources with links
  - Time estimates (hours/days)
  - Project suggestions

---

## 5. Sample Inputs & Outputs

### Sample Job Description
```
Software Engineer - Machine Learning
Requirements:
- 3+ years Python development
- Experience with ML frameworks (TensorFlow, PyTorch)
- Strong SQL and database design
- Cloud platforms (AWS/GCP)
- Experience with APIs and microservices
- Strong problem-solving skills
- Communication skills
```

### Sample Resume
```
Senior Software Developer
- 5 years Python, Django, Flask
- Built REST APIs for e-commerce platform
- SQL/MySQL experience
- AWS certified
- Led team of 4 developers
- Computer Science degree
```

### Expected Assessment Output
```
SKILL ASSESSMENT:
├── Python: 85/100 (Advanced) ✓
│   Evidence: 5 years professional experience, multiple projects
├── ML Frameworks: 25/100 (Beginner) ✗
│   Gap: No direct ML experience
├── Database Design: 75/100 (Advanced) ✓
│   Evidence: SQL, MySQL, API design
├── Cloud Platforms: 70/100 (Advanced) ✓
│   Evidence: AWS Certified
├── APIs/Microservices: 80/100 (Advanced) ✓
│   Evidence: Built REST APIs for production
├── Problem-Solving: 75/100 (Advanced) ✓
│   Evidence: Technical lead role
└── Communication: 70/100 (Advanced) ✓
    Evidence: Led team, cross-functional work

LEARNING PLAN:
Priority 1: Machine Learning Foundations (Week 1-4)
- [Andrew Ng's ML Course] - 40 hours
- PyTorch Tutorial Projects - 20 hours
- Estimated to Intermediate: 60 hours

Priority 2: ML in Production (Week 5-8)
- ML Deployment Course - 15 hours
- Build Image Classifier Project - 20 hours
```