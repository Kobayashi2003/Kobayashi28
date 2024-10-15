document.addEventListener('DOMContentLoaded', () => {
  const pagination = document.querySelector('.pagination');
  const firstPageBtn = document.getElementById('firstPage');
  const prevPageBtn = document.getElementById('prevPage');
  const nextPageBtn = document.getElementById('nextPage');
  const lastPageBtn = document.getElementById('lastPage');
  const pageNumbers = document.getElementById('pageNumbers');

  const vns = Array.from(vnsContainer.children);

  const itemsPerPage = 30;
  let currentPage = 1;
  let totalItems = vns.length; // This should be dynamically set based on your data

  const totalPages = Math.ceil(totalItems / itemsPerPage);

  function showPage(page) {
    currentPage = page;
    // Implement your logic to show items for the current page
    updatePagination();
  }

  function updatePagination() {
    firstPageBtn.disabled = currentPage === 1;
    prevPageBtn.disabled = currentPage === 1;
    nextPageBtn.disabled = currentPage === totalPages;
    lastPageBtn.disabled = currentPage === totalPages;

    pageNumbers.innerHTML = '';

    const maxVisiblePages = getMaxVisiblePages();
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    if (startPage > 1) {
      addPageNumber(1);
      if (startPage > 2) {
        pageNumbers.appendChild(document.createTextNode('...'));
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      addPageNumber(i);
    }

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        pageNumbers.appendChild(document.createTextNode('...'));
      }
      addPageNumber(totalPages);
    }
  }

  function addPageNumber(i) {
    const pageNumber = document.createElement('span');
    pageNumber.classList.add('page-number');
    pageNumber.textContent = i;
    if (i === currentPage) {
      pageNumber.classList.add('active');
    }
    pageNumber.addEventListener('click', () => showPage(i));
    pageNumbers.appendChild(pageNumber);
  }

  function getMaxVisiblePages() {
    if (window.innerWidth <= 480) return 3;
    if (window.innerWidth <= 768) return 5;
    return 7;
  }

  firstPageBtn.addEventListener('click', () => showPage(1));
  prevPageBtn.addEventListener('click', () => showPage(Math.max(1, currentPage - 1)));
  nextPageBtn.addEventListener('click', () => showPage(Math.min(totalPages, currentPage + 1)));
  lastPageBtn.addEventListener('click', () => showPage(totalPages));

  window.addEventListener('resize', updatePagination);

  // Initial setup
  updatePagination();
});