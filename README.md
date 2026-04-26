# Catalyst - AI-Powered Skill Assessment & Personalized Learning Plan Agent


<p align="center">
  An AI agent that takes a Job Description and a candidate's resume, assesses real proficiency on each required skill, identifies gaps, and generates a personalized learning plan with curated resources and time estimates.
</p>

---

## Features

- **Skill Extraction**: Automatically extracts required skills from job descriptions using LLM
- **Proficiency Assessment**: Scores candidate proficiency (0-100) based on resume evidence
- **Gap Analysis**: Identifies critical gaps and adjacent learning opportunities
- **Learning Plan**: Generates personalized learning paths with resources and time estimates
- **File Upload**: Supports PDF and TXT files for Job Description and Resume
- **Interactive UI**: Streamlit web interface with file upload support

---

## Architecture

```
+------------------------------------------------------------------+
|                         FRONTEND                                 |
|                     (streamlit_app.py)                           |
|  +-------------+  +-------------+  +---------------------------+   |
|  | Job Desc   |  | Resume     |  | Assessment Results       |   |
|  | (File/    |  | (File/    |  | + Learning Plan           |   |
|  |  Text)    |  |  Text)    |  |                           |   |
|  +-------------+  +-------------+  +---------------------------+   |
+---------------------------+---------------------------------------+
                            |
                            v
+------------------------------------------------------------------+
|                         BACKEND                                  |
|                     (agent_engine.py)                           |
|  +------------+  +-----------+  +----------------------------+   |
|  | Skill    |  | Assessor |  | Learning Plan            |   |
|  | Parser   |  |          |  | Generator                |   |
|  +------------+  +-----------+  +----------------------------+   |
+---------------------------+---------------------------------------+
                            |
                            v
+------------------------------------------------------------------+
|                      LLM INTEGRATION                            |
|                  (Groq API - Llama 3.3 70B)                       |
|  - Skill Extraction from JD                                     |
|  - Proficiency Scoring                                         |
|  - Gap Analysis                                                 |
|  - Learning Plan Generation                                    |
+------------------------------------------------------------------+
```

### Scoring Logic

| Score Range | Level | Description |
|-------------|-------|--------------|
| 0-20 | Novice | No evidence of skill |
| 21-40 | Beginner | Limited awareness |
| 41-60 | Intermediate | Can perform with guidance |
| 61-80 | Advanced | Can perform independently |
| 81-100 | Expert | Can teach/mentor others |

**Scoring Factors:**
- Resume Evidence (40%): Keywords, projects, certifications
- Depth of Experience (30%): Years, complexity
- Proof of Application (30%): Quantifiable outcomes, leadership

---

## Setup

### Prerequisites

- Python 3.10+
- Groq API Key (free at https://console.groq.com)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Jashwanth020/AI-Powered-Skill-Assessment-Personalized-Learning-Plan.git
cd AI-Powered-Skill-Assessment-Personalized-Learning-Plan
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set Groq API key:**
```bash
# Linux/Mac
export GROQ_API_KEY=your-groq-api-key

# Windows (PowerShell)
$env:GROQ_API_KEY="your-groq-api-key"

# Windows (Command Prompt)
set GROQ_API_KEY=your-groq-api-key
```

Get your free Groq API key at: https://console.groq.com

### Running the App

**Streamlit Web App:**
```bash
streamlit run streamlit_app.py
```

**Python Script (CLI):**
```bash
python agent_engine.py
```

---

## Usage

1. **Open the app** at `http://localhost:8501`

2. **Enter your Groq API key** in the sidebar

3. **Upload Job Description** (PDF/TXT) or paste text

4. **Upload Resume** (PDF/TXT) or paste text

5. **Click "Analyze Skills"**

6. **View Results:**
   - Skill Assessment (scores with color coding)
   - Gap Analysis (critical gaps, adjacent opportunities)
   - Learning Plan (prioritized skills, resources, time estimates)

---

## Sample Output

```
SKILL ASSESSMENT:
+ Python: 90/100 (Expert) [OK]
+ Machine Learning: 0/100 (Novice) [GAP]
+ SQL: 80/100 (Advanced) [OK]
+ AWS: 90/100 (Expert) [OK]
+ REST APIs: 90/100 (Expert) [OK]

LEARNING PLAN:
Priority 1: Machine Learning
  Timeline: Week 1-8 (75 hours)
  Resources: Andrew Ng's ML Course, PyTorch Tutorials
  First step: Complete ML Crash Course (Week 1-2)
```

---

## Project Structure

```
catalyst/
+ agent_engine.py              # Main orchestration
+ skill_parser.py             # Extracts skills from JD
+ assessor.py                 # Assesses proficiency
+ gap_analyzer.py             # Identifies gaps
+ learning_plan_generator.py # Creates learning plan
+ streamlit_app.py           # Web UI with file upload
+ requirements.txt          # Dependencies (groq, streamlit, PyPDF2)
+ README.md                  # Setup instructions
+ SPEC.md                   # Full specification
+ sample_data.json          # Sample inputs/outputs
```

---

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM**: Groq API (Llama 3.3 70B)
- **File Processing**: PyPDF2

---

