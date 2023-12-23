document.addEventListener('DOMContentLoaded', function () {
    // Get the "Edit" button element
    var editButton = document.getElementById('editProfileButton');

    // Get the modal element
    var modal = document.getElementById('editProfileModal');

    // Open the modal when the "Edit" button is clicked
    editButton.addEventListener('click', function () {
        modal.classList.add('show'); // Add the "show" class to the modal
        modal.style.display = 'block'; // Set the display style to "block"
    });

    // Close the modal when the close button is clicked
    var closeButton = modal.querySelector('.close');
    closeButton.addEventListener('click', function () {
        modal.classList.remove('show'); // Remove the "show" class from the modal
        modal.style.display = 'none'; // Set the display style to "none"
    });
});