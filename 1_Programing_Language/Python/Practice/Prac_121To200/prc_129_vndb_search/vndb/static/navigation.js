document.addEventListener('DOMContentLoaded', function() {
  const nav = document.querySelector('.vn-nav')
  const navToggle = document.querySelector('.vn-nav__toggle');
  const navList = document.querySelector('.vn-nav__list');

  let lastScrollTop = 0;

  navToggle.addEventListener('click', function() {
    navList.classList.toggle('active');
  });

  // Close the menu when clicking outside
  document.addEventListener('click', function(event) {
    const isClickInsideNav = navToggle.contains(event.target) || navList.contains(event.target);
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
});