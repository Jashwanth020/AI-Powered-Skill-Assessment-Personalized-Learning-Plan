"""
Assessor - Conversational skill assessment using LLM
"""

import json
from typing import List, Dict, Any

class Assessor:
    """Assesses candidate proficiency on each required skill"""
    
    def __init__(self, client, model: str = "llama-3.3-70b-versatile"):
        self.client = client
        self.model = model
    
    def assess_skills(self, resume: str, job_description: str, extracted_skills: List[Dict]) -> List[Dict]:
        """Assess proficiency for each extracted skill"""
        prompt = self._build_assessment_prompt(resume, job_description, extracted_skills)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert technical recruiter. Assess candidate proficiency from resume evidence."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result.get("assessments", [])
    
    def _build_assessment_prompt(self, resume: str, job_description: str, skills: List[Dict]) -> str:
        skills_text = json.dumps(skills, indent=2)
        
        return f"""Analyze the resume against the required skills for this job.

Job Description:
{job_description}

Candidate Resume:
{resume}

Required Skills (from job description):
{skills_text}

For each skill, assess the candidate's proficiency (0-100) based on resume evidence.
Return JSON with this structure:

{{
    "assessments": [
        {{
            "skill": "skill name",
            "score": 0-100,
            "level": "Novice|Beginner|Intermediate|Advanced|Expert",
            "evidence": "specific resume evidence supporting score",
            "reasoning": "1-2 sentences explaining the score"
        }}
    ]
}}

Scoring Guide:
- 0-20 Novice: No evidence of skill
- 21-40 Beginner: Limited awareness, basic concepts
- 41-60 Intermediate: Can perform with guidance  
- 61-80 Advanced: Can perform independently
- 81-100 Expert: Can teach/mentor others

Be objective and base scores strictly on resume evidence."""