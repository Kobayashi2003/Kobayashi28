document.addEventListener('DOMContentLoaded', () => {
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');
  const mainTitle = document.getElementById('mainTitle');
  const menuToggle = document.getElementById('menuToggle');
  const headerNav = document.getElementById('headerNav');

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

  updateContentVisibility();
});