document.addEventListener('DOMContentLoaded', function() {
  const nav = document.querySelector('.vn-nav');
  const navToggle = document.querySelector('.vn-nav__toggle');
  const navList = document.querySelector('.vn-nav__list');
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');

  let lastScrollTop = 0;

  navToggle.addEventListener('click', function() {
    navList.classList.toggle('active');
  });

  // Close the menu when clicking outside
  document.addEventListener('click', function(event) {
    const isClickInsideNav = nav.contains(event.target);
    if (!isClickInsideNav && navList.classList.contains('active')) {
      navList.classList.remove('active');
    }
  });

  window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop) {
      // Scrolling down
      nav.classList.add('hidden');
      if (navList.classList.contains('active')) {
        navList.classList.remove('active');
      }
    } else {
      // Scrolling up
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