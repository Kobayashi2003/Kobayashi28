document.addEventListener('DOMContentLoaded', function() {
  const nav = document.querySelector('.vn-nav');
  const navToggle = document.querySelector('.vn-nav__toggle');
  const navMenu = document.querySelector('.vn-nav__menu');
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');
  const actionButton = document.querySelector('.vn-nav__action-button');
  const actionStatus = document.getElementById('actionStatus');

  let lastScrollTop = 0;
  let isMenuOpen = false;

  navToggle.addEventListener('click', function(e) {
    e.stopPropagation();
    isMenuOpen = !isMenuOpen;
    navMenu.classList.toggle('active');
    navToggle.setAttribute('aria-expanded', isMenuOpen);
  });

  // Close the menu when clicking outside
  document.addEventListener('click', function(event) {
    const isClickInsideNav = nav.contains(event.target);
    if (!isClickInsideNav && isMenuOpen) {
      isMenuOpen = false;
      navMenu.classList.remove('active');
      navToggle.setAttribute('aria-expanded', 'false');
    }
  });

  window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop && !isMenuOpen) {
      // Scrolling down and menu is closed
      nav.classList.add('hidden');
    } else {
      // Scrolling up or menu is open
      nav.classList.remove('hidden');
    }

    lastScrollTop = scrollTop;
  });

  function updateContentVisibility() {
    const showSexual = showSexualCheckbox.checked;
    const showViolent = showViolentCheckbox.checked;

    document.querySelectorAll('.cover__img--sexual, .character__img--sexual').forEach(el => {
      el.style.display = showSexual ? 'block' : 'none';
    });

    document.querySelectorAll('.cover__img--violence, .character__img--violence').forEach(el => {
      el.style.display = showViolent ? 'block' : 'none';
    });

    // Trigger the screenshot carousel update
    const event = new Event('contentVisibilityChanged');
    document.dispatchEvent(event);
  }

  showSexualCheckbox.addEventListener('change', updateContentVisibility);
  showViolentCheckbox.addEventListener('change', updateContentVisibility);

  // Initial update
  updateContentVisibility();

  // Download/Delete functionality
  if (actionButton) {
    actionButton.addEventListener('click', function() {
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
          // Toggle button state
          actionButton.textContent = isDelete ? 'Download VN' : 'Delete VN';
          actionButton.classList.toggle('vn-nav__action-button--delete');
          actionButton.classList.toggle('vn-nav__action-button--download');

          // Set a timeout to clear the success message after 5 seconds
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
    });
  }
});