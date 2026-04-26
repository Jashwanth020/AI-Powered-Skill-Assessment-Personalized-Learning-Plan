# Catalyst - AI-Powered Skill Assessment & Personalized Learning Plan Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.30+-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-green" alt="OpenAI">
</p>

<p align="center">
  An AI agent that takes a Job Description and a candidate's resume, assesses real proficiency on each required skill, identifies gaps, and generates a personalized learning plan with curated resources and time estimates.
</p>

---

## Features

- **Skill Extraction**: Automatically extracts required skills from job descriptions using LLM
- **Proficiency Assessment**: Scores candidate proficiency (0-100) based on resume evidence
- **Gap Analysis**: Identifies critical gaps and adjacent learning opportunities
- **Learning Plan**: Generates personalized learning paths with resources and time estimates
- **Interactive UI**: Streamlit web interface for easy interaction

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                 │
│                    (streamlit_app.py)                          │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────────────────┐  │
│  │ Job Desc    │  │ Resume     │  │ Assessment Results     │  │
│  │ Input       │  │ Input      │  │ + Learning Plan        │  │
│  └──────────────┘  └─────────────┘  └────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND                                  │
│                    (agent_engine.py)                           │
│  ┌─────────────┐  ┌───────────┐  ┌─────────────────────────┐   │
│  │ Skill      │  │ Assessor │  │ Learning Plan           │   │
│  │ Parser     │  │          │  │ Generator               │   │
│  └─────────────┘  └───────────┘  └─────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LLM INTEGRATION                              │
│                    (OpenAI GPT-4o)                             │
│  - Skill Extraction from JD                                     │
│  - Proficiency Scoring                                         │
│  - Gap Analysis                                                 │
│  - Learning Plan Generation                                    │
└─────────────────────────────────────────────────────────────────┘
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
- OpenAI API Key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/catalyst.git
cd catalyst
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set environment variable:**
```bash
# Linux/Mac
export OPENAI_API_KEY=sk-your-api-key

# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-your-api-key"

# Windows (Command Prompt)
set OPENAI_API_KEY=sk-your-api-key
```

### Running the App

**Option 1: Streamlit Web App**
```bash
streamlit run streamlit_app.py
```

**Option 2: Python Script (CLI)**
```bash
python agent_engine.py
```

---

## Usage

1. **Open the app** at `http://localhost:8501`

2. **Enter your OpenAI API key** in the sidebar

3. **Paste Job Description** in the text area

4. **Paste Resume** in the text area

5. **Click "Analyze Skills"**

6. **View Results:**
   - Skill Assessment (scores with color coding)
   - Gap Analysis (critical gaps, adjacent opportunities)
   - Learning Plan (prioritized skills, resources, time estimates)

---

## Sample Run

```python
from agent_engine import CatalystAgent
import os

agent = CatalystAgent(os.environ["OPENAI_API_KEY"])

job_description = """
Software Engineer - Machine Learning
Requirements:
- 3+ years Python development
- ML frameworks (TensorFlow, PyTorch)
- SQL and database design
- Cloud platforms (AWS/GCP)
"""

resume = """
Senior Software Developer
- 5 years Python (Django, Flask)
- Built REST APIs for e-commerce
- AWS certified
- Led team of 4
"""

result = agent.assess(job_description, resume)
# Returns: assessments, gap_analysis, learning_plan
```

---

## Project Structure

```
catalyst/
├── agent_engine.py          # Main orchestration
├── skill_parser.py          # Extracts skills from JD
├── assessor.py              # Assesses proficiency
├── gap_analyzer.py         # Identifies gaps
├── learning_plan_generator.py  # Creates learning plan
├── streamlit_app.py         # Web UI
├── requirements.txt       # Dependencies
├── sample_data.json       # Sample inputs/outputs
├── SPEC.md               # Detailed specification
└── README.md             # This file
```

---

## API Keys

Get your OpenAI API key from: https://platform.openai.com/api-keys

> **Note:** The app uses GPT-4o which requires API billing setup. Token usage is approximately:
> - Skill Extraction: ~500 tokens
> - Assessment: ~1000 tokens
> - Gap Analysis: ~500 tokens
> - Learning Plan: ~1000 tokens
> - **Total: ~3000 tokens per analysis**

---

## License

MIT License - See LICENSE file for details.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request