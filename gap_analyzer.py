"""
Gap Analyzer - Identifies skill gaps between required and demonstrated skills
"""

import json
from typing import List, Dict, Any

class GapAnalyzer:
    """Analyzes gaps between required and demonstrated skills"""
    
    def __init__(self, client, model: str = "llama-3.3-70b-versatile"):
        self.client = client
        self.model = model
    
    def analyze_gaps(self, assessments: List[Dict], extracted_skills: List[Dict]) -> Dict[str, Any]:
        """Identify and categorize skill gaps"""
        prompt = self._build_gap_analysis_prompt(assessments, extracted_skills)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert career analyst. Identify skill gaps and recommend adjacent opportunities."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def _build_gap_analysis_prompt(self, assessments: List[Dict], skills: List[Dict]) -> str:
        return f"""Analyze skill gaps and identify adjacent learning opportunities.

Required Skills (with importance):
{json.dumps(skills, indent=2)}

Candidate Assessments (with scores):
{json.dumps(assessments, indent=2)}

For each gap:
1. Classify as "critical_gap" (must-have skill with score < 50), "secondary_gap" (nice-to-have or score 50-70), or "adjacent_opportunity" (high-score skills to leverage)
2. Calculate "learnability_score" based on:
   - Is it adjacent to existing strong skills?
   - Are there many learning resources available?
   - How large is the gap (lower gap = easier to learn)?
3. Provide specific adjacent skills that could help (e.g., Python -> data science, SQL -> database admin)

Return JSON:
{{
    "critical_gaps": [
        {{
            "skill": "name",
            "current_score": number,
            "target_score": number,
            "gap_size": number,
            "learnability_score": 0-100,
            "reasoning": "why this is learnable"
        }}
    ],
    "secondary_gaps": [...],
    "adjacent_opportunities": [
        {{
            "current_skill": "skill candidate has (score > 70)",
            "adjacent_skill": "related skill to learn",
            "correlation": "how they relate",
            "learning_ease": "high|medium|low"
        }}
    ],
    "summary": "2-3 sentence overall gap analysis"
}}"""
    
    def categorize_gaps(self, assessments: List[Dict], threshold: int = 50) -> Dict[str, List[Dict]]:
        """Simple categorization without LLM for faster results"""
        categorized = {
            "strong_skills": [],
            "moderate_skills": [],
            "critical_gaps": [],
            "learning_opportunities": []
        }
        
        for assessment in assessments:
            score = assessment.get("score", 0)
            skill = assessment.get("skill", "")
            
            if score >= 70:
                categorized["strong_skills"].append(assessment)
            elif score >= 40:
                categorized["moderate_skills"].append(assessment)
            else:
                categorized["critical_gaps"].append(assessment)
                categorized["learning_opportunities"].append({
                    "skill": skill,
                    "gap": 100 - score,
                    "priority": "high" if score < 25 else "medium"
                })
        
        return categorized