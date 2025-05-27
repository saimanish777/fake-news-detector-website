document.addEventListener('DOMContentLoaded', () => {
    // Correctly match HTML IDs from Gemini.html
    const newsInput = document.getElementById('news-input');
    const checkButton = document.getElementById('check-button');
    const resultsContainer = document.getElementById('results-container');
    const trustScoreDisplay = document.getElementById('trust-score');
    const trustLevelDisplay = document.getElementById('trust-level');
    const trustExplanationDisplay = document.getElementById('trust-explanation');
    const spinnerIcon = document.getElementById('spinner-icon'); // Using this for loader
    const trustIcon = document.getElementById('trust-icon'); // For updating the trust icon

    // Mobile menu toggle functionality (extracted from your original HTML)
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // THIS IS THE URL FOR YOUR DEPLOYED NETLIFY SERVERLESS FUNCTION:
    const SERVERLESS_FUNCTION_URL = 'https://eclectic-horse-552b00.netlify.app/.netlify/functions/analyze-fact-check';

    checkButton.addEventListener('click', async () => {
        const factText = newsInput.value.trim();

        if (factText === "") {
            alert("Please enter some text to fact-check.");
            return;
        }

        // Show loading state and clear previous results
        if (spinnerIcon) spinnerIcon.classList.remove('hidden'); // Show spinner
        checkButton.disabled = true; // Disable button during analysis
        resultsContainer.classList.add('hidden'); // Hide previous results
        trustScoreDisplay.textContent = 'Analyzing...';
        trustLevelDisplay.textContent = ''; // Clear trust level
        trustExplanationDisplay.textContent = ''; // Clear explanation
        trustScoreDisplay.style.color = '#333'; // Reset color

        try {
            const response = await fetch(SERVERLESS_FUNCTION_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: factText })
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            const trustScore = data.trust_score;
            const analysisDetails = data.analysis_details;

            // Update UI with results
            resultsContainer.classList.remove('hidden');
            trustScoreDisplay.textContent = `${trustScore}/100`;
            trustExplanationDisplay.textContent = analysisDetails;

            // Update trust level and icon based on score
            let trustLevelText = 'Analyzing...';
            let iconColorClass = 'text-gray-500';
            let iconPath = `<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />`; // Default: checkmark

            if (trustScore >= 80) {
                trustLevelText = 'Very High Trust';
                iconColorClass = 'text-green-600';
            } else if (trustScore >= 60) {
                trustLevelText = 'High Trust';
                iconColorClass = 'text-lime-600';
            } else if (trustScore >= 40) {
                trustLevelText = 'Moderate Trust';
                iconColorClass = 'text-yellow-600';
                iconPath = `<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.706c1.73 0 2.813-1.874 1.948-3.374l-4.306-7.425c-.49-.844-1.757-.844-2.247 0l-4.306 7.425z" />`; // Warning sign
            } else if (trustScore >= 20) {
                trustLevelText = 'Low Trust';
                iconColorClass = 'text-orange-600';
                iconPath = `<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.706c1.73 0 2.813-1.874 1.948-3.374l-4.306-7.425c-.49-.844-1.757-.844-2.247 0l-4.306 7.425z" />`; // Warning sign (or a stronger X)
            } else {
                trustLevelText = 'Very Low Trust';
                iconColorClass = 'text-red-600';
                iconPath = `<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />`; // X mark
            }

            trustLevelDisplay.textContent = trustLevelText;
            // Dynamically update the SVG icon inside the trustIcon div
            if (trustIcon) { // Check if trustIcon element exists
                trustIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 <span class="math-inline">\{iconColorClass\}"\></span>{iconPath}</svg>`;
            }

        } catch (error) {
            console.error('Error during fact-check:', error);
            trustScoreDisplay.textContent = 'Error!';
            trustScoreDisplay.style.color = 'red';
            trustLevelDisplay.textContent = 'Analysis Failed';
            trustExplanationDisplay.textContent = `Could not get analysis. Please try again later. Error: ${error.message}`;
        } finally {
            if (spinnerIcon) spinnerIcon.classList.add('hidden'); // Hide spinner
            checkButton.disabled = false; // Enable button
        }
    });
});