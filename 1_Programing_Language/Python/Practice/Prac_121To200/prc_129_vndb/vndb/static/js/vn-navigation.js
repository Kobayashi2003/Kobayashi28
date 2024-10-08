document.addEventListener('DOMContentLoaded', function() {
  const nav = document.querySelector('.vn-nav');
  const navToggle = document.querySelector('.vn-nav__toggle');
  const navMenu = document.querySelector('.vn-nav__menu');
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');

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
});