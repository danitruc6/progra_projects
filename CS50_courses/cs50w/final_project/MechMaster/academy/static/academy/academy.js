// Function to handle course registration
function registerCourse(event, courseId, buttonElement) {
  event.preventDefault(); // Prevent default behavior of the <> to redirect to the course page

  const url = `/course_registration/${courseId}/`;
  fetch(url, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle the response from the server
      if (data.success) {
        // Replace the register button with the registered badge
        const registeredBadge = document.createElement('span');
        registeredBadge.className = 'registered-badge';
        registeredBadge.textContent = 'Registered';
        buttonElement.parentNode.replaceChild(registeredBadge, buttonElement);
        // Perform any additional actions, such as updating the UI
      } else {
        // Course registration failed
        alert('Course registration failed!');
        // Perform any additional error handling or display error messages
      }
    })
    .catch((error) => {
      // Handle any error that occurred during the request
      console.error('Error:', error);
      alert('An error occurred during course registration.');
    });
}

  
// Function to get the value of a cookie
function getCookie(name) {
  const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return cookieValue ? cookieValue.pop() : '';
}
  
document.addEventListener('DOMContentLoaded', function() {
  // New code to display star icons based on average rating
  const courseRatingElements = document.querySelectorAll('.course-rating');
  courseRatingElements.forEach(function(ratingElement) {
    const averageRating = parseFloat(ratingElement.dataset.averageRating);
    const fullStars = Math.floor(averageRating);
    const decimalPart = averageRating - fullStars;
    const hasHalfStar = decimalPart >= 0.5;

    // Clear previous star icons and message
    ratingElement.innerHTML = '';

    // Add star icons if there are ratings
    if (averageRating > 0) {
      // Add full star icons
      for (let i = 0; i < fullStars; i++) {
        const fullStarIcon = document.createElement('i');
        fullStarIcon.classList.add('fas', 'fa-star', 'rating-stars');
        ratingElement.appendChild(fullStarIcon);
      }

      // Add half star icon if necessary
      if (hasHalfStar) {
        const halfStarIcon = document.createElement('i');
        halfStarIcon.classList.add('fas', 'fa-star-half-alt', 'rating-stars');
        ratingElement.appendChild(halfStarIcon);
      }

      // Add empty star icons to fill up the remaining space
      const remainingStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
      for (let i = 0; i < remainingStars; i++) {
        const emptyStarIcon = document.createElement('i');
        emptyStarIcon.classList.add('far', 'fa-star', 'rating-stars');
        ratingElement.appendChild(emptyStarIcon);
      }
    } else {
      // Add "no ratings yet" message
      const noRatingsMessage = document.createElement('p');
      noRatingsMessage.textContent = 'No ratings yet';
      ratingElement.appendChild(noRatingsMessage);
    }
  });
});