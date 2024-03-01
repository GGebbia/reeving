async function fetchTotals() {
    const response = await fetch('http://localhost:8000/api/totals/', {
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
        displaySummary(data);
    })
    .catch(error =>{
        console.error('There has been a problem with your fetch operation:', error);
      });
  }
  
  function displaySummary(data) {
    const tableBody = document.getElementById('revenue_source').getElementsByTagName('tbody')[0];

    data.forEach(source => {
        let row = `<tr>
            <td>${source.revenue_source}</td>
            <td>${source.total_value}</td>
            <td>${source.total_advance}</td>
            <td>${source.total_expected_fee}</td>
        </tr>`;
        tableBody.innerHTML += row;

    });

  }
  
  fetchTotals();