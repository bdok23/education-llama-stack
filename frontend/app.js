
const API_BASE_URL = 'https://user:3e2cf93917ff32359e3b4c3e7bc29f6b@education-content-generator-tunnel-bxzapupu.devinapps.com';

function showLoading(formId, buttonText = 'Generating...') {
    const form = document.getElementById(formId);
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${buttonText}`;
    submitButton.disabled = true;
}

function hideLoading(formId, buttonText = 'Generate') {
    const form = document.getElementById(formId);
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.innerHTML = buttonText;
    submitButton.disabled = false;
}

function showResult(resultId, content) {
    const resultContainer = document.getElementById(resultId);
    const contentContainer = document.getElementById(`${resultId}-content`);
    
    contentContainer.innerHTML = content;
    resultContainer.style.display = 'block';
    
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function setupCopyButton(buttonId, contentId) {
    const copyButton = document.getElementById(buttonId);
    copyButton.addEventListener('click', () => {
        const content = document.getElementById(contentId).innerText;
        navigator.clipboard.writeText(content)
            .then(() => {
                const originalText = copyButton.innerText;
                copyButton.innerText = 'Copied!';
                setTimeout(() => {
                    copyButton.innerText = originalText;
                }, 2000);
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
            });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setupCopyButton('copy-lesson-plan', 'lesson-plan-content');
    setupCopyButton('copy-quiz', 'quiz-content');
    setupCopyButton('copy-adaptation', 'adaptation-content');
    setupCopyButton('copy-scenario', 'scenario-content');
    setupCopyButton('copy-feedback', 'feedback-content');
    setupCopyButton('copy-resources', 'subject-resources-content');
    setupCopyButton('copy-curriculum', 'curriculum-content');
    setupCopyButton('copy-path', 'personalized-path-content');
});

document.getElementById('subject-resources-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading('subject-resources-form', 'Generating Resources...');
    
    const subjectType = document.getElementById('subject-type').value;
    const level = document.getElementById('subject-level').value;
    const topic = document.getElementById('subject-topic').value;
    
    const requestData = {
        subject_type: subjectType,
        level: level
    };
    
    if (topic) {
        requestData.topic = topic;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/subjects/resources`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const formattedContent = data.resources.replace(/\n/g, '<br>');
        
        showResult('subject-resources-result', formattedContent);
    } catch (error) {
        console.error('Error generating subject resources:', error);
        alert(`Error generating subject resources: ${error.message}`);
    } finally {
        hideLoading('subject-resources-form', 'Generate Resources');
    }
});

document.getElementById('curriculum-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading('curriculum-form', 'Generating Curriculum...');
    
    const subjectType = document.getElementById('curriculum-subject').value;
    const level = document.getElementById('curriculum-level').value;
    const duration = parseInt(document.getElementById('curriculum-duration').value);
    const includeAssessments = document.getElementById('include-assessments').checked;
    const includeResources = document.getElementById('include-resources').checked;
    
    const requestData = {
        subject_type: subjectType,
        level: level,
        duration_weeks: duration,
        include_assessments: includeAssessments,
        include_resources: includeResources
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/subjects/curriculum`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const formattedContent = data.curriculum.replace(/\n/g, '<br>');
        
        showResult('curriculum-result', formattedContent);
    } catch (error) {
        console.error('Error generating curriculum:', error);
        alert(`Error generating curriculum: ${error.message}`);
    } finally {
        hideLoading('curriculum-form', 'Generate Curriculum');
    }
});

document.getElementById('personalized-path-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading('personalized-path-form', 'Generating Learning Path...');
    
    const subjectType = document.getElementById('path-subject').value;
    const topicsKnown = document.getElementById('topics-known').value.split('\n').filter(topic => topic.trim() !== '');
    const learningObjectives = document.getElementById('learning-objectives-path').value.split('\n').filter(obj => obj.trim() !== '');
    const preferredLearningStyle = document.getElementById('preferred-learning-style').value;
    
    const requestData = {
        subject_type: subjectType,
        topics_known: topicsKnown,
        learning_objectives: learningObjectives
    };
    
    if (preferredLearningStyle) {
        requestData.preferred_learning_style = preferredLearningStyle;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/subjects/personalized-path`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const formattedContent = data.learning_path.replace(/\n/g, '<br>');
        
        showResult('personalized-path-result', formattedContent);
    } catch (error) {
        console.error('Error generating personalized learning path:', error);
        alert(`Error generating personalized learning path: ${error.message}`);
    } finally {
        hideLoading('personalized-path-form', 'Generate Learning Path');
    }
});

document.getElementById('lesson-plan-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading('lesson-plan-form');
    
    const subject = document.getElementById('subject').value;
    const gradeLevel = document.getElementById('grade-level').value;
    const topic = document.getElementById('topic').value;
    const learningObjectives = document.getElementById('learning-objectives').value.split('\n').filter(obj => obj.trim() !== '');
    const duration = parseInt(document.getElementById('duration').value);
    
    const requestData = {
        subject,
        grade_level: gradeLevel,
        topic,
        learning_objectives: learningObjectives,
        duration_minutes: duration
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/lesson-plans/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const formattedContent = data.lesson_plan.replace(/\n/g, '<br>');
        
        showResult('lesson-plan-result', formattedContent);
    } catch (error) {
        console.error('Error generating lesson plan:', error);
        alert(`Error generating lesson plan: ${error.message}`);
    } finally {
        hideLoading('lesson-plan-form');
    }
});

document.getElementById('quiz-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading('quiz-form');
    
    const subject = document.getElementById('quiz-subject').value;
    const topic = document.getElementById('quiz-topic').value;
    const difficulty = parseInt(document.getElementById('difficulty').value);
    const numQuestions = parseInt(document.getElementById('num-questions').value);
    
    const questionTypes = [];
    if (document.getElementById('multiple-choice').checked) {
        questionTypes.push('multiple_choice');
    }
    if (document.getElementById('short-answer').checked) {
        questionTypes.push('short_answer');
    }
    if (document.getElementById('true-false').checked) {
        questionTypes.push('true_false');
    }
    
    const requestData = {
        subject,
        topic,
        difficulty,
        num_questions: numQuestions,
        question_types: questionTypes
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/quizzes/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const formattedContent = data.quiz.replace(/\n/g, '<br>');
        
        showResult('quiz-result', formattedContent);
    } catch (error) {
        console.error('Error generating quiz:', error);
        alert(`Error generating quiz: ${error.message}`);
    } finally {
        hideLoading('quiz-form');
    }
});

document.getElementById('adaptation-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading('adaptation-form', 'Adapting...');
    
    const content = document.getElementById('original-content').value;
    const readingLevel = document.getElementById('reading-level').value;
    const learningStyle = document.getElementById('learning-style').value;
    const simplify = document.getElementById('simplify').checked;
    
    const requestData = {
        content,
        target_reading_level: readingLevel,
        simplify
    };
    
    if (learningStyle) {
        requestData.target_learning_style = learningStyle;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/content-adaptation/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const formattedContent = data.adapted_content.replace(/\n/g, '<br>');
        
        showResult('adaptation-result', formattedContent);
    } catch (error) {
        console.error('Error adapting content:', error);
        alert(`Error adapting content: ${error.message}`);
    } finally {
        hideLoading('adaptation-form', 'Adapt Content');
    }
});

document.getElementById('scenario-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading('scenario-form');
    
    const subject = document.getElementById('scenario-subject').value;
    const gradeLevel = document.getElementById('scenario-grade-level').value;
    const topic = document.getElementById('scenario-topic').value;
    const scenarioType = document.getElementById('scenario-type').value;
    const learningObjectives = document.getElementById('scenario-objectives').value.split('\n').filter(obj => obj.trim() !== '');
    const duration = parseInt(document.getElementById('scenario-duration').value);
    const complexity = parseInt(document.getElementById('scenario-complexity').value);
    const includeMaterials = document.getElementById('include-materials').checked;
    const includeInstructions = document.getElementById('include-instructions').checked;
    
    const requestData = {
        subject,
        grade_level: gradeLevel,
        topic,
        scenario_type: scenarioType,
        learning_objectives: learningObjectives,
        duration_minutes: duration,
        complexity,
        include_materials: includeMaterials,
        include_instructions: includeInstructions
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/interactive-scenarios/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const formattedContent = data.scenario.replace(/\n/g, '<br>');
        
        showResult('scenario-result', formattedContent);
    } catch (error) {
        console.error('Error generating scenario:', error);
        alert(`Error generating scenario: ${error.message}`);
    } finally {
        hideLoading('scenario-form');
    }
});

document.getElementById('feedback-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    showLoading('feedback-form', 'Generating Feedback...');
    
    const studentWork = document.getElementById('student-work').value;
    const subject = document.getElementById('feedback-subject').value;
    const gradeLevel = document.getElementById('feedback-grade-level').value;
    const assignmentDescription = document.getElementById('assignment-description').value;
    const feedbackType = document.getElementById('feedback-type').value;
    const feedbackTone = document.getElementById('feedback-tone').value;
    const includeStrengths = document.getElementById('include-strengths').checked;
    const includeAreasForImprovement = document.getElementById('include-areas').checked;
    const includeNextSteps = document.getElementById('include-next-steps').checked;
    
    const requestData = {
        student_work: studentWork,
        subject,
        grade_level: gradeLevel,
        assignment_description: assignmentDescription,
        feedback_type: feedbackType,
        feedback_tone: feedbackTone,
        include_strengths: includeStrengths,
        include_areas_for_improvement: includeAreasForImprovement,
        include_next_steps: includeNextSteps
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/feedback/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        
        const formattedContent = data.feedback.replace(/\n/g, '<br>');
        
        showResult('feedback-result', formattedContent);
    } catch (error) {
        console.error('Error generating feedback:', error);
        alert(`Error generating feedback: ${error.message}`);
    } finally {
        hideLoading('feedback-form', 'Generate Feedback');
    }
});
