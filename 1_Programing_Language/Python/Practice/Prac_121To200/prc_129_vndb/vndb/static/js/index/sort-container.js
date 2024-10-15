document.addEventListener('DOMContentLoaded', () => {
  const sortSelect = document.getElementById('sortSelect');
  const sortOrder = document.getElementById('sortOrder');

  sortSelect.addEventListener('change', () => {
    // Trigger sort action
    triggerSort();
  });

  sortOrder.addEventListener('change', () => {
    // Trigger sort action
    triggerSort();
  });

  function triggerSort() {
    // Implement your sorting logic here
    console.log('Sorting:', sortSelect.value, 'Order:', sortOrder.checked ? 'DESC' : 'ASC');
    // You might want to make an AJAX call here to get sorted data
    // or submit a form to reload the page with sorted results
  }
});