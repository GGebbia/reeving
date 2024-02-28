function fetchInvoices() {
    try {
      const response = fetch('http://localhost:8000/api/invoices/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = response.json();
      displayInvoices(data);
    } catch (error) {
      console.error('There has been a problem with your fetch operation:', error);
    }
  }
  
  function displayInvoices(invoices) {
    const tableBody = document.getElementById('invoices').getElementsByTagName('tbody')[0];
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
  
  fetchInvoices();