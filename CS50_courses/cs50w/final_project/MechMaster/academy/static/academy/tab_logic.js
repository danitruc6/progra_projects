document.addEventListener('DOMContentLoaded', function() {
    var profileTabs = document.querySelectorAll('#profileTabs a');
    var tabContents = document.querySelectorAll('.tab-pane');
  
    profileTabs.forEach(function(tab) {
      tab.addEventListener('click', function(e) {
        e.preventDefault();
        var targetTab = this.getAttribute('href');
  
        // Remove 'active' class from all tabs
        profileTabs.forEach(function(tab) {
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
  });
  