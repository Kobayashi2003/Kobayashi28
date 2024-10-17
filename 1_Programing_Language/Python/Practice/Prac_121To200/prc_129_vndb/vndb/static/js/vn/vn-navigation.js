document.addEventListener('DOMContentLoaded', function() {
  // DOM Elements
  const nav = document.querySelector('.vn-nav');
  const navToggle = document.querySelector('.vn-nav__toggle');
  const navMenu = document.querySelector('.vn-nav__menu');
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');
  const actionButton = document.querySelector('.vn-nav__action-button');
  const actionStatus = document.getElementById('actionStatus');

  let lastScrollTop = 0;
  let isMenuOpen = false;

  // Navigation Functions
  function toggleMenu(e) {
    e.stopPropagation();
    isMenuOpen = !isMenuOpen;
    navMenu.classList.toggle('active');
    navToggle.setAttribute('aria-expanded', isMenuOpen);
  }

  function closeMenuOutside(event) {
    if (!nav.contains(event.target) && isMenuOpen) {
      isMenuOpen = false;
      navMenu.classList.remove('active');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  }

  function handleScroll() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    if (scrollTop > lastScrollTop && !isMenuOpen) {
      nav.classList.add('hidden');
    } else {
      nav.classList.remove('hidden');
    }
    lastScrollTop = scrollTop;
  }

  // Content Visibility
  function updateContentVisibility() {
    const showSexual = showSexualCheckbox.checked;
    const showViolent = showViolentCheckbox.checked;

    document.querySelectorAll('.cover__img--sexual, .character__img--sexual').forEach(el => {
      el.style.display = showSexual ? 'block' : 'none';
    });

    document.querySelectorAll('.cover__img--violence, .character__img--violence').forEach(el => {
      el.style.display = showViolent ? 'block' : 'none';
    });

    document.dispatchEvent(new Event('contentVisibilityChanged'));
  }

  // Download/Delete Functionality
  function handleActionButtonClick() {
    const vnId = this.getAttribute('data-vn-id');
    const isDelete = this.classList.contains('vn-nav__action-button--delete');
    const url = isDelete ? `/delete/${vnId}` : `/download/${vnId}`;
    const actionText = isDelete ? 'Deleting' : 'Downloading';

    actionButton.disabled = true;
    actionStatus.textContent = `${actionText}...`;
    actionStatus.className = 'vn-nav__action-status';

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        actionStatus.textContent = `${isDelete ? 'Deleted' : 'Downloaded'} successfully!`;
        actionStatus.className = 'vn-nav__action-status vn-nav__action-status--success';
        actionButton.textContent = isDelete ? 'Download VN' : 'Delete VN';
        actionButton.classList.toggle('vn-nav__action-button--delete');
        actionButton.classList.toggle('vn-nav__action-button--download');

        setTimeout(() => {
          actionStatus.textContent = '';
          actionStatus.className = 'vn-nav__action-status';
        }, 5000);
      } else {
        throw new Error(data.message || `${actionText} failed`);
      }
    })
    .catch(error => {
      actionStatus.textContent = `${actionText} failed: ${error.message}`;
      actionStatus.className = 'vn-nav__action-status vn-nav__action-status--error';
    })
    .finally(() => {
      actionButton.disabled = false;
    });
  }

  // Event Listeners
  navToggle.addEventListener('click', toggleMenu);
  document.addEventListener('click', closeMenuOutside);
  window.addEventListener('scroll', handleScroll);
  [showSexualCheckbox, showViolentCheckbox].forEach(checkbox => 
    checkbox.addEventListener('change', updateContentVisibility)
  );
  if (actionButton) {
    actionButton.addEventListener('click', handleActionButtonClick);
  }

  // Initialization
  updateContentVisibility();
});