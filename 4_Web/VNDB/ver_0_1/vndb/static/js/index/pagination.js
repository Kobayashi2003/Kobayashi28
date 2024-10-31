document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const pagination = document.querySelector('.pagination');
  const firstPageBtn = document.getElementById('firstPage');
  const prevPageBtn = document.getElementById('prevPage');
  const nextPageBtn = document.getElementById('nextPage');
  const lastPageBtn = document.getElementById('lastPage');
  const pageNumbers = document.getElementById('pageNumbers');
  const vnsContainer = document.getElementById('vnsContainer');

  // Pagination Configuration
  const itemsPerPage = 30;
  let currentPage = 1;
  let vns = Array.from(vnsContainer.children);
  let totalPages = Math.ceil(vns.length / itemsPerPage);

  /**
   * Update displayed VNs based on current page
   */
  function updateDisplayedVNs() {
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    vns.forEach((vn, index) => {
      vn.style.display = (index >= startIndex && index < endIndex) ? 'block' : 'none';
    });

    lazyLoadImages(startIndex, endIndex);
  }

  /**
   * Show specified page
   * @param {number} page - Page number to show
   */
  function showPage(page) {
    currentPage = page;
    updateDisplayedVNs();
    updatePagination();
    updateURL();
    window.scrollTo(0, 0);
  }

  /**
   * Update URL with current page
   */
  function updateURL() {
    const url = new URL(window.location);
    url.searchParams.set('page', currentPage);
    window.history.pushState({}, '', url);
  }

  /**
   * Update pagination UI
   */
  function updatePagination() {
    updateButtonStates();
    renderPageNumbers();
  }

  /**
   * Update pagination button states
   */
  function updateButtonStates() {
    firstPageBtn.disabled = currentPage === 1;
    prevPageBtn.disabled = currentPage === 1;
    nextPageBtn.disabled = currentPage === totalPages;
    lastPageBtn.disabled = currentPage === totalPages;
  }

  /**
   * Render page numbers
   */
  function renderPageNumbers() {
    pageNumbers.innerHTML = '';
    const maxVisiblePages = getMaxVisiblePages();
    const { startPage, endPage } = calculatePageRange(maxVisiblePages);

    if (startPage > 1) {
      addPageNumber(1);
      if (startPage > 2) addEllipsis();
    }

    for (let i = startPage; i <= endPage; i++) {
      addPageNumber(i);
    }

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) addEllipsis();
      addPageNumber(totalPages);
    }
  }

  /**
   * Calculate page range for pagination
   * @param {number} maxVisiblePages - Maximum number of visible page numbers
   * @returns {Object} Start and end page numbers
   */
  function calculatePageRange(maxVisiblePages) {
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    return { startPage, endPage };
  }

  /**
   * Add page number to pagination
   * @param {number} pageNum - Page number to add
   */
  function addPageNumber(pageNum) {
    const pageNumber = document.createElement('span');
    pageNumber.classList.add('page-number');
    pageNumber.textContent = pageNum;
    if (pageNum === currentPage) {
      pageNumber.classList.add('active');
    }
    pageNumber.addEventListener('click', () => showPage(pageNum));
    pageNumbers.appendChild(pageNumber);
  }

  /**
   * Add ellipsis to pagination
   */
  function addEllipsis() {
    pageNumbers.appendChild(document.createTextNode('...'));
  }

  /**
   * Get maximum number of visible pages based on screen width
   * @returns {number} Maximum number of visible pages
   */
  function getMaxVisiblePages() {
    if (window.innerWidth <= 480) return 3;
    if (window.innerWidth <= 768) return 5;
    return 7;
  }

  /**
   * Lazy load images for current page
   * @param {number} startIndex - Start index of current page
   * @param {number} endIndex - End index of current page
   */
  function lazyLoadImages(startIndex, endIndex) {
    vns.slice(startIndex, endIndex).forEach(vn => {
      const img = vn.querySelector('img');
      if (img && img.dataset.src) {
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
      }
      img.classList.remove('lazy');
      img.classList.add('loaded');
    });
  }

  /**
   * Initialize pagination
   */
  function initialize() {
    const urlParams = new URLSearchParams(window.location.search);
    const pageParam = urlParams.get('page');
    if (pageParam) {
      const parsedPage = parseInt(pageParam, 10);
      if (!isNaN(parsedPage) && parsedPage > 0 && parsedPage <= totalPages) {
        currentPage = parsedPage;
      }
    }
    showPage(currentPage);
  }

  /**
   * Update VNs after sorting
   */
  function updateVNsAfterSort() {
    vns = Array.from(vnsContainer.children);
    totalPages = Math.ceil(vns.length / itemsPerPage);
    currentPage = 1;
    showPage(1);
  }

  // Event Listeners
  firstPageBtn.addEventListener('click', () => showPage(1));
  prevPageBtn.addEventListener('click', () => showPage(Math.max(1, currentPage - 1)));
  nextPageBtn.addEventListener('click', () => showPage(Math.min(totalPages, currentPage + 1)));
  lastPageBtn.addEventListener('click', () => showPage(totalPages));
  window.addEventListener('resize', updatePagination);

  document.addEventListener('sortingComplete', updateVNsAfterSort);

  // Initialization
  initialize();
});