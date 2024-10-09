document.addEventListener('DOMContentLoaded', () => {
  const vnsContainer = document.getElementById('vnsContainer');
  const pagination = document.getElementById('pagination');
  const firstPageBtn = document.getElementById('firstPage');
  const prevPageBtn = document.getElementById('prevPage');
  const nextPageBtn = document.getElementById('nextPage');
  const lastPageBtn = document.getElementById('lastPage');
  const pageNumbers = document.getElementById('pageNumbers');

  const itemsPerPage = 30; // 5 columns * 6 rows
  let currentPage = 1;

  const vns = Array.from(vnsContainer.children);
  const totalPages = Math.ceil(vns.length / itemsPerPage);

  function showPage(page) {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    vns.forEach((vn, index) => {
      if (index >= startIndex && index < endIndex) {
        vn.style.display = 'block';
      } else {
        vn.style.display = 'none';
      }
    });

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

    function addPageNumber(i) {
      const pageNumber = document.createElement('span');
      pageNumber.classList.add('page-number');
      pageNumber.textContent = i;
      if (i === currentPage) {
        pageNumber.classList.add('active');
      }
      pageNumber.addEventListener('click', () => {
        currentPage = i;
        showPage(currentPage);
      });
      pageNumbers.appendChild(pageNumber);
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

  function getMaxVisiblePages() {
    if (window.innerWidth <= 480) {
      return 3;
    } else if (window.innerWidth <= 768) {
      return 5;
    } else {
      return 7;
    }
  }

  firstPageBtn.addEventListener('click', () => {
    currentPage = 1;
    showPage(currentPage);
  });

  prevPageBtn.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      showPage(currentPage);
    }
  });

  nextPageBtn.addEventListener('click', () => {
    if (currentPage < totalPages) {
      currentPage++;
      showPage(currentPage);
    }
  });

  lastPageBtn.addEventListener('click', () => {
    currentPage = totalPages;
    showPage(currentPage);
  });

  window.addEventListener('resize', () => {
    showPage(currentPage);
  });

  // Function to reset pagination
  window.resetPagination = () => {
    currentPage = 1;
    showPage(currentPage);
  };

  showPage(currentPage);
});