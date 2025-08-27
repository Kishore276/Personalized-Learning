// Enhanced JavaScript with smooth animations and transitions
document.addEventListener('DOMContentLoaded', function() {
    initializeExercises();
    initializeScrollEffects();
    initializeTooltips();
    initializeProgressTracking();
});

function initializeExercises() {
    // Initially hide all exercises except the first one
    const exercises = document.querySelectorAll('.exercise-section');
    exercises.forEach((exercise, index) => {
        if (index > 0) {
            exercise.classList.remove('enabled');
            exercise.style.opacity = '0.3';
            exercise.style.pointerEvents = 'none';
            exercise.style.transform = 'translateY(20px)';
        }
    });
}

function initializeScrollEffects() {
    // Back to top button
    const backToTop = document.createElement('button');
    backToTop.className = 'back-to-top';
    backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTop.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
    document.body.appendChild(backToTop);

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    });
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

function initializeProgressTracking() {
    updateProgress();
}

function updateProgress() {
    const totalExercises = document.querySelectorAll('.exercise-section').length;
    const enabledExercises = document.querySelectorAll('.exercise-section.enabled').length + 1; // +1 for first exercise
    const percentage = Math.round((enabledExercises / totalExercises) * 100);
    
    // Create progress indicator if it doesn't exist
    let progressIndicator = document.querySelector('.exercise-progress');
    if (!progressIndicator && totalExercises > 1) {
        progressIndicator = document.createElement('div');
        progressIndicator.className = 'exercise-progress';
        document.body.appendChild(progressIndicator);
    }
    
    if (progressIndicator) {
        progressIndicator.innerHTML = `
            <div class="text-center">
                <div class="small text-muted mb-2">Progress</div>
                <div class="progress mb-2" style="height: 8px;">
                    <div class="progress-bar" style="width: ${percentage}%"></div>
                </div>
                <div class="small">${enabledExercises}/${totalExercises} Exercises</div>
            </div>
        `;
    }
}

// Enhanced start exercise function with smooth animations
window.startExercise = function(exerciseId) {
    const currentExercise = document.querySelector(`#exercise${exerciseId}`);
    const nextExerciseId = exerciseId + 1;
    const nextExercise = document.querySelector(`#exercise${nextExerciseId}`);
    
    if (currentExercise) {
        // Add completion animation to current exercise
        currentExercise.style.transform = 'scale(1.02)';
        currentExercise.style.boxShadow = '0 8px 25px rgba(99, 102, 241, 0.2)';
        
        setTimeout(() => {
            currentExercise.style.transform = 'scale(1)';
            currentExercise.style.boxShadow = '';
        }, 300);

        // Hide start button and show exercise content with animation
        const startBtn = currentExercise.querySelector('.start-exercise-btn');
        if (startBtn) {
            startBtn.style.transform = 'scale(0)';
            startBtn.style.opacity = '0';
            setTimeout(() => {
                startBtn.style.display = 'none';
            }, 300);
        }
    }
    
    if (nextExercise) {
        // Show next exercise with smooth transition
        setTimeout(() => {
            nextExercise.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            nextExercise.style.opacity = '1';
            nextExercise.style.transform = 'translateY(0)';
            nextExercise.style.pointerEvents = 'all';
            nextExercise.classList.add('enabled');
            
            // Smooth scroll to next exercise
            setTimeout(() => {
                nextExercise.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }, 200);
            
            updateProgress();
            showToast('Success!', `Exercise ${nextExerciseId} is now available!`, 'success');
        }, 400);
    }
};

// Enhanced option selection with visual feedback
window.selectOption = function(optionId, optionIndex) {
    const allOptions = document.querySelectorAll(`[id*="${optionId.split('-')[0]}"] .quiz-option`);
    
    // Remove previous selections with animation
    allOptions.forEach(option => {
        option.classList.remove('selected');
        option.style.transform = 'scale(1)';
    });
    
    // Select current option with animation
    const selectedOption = document.getElementById(optionId);
    if (selectedOption) {
        selectedOption.classList.add('selected');
        selectedOption.style.transform = 'scale(1.02)';
        
        // Store the selected answer
        selectedOption.closest('.exercise-section').dataset.selectedAnswer = optionIndex;
        
        // Add ripple effect
        createRippleEffect(selectedOption);
    }
};

function createRippleEffect(element) {
    const ripple = document.createElement('div');
    ripple.className = 'ripple';
    ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(99, 102, 241, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
    `;
    
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = (rect.width / 2 - size / 2) + 'px';
    ripple.style.top = (rect.height / 2 - size / 2) + 'px';
    
    element.style.position = 'relative';
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Enhanced submit solution with animations
window.submitSolution = function(exerciseId) {
    const exercise = document.querySelector(`#exercise${exerciseId}`);
    if (!exercise) return;

    const selectedAnswer = exercise.dataset.selectedAnswer;
    if (selectedAnswer === undefined) {
        showToast('Warning', 'Please select an answer first!', 'warning');
        return;
    }

    // Get correct answer (assuming it's stored in data-correct attribute)
    const correctAnswer = exercise.dataset.correctAnswer || 0;
    const isCorrect = parseInt(selectedAnswer) === parseInt(correctAnswer);

    // Add visual feedback to options
    const options = exercise.querySelectorAll('.quiz-option');
    options.forEach((option, index) => {
        if (index === parseInt(correctAnswer)) {
            option.classList.add('correct');
            option.innerHTML += ' <i class="fas fa-check-circle text-success ms-2"></i>';
        } else if (index === parseInt(selectedAnswer) && !isCorrect) {
            option.classList.add('incorrect');
            option.innerHTML += ' <i class="fas fa-times-circle text-danger ms-2"></i>';
        }
        option.style.pointerEvents = 'none';
    });

    // Update global score tracking
    if (!window.exerciseResults) {
        window.exerciseResults = [];
    }
    window.exerciseResults[exerciseId - 1] = isCorrect;

    // Show score with animation
    let scoreDisplay = exercise.querySelector('.score-display');
    if (!scoreDisplay) {
        scoreDisplay = document.createElement('div');
        scoreDisplay.className = 'score-display';
        exercise.appendChild(scoreDisplay);
    }

    scoreDisplay.className = `score-display ${isCorrect ? 'correct' : 'incorrect'} show`;
    scoreDisplay.innerHTML = `
        <div class="d-flex align-items-center justify-content-center">
            <i class="fas ${isCorrect ? 'fa-check-circle' : 'fa-times-circle'} me-2"></i>
            <span>${isCorrect ? 'Correct!' : 'Incorrect'}</span>
        </div>
    `;

    // Show overall results if this is the last exercise
    const totalExercises = document.querySelectorAll('.exercise-section').length;
    if (window.exerciseResults.filter(result => result !== undefined).length === totalExercises) {
        setTimeout(() => showOverallResults(), 1000);
    }

    // Show solution button with animation
    const solutionBtn = exercise.querySelector('.show-solution');
    const submitBtn = exercise.querySelector('button[onclick*="submitSolution"]');
    
    if (solutionBtn) {
        solutionBtn.style.display = 'inline-block';
        solutionBtn.style.transform = 'scale(0)';
        setTimeout(() => {
            solutionBtn.style.transform = 'scale(1)';
            solutionBtn.classList.add('active');
        }, 200);
    }
    
    if (submitBtn) {
        submitBtn.style.transform = 'scale(0)';
        setTimeout(() => {
            submitBtn.style.display = 'none';
        }, 300);
    }

    showToast('Answer Submitted!', isCorrect ? 'Well done!' : 'Review the solution to learn more.', isCorrect ? 'success' : 'info');
};

function showOverallResults() {
    const correct = window.exerciseResults.filter(result => result === true).length;
    const total = window.exerciseResults.length;
    const percentage = Math.round((correct / total) * 100);
    
    const resultsModal = `
        <div class="modal fade" id="resultsModal" tabindex="-1">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header bg-primary text-white">
                        <h5 class="modal-title">
                            <i class="fas fa-trophy me-2"></i>Exercise Results
                        </h5>
                    </div>
                    <div class="modal-body text-center">
                        <div class="row mb-4">
                            <div class="col-4">
                                <div class="text-success">
                                    <i class="fas fa-check-circle fa-2x"></i>
                                    <h4>${correct}</h4>
                                    <small>Correct</small>
                                </div>
                            </div>
                            <div class="col-4">
                                <div class="text-danger">
                                    <i class="fas fa-times-circle fa-2x"></i>
                                    <h4>${total - correct}</h4>
                                    <small>Wrong</small>
                                </div>
                            </div>
                            <div class="col-4">
                                <div class="text-primary">
                                    <i class="fas fa-percentage fa-2x"></i>
                                    <h4>${percentage}%</h4>
                                    <small>Score</small>
                                </div>
                            </div>
                        </div>
                        <div class="alert ${percentage >= 80 ? 'alert-success' : percentage >= 60 ? 'alert-warning' : 'alert-info'}">
                            <h5>${percentage >= 80 ? '🎉 Excellent Work!' : percentage >= 60 ? '👍 Good Job!' : '📚 Keep Practicing!'}</h5>
                            <p class="mb-0">
                                ${percentage >= 80 ? 'You have mastered this topic!' : 
                                  percentage >= 60 ? 'You\'re doing well, review the solutions for better understanding.' : 
                                  'Consider reviewing the material and trying again.'}
                            </p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Continue Learning</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', resultsModal);
    const modal = new bootstrap.Modal(document.getElementById('resultsModal'));
    modal.show();
    
    // Remove modal from DOM when hidden
    document.getElementById('resultsModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// Enhanced solution display
window.showSolution = function(exerciseId) {
    const exercise = document.querySelector(`#exercise${exerciseId}`);
    if (!exercise) return;
    
    const solutions = exercise.querySelectorAll('.solution');
    const solutionBtn = exercise.querySelector('.show-solution');
    
    solutions.forEach(solution => {
        if (solution.style.display === 'none' || solution.style.display === '') {
            solution.style.display = 'block';
            solution.style.opacity = '0';
            solution.style.transform = 'translateY(-10px)';
            solution.classList.add('active');
            
            setTimeout(() => {
                solution.style.opacity = '1';
                solution.style.transform = 'translateY(0)';
            }, 100);
            
            if (solutionBtn) {
                solutionBtn.textContent = 'Hide Solution';
                solutionBtn.classList.remove('btn-secondary');
                solutionBtn.classList.add('btn-outline-secondary');
            }
        } else {
            solution.style.opacity = '0';
            solution.style.transform = 'translateY(-10px)';
            
            setTimeout(() => {
                solution.style.display = 'none';
                solution.classList.remove('active');
            }, 300);
            
            if (solutionBtn) {
                solutionBtn.textContent = 'Show Solution';
                solutionBtn.classList.remove('btn-outline-secondary');
                solutionBtn.classList.add('btn-secondary');
            }
        }
    });
};

// Toast notification system
function showToast(title, message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    const toastId = 'toast-' + Date.now();
    
    const toastHtml = `
        <div id="${toastId}" class="toast" role="alert">
            <div class="toast-header">
                <i class="fas ${getToastIcon(type)} text-${type === 'warning' ? 'warning' : type} me-2"></i>
                <strong class="me-auto">${title}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">${message}</div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toast = new bootstrap.Toast(document.getElementById(toastId));
    toast.show();
    
    // Remove toast element after it's hidden
    document.getElementById(toastId).addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

function getOrCreateToastContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1055';
        document.body.appendChild(container);
    }
    return container;
}

function getToastIcon(type) {
    switch(type) {
        case 'success': return 'fa-check-circle';
        case 'warning': return 'fa-exclamation-triangle';
        case 'error': return 'fa-times-circle';
        default: return 'fa-info-circle';
    }
}

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
