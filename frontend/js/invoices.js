async function fetchInvoices(pageNumber = 1) {
    const limit = 20;
    const response = await fetch(`http://localhost:8000/api/invoices/?page=${pageNumber}&limit=${limit}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then((data) => {
        displayInvoices(data['results']);
        updatePagination(data, pageNumber);;
    })
    .catch(error =>{
        console.error('There has been a problem with your fetch operation:', error);
      });
  }
  
  function displayInvoices(invoices) {
    const tableBody = document.getElementById('invoices').getElementsByTagName('tbody')[0];
    tableBody.innerHTML = '';
    
    invoices.forEach(invoice => {
        let row = `<tr>
            <td>${invoice.invoice_number}</td>
            <td>${invoice.date}</td>
            <td>${invoice.customer}</td>
            <td>${invoice.revenue_source}</td>
            <td>${invoice.value}</td>
            <td>${invoice.haircut_percent}%</td>
            <td>${invoice.daily_fee_percent}%</td>
            <td>${invoice.currency}</td>
            <td>${invoice.expected_payment_duration} days</td>
        </tr>`;
        tableBody.innerHTML += row;

    });
  }
  
// Function to update pagination links
function updatePagination(data, pageNumber) {
    const paginationContainer = document.querySelector('.pagination');
    paginationContainer.innerHTML = ''; // Clear existing pagination

    const totalPages = Math.ceil(data.count / data.results.length);

    // Calculate the start and end page numbers to display
    let startPage = Math.max(1, pageNumber - 2);
    let endPage = Math.min(totalPages, pageNumber + 2);

    // Adjust startPage and endPage if they fall out of range
    if (endPage - startPage < 4) {
        if (startPage === 1) {
            endPage = Math.min(totalPages, startPage + 4);
        } else {
            startPage = Math.max(1, endPage - 4);
        }
    }

    // Add "Previous" link if there is a previous page
    if (data.previous) {
        const previousLi = document.createElement('li');
        previousLi.classList.add('page-item');
        previousLi.innerHTML = `<a class="page-link" href="#" onclick="fetchInvoices(${pageNumber - 1})">Previous</a>`;
        paginationContainer.appendChild(previousLi);
    }

    // Add page links
    for (let i = startPage; i <= endPage; i++) {
        const pageLi = document.createElement('li');
        pageLi.classList.add('page-item');
        if (i === pageNumber) {
            pageLi.classList.add('active');
            pageLi.setAttribute('aria-current', 'page');
        }
        pageLi.innerHTML = `<a class="page-link" href="#" onclick="fetchInvoices(${i})">${i}</a>`;
        paginationContainer.appendChild(pageLi);
    }

    // Add "Next" link if there is a next page
    if (data.next) {
        const nextLi = document.createElement('li');
        nextLi.classList.add('page-item');
        nextLi.innerHTML = `<a class="page-link" href="#" onclick="fetchInvoices(${pageNumber + 1})">Next</a>`;
        paginationContainer.appendChild(nextLi);
    }
}
