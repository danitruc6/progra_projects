document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            const topicId = button.dataset.topicId;
            const likesCount = document.querySelector(`#topic-likes-${topicId}`);
            const heartIcon = button.querySelector('.heart-icon');
            const isLiked = button.classList.contains('liked');

            fetch(`/like_topic/${topicId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ is_liked: !isLiked }),
            })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    // Update the like count displayed on the page
                    likesCount.textContent = data.likes_count;

                    // Toggle the liked class on the button and heart icon
                    button.classList.toggle('liked');
                    heartIcon.classList.toggle('far-heart');
                    heartIcon.classList.toggle('fas-heart');
                }
            });
        });
    });
});

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}
