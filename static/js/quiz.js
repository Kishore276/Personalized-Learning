// Quiz functionality
let userAnswers = {};

// Handle option selection
function selectOption(questionId, optionId) {
    userAnswers[questionId] = optionId;
    
    // Update UI to show selected option
    const questionContainer = document.querySelector(`[data-question="${questionId}"]`);
    questionContainer.querySelectorAll('.quiz-option').forEach((option, index) => {
        option.classList.toggle('selected', index === optionId);
    });
}

// Handle solution submission
function submitSolution(exerciseId) {
    const exercise = document.querySelector(`#exercise${exerciseId}`);
    const questions = exercise.querySelectorAll('.question-container');
    let correct = 0;
    let total = questions.length;

    questions.forEach((question, index) => {
        const questionId = `${exerciseId}-${index}`;
        const correctAnswer = parseInt(question.dataset.correct);
        const userAnswer = userAnswers[questionId];

        const scoreDisplay = question.querySelector('.score-display');
        if (userAnswer === correctAnswer) {
            correct++;
            scoreDisplay.textContent = "Correct!";
            scoreDisplay.classList.add('correct');
            scoreDisplay.classList.remove('incorrect');
        } else {
            scoreDisplay.textContent = "Incorrect";
            scoreDisplay.classList.add('incorrect');
            scoreDisplay.classList.remove('correct');
        }
        scoreDisplay.style.display = 'block';
    });

    // Show total score
    const totalScore = exercise.querySelector('.total-score');
    totalScore.textContent = `Total Score: ${correct} out of ${total}`;
    totalScore.style.display = 'block';

    // Show solution button
    const solutionBtn = exercise.querySelector('.show-solution');
    if (solutionBtn) {
        solutionBtn.style.display = 'block';
    }
    
    // If user got all correct, unlock and show next exercise
    if (correct === total) {
        unlockNextExercise(exerciseId);
    }
}

// Handle showing solutions
function showSolution(exerciseId) {
    const exercise = document.querySelector(`#exercise${exerciseId}`);
    const solutions = exercise.querySelectorAll('.solution');
    solutions.forEach(solution => {
        solution.style.display = 'block';
    });
}
