document.addEventListener('DOMContentLoaded', function() {
    const scrapeButton = document.getElementById('scrape-button');
    const messageDiv = document.getElementById('message');
    const stocksGrid = document.getElementById('stocks-grid');
    const modal = document.getElementById('stock-modal');
    const modalBody = document.getElementById('modal-body');
    const closeButton = document.querySelector('.close-button');

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
                    card.dataset.symbol = stock.symbol;

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

    stocksGrid.addEventListener('click', function(event) {
        const card = event.target.closest('.stock-card');
        if (card) {
            const symbol = card.dataset.symbol;
            openModal(symbol);
        }
    });

    function openModal(symbol) {
        modalBody.innerHTML = '<p>Loading...</p>';
        modal.style.display = 'block';

        fetch(`/api/stock/${symbol}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    modalBody.innerHTML = `<p>${data.error}</p>`;
                    return;
                }

                const newsList = data.news.map(item => `<li><a href="${item.link}" target="_blank">${item.headline}</a></li>`).join('');
                const analysisList = Object.entries(data.analysis).map(([key, value]) => `<li><strong>${key.replace('_', ' ').toUpperCase()}:</strong> ${value}</li>`).join('');

                modalBody.innerHTML = `
                    <div class="stock-graph-large">
                        <img src="https://finviz.com/chart.ashx?t=${symbol}&ty=c&ta=1&p=d&s=l" alt="${symbol} graph">
                    </div>
                    <div>
                        <h2>Latest News</h2>
                        <ul class="stock-news">${newsList}</ul>
                        <h2>Analysis</h2>
                        <ul class="stock-analysis">${analysisList}</ul>
                    </div>
                `;
            })
            .catch(error => {
                console.error('Error fetching stock details:', error);
                modalBody.innerHTML = '<p>Error fetching stock details.</p>';
            });
    }

    closeButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    fetchStocks();
});