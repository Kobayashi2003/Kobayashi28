document.addEventListener('DOMContentLoaded', () => {
  const vnsContainer = document.getElementById('vnsContainer');
  const vns = Array.from(vnsContainer.children);

  // Function to show/hide sexual and violent content
  function updateContentVisibility() {
    const showSexual = localStorage.getItem('showSexual') === 'true';
    const showViolent = localStorage.getItem('showViolent') === 'true';

    vns.forEach(vn => {
      if (vn.classList.contains('vn-sexual')) {
        vn.classList.toggle('show-sexual', showSexual);
      }
      if (vn.classList.contains('vn-violent')) {
        vn.classList.toggle('show-violent', showViolent);
      }
    });
  }

  // Initial update of content visibility
  updateContentVisibility();

  // Listen for changes in content visibility settings
  window.addEventListener('storage', (event) => {
    if (event.key === 'showSexual' || event.key === 'showViolent') {
      updateContentVisibility();
    }
  });

  // Function to apply sorting
  function applySorting(sortBy, sortOrder) {
    const sortedVns = vns.sort((a, b) => {
      const aValue = a.querySelector('h2').textContent;
      const bValue = b.querySelector('h2').textContent;
      return sortOrder === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
    });

    vnsContainer.innerHTML = '';
    sortedVns.forEach(vn => vnsContainer.appendChild(vn));
  }

  // Listen for custom event from sort-container.js
  document.addEventListener('sortChanged', (event) => {
    const { sortBy, sortOrder } = event.detail;
    applySorting(sortBy, sortOrder);
  });

  // Function to update displayed VNs based on pagination
  function updateDisplayedVNs(startIndex, endIndex) {
    vns.forEach((vn, index) => {
      vn.style.display = (index >= startIndex && index < endIndex) ? 'block' : 'none';
    });
  }

  // Listen for custom event from pagination.js
  document.addEventListener('pageChanged', (event) => {
    const { startIndex, endIndex } = event.detail;
    updateDisplayedVNs(startIndex, endIndex);
  });
});