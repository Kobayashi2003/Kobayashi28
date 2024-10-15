document.addEventListener('DOMContentLoaded', () => {
  const searchModal = document.getElementById('searchModal');
  const closeSearch = document.getElementById('closeSearch');
  const localSearchTab = document.getElementById('localSearchTab');
  const vndbSearchTab = document.getElementById('vndbSearchTab');
  const localSearchForm = document.getElementById('localSearchForm');
  const vndbSearchForm = document.getElementById('vndbSearchForm');
  const vndbMoreOptions = document.getElementById('vndbMoreOptions');
  const vndbMoreOptionsContent = document.getElementById('vndbMoreOptionsContent');

  function openSearchModal() {
    searchModal.style.display = 'block';
  }

  function closeSearchModal() {
    searchModal.style.display = 'none';
  }

  closeSearch.addEventListener('click', closeSearchModal);

  window.addEventListener('click', (event) => {
    if (event.target === searchModal) {
      closeSearchModal();
    }
  });

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

  vndbMoreOptions.addEventListener('click', () => {
    vndbMoreOptionsContent.classList.toggle('active');
    vndbMoreOptions.textContent = vndbMoreOptionsContent.classList.contains('active') ? 'Less Options' : 'More Options';
  });

  document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === 'f') {
      event.preventDefault();
      openSearchModal();
    }
    
    if (event.key === 'Escape') {
      closeSearchModal();
    }
  });

  // Prevent submission of empty form fields
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

  window.openSearchModal = openSearchModal;
});