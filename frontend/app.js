
const API_BASE_URL = window.location.hostname === 'localhost' 
  ? 'http://localhost:8000' 
  : 'https://api.education-content-generator.com';

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
    console.log(`showResult called with resultId: ${resultId}`);
    
    const resultContainer = document.getElementById(resultId);
    if (!resultContainer) {
        console.error(`Result container not found: ${resultId}`);
        return;
    }
    
    let contentId;
    if (resultId === 'lesson-plan-result') {
        contentId = 'lesson-plan-content';
    } else {
        contentId = `${resultId.replace('-result', '')}-content`;
    }
    
    console.log(`Looking for content container with ID: ${contentId}`);
    const contentContainer = document.getElementById(contentId);
    
    if (!contentContainer) {
        console.error(`Content container not found: ${contentId}`);
        return;
    }
    
    console.log('Setting innerHTML for content container');
    
    contentContainer.innerHTML = '<div class="text-center p-5"><div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;"><span class="visually-hidden">Loading...</span></div><p class="mt-3">Preparing your content...</p></div>';
    resultContainer.style.display = 'block';
    
    setTimeout(() => {
        const copyButtonContainer = document.createElement('div');
        copyButtonContainer.className = 'copy-button-container';
        
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '<i class="fas fa-copy"></i> Copy to clipboard';
        copyButton.title = 'Copy content to clipboard';
        
        copyButton.addEventListener('click', () => {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = content;
            const textContent = tempDiv.textContent || tempDiv.innerText || '';
            
            navigator.clipboard.writeText(textContent.trim());
            copyButton.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
                copyButton.innerHTML = '<i class="fas fa-copy"></i> Copy to clipboard';
            }, 2000);
        });
        
        copyButtonContainer.appendChild(copyButton);
        resultContainer.insertBefore(copyButtonContainer, resultContainer.firstChild);
        
        contentContainer.innerHTML = content;
        contentContainer.classList.add('fade-in');
        
        const codeBlocks = contentContainer.querySelectorAll('pre, code');
        codeBlocks.forEach(block => {
            const copyButton = document.createElement('button');
            copyButton.className = 'btn btn-sm btn-outline-primary copy-code-btn';
            copyButton.innerHTML = '<i class="fas fa-copy"></i>';
            copyButton.title = 'Copy to clipboard';
            
            copyButton.addEventListener('click', () => {
                navigator.clipboard.writeText(block.textContent);
                copyButton.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    copyButton.innerHTML = '<i class="fas fa-copy"></i>';
                }, 2000);
            });
            
            block.parentNode.style.position = 'relative';
            block.parentNode.appendChild(copyButton);
        });
        
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 800);
}

function formatOutputWithStyles(content, type) {
    let formattedContent = '<div class="styled-output">';
    
    content = content.replace(/^# (.+)$/gm, '<h1><i class="fas fa-book-open"></i> $1</h1>');
    content = content.replace(/^## (.+)$/gm, '<h2><i class="fas fa-bookmark"></i> $1</h2>');
    content = content.replace(/^### (.+)$/gm, '<h3><i class="fas fa-angle-right"></i> $1</h3>');
    
    content = content.replace(/^- (.+)$/gm, '<li>$1</li>');
    
    let lines = content.split('\n');
    let inList = false;
    let newContent = [];
    
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('- ')) {
            if (!inList) {
                newContent.push('<ul class="styled-list">');
                inList = true;
            }
            newContent.push('<li>' + lines[i].substring(2) + '</li>');
        } else {
            if (inList) {
                newContent.push('</ul>');
                inList = false;
            }
            newContent.push(lines[i]);
        }
    }
    
    if (inList) {
        newContent.push('</ul>');
    }
    
    content = newContent.join('\n');
    
    if (type === 'lesson-plan') {
        content = content.replace(/Learning Objectives:/g, '<div class="content-section lesson-plan-header"><h3><i class="fas fa-bullseye"></i> Learning Objectives:</h3>');
        content = content.replace(/Materials:/g, '<div class="content-section"><h3><i class="fas fa-tools"></i> Materials:</h3>');
        content = content.replace(/Procedure:/g, '<div class="content-section"><h3><i class="fas fa-tasks"></i> Procedure:</h3>');
        content = content.replace(/Assessment:/g, '<div class="content-section"><h3><i class="fas fa-check-square"></i> Assessment:</h3>');
        content = content.replace(/Closure:/g, '<div class="content-section"><h3><i class="fas fa-door-closed"></i> Closure:</h3>');
        content = content.replace(/Extensions:/g, '<div class="content-section"><h3><i class="fas fa-external-link-alt"></i> Extensions:</h3>');
        
        content = content.replace(/Step (\d+): ([^<(]+)(\((\d+) minutes\))?/g, 
            '<div class="content-section lesson-step"><h3><i class="fas fa-flag"></i> Step $1: $2 <span class="step-duration">$4 minutes</span></h3>');
        
        content = content.replace(/\n\n/g, '</div>\n\n');
    }
    else if (type === 'quiz') {
        content = content.replace(/Question (\d+):/g, '<div class="content-section quiz-header"><h3><i class="fas fa-question-circle"></i> Question $1:</h3>');
        content = content.replace(/A\) /g, '<div class="quiz-option"><strong>A)</strong> ');
        content = content.replace(/B\) /g, '<div class="quiz-option"><strong>B)</strong> ');
        content = content.replace(/C\) /g, '<div class="quiz-option"><strong>C)</strong> ');
        content = content.replace(/D\) /g, '<div class="quiz-option"><strong>D)</strong> ');
        content = content.replace(/Correct Answer: /g, '<div class="quiz-answer"><i class="fas fa-check-circle"></i> <strong>Correct Answer:</strong> ');
        content = content.replace(/Explanation: /g, '<div class="quiz-explanation"><i class="fas fa-info-circle"></i> <strong>Explanation:</strong> ');
        
        content = content.replace(/\n\n/g, '</div></div>\n\n');
    } 
    else if (type === 'adaptation') {
        content = content.replace(/Adapted Content:/g, '<div class="content-section adaptation-header"><h3><i class="fas fa-sync-alt"></i> Adapted Content:</h3>');
        content = content.replace(/Reading Level:/g, '<div class="content-section"><h3><i class="fas fa-book-reader"></i> Reading Level:</h3>');
        content = content.replace(/Learning Style:/g, '<div class="content-section"><h3><i class="fas fa-brain"></i> Learning Style:</h3>');
        
        content = content.replace(/\n\n/g, '</div>\n\n');
    } 
    else if (type === 'scenario') {
        content = content.replace(/Scenario Title:/g, '<div class="content-section scenario-header"><h3><i class="fas fa-theater-masks"></i> Scenario Title:</h3>');
        content = content.replace(/Learning Objectives:/g, '<div class="content-section"><h3><i class="fas fa-bullseye"></i> Learning Objectives:</h3>');
        content = content.replace(/Materials Needed:/g, '<div class="content-section"><h3><i class="fas fa-tools"></i> Materials Needed:</h3>');
        content = content.replace(/Setup Instructions:/g, '<div class="content-section"><h3><i class="fas fa-cogs"></i> Setup Instructions:</h3>');
        content = content.replace(/Scenario Description:/g, '<div class="content-section"><h3><i class="fas fa-book-open"></i> Scenario Description:</h3>');
        content = content.replace(/Student Instructions:/g, '<div class="content-section"><h3><i class="fas fa-user-graduate"></i> Student Instructions:</h3>');
        content = content.replace(/Teacher Notes:/g, '<div class="content-section"><h3><i class="fas fa-chalkboard-teacher"></i> Teacher Notes:</h3>');
        content = content.replace(/Assessment Criteria:/g, '<div class="content-section"><h3><i class="fas fa-clipboard-check"></i> Assessment Criteria:</h3>');
        
        content = content.replace(/\n\n/g, '</div>\n\n');
    } 
    else if (type === 'feedback') {
        content = content.replace(/Overall Assessment:/g, '<div class="content-section feedback-header"><h3><i class="fas fa-star"></i> Overall Assessment:</h3>');
        content = content.replace(/Strengths:/g, '<div class="content-section"><h3><i class="fas fa-thumbs-up"></i> Strengths:</h3>');
        content = content.replace(/Areas for Improvement:/g, '<div class="content-section"><h3><i class="fas fa-wrench"></i> Areas for Improvement:</h3>');
        content = content.replace(/Next Steps:/g, '<div class="content-section"><h3><i class="fas fa-forward"></i> Next Steps:</h3>');
        content = content.replace(/Additional Resources:/g, '<div class="content-section"><h3><i class="fas fa-external-link-alt"></i> Additional Resources:</h3>');
        
        content = content.replace(/\n\n/g, '</div>\n\n');
    }
    else if (type === 'resources') {
        content = content.replace(/^(\d+)\. \*\*(.+)\*\* - (.+)$/gm, 
            '<div class="content-section"><h3><i class="fas fa-book"></i> $2</h3><p>$3</p></div>');
    }
    else if (type === 'curriculum') {
        content = content.replace(/Week (\d+):/g, '<div class="content-section"><h3><i class="fas fa-calendar-week"></i> Week $1:</h3>');
        content = content.replace(/Learning Objectives:/g, '<h4><i class="fas fa-bullseye"></i> Learning Objectives:</h4>');
        content = content.replace(/Key Concepts:/g, '<h4><i class="fas fa-key"></i> Key Concepts:</h4>');
        content = content.replace(/Activities:/g, '<h4><i class="fas fa-tasks"></i> Activities:</h4>');
        content = content.replace(/Assessments:/g, '<h4><i class="fas fa-check-square"></i> Assessments:</h4>');
        content = content.replace(/Additional Resources:/g, '<h4><i class="fas fa-external-link-alt"></i> Additional Resources:</h4>');
        
        content = content.replace(/\n\n/g, '</div>\n\n');
    }
    else if (type === 'path') {
        content = content.replace(/Step (\d+):/g, '<div class="content-section"><h3><i class="fas fa-shoe-prints"></i> Step $1:</h3>');
        content = content.replace(/Focus Areas:/g, '<h4><i class="fas fa-crosshairs"></i> Focus Areas:</h4>');
        content = content.replace(/Resources:/g, '<h4><i class="fas fa-book"></i> Resources:</h4>');
        content = content.replace(/Activities:/g, '<h4><i class="fas fa-tasks"></i> Activities:</h4>');
        
        content = content.replace(/\n\n/g, '</div>\n\n');
    }
    
    content = content.replace(/\n/g, '<br>');
    
    formattedContent += content + '</div>';
    
    return formattedContent;
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
        
        const formattedContent = formatOutputWithStyles(data.resources, 'resources');
        
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
        
        const formattedContent = formatOutputWithStyles(data.curriculum, 'curriculum');
        
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
        
        const formattedContent = formatOutputWithStyles(data.learning_path, 'path');
        
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
        
        const formattedContent = formatOutputWithStyles(data.lesson_plan, 'lesson-plan');
        
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
        
        const formattedContent = formatOutputWithStyles(data.quiz, 'quiz');
        
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
        
        const formattedContent = formatOutputWithStyles(data.adapted_content, 'adaptation');
        
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
        
        const formattedContent = formatOutputWithStyles(data.scenario, 'scenario');
        
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
        
        const formattedContent = formatOutputWithStyles(data.feedback, 'feedback');
        
        showResult('feedback-result', formattedContent);
    } catch (error) {
        console.error('Error generating feedback:', error);
        alert(`Error generating feedback: ${error.message}`);
    } finally {
        hideLoading('feedback-form', 'Generate Feedback');
    }
});
