# Personalized Tutor Skill

import asyncio
from typing import List
from pydantic import BaseModel


class TutorRequest(BaseModel):
    question: str
    context: str = None
    student_level: str = "intermediate"  # beginner, intermediate, advanced


class TutorResponse(BaseModel):
    explanation: str
    examples: List[str]
    followup_questions: List[str]


class PersonalizedTutor:
    """
    Skill to provide personalized tutoring and explanations
    """
    
    def __init__(self):
        pass
        
    async def provide_explanation(self, question: str, context: str = None, student_level: str = "intermediate") -> TutorResponse:
        """
        Provides tailored explanations based on the student's level
        """
        # In a real implementation, we would use AI to provide personalized explanations
        # For now, returning placeholder data
        explanation = f"Explanation for the question: {question}. This is tailored for a {student_level} level student."
        examples = [
            "Example related to the concept",
            "Practical application"
        ]
        followup_questions = [
            "Would you like a more technical explanation?",
            "Can you provide an example of what you're struggling with?"
        ]
        
        return TutorResponse(
            explanation=explanation,
            examples=examples,
            followup_questions=followup_questions
        )