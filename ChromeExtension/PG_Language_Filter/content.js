// Function to replace all sentences in tweets with 'PG_Ready_Text'
async function replaceSentencesWithPGReadyText() {
    const tweetElements = document.querySelectorAll("article [lang]");

    for (let element of tweetElements) {
        let text = element.innerText; // Get the inner text of the tweet
        const sentences = text.match(/[^.!?]*[.!?]/g); // Split text into sentences

        if (sentences) {
            // Replace each sentence with 'PG_Ready_Text'
            const modifiedSentences = sentences.map(() => "PG_Ready_Text");
            element.innerText = modifiedSentences.join(' '); // Join modified sentences back into a single string
        }
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