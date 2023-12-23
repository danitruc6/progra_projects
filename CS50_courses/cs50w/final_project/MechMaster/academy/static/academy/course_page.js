document.addEventListener('DOMContentLoaded', function() {
    var courseTabs = document.querySelectorAll('#courseTabs a');
    var tabContents = document.querySelectorAll('.tab-pane');
  
    courseTabs.forEach(function(tab) {
      tab.addEventListener('click', function(e) {
        e.preventDefault();
        var targetTab = this.getAttribute('href');
  
        // Remove 'active' class from all tabs
        courseTabs.forEach(function(tab) {
          tab.classList.remove('active');
        });
  
        // Add 'active' class to the clicked tab
        this.classList.add('active');
  
        // Remove 'show' class from all tab contents
        tabContents.forEach(function(content) {
          content.classList.remove('show', 'active');
        });
  
        // Add 'show active' class to the target tab content
        document.querySelector(targetTab).classList.add('show', 'active');
      });
    });
  
    // JS code to handle 5 review comments at the same time
  
    var reviewsContainer = document.getElementById('reviews-container');
    var reviewCards = reviewsContainer.getElementsByClassName('review-card');
    var loadMoreBtn = document.getElementById('load-more-btn');
  
    var visibleCount = 5; // Number of initially visible comments
    var increment = 5; // Number of comments to load on each click
  
    // Hide all comments except the first 'visibleCount'
    for (var i = visibleCount; i < reviewCards.length; i++) {
      reviewCards[i].style.display = 'none';
    }
  
    // Show 'Load More' button if there are more comments to display
    if (reviewCards.length <= visibleCount) {
      loadMoreBtn.style.display = 'none';
    }
  
    // Handle 'Load More' button click
    loadMoreBtn.addEventListener('click', function() {
      var hiddenCount = reviewCards.length - visibleCount;
      var toShow = Math.min(increment, hiddenCount);
  
      // Show the next batch of comments
      for (var i = visibleCount; i < visibleCount + toShow; i++) {
        reviewCards[i].style.display = '';
      }
  
      visibleCount += toShow;
  
      // Hide 'Load More' button if there are no more comments to display
      if (visibleCount >= reviewCards.length) {
        loadMoreBtn.style.display = 'none';
      }
    });
  
    // average rating stars calculation
    const starIconsContainer = document.getElementById('star-icons');
    const averageRating = parseFloat(starIconsContainer.dataset.averageRating);
    const fullStars = Math.floor(averageRating);
    const decimalPart = averageRating - fullStars;
    const hasHalfStar = decimalPart >= 0.5;
  
    for (let i = 0; i < fullStars; i++) {
      const fullStarIcon = document.createElement('i');
      fullStarIcon.classList.add('fas', 'fa-star', 'i-star');
      starIconsContainer.appendChild(fullStarIcon);
    }
  
    if (hasHalfStar) {
      const halfStarIcon = document.createElement('i');
      halfStarIcon.classList.add('fas', 'fa-star-half-alt', 'i-star');
      starIconsContainer.appendChild(halfStarIcon);
    }
  
    const remainingStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
  
    for (let i = 0; i < remainingStars; i++) {
      const emptyStarIcon = document.createElement('i');
      emptyStarIcon.classList.add('far', 'fa-star', 'i-star');
      starIconsContainer.appendChild(emptyStarIcon);
    }
  });

// Function to get the value of a cookie
function getCookie(name) {
  const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
  return cookieValue ? cookieValue.pop() : '';
}

// Function to handle course registration/unregistration
function handleCourseRegistration(courseId, action, buttonElement) {
  const url = `/course_registration/${courseId}/`;
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ action: action }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle the response from the server
      if (data.success) {
        // Course registration/unregistration successful
        if (action === 'register') {
          // Update the button text and action
          buttonElement.textContent = 'Unregister';
          buttonElement.classList.remove('button');
          buttonElement.classList.add('button-alt');
          // buttonElement.removeEventListener('click', registerCourse);
          // buttonElement.addEventListener('click', () => handleCourseRegistration(courseId, 'unregister', buttonElement));
        } else {
          // Update the button text and action
          buttonElement.textContent = 'Register';
          buttonElement.classList.remove('button-alt');
          buttonElement.classList.add('button');
          // buttonElement.removeEventListener('click', unregisterCourse);
          // buttonElement.addEventListener('click', () => handleCourseRegistration(courseId, 'register', buttonElement));
        }
      } else {
        // Course registration/unregistration failed
        console.error('Operation failed:', data.error);
        // Perform any additional error handling or display error messages
      }
    })
    .catch((error) => {
      // Handle any error that occurred during the request
      console.error('Error:', error);
      alert('An error occurred during the operation.');
    });
}


// Updated click handler for registration/unregistration
function handleCourseToggle(courseId, buttonElement) {
  const isRegistered = buttonElement.classList.contains('button-alt');

  // Determine the action based on the current button state
  const action = isRegistered ? 'unregister' : 'register';

  handleCourseRegistration(courseId, action, buttonElement);
}