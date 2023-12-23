document.addEventListener('DOMContentLoaded', () => {

const editButtons = document.querySelectorAll('.edit-post-btn');

editButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    const postId = button.dataset.postId;
    const postContent = document.getElementById(`post-content-${postId}`);
    const editForm = document.createElement('form');
    editForm.dataset.postId = postId;

    const textarea = document.createElement('textarea');
    textarea.id = `edit-post-content-${postId}`;
    textarea.value = postContent.textContent.trim();
    editForm.appendChild(textarea);

    const saveButton = document.createElement('button');
    saveButton.type = 'submit';
    saveButton.textContent = 'Save';
    saveButton.classList.add('btn', 'btn-secondary', 'btn-sm');
    editForm.appendChild(saveButton);

    postContent.replaceWith(editForm);
    button.style.display = 'none';

    editForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const form = event.target;
      const postId = form.dataset.postId;
      const editedContent = form.querySelector(`#edit-post-content-${postId}`).value.trim();

      fetch(`/edit_post/${postId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ edited_content: editedContent }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const updatedPostContent = document.createElement('p');
            updatedPostContent.id = `post-content-${postId}`;
            updatedPostContent.textContent = data.content;

            form.replaceWith(updatedPostContent);
            button.style.display = 'inline-block';
          }
        });
    });
  });
});




const likeButtons = document.querySelectorAll('.like-btn');

likeButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
      const postId = button.dataset.postId;
    const likesCount = document.querySelector(`#post-likes-${postId}`);
      const heartIcon = button.querySelector('.heart-icon');
    const isLiked = button.classList.contains('liked');

    fetch(`/like_post/${postId}/`, {
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
          heartIcon.classList.toggle('fa-heart-o');
          heartIcon.classList.toggle('fa-heart');
        }
      });
  });
});




});

function getCookie(name) {
const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
return cookieValue ? cookieValue.pop() : '';
}
