// Function to replace all sentences in tweets with 'PG_Ready_Text'
async function replaceSentencesWithPGReadyText() {
    const tweetElements = document.querySelectorAll("article [lang]");

    for (let element of tweetElements) {
        let text = element.innerText; // Get the inner text of the tweet

        // Skip if the tweet has already been checked or altered
        if (text.endsWith("(safe)") || text.endsWith("(altered)")) {
            continue;
        }

        if (text) {
            // Send the original text to the backend for processing
            const response = await sendToBackend(text);

            // Check the response from the backend
            if (response && response.replacementText !== "None") {
                element.innerText = response.replacementText + " (altered)";
            } else {
                element.innerText = text + " (safe)";
            }
        }
    }
}

async function sendToBackend(originalText) {
    try {
        const response = await fetch('http://127.0.0.1:5000/predict', { // Change the URL if needed
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Specifies the content type
                // 'Authorization': 'Bearer YOUR_TOKEN'  // Uncomment if authentication is needed
            },
            body: JSON.stringify({ sentence: originalText }), // Send the original text
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return await response.json(); // Parse the JSON response
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        return null; // Return null in case of error
    }
}

// Initial function call and observer setup
replaceSentencesWithPGReadyText();

// Use a MutationObserver to reapply replacements on dynamic content
const targetNode = document.querySelector("main");

if (targetNode) {
    const observer = new MutationObserver(() => {
        requestAnimationFrame(replaceSentencesWithPGReadyText);
    });

    observer.observe(targetNode, { childList: true, subtree: true });
}

// Fallback interval in case MutationObserver misses some updates
setInterval(replaceSentencesWithPGReadyText, 3000);