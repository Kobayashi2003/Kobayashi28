document.addEventListener('DOMContentLoaded', () => {
  const searchModal = document.getElementById('searchModal');
  const closeSearch = document.getElementById('closeSearch');
  const localSearchTab = document.getElementById('localSearchTab');
  const vndbSearchTab = document.getElementById('vndbSearchTab');
  const localSearchForm = document.getElementById('localSearchForm');
  const vndbSearchForm = document.getElementById('vndbSearchForm');

  // Function to open the search modal
  function openSearchModal() {
    searchModal.style.display = 'block';
  }

  // Function to close the search modal
  function closeSearchModal() {
    searchModal.style.display = 'none';
  }

  // Event listener for closing the modal
  closeSearch.addEventListener('click', closeSearchModal);

  // Event listener for clicking outside the modal
  window.addEventListener('click', (event) => {
    if (event.target === searchModal) {
      closeSearchModal();
    }
  });

  // Tab switching functionality
  localSearchTab.addEventListener('click', () => {
    localSearchTab.classList.add('active');
    vndbSearchTab.classList.remove('active');
    localSearchForm.classList.add('active');
    vndbSearchForm.classList.remove('active');
  });

  vndbSearchTab.addEventListener('click', () => {
    vndbSearchTab.classList.add('active');
    localSearchTab.classList.remove('active');
    vndbSearchForm.classList.add('active');
    localSearchForm.classList.remove('active');
  });

  // Event listener for keydown events
  document.addEventListener('keydown', (event) => {
    // Check if Ctrl+F is pressed
    if (event.ctrlKey && event.key === 'f') {
      event.preventDefault(); // Prevent the default browser search
      openSearchModal();
    }
    
    // Check if Esc is pressed
    if (event.key === 'Escape') {
      closeSearchModal();
    }
  });

  // Expose the openSearchModal function globally
  window.openSearchModal = openSearchModal;
});