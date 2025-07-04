document.addEventListener('DOMContentLoaded', function() {
    const scrapeButton = document.getElementById('scrape-button');
    const messageDiv = document.getElementById('message');
    const stocksGrid = document.getElementById('stocks-grid');

    function fetchStocks() {
        fetch('/api/stocks')
            .then(response => response.json())
            .then(data => {
                stocksGrid.innerHTML = ''; // Clear existing cards
                if (data.length === 0) {
                    stocksGrid.innerHTML = '<p>No stock data available. Scrape to get data.</p>';
                    return;
                }
                data.forEach(stock => {
                    const card = document.createElement('div');
                    card.className = 'stock-card';

                    card.innerHTML = `
                        <div class="stock-header">
                            <img src="${stock.logo_url}" alt="${stock.name} logo" class="stock-logo">
                            <div class="stock-info">
                                <h2>${stock.symbol}</h2>
                                <p>${stock.name}</p>
                            </div>
                        </div>
                        <div class="stock-price">$${stock.price}</div>
                        <div class="stock-graph">
                            <img src="${stock.graph_url}" alt="${stock.name} graph">
                        </div>
                    `;
                    stocksGrid.appendChild(card);
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
        messageDiv.style.color = '#bf9fee';
        fetch('/api/scrape', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            messageDiv.textContent = data.message;
            messageDiv.style.color = '#50fa7b';
            setTimeout(fetchStocks, 5000); 
        })
        .catch(error => {
            console.error('Error triggering scrape:', error);
            messageDiv.textContent = 'Error triggering scrape.';
            messageDiv.style.color = '#ff5555';
        });
    });

    fetchStocks();
});