import os
import logging
import json
import requests
from dotenv import load_dotenv
from app.models.subjects import SubjectRequest, CurriculumRequest, StudentKnowledgeRequest

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
DEFAULT_MODEL = "meta-llama/Llama-3-70b-chat-hf"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MOCK_MODE = not TOGETHER_API_KEY or TOGETHER_API_KEY == "your_api_key_here"

def call_together_api(prompt, max_tokens=1500):
    """
    Call Together API directly for subject-specific content generation
    """
    if MOCK_MODE:
        return None
        
    try:
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": DEFAULT_MODEL,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 50
        }
        
        response = requests.post(
            "https://api.together.xyz/v1/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("text", "")
        else:
            logger.error(f"Together API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error calling Together API: {e}")
        return None

async def generate_subject_resources(request: SubjectRequest) -> str:
    """
    Generate resources for a specific subject and level.
    """
    topic_text = f" on {request.topic}" if request.topic else ""
    
    prompt = f"""
    Generate a comprehensive list of educational resources for {request.level.value} level {request.subject_type.value}{topic_text}.
    
    Include the following types of resources:
    1. Textbooks and books
    2. Online courses and tutorials
    3. Interactive tools and simulations
    4. Video lectures and demonstrations
    5. Practice problems and exercises
    6. Communities and forums
    
    For each resource, provide:
    - Name/title
    - Brief description (1-2 sentences)
    - URL or where to find it (if applicable)
    - Why it's valuable for learning this subject
    
    Format the resources in a clear, structured way that's easy to navigate.
    """
    
    if MOCK_MODE:
        logger.info(f"Generating mock resources for {request.subject_type.value} at {request.level.value} level")
        return f"""

1. **Introduction to {request.subject_type.value}** - A comprehensive introduction to {request.subject_type.value} concepts for {request.level.value} students.
2. **{request.subject_type.value} Made Simple** - An accessible guide with clear explanations and examples.

1. **Coursera: {request.subject_type.value} Fundamentals** - A structured online course covering key concepts.
2. **Khan Academy: {request.subject_type.value}** - Free video tutorials and practice problems.

1. **{request.subject_type.value} Lab** - Interactive simulations to visualize concepts.
2. **Practice Platform** - Hands-on exercises with immediate feedback.

1. **YouTube: {request.subject_type.value} Explained** - Clear, concise video explanations of key topics.
2. **MIT OpenCourseWare** - University-level lectures available for free.

1. **{request.subject_type.value} Workbook** - Graduated exercises from basic to advanced.
2. **Problem Solving in {request.subject_type.value}** - Challenging problems with detailed solutions.

1. **Reddit r/{request.subject_type.value}** - Active community for questions and discussions.
2. **Stack Exchange** - Q&A platform for specific problems and concepts.
"""
    
    result = call_together_api(prompt, max_tokens=1500)
    
    if result:
        return result
    else:
        logger.error("Failed to generate subject resources")
        raise Exception("Failed to generate subject resources")

async def generate_curriculum(request: CurriculumRequest) -> str:
    """
    Generate a curriculum for a specific subject and level.
    """
    prompt = f"""
    Create a {request.duration_weeks}-week curriculum for teaching {request.level.value} level {request.subject_type.value}.
    
    Structure the curriculum with:
    1. Weekly topics and learning objectives
    2. Key concepts to cover each week
    3. Suggested activities and exercises
    4. Recommended resources
    {("5. Assessment methods and checkpoints" if request.include_assessments else "")}
    {("6. Additional resources and materials" if request.include_resources else "")}
    
    The curriculum should progress logically, building on previous knowledge, and be appropriate for {request.level.value} students.
    Format the curriculum in a clear, structured way that would be useful for educators.
    """
    
    if MOCK_MODE:
        logger.info(f"Generating mock curriculum for {request.subject_type.value} at {request.level.value} level")
        return f"""

**Learning Objectives:**
- Understand basic principles of {request.subject_type.value}
- Become familiar with key terminology

**Key Concepts:**
- Fundamental principles
- Historical context

**Activities:**
- Introductory exercises
- Group discussion on applications

**Learning Objectives:**
- Master foundational techniques
- Apply basic principles to simple problems

**Key Concepts:**
- Building blocks of {request.subject_type.value}
- Practical applications

**Activities:**
- Hands-on practice
- Problem-solving exercises


{("## Assessments:\n- Weekly quizzes\n- Mid-term project\n- Final examination" if request.include_assessments else "")}

{("## Additional Resources:\n- Supplementary readings\n- Online tools and simulators\n- Video tutorials" if request.include_resources else "")}
"""
    
    result = call_together_api(prompt, max_tokens=2000)
    
    if result:
        return result
    else:
        logger.error("Failed to generate curriculum")
        raise Exception("Failed to generate curriculum")

async def generate_personalized_path(request: StudentKnowledgeRequest) -> str:
    """
    Generate a personalized learning path based on student's prior knowledge.
    """
    known_topics = ", ".join(request.topics_known)
    learning_objectives = ", ".join(request.learning_objectives)
    learning_style = f"The student prefers {request.preferred_learning_style} learning." if request.preferred_learning_style else ""
    
    prompt = f"""
    Create a personalized learning path for a student studying {request.subject_type.value}.
    
    The student already knows: {known_topics}
    
    The student wants to learn: {learning_objectives}
    
    {learning_style}
    
    Provide a structured learning path that:
    1. Builds on the student's existing knowledge
    2. Addresses gaps in prerequisite knowledge
    3. Progresses toward the learning objectives
    4. Includes recommended resources for each step
    5. Suggests appropriate practice exercises
    6. Includes checkpoints to assess understanding
    
    Format the learning path in a clear, step-by-step structure that the student can follow independently.
    """
    
    if MOCK_MODE:
        logger.info(f"Generating mock personalized learning path for {request.subject_type.value}")
        return f"""

Since you already know {request.topics_known[0] if request.topics_known else "some basics"}, but need to learn {request.learning_objectives[0] if request.learning_objectives else "advanced concepts"}, we'll start by addressing any prerequisite knowledge.

**Resources:**
- Targeted tutorials on prerequisite concepts
- Quick review exercises

**Focus Areas:**
- Core concepts related to your learning objectives
- Fundamental principles

**Resources:**
- Interactive tutorials
- Structured practice problems

**Activities:**
- Hands-on projects
- Real-world applications

**Resources:**
- Project guides
- Case studies

**Focus Areas:**
- Specialized topics from your learning objectives
- Advanced techniques

**Resources:**
- In-depth tutorials
- Advanced problem sets

- Self-assessment quizzes after each step
- Comprehensive review project
"""
    
    result = call_together_api(prompt, max_tokens=1500)
    
    if result:
        return result
    else:
        logger.error("Failed to generate personalized learning path")
        raise Exception("Failed to generate personalized learning path")
