document.addEventListener('DOMContentLoaded', () => {
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');
  const mainTitle = document.getElementById('mainTitle');
  const menuToggle = document.getElementById('menuToggle');
  const headerNav = document.getElementById('headerNav');
  const searchToggle = document.getElementById('searchToggle');

  function updateContentVisibility() {
    const showSexual = showSexualCheckbox.checked;
    const showViolent = showViolentCheckbox.checked;

    document.querySelectorAll('.vn-sexual').forEach(vn => {
      vn.classList.toggle('show-sexual', showSexual);
    });

    document.querySelectorAll('.vn-violent').forEach(vn => {
      vn.classList.toggle('show-violent', showViolent);
    });
  }

  showSexualCheckbox.addEventListener('change', updateContentVisibility);
  showViolentCheckbox.addEventListener('change', updateContentVisibility);

  menuToggle.addEventListener('click', () => {
    headerNav.classList.toggle('show');
  });

  mainTitle.addEventListener('click', () => {
    if (typeof resetPagination === 'function') {
      resetPagination();
    }
  });

  searchToggle.addEventListener('click', () => {
    if (typeof openSearchModal === 'function') {
      openSearchModal();
    }
  });

  // Add event listeners for mobile menu items
  document.querySelectorAll('.mobile-menu-item').forEach(item => {
    item.addEventListener('click', (e) => {
      const action = e.currentTarget.getAttribute('aria-label').toLowerCase();
      switch(action) {
        case 'user profile':
          console.log('User profile clicked');
          // Add your user profile action here
          break;
        case 'settings':
          console.log('Settings clicked');
          // Add your settings action here
          break;
        case 'sort':
          console.log('Sort clicked');
          // Add your sort action here
          break;
      }
    });
  });

  updateContentVisibility();
});