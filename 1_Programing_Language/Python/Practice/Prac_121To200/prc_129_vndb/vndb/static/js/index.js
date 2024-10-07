document.addEventListener('DOMContentLoaded', () => {
  const vnsContainer = document.getElementById('vnsContainer');
  const showSexualCheckbox = document.getElementById('showSexual');
  const showViolentCheckbox = document.getElementById('showViolent');
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

  function updatePagination() {
    firstPageBtn.disabled = currentPage === 1;
    prevPageBtn.disabled = currentPage === 1;
    nextPageBtn.disabled = currentPage === totalPages;
    lastPageBtn.disabled = currentPage === totalPages;

    pageNumbers.innerHTML = '';

    const maxVisiblePages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    if (startPage > 1) {
      pageNumbers.innerHTML += '<span class="page-number">1</span>';
      if (startPage > 2) {
        pageNumbers.innerHTML += '<span class="page-number">...</span>';
      }
    }

    for (let i = startPage; i <= endPage; i++) {
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

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        pageNumbers.innerHTML += '<span class="page-number">...</span>';
      }
      pageNumbers.innerHTML += `<span class="page-number">${totalPages}</span>`;
    }
  }

  showSexualCheckbox.addEventListener('change', updateContentVisibility);
  showViolentCheckbox.addEventListener('change', updateContentVisibility);
  updateContentVisibility();

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

  showPage(currentPage);
});