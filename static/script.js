document.addEventListener('DOMContentLoaded', function() {
    const scrapeButton = document.getElementById('scrape-button');
    const messageDiv = document.getElementById('message');
    const stocksTableBody = document.querySelector('#stocks-table tbody');

    function fetchStocks() {
        fetch('/api/stocks')
            .then(response => response.json())
            .then(data => {
                stocksTableBody.innerHTML = ''; // Clear existing rows
                if (data.length === 0) {
                    stocksTableBody.innerHTML = '<tr><td colspan="4">No stock data available. Scrape to get data.</td></tr>';
                    return;
                }
                data.forEach(stock => {
                    const row = stocksTableBody.insertRow();
                    row.insertCell().textContent = stock.symbol;
                    row.insertCell().textContent = stock.name;
                    row.insertCell().textContent = stock.price;
                    row.insertCell().textContent = stock.scraped_at;
                });
            })
            .catch(error => {
                console.error('Error fetching stocks:', error);
                messageDiv.textContent = 'Error fetching stock data.';
                messageDiv.style.color = 'red';
            });
    }

    scrapeButton.addEventListener('click', function() {
        messageDiv.textContent = 'Scraping in progress...';
        messageDiv.style.color = 'orange';
        fetch('/api/scrape', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            messageDiv.textContent = data.message;
            messageDiv.style.color = 'green';
            // Optionally, refresh stocks after a delay to allow scraping to complete
            setTimeout(fetchStocks, 5000); 
        })
        .catch(error => {
            console.error('Error triggering scrape:', error);
            messageDiv.textContent = 'Error triggering scrape.';
            messageDiv.style.color = 'red';
        });
    });

    // Initial fetch when the page loads
    fetchStocks();
});
