import os
import logging
import requests
import json
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage

from app.models.lesson_plans import LessonPlanRequest
from app.models.quizzes import QuizRequest
from app.models.content_adaptation import ContentAdaptationRequest
from app.models.interactive_scenarios import InteractiveScenarioRequest
from app.models.feedback import FeedbackRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
LLAMA_STACK_PORT = os.getenv("LLAMA_STACK_PORT", "8321")

if not TOGETHER_API_KEY or TOGETHER_API_KEY == "your_api_key_here":
    logger.warning("TOGETHER_API_KEY environment variable is not set or is using a placeholder value. Using mock responses for testing.")
    MOCK_MODE = True
else:
    try:
        client = LlamaStackClient(base_url=f"http://localhost:{LLAMA_STACK_PORT}")
        logger.info(f"Connected to Llama Stack server on port {LLAMA_STACK_PORT}")
        MOCK_MODE = False
    except Exception as e:
        logger.warning(f"Failed to connect to Llama Stack server: {e}")
        logger.info("Attempting to use Together API directly as fallback")
        try:
            headers = {
                "Authorization": f"Bearer {TOGETHER_API_KEY}"
            }
            response = requests.get("https://api.together.xyz/v1/models", headers=headers)
            if response.status_code == 200:
                logger.info("Successfully connected to Together API")
                MOCK_MODE = False
            else:
                logger.warning(f"Failed to connect to Together API: {response.status_code}")
                MOCK_MODE = True
        except Exception as e:
            logger.warning(f"Error connecting to Together API: {e}")
            MOCK_MODE = True

DEFAULT_MODEL = "deepseek-ai/DeepSeek-V3"

def call_together_api(prompt, max_tokens=1000):
    """
    Call Together API directly as a fallback when Llama Stack client is not available
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

async def generate_lesson_plan(request: LessonPlanRequest) -> str:
    """
    Generate a lesson plan using Llama Stack or Together API.
    """
    prompt = f"""
    Create a detailed lesson plan for {request.grade_level} students on {request.subject}, 
    specifically covering {request.topic}.
    
    Learning objectives:
    {' '.join(['- ' + obj for obj in request.learning_objectives])}
    
    The lesson should be designed for {request.duration_minutes} minutes.
    
    Include the following sections:
    1. Introduction/Hook
    2. Main content/activities
    3. Practice exercises
    4. Assessment
    5. Conclusion
    6. Materials needed
    7. Extensions for advanced students
    8. Accommodations for struggling students
    
    Format the lesson plan in a structured, easy-to-follow format.
    """
    
    if MOCK_MODE:
        logger.info(f"Generating mock lesson plan for {request.subject} - {request.topic}")
        return f"""

Begin with a brief discussion about {request.topic} and its relevance to students' lives.

Present key concepts related to {request.topic} through interactive demonstrations and guided practice.

Students will work in pairs to complete practice problems that reinforce the concepts learned.

Quick formative assessment to gauge understanding of the key concepts.

Summarize the main points and preview the next lesson.

- Textbooks
- Worksheets
- Visual aids

Additional challenging problems that extend the concepts learned.

Simplified practice problems and additional one-on-one support.
"""
    
    try:
        response = client.inference.chat_completion(
            messages=[
                UserMessage(content=prompt, role="user"),
            ],
            model_id=DEFAULT_MODEL,
        )
        return response.completion_message.content
    except Exception as e:
        logger.warning(f"Error using Llama Stack client: {e}")
        
        logger.info("Attempting to use Together API directly for lesson plan generation")
        result = call_together_api(prompt, max_tokens=1500)
        
        if result:
            return result
        else:
            logger.error("Failed to generate lesson plan using both Llama Stack and Together API")
            raise Exception("Failed to generate lesson plan")

async def generate_quiz(request: QuizRequest) -> str:
    """
    Generate a quiz using Llama Stack or Together API.
    """
    prompt = f"""
    Create a {request.num_questions}-question quiz on {request.subject}, 
    specifically covering {request.topic}.
    The difficulty level should be {request.difficulty} (on a 1-5 scale).
    
    Include the following question types: {', '.join([qt.value for qt in request.question_types])}
    
    For each question:
    1. Include the question
    2. Provide answer options (for multiple choice)
    3. Mark the correct answer
    4. Include a brief explanation of why the answer is correct
    
    Format the quiz in a structured way that's easy to parse.
    """
    
    if MOCK_MODE:
        logger.info(f"Generating mock quiz for {request.subject} - {request.topic}")
        return f"""

What is the main concept of {request.topic}?
A) First option
B) Second option
C) Third option
D) Fourth option

**Correct Answer: B**

Explanation: The second option is correct because it accurately describes the fundamental principle of {request.topic}.

Which of the following best demonstrates {request.topic} in action?
A) Example one
B) Example two
C) Example three
D) Example four

**Correct Answer: C**

Explanation: Example three shows a practical application of {request.topic} in a real-world context.
"""
    
    try:
        response = client.inference.chat_completion(
            messages=[
                UserMessage(content=prompt, role="user"),
            ],
            model_id=DEFAULT_MODEL,
        )
        return response.completion_message.content
    except Exception as e:
        logger.warning(f"Error using Llama Stack client: {e}")
        
        logger.info("Attempting to use Together API directly for quiz generation")
        result = call_together_api(prompt, max_tokens=1500)
        
        if result:
            return result
        else:
            logger.error("Failed to generate quiz using both Llama Stack and Together API")
            raise Exception("Failed to generate quiz")

async def adapt_content(request: ContentAdaptationRequest) -> str:
    """
    Adapt educational content using Llama Stack or Together API.
    """
    learning_style_prompt = ""
    if request.target_learning_style:
        learning_style_prompt = f"Adapt the content for {request.target_learning_style.value} learners."
    
    simplify_prompt = ""
    if request.simplify:
        simplify_prompt = "Simplify the content while preserving the key information."
    
    prompt = f"""
    Adapt the following educational content for {request.target_reading_level.value} reading level.
    {learning_style_prompt}
    {simplify_prompt}
    
    Original content:
    {request.content}
    
    Provide the adapted content in a clear, well-structured format.
    """
    
    if MOCK_MODE:
        logger.info(f"Generating mock adapted content for {request.target_reading_level.value} reading level")
        learning_style_text = f" for {request.target_learning_style.value} learners" if request.target_learning_style else ""
        simplify_text = ", simplified" if request.simplify else ""
        
        return f"""

{request.content[:50]}... [content adapted for {request.target_reading_level.value} reading level{learning_style_text}{simplify_text}]

The content has been modified to use vocabulary and sentence structures appropriate for {request.target_reading_level.value} students.
"""
    
    try:
        response = client.inference.chat_completion(
            messages=[
                UserMessage(content=prompt, role="user"),
            ],
            model_id=DEFAULT_MODEL,
        )
        return response.completion_message.content
    except Exception as e:
        logger.warning(f"Error using Llama Stack client: {e}")
        
        logger.info("Attempting to use Together API directly for content adaptation")
        result = call_together_api(prompt, max_tokens=1500)
        
        if result:
            return result
        else:
            logger.error("Failed to adapt content using both Llama Stack and Together API")
            raise Exception("Failed to adapt content")

async def generate_interactive_scenario(request: InteractiveScenarioRequest) -> str:
    """
    Generate an interactive learning scenario using Llama Stack or Together API.
    """
    scenario_type_desc = {
        "role_playing": "a role-playing activity where students take on specific roles",
        "problem_solving": "a problem-solving exercise that challenges students to find solutions",
        "simulation": "a simulation that models real-world processes or phenomena",
        "case_study": "a case study that examines a specific situation or example"
    }
    
    scenario_type_description = scenario_type_desc.get(request.scenario_type.value, "an interactive learning activity")
    
    prompt = f"""
    Create {scenario_type_description} for {request.grade_level} students on {request.subject}, 
    specifically covering {request.topic}.
    
    Learning objectives:
    {' '.join(['- ' + obj for obj in request.learning_objectives])}
    
    The scenario should be designed for {request.duration_minutes} minutes and have a complexity level of {request.complexity} (on a 1-5 scale).
    
    {("Include a list of required materials." if request.include_materials else "")}
    {("Include detailed instructions for teachers." if request.include_instructions else "")}
    
    Format the scenario in a structured, easy-to-follow format with clear sections for:
    1. Overview
    2. Setup instructions
    3. Student instructions/prompts
    4. Discussion questions
    5. Assessment criteria
    6. Extensions or variations
    """
    
    if MOCK_MODE:
        logger.info(f"Generating mock interactive scenario for {request.subject} - {request.topic}")
        return f"""

This {request.scenario_type.value} activity engages students with {request.topic} through an interactive approach.

Arrange the classroom to facilitate group work. Prepare materials in advance.

Students will explore {request.topic} by working in small groups to solve problems related to the concept.

- How does {request.topic} relate to real-world situations?
- What challenges did you encounter while working with {request.topic}?

Students will be evaluated on their understanding of {request.topic} and their ability to apply the concepts.

For advanced students, increase the complexity by adding additional constraints or challenges.
"""
    
    try:
        response = client.inference.chat_completion(
            messages=[
                UserMessage(content=prompt, role="user"),
            ],
            model_id=DEFAULT_MODEL,
        )
        return response.completion_message.content
    except Exception as e:
        logger.warning(f"Error using Llama Stack client: {e}")
        
        logger.info("Attempting to use Together API directly for interactive scenario generation")
        result = call_together_api(prompt, max_tokens=1500)
        
        if result:
            return result
        else:
            logger.error("Failed to generate interactive scenario using both Llama Stack and Together API")
            raise Exception("Failed to generate interactive scenario")

async def generate_feedback(request: FeedbackRequest) -> str:
    """
    Generate feedback for student work using Llama Stack or Together API.
    """
    tone_instructions = {
        "encouraging": "Be positive and encouraging, focusing on strengths while gently addressing areas for improvement.",
        "constructive": "Provide balanced feedback that addresses both strengths and areas for improvement in a helpful way.",
        "detailed": "Provide comprehensive, detailed feedback covering all aspects of the work.",
        "brief": "Provide concise, to-the-point feedback highlighting only the most important points."
    }
    
    tone_instruction = tone_instructions.get(request.feedback_tone.value, "Provide balanced feedback.")
    
    sections = []
    if request.include_strengths:
        sections.append("1. Strengths: Highlight what the student did well.")
    if request.include_areas_for_improvement:
        sections.append("2. Areas for Improvement: Identify specific aspects that could be improved.")
    if request.include_next_steps:
        sections.append("3. Next Steps: Suggest concrete actions the student can take to improve.")
    
    sections_text = "\n".join(sections)
    
    prompt = f"""
    Provide feedback on the following {request.feedback_type.value} for a {request.grade_level} student in {request.subject}.
    
    Assignment Description:
    {request.assignment_description}
    
    Student Work:
    {request.student_work}
    
    {tone_instruction}
    
    Include the following sections in your feedback:
    {sections_text}
    
    Format the feedback in a clear, structured way that will be helpful and motivating for the student.
    """
    
    if MOCK_MODE:
        logger.info(f"Generating mock feedback for {request.feedback_type.value} in {request.subject}")
        
        feedback_sections = []
        if request.include_strengths:
            feedback_sections.append(f"""
You demonstrated a good understanding of the core concepts related to {request.subject}. Your work shows creativity and effort.
""")
        
        if request.include_areas_for_improvement:
            feedback_sections.append(f"""
Consider providing more detailed explanations and examples to support your points about {request.subject}.
""")
        
        if request.include_next_steps:
            feedback_sections.append(f"""
Review the key concepts of {request.subject} and practice applying them in different contexts. Consider seeking additional resources on this topic.
""")
        
        return "".join(feedback_sections)
    
    try:
        response = client.inference.chat_completion(
            messages=[
                UserMessage(content=prompt, role="user"),
            ],
            model_id=DEFAULT_MODEL,
        )
        return response.completion_message.content
    except Exception as e:
        logger.warning(f"Error using Llama Stack client: {e}")
        
        logger.info("Attempting to use Together API directly for feedback generation")
        result = call_together_api(prompt, max_tokens=1500)
        
        if result:
            return result
        else:
            logger.error("Failed to generate feedback using both Llama Stack and Together API")
            raise Exception("Failed to generate feedback")
