"""
Learning Plan Generator - Creates personalized learning plans with resources
"""

import json
from typing import List, Dict, Any

class LearningPlanGenerator:
    """Generates personalized learning plans with curated resources"""
    
    def __init__(self, client, model: str = "llama-3.3-70b-versatile"):
        self.client = client
        self.model = model
    
    def generate_plan(self, gap_analysis: Dict, current_skills: List[Dict]) -> Dict[str, Any]:
        """Generate personalized learning plan"""
        prompt = self._build_plan_prompt(gap_analysis, current_skills)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert career coach. Create actionable learning plans with specific resources."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _build_plan_prompt(self, gap_analysis: Dict, current_skills: List[Dict]) -> str:
        return f"""Create a personalized learning plan based on gap analysis.

Current Strong Skills (score > 60):
{json.dumps([s for s in current_skills if s.get("score", 0) >= 60], indent=2)}

Gap Analysis:
{json.dumps(gap_analysis, indent=2)}

Create a learning plan with:
1. Prioritized skills to learn (focus on high learnability + high impact)
2. Specific resources (free courses, paid courses, projects, certifications)
3. Weekly milestones
4. Time estimates in hours
5. Project suggestions to build portfolio

Return JSON:
{{
    "learning_plan": [
        {{
            "skill": "skill name",
            "priority": 1-5,
            "weeks": "Week X-Y",
            "resources": [
                {{
                    "name": "resource name",
                    "type": "course|project|certification|book|article",
                    "url": "link or 'search for [name]'",
                    "cost": "free|paid",
                    "hours": number
                }}
            ],
            "milestones": ["week 1 milestone", "week 2 milestone"],
            "total_hours": number,
            "target_proficiency": "Intermediate|Advanced",
            "reasoning": "why this skill/path"
        }}
    ],
    "total_learning_hours": number,
    "estimated_completion": "X weeks to Y months",
    "actionable_first_step": "specific first action to take",
    "career_alignment": "how this connects to target role"
}}

Be realistic with time estimates. Include a mix of free and paid resources."""