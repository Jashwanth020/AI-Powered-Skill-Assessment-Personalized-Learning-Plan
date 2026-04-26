"""
Skill Parser - Extracts required skills from job descriptions using LLM
"""

from typing import List, Dict, Any, Optional

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class SkillParser:
    """Parses job descriptions to extract required skills with proficiency levels"""
    
    CATEGORIES = ["Technical", "Soft", "Domain", "Tools"]
    LEVELS = ["Entry", "Mid", "Senior", "Expert"]
    
    def __init__(self, client, model: str = "llama-3.3-70b-versatile"):
        self.client = client
        self.model = model
    
    def parse(self, job_description: str) -> Dict[str, Any]:
        """Extract skills from job description"""
        prompt = self._build_extraction_prompt(job_description)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert HR analyst. Extract skills from job descriptions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    
    def _build_extraction_prompt(self, job_description: str) -> str:
        return f"""Analyze this job description and extract all required skills.

Job Description:
{job_description}

Return a JSON object with this structure:
{{
    "skills": [
        {{
            "name": "skill name",
            "category": "Technical|Soft|Domain|Tools",
            "proficiency_level": "Entry|Mid|Senior|Expert",
            "importance": "must-have|nice-to-have",
            "years_experience": number or null
        }}
    ],
    "role_summary": "2-3 sentence summary of the role",
    "key_responsibilities": ["list of main responsibilities"]
}}

Be thorough - extract all hard skills, soft skills, tools, certifications mentioned."""