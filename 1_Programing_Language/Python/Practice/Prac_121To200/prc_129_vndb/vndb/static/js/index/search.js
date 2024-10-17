document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const searchModal = document.getElementById('searchModal');
  const closeSearch = document.getElementById('closeSearch');
  const localSearchTab = document.getElementById('localSearchTab');
  const vndbSearchTab = document.getElementById('vndbSearchTab');
  const localSearchForm = document.getElementById('localSearchForm');
  const vndbSearchForm = document.getElementById('vndbSearchForm');
  const vndbMoreOptions = document.getElementById('vndbMoreOptions');
  const vndbMoreOptionsContent = document.getElementById('vndbMoreOptionsContent');

  // Modal Functions
  function openSearchModal() {
    searchModal.style.display = 'block';
  }

  function closeSearchModal() {
    searchModal.style.display = 'none';
  }

  // Event Listeners
  closeSearch.addEventListener('click', closeSearchModal);

  window.addEventListener('click', (event) => {
    if (event.target === searchModal) {
      closeSearchModal();
    }
  });

  // Tab Switching
  localSearchTab.addEventListener('click', () => {
    [localSearchTab, localSearchForm].forEach(el => el.classList.add('active'));
    [vndbSearchTab, vndbSearchForm].forEach(el => el.classList.remove('active'));
  });

  vndbSearchTab.addEventListener('click', () => {
    [vndbSearchTab, vndbSearchForm].forEach(el => el.classList.add('active'));
    [localSearchTab, localSearchForm].forEach(el => el.classList.remove('active'));
  });

  // VNDB More Options Toggle
  vndbMoreOptions.addEventListener('click', () => {
    vndbMoreOptionsContent.classList.toggle('active');
    vndbMoreOptions.textContent = vndbMoreOptionsContent.classList.contains('active') ? 'Less Options' : 'More Options';
  });

  // Keyboard Shortcuts
  document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 'f') {
      event.preventDefault();
      openSearchModal();
    }
    
    if (event.key === 'Escape') {
      closeSearchModal();
    }
  });

  // Form Submission Handling
  document.querySelectorAll('.search-form-local, .search-form-vndb').forEach(form => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const formData = new FormData(form);
      const cleanedFormData = new FormData();

      for (let [key, value] of formData.entries()) {
        if (value.trim() !== '') {
          cleanedFormData.append(key, value.trim());
        }
      }

      const queryString = new URLSearchParams(cleanedFormData).toString();
      window.location.href = `${form.action}?${queryString}`;
    });
  });

  // Expose openSearchModal to global scope
  window.openSearchModal = openSearchModal;
});