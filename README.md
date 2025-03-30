# Educational Content Generator

An AI-powered educational content generator using Llama Stack and Together API to create personalized learning materials based on specific learning objectives, student needs, and curriculum requirements.

## Features

### Core Features
1. **Lesson Plan Generator** - Create structured lesson plans based on curriculum standards and learning objectives
2. **Quiz Generator** - Generate questions at varying difficulty levels with answer keys
3. **Content Adaptation** - Rewrite educational materials for different reading levels or learning styles
4. **Interactive Learning Scenarios** - Create role-playing scenarios or problem-solving exercises
5. **Feedback Generator** - Develop constructive feedback for student assignments

### Subject-Specific Tools
1. **Subject Resources** - Generate comprehensive educational resources for specific subjects
2. **Curriculum Generator** - Create structured curriculum plans for any subject
3. **Personalized Learning Paths** - Generate tailored learning paths based on student's prior knowledge

## Setup Instructions

### Prerequisites
- Python 3.8+
- Together API key

### Backend Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/education-llama-stack.git
   cd education-llama-stack
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Configure your API key:
   - Create a `.env` file in the `backend` directory
   - Add your Together API key:
     ```
     TOGETHER_API_KEY=your_api_key_here
     ```

5. Start the backend server:
   ```bash
   python -m uvicorn main:app --reload
   ```
   The backend will be available at http://localhost:8000

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Start a simple HTTP server:
   ```bash
   python -m http.server 5000
   ```
   The frontend will be available at http://localhost:5000

## API Endpoints

### Lesson Plans
- `POST /api/lesson-plans/` - Generate a lesson plan

### Quizzes
- `POST /api/quizzes/` - Generate a quiz

### Content Adaptation
- `POST /api/content-adaptation/` - Adapt educational content

### Interactive Scenarios
- `POST /api/interactive-scenarios/` - Generate an interactive learning scenario

### Feedback
- `POST /api/feedback/` - Generate feedback for student work

### Subject-Specific Tools
- `POST /api/subjects/resources` - Generate resources for a specific subject
- `POST /api/subjects/curriculum` - Generate a curriculum for a specific subject
- `POST /api/subjects/personalized-path` - Generate a personalized learning path

## Technologies Used
- **Backend**: FastAPI, Python
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Llama Stack, Together API

## License
MIT
