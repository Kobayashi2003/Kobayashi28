document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');
  const mainTitle = document.getElementById('mainTitle');
  const header = document.querySelector('.header');
  const menuToggle = document.getElementById('menuToggle');
  const dropdownMenu = document.getElementById('dropdownMenu');
  const configToggle = document.getElementById('configToggle');
  const configMenu = document.getElementById('configMenu');

  // Constants
  const scrollThreshold = 5;
  let lastScrollTop = 0;

  // Content Visibility Management
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

  // Header Visibility Management
  function handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (Math.abs(scrollTop - lastScrollTop) <= scrollThreshold) return;

    if (scrollTop > lastScrollTop && scrollTop > header.offsetHeight) {
      header.classList.replace('visible', 'hidden');
      dropdownMenu.classList.remove('show');
      configMenu.classList.remove('show');
    } else {
      header.classList.replace('hidden', 'visible');
    }

    lastScrollTop = scrollTop;
  }

  // Responsive Menu Management
  function handleResize() {
    if (window.innerWidth > 768) {
      dropdownMenu.classList.remove('show');
      dropdownMenu.style.display = 'flex';
    } else {
      dropdownMenu.style.display = dropdownMenu.classList.contains('show') ? 'block' : 'none';
    }
  }

  // Menu Toggle Handlers
  function toggleDropdownMenu(e) {
    e.stopPropagation();
    dropdownMenu.classList.toggle('show');
    configMenu.classList.remove('show');
    handleResize();
  }

  function toggleConfigMenu(e) {
    e.stopPropagation();
    configMenu.classList.toggle('show');
    dropdownMenu.classList.remove('show');
  }

  // Close Menus When Clicking Outside
  function closeMenusOnClickOutside(e) {
    if (!dropdownMenu.contains(e.target) && e.target !== menuToggle) {
      dropdownMenu.classList.remove('show');
    }
    if (!configMenu.contains(e.target) && e.target !== configToggle) {
      configMenu.classList.remove('show');
    }
    handleResize();
  }

  // Dropdown Item Click Handler
  function handleDropdownItemClick(e) {
    const action = e.currentTarget.getAttribute('aria-label').toLowerCase();
    switch(action) {
      case 'search':
        if (typeof openSearchModal === 'function') {
          openSearchModal();
        }
        break;
      case 'user profile':
        console.log('User profile clicked');
        // Add your user profile action here
        break;
    }
    dropdownMenu.classList.remove('show');
    handleResize();
  }

  // Event Listeners
  showSexualCheckbox.addEventListener('change', updateContentVisibility);
  showViolentCheckbox.addEventListener('change', updateContentVisibility);
  menuToggle.addEventListener('click', toggleDropdownMenu);
  configToggle.addEventListener('click', toggleConfigMenu);
  document.addEventListener('click', closeMenusOnClickOutside);
  mainTitle.addEventListener('click', () => {
    if (typeof resetPagination === 'function') {
      resetPagination();
    }
  });
  document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', handleDropdownItemClick);
  });
  window.addEventListener('scroll', handleScroll, { passive: true });
  window.addEventListener('resize', handleResize);

  // Initialization
  updateContentVisibility();
  handleResize();
});