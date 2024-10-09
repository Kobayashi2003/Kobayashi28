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

  // Add event listeners for form submissions
  localSearchForm.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    // Handle local search submission
    console.log('Local search submitted');
    // Add your search logic here
  });

  vndbSearchForm.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    // Handle VNDB search submission
    console.log('VNDB search submitted');
    // Add your search logic here
  });

  // Expose the openSearchModal function globally
  window.openSearchModal = openSearchModal;
});