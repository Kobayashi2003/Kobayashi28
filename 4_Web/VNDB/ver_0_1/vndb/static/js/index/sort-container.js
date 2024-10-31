document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const sortSelect = document.getElementById('sortSelect');
  const sortOrder = document.getElementById('sortOrder');

  // Event Listeners
  sortSelect.addEventListener('change', triggerSort);
  sortOrder.addEventListener('change', triggerSort);

  /**
   * Trigger sorting and dispatch event
   */
  function triggerSort() {
    const sortBy = sortSelect.value;
    const isDescending = sortOrder.checked;
    const event = new CustomEvent('sortChanged', {
      detail: { sortBy, sortOrder: isDescending ? 'desc' : 'asc' }
    });
    document.dispatchEvent(event);
  }

  /**
   * Custom sorting function
   * @param {HTMLElement} a - First element to compare
   * @param {HTMLElement} b - Second element to compare
   * @param {string} sortBy - Sorting criteria
   * @param {boolean} isDescending - Sort order
   * @returns {number} Comparison result
   */
  window.customSort = function(a, b, sortBy, isDescending) {
    let aValue = a.dataset[sortBy];
    let bValue = b.dataset[sortBy];

    if (!isValidValue(aValue, sortBy) && !isValidValue(bValue, sortBy)) return 0;
    if (!isValidValue(aValue, sortBy)) return 1;
    if (!isValidValue(bValue, sortBy)) return -1;

    switch (sortBy) {
      case 'id':
        aValue = parseInt(aValue.substring(1));
        bValue = parseInt(bValue.substring(1));
        break;
      case 'released':
      case 'date':
        aValue = new Date(aValue);
        bValue = new Date(bValue);
        if (isNaN(aValue.getTime())) return 1;
        if (isNaN(bValue.getTime())) return -1;
        break;
      case 'title':
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
        break;
    }

    if (aValue < bValue) return isDescending ? 1 : -1;
    if (aValue > bValue) return isDescending ? -1 : 1;
    return 0;
  };

  /**
   * Check if a value is valid for sorting
   * @param {*} value - Value to check
   * @param {string} sortBy - Sorting criteria
   * @returns {boolean} Whether the value is valid
   */
  function isValidValue(value, sortBy) {
    if (value === undefined || value === null || value === '') return false;
    
    switch (sortBy) {
      case 'id': return /^v\d+$/.test(value);
      case 'released': return /^\d{4}(-\d{2}(-\d{2})?)?$/.test(value);
      case 'date': return !isNaN(new Date(value).getTime());
      case 'title': return true;
      default: return false;
    }
  }

  // Initial sort
  triggerSort();
});