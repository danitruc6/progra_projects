document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('quiz-form');
    form.addEventListener('submit', function(event) {

        const questions = document.querySelectorAll('.question');
        let score = 0;
        let hasError = false;

        questions.forEach(question => {
            const selectedOption = question.querySelector('input[type="radio"]:checked');
            if (!selectedOption) {
                const errorDiv = question.querySelector(`#error-${question.dataset.questionId}`);
                errorDiv.style.display = 'block';
                hasError = true;
            } else {
                const isCorrect = selectedOption.getAttribute('data-is-correct') === 'true';
                if (isCorrect) {
                    score++;
                }
            }
        });

        if (hasError) {
            return; // Stop form submission if there are errors
        }

    });
});
