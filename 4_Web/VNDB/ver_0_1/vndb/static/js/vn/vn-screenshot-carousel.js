document.addEventListener('DOMContentLoaded', function() {
  // DOM Elements
  const carousel = document.querySelector('.screenshots__carousel');
  const items = carousel.querySelectorAll('.screenshots__item');
  const prevButton = carousel.querySelector('.screenshots__nav--prev');
  const nextButton = carousel.querySelector('.screenshots__nav--next');
  const thumbnailsContainer = document.querySelector('.screenshots__thumbnails');
  const thumbnails = thumbnailsContainer.querySelectorAll('.screenshots__thumbnail');
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');

  let currentIndex = 0;

  // Carousel Functions
  function showItem(index) {
    items.forEach((item, i) => item.classList.toggle('active', i === index));
    thumbnails.forEach((thumb, i) => thumb.classList.toggle('active', i === index));
    currentIndex = index;
    updateNavigation();
  }

  function nextItem(e) {
    e.preventDefault();
    do {
      currentIndex = (currentIndex + 1) % items.length;
    } while (items[currentIndex].style.display === 'none' && currentIndex !== 0);
    showItem(currentIndex);
  }

  function prevItem(e) {
    e.preventDefault();
    do {
      currentIndex = (currentIndex - 1 + items.length) % items.length;
    } while (items[currentIndex].style.display === 'none' && currentIndex !== items.length - 1);
    showItem(currentIndex);
  }

  function updateNavigation() {
    const visibleItems = Array.from(items).filter(item => item.style.display !== 'none');
    [prevButton, nextButton].forEach(button => button.style.display = visibleItems.length > 1 ? 'block' : 'none');
  }

  // Content Visibility
  function updateContentVisibility() {
    const showSexual = showSexualCheckbox.checked;
    const showViolent = showViolentCheckbox.checked;

    items.forEach((item, index) => {
      const isSexual = item.querySelector('.screenshots__img--sexual');
      const isViolent = item.querySelector('.screenshots__img--violence');
      const shouldShow = (showSexual || !isSexual) && (showViolent || !isViolent);
      item.style.display = shouldShow ? 'block' : 'none';
      thumbnails[index].parentElement.style.display = shouldShow ? 'block' : 'none';
    });

    const visibleIndex = Array.from(items).findIndex(item => item.style.display !== 'none');
    showItem(visibleIndex !== -1 ? visibleIndex : 0);
    updateNavigation();
  }

  // Event Listeners
  nextButton.addEventListener('click', nextItem);
  prevButton.addEventListener('click', prevItem);

  thumbnailsContainer.addEventListener('click', function(e) {
    e.preventDefault(); // Prevent default link behavior
    const clickedThumbnail = e.target.closest('.screenshots__thumbnail');
    if (clickedThumbnail) {
      const index = Array.from(thumbnails).indexOf(clickedThumbnail);
      if (index !== -1 && items[index].style.display !== 'none') {
        showItem(index);
      }
    }
  });

  [showSexualCheckbox, showViolentCheckbox].forEach(checkbox => 
    checkbox.addEventListener('change', updateContentVisibility)
  );

  // Keyboard navigation
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') {
      prevItem(e);
    } else if (e.key === 'ArrowRight') {
      nextItem(e);
    }
  });

  // Initialization
  updateContentVisibility();
});