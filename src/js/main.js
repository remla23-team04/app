const predictionEndpoint = '/predict';
const evaluationContainer = document.getElementById('evaluationContainer');
const correctButton = document.getElementById('correctButton');
const incorrectButton = document.getElementById('incorrectButton');
const correctEndpoint = '/evaluation/correct';
const wrongEndpoint = '/evaluation/wrong';

document.getElementById('submitButton').addEventListener('click', async (event) => {
    event.preventDefault();
    const review = document.getElementById('review').value;
    const resultDiv = document.getElementById('sentimentResult')

    if (review) {
        try {
            const response = await fetch(predictionEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ review }),
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);
                const sentiment = data.sentiment;
                resultDiv.innerHTML = '';

                if (sentiment === 'positive') {
                    resultDiv.innerHTML = 'positive :)';
                } else if (sentiment === 'negative') {
                    resultDiv.innerHTML = 'negative :(';
                } else {
                    resultDiv.innerHTML = '[Error: Invalid sentiment response]';
                }
                evaluationContainer.style.display = 'block';
            } else {
                console.error('Error:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        resultDiv.innerHTML = "..."
    }
});
correctButton.addEventListener('click', async () => {
    try {
        const response = await fetch(correctEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
        });

        if (response.ok) {
            console.log("Correct evaluation sent successfully");
        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }

    evaluationContainer.style.display = 'none';
});

incorrectButton.addEventListener('click', async () => {
    try {
        const response = await fetch(wrongEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({}),
        });

        if (response.ok) {
            console.log("Incorrect evaluation sent successfully");
        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }

    evaluationContainer.style.display = 'none';
});