"""
Catalyst Agent Engine - Orchestrates skill assessment pipeline
"""

import json
import os
from typing import Dict, Any, Optional
from groq import Groq
from skill_parser import SkillParser
from assessor import Assessor
from gap_analyzer import GapAnalyzer
from learning_plan_generator import LearningPlanGenerator

class CatalystAgent:
    """Main agent that orchestrates the skill assessment and learning plan pipeline"""
    
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.skill_parser = SkillParser(self.client, model)
        self.assessor = Assessor(self.client, model)
        self.gap_analyzer = GapAnalyzer(self.client, model)
        self.plan_generator = LearningPlanGenerator(self.client, model)
    
    def assess(self, job_description: str, resume: str, target_role: Optional[str] = None) -> Dict[str, Any]:
        """Run full assessment pipeline"""
        
        extracted_skills = self.skill_parser.parse(job_description)
        
        assessments = self.assessor.assess_skills(resume, job_description, extracted_skills.get("skills", []))
        
        gap_analysis = self.gap_analyzer.analyze_gaps(assessments, extracted_skills.get("skills", []))
        
        learning_plan = self.plan_generator.generate_plan(gap_analysis, assessments)
        
        return {
            "role_summary": extracted_skills.get("role_summary", ""),
            "extracted_skills": extracted_skills.get("skills", []),
            "assessments": assessments,
            "gap_analysis": gap_analysis,
            "learning_plan": learning_plan.get("learning_plan", []),
            "summary": {
                "total_skills_required": len(extracted_skills.get("skills", [])),
                "skills_strong": len([a for a in assessments if a.get("score", 0) >= 60]),
                "skills_gapped": len([a for a in assessments if a.get("score", 0) < 60]),
                "total_learning_hours": learning_plan.get("total_learning_hours", 0),
                "estimated_completion": learning_plan.get("estimated_completion", "")
            }
        }
    
    def quick_assess(self, job_description: str, resume: str) -> Dict[str, Any]:
        """Fast assessment without full LLM gap analysis"""
        
        extracted_skills = self.skill_parser.parse(job_description)
        assessments = self.assessor.assess_skills(resume, job_description, extracted_skills.get("skills", []))
        
        categorized = self.gap_analyzer.categorize_gaps(assessments)
        
        return {
            "role_summary": extracted_skills.get("role_summary", ""),
            "extracted_skills": extracted_skills.get("skills", []),
            "assessments": assessments,
            "categorized_gaps": categorized,
            "summary": {
                "total_skills_required": len(extracted_skills.get("skills", [])),
                "skills_strong": len(categorized["strong_skills"]),
                "skills_gapped": len(categorized["critical_gaps"])
            }
        }


def run_demo():
    """Run with sample data to demonstrate"""
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        print("Warning: GROQ_API_KEY not set")
        return None
    
    agent = CatalystAgent(api_key)
    
    sample_jd = """
    Software Engineer - Machine Learning
    
    Requirements:
    - 3+ years Python development experience
    - Experience with ML frameworks (TensorFlow, PyTorch)
    - Strong SQL and database design skills
    - Cloud platforms experience (AWS or GCP)
    - Experience with REST APIs and microservices
    - Strong problem-solving skills
    - Excellent communication skills
    - BS/MS in Computer Science or related field
    """
    
    sample_resume = """
    John Smith - Senior Software Developer
    
    Experience:
    - 5 years Python development (Django, Flask, FastAPI)
    - Built REST APIs serving 1M+ requests/day for e-commerce
    - MySQL and PostgreSQL database design and optimization
    - AWS certified Solutions Architect
    - Led team of 4 developers at TechCorp
    - Computer Science degree from State University
    
    Skills: Python, Django, Flask, SQL, MySQL, PostgreSQL, AWS, REST APIs, Git
    """
    
    result = agent.assess(sample_jd, sample_resume)
    
    print("\n" + "="*60)
    print("CATALYST ASSESSMENT RESULTS")
    print("="*60)
    print(f"\nRole: {result['role_summary']}")
    print(f"\nSkills Required: {result['summary']['total_skills_required']}")
    print(f"Skills Strong: {result['summary']['skills_strong']}")
    print(f"Skills Gapped: {result['summary']['skills_gapped']}")
    
    print("\n--- Skill Assessments ---")
    for assessment in result["assessments"]:
        score = assessment.get("score", 0)
        level = assessment.get("level", "")
        status = "[OK]" if score >= 60 else "[GAP]"
        print(f"  {assessment['skill']}: {score}/100 ({level}) {status}")
        print(f"    Evidence: {assessment['evidence']}")
    
    print("\n--- Learning Plan ---")
    for item in result["learning_plan"][:3]:
        print(f"  Priority {item.get('priority', 'N/A')}: {item.get('skill', 'N/A')}")
        print(f"    Timeline: {item.get('weeks', 'N/A')} ({item.get('total_hours', 0)} hours)")
        first_step = item.get('actionable_first_step') or item.get('milestones', ['N/A'])[0] if item else 'N/A'
        print(f"    First step: {first_step}")
    
    return result


if __name__ == "__main__":
    run_demo()