document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chat-log');
    const userInput = document.getElementById('user-input');
    const sendChatBtn = document.getElementById('send-chat-btn');

    const getExerciseBtn = document.getElementById('get-exercise-btn');
    const exerciseDisplay = document.getElementById('exercise-display');
    const answerSubmissionArea = document.getElementById('answer-submission-area');
    const exerciseAnswerInput = document.getElementById('exercise-answer-input');
    const submitAnswerBtn = document.getElementById('submit-answer-btn');
    const exerciseFeedback = document.getElementById('exercise-feedback');

    let currentExerciseId = null;

    // --- Chat Functionality ---
    sendChatBtn.addEventListener('click', handleSendChat);
    userInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            handleSendChat();
        }
    });

    async function handleSendChat() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage('You', message);
        userInput.value = '';

        try {
            // Assuming backend is running on port 5000
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            appendMessage('AI', data.response);
        } catch (error) {
            console.error('Error sending chat message:', error);
            appendMessage('Error', 'Could not connect to AI. (Check console)');
        }
    }

    function appendMessage(sender, message) {
        const p = document.createElement('p');
        p.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatLog.appendChild(p);
        chatLog.scrollTop = chatLog.scrollHeight; // Scroll to bottom
    }

    // --- Exercise Functionality ---
    getExerciseBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('http://localhost:5000/get_exercise');
            if (!response.ok) {
                const errData = await response.json();
                exerciseDisplay.innerHTML = `<p>Error: ${errData.error || 'Could not fetch exercise.'}</p>`;
                answerSubmissionArea.style.display = 'none';
                return;
            }
            const exercise = await response.json();
            displayExercise(exercise);
        } catch (error) {
            console.error('Error fetching exercise:', error);
            exerciseDisplay.innerHTML = '<p>Could not fetch exercise. (Check console)</p>';
            answerSubmissionArea.style.display = 'none';
        }
    });

    function displayExercise(exercise) {
        currentExerciseId = exercise.exercise_id;
        let html = `<p><strong>ID:</strong> ${exercise.exercise_id}</p>`;
        html += `<p><strong>Concept:</strong> ${exercise.concepts_tested.join(', ')}</p>`;
        html += `<p><strong>Type:</strong> ${exercise.exercise_type}</p>`;
        html += `<p><strong>Prompt:</strong> ${exercise.question_prompt}</p>`;

        if (exercise.exercise_type === 'multiple_choice' && exercise.options) {
            html += '<ul>';
            exercise.options.forEach((opt, index) => {
                // For submission, we'll use the option_text.
                // In a real app, you might use radio buttons and values.
                html += `<li>${opt.option_text}</li>`;
            });
            html += '</ul>';
            exerciseAnswerInput.placeholder = "Type the exact option text";
        } else if (exercise.exercise_type === 'true_false') {
            exerciseAnswerInput.placeholder = "Type 'True' or 'False'";
        } else {
            exerciseAnswerInput.placeholder = "Your short answer...";
        }

        exerciseDisplay.innerHTML = html;
        answerSubmissionArea.style.display = 'block';
        exerciseFeedback.innerHTML = ''; // Clear previous feedback
        exerciseAnswerInput.value = ''; // Clear previous answer
    }

    submitAnswerBtn.addEventListener('click', async () => {
        const answer = exerciseAnswerInput.value.trim();
        if (!answer || !currentExerciseId) {
            exerciseFeedback.innerHTML = '<p>Please enter an answer for the current exercise.</p>';
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/submit_answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ exercise_id: currentExerciseId, answer: answer })
            });
            const data = await response.json();
            exerciseFeedback.innerHTML = `<p><strong>Feedback:</strong> ${data.feedback} (Correct: ${data.correct})</p>`;
        } catch (error) {
            console.error('Error submitting answer:', error);
            exerciseFeedback.innerHTML = '<p>Could not submit answer. (Check console)</p>';
        }
    });
});
