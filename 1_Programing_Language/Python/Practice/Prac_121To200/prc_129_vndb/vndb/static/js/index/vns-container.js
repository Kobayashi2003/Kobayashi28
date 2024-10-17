document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const vnsContainer = document.getElementById('vnsContainer');
  const vns = Array.from(vnsContainer.children);

  /**
   * Update content visibility based on user preferences
   */
  function updateContentVisibility() {
    const showSexual = localStorage.getItem('showSexual') === 'true';
    const showViolent = localStorage.getItem('showViolent') === 'true';

    vns.forEach(vn => {
      vn.classList.toggle('show-sexual', showSexual && vn.classList.contains('vn-sexual'));
      vn.classList.toggle('show-violent', showViolent && vn.classList.contains('vn-violent'));
    });
  }

  /**
   * Apply sorting to all VNs
   * @param {string} sortBy - Sorting criteria
   * @param {string} sortOrder - Sorting order ('asc' or 'desc')
   */
  function applySorting(sortBy, sortOrder) {
    const sortedVns = vns.sort((a, b) => window.customSort(a, b, sortBy, sortOrder === 'desc'));
    vnsContainer.innerHTML = '';
    sortedVns.forEach(vn => vnsContainer.appendChild(vn));
    document.dispatchEvent(new CustomEvent('sortingComplete'));
  }

  // Event Listeners
  window.addEventListener('storage', (event) => {
    if (event.key === 'showSexual' || event.key === 'showViolent') {
      updateContentVisibility();
    }
  });

  document.addEventListener('sortChanged', (event) => {
    const { sortBy, sortOrder } = event.detail;
    applySorting(sortBy, sortOrder);
  });

  // Initialization
  updateContentVisibility();
});