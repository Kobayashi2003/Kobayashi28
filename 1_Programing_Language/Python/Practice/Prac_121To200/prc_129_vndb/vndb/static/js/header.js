document.addEventListener('DOMContentLoaded', () => {
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');
  const mainTitle = document.getElementById('mainTitle');
  const header = document.querySelector('.header');
  const menuToggle = document.getElementById('menuToggle');
  const dropdownMenu = document.getElementById('dropdownMenu');
  const configToggle = document.getElementById('configToggle');
  const configMenu = document.getElementById('configMenu');

  let lastScrollTop = 0;
  const scrollThreshold = 5;

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

  function handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (Math.abs(scrollTop - lastScrollTop) <= scrollThreshold) return;

    if (scrollTop > lastScrollTop && scrollTop > header.offsetHeight) {
      header.classList.remove('visible');
      header.classList.add('hidden');
      dropdownMenu.classList.remove('show');
      configMenu.classList.remove('show');
    } else {
      header.classList.remove('hidden');
      header.classList.add('visible');
    }

    lastScrollTop = scrollTop;
  }

  function handleResize() {
    if (window.innerWidth > 768) {
      dropdownMenu.classList.remove('show');
      dropdownMenu.style.display = 'flex';
    } else {
      dropdownMenu.style.display = dropdownMenu.classList.contains('show') ? 'block' : 'none';
    }
  }

  showSexualCheckbox.addEventListener('change', updateContentVisibility);
  showViolentCheckbox.addEventListener('change', updateContentVisibility);

  menuToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdownMenu.classList.toggle('show');
    configMenu.classList.remove('show');
    handleResize();
  });

  configToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    configMenu.classList.toggle('show');
    dropdownMenu.classList.remove('show');
  });

  document.addEventListener('click', (e) => {
    if (!dropdownMenu.contains(e.target) && e.target !== menuToggle) {
      dropdownMenu.classList.remove('show');
    }
    if (!configMenu.contains(e.target) && e.target !== configToggle) {
      configMenu.classList.remove('show');
    }
    handleResize();
  });

  mainTitle.addEventListener('click', () => {
    if (typeof resetPagination === 'function') {
      resetPagination();
    }
  });

  document.querySelectorAll('.dropdown-item').forEach(item => {
    item.addEventListener('click', (e) => {
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
    });
  });

  window.addEventListener('scroll', handleScroll, { passive: true });
  window.addEventListener('resize', handleResize);

  updateContentVisibility();
  handleResize();
});