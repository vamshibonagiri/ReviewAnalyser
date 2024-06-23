document.getElementById('review-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const reviewText = document.getElementById('review-text').value;
    toggleLoading(true);

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ review: reviewText })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error); });
        }
        return response.json();
    })
    .then(data => {
        let resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `
            <h2>Sentiment Analysis</h2>
            <p>Sentiment: ${data.sentiment}</p>
            <p>Scores: ${JSON.stringify(data.scores)}</p>
            <h2>Part-of-Speech Tagging</h2>
            <p>${data.pos_tags.map(tag => `${tag[0]} (${tag[1]})`).join(', ')}</p>
        `;
        toggleLoading(false);
    })
    .catch(error => {
        let resultDiv = document.getElementById('result');
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        toggleLoading(false);
    });
});

document.getElementById('url-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const reviewUrl = document.getElementById('review-url').value;
    toggleLoading(true);

    fetch('/fetch_and_analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: reviewUrl })
    })
    .then(response => response.json())
    .then(data => {
        let urlResultDiv = document.getElementById('url-result');
        urlResultDiv.innerHTML = `
            <h2>Top Reviews</h2>
            ${data.reviews.map((review, index) => `
                <div class="review">
                    <p>${index + 1}) ${review}</p>
                </div>
            `).join('')}
        `;
        toggleLoading(false);
    });
});

function toggleLoading(show) {
    const loadingDiv = document.getElementById('loading');
    if (show) {
        loadingDiv.style.display = 'block';
    } else {
        loadingDiv.style.display = 'none';
    }
}
