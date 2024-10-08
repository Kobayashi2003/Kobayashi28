document.addEventListener('DOMContentLoaded', function() {
  const carousel = document.querySelector('.screenshots__carousel');
  const items = carousel.querySelectorAll('.screenshots__item');
  const prevButton = carousel.querySelector('.screenshots__nav--prev');
  const nextButton = carousel.querySelector('.screenshots__nav--next');
  const thumbnailsContainer = document.querySelector('.screenshots__thumbnails');
  const thumbnails = thumbnailsContainer.querySelectorAll('.screenshots__thumbnail');
  let currentIndex = 0;

  function showItem(index) {
    items.forEach((item, i) => {
      item.classList.toggle('active', i === index);
    });
    thumbnails.forEach((thumb, i) => {
      thumb.classList.toggle('active', i === index);
    });
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
    let visibleItems = Array.from(items).filter(item => item.style.display !== 'none');
    prevButton.style.display = visibleItems.length > 1 ? 'block' : 'none';
    nextButton.style.display = visibleItems.length > 1 ? 'block' : 'none';
  }

  nextButton.addEventListener('click', nextItem);
  prevButton.addEventListener('click', prevItem);

  thumbnailsContainer.addEventListener('click', function(e) {
    e.preventDefault();
    const clickedThumbnail = e.target.closest('.screenshots__thumbnail');
    if (clickedThumbnail) {
      const index = Array.from(thumbnails).indexOf(clickedThumbnail);
      if (index !== -1 && items[index].style.display !== 'none') {
        showItem(index);
      }
    }
  });

  // Show the first visible item initially
  let initialIndex = Array.from(items).findIndex(item => item.style.display !== 'none');
  if (initialIndex === -1) initialIndex = 0;
  showItem(initialIndex);

  // Update content visibility based on checkboxes
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');

  function updateContentVisibility() {
    const showSexual = showSexualCheckbox.checked;
    const showViolent = showViolentCheckbox.checked;

    items.forEach((item, index) => {
      const isSexual = item.querySelector('.screenshots__img--sexual');
      const isViolent = item.querySelector('.screenshots__img--violence');
      const shouldShow = (showSexual || !isSexual) && (showViolent || !isViolent);
      item.style.display = shouldShow ? 'block' : 'none';
      thumbnails[index].style.display = shouldShow ? 'block' : 'none';
    });

    let visibleIndex = Array.from(items).findIndex(item => item.style.display !== 'none');
    if (visibleIndex === -1) visibleIndex = 0;
    showItem(visibleIndex);
    updateNavigation();
  }

  showSexualCheckbox.addEventListener('change', updateContentVisibility);
  showViolentCheckbox.addEventListener('change', updateContentVisibility);

  // Initial update
  updateContentVisibility();
});