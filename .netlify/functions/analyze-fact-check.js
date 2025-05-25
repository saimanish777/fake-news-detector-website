// netlify/functions/analyze-fact-check.js
// This function will be deployed as a Netlify Function
const fetch = require('node-fetch'); // This line is for Node.js environments

// Your Google Fact Check Tools API Key will be an environment variable
// in your Netlify project settings (NOT hardcoded here!)
const GOOGLE_API_KEY = process.env.GOOGLE_FACT_CHECK_API_KEY; // This is how you access it securely

exports.handler = async function(event, context) {
    // Enable CORS (Cross-Origin Resource Sharing)
    // This allows your frontend (from its Netlify domain) to call this function.
    const headers = {
        'Access-Control-Allow-Origin': '', // IMPORTANT: For production, change '' to your actual Netlify frontend domain (e.g., 'https://your-fakelatestnewsdetector.netlify.app')
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Handle preflight OPTIONS request for CORS
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers: headers,
            body: ''
        };
    }

    // Only allow POST requests for the actual API call
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers: headers,
            body: JSON.stringify({ error: 'Method Not Allowed' })
        };
    }

    try {
        // Parse the request body from the frontend
        const body = JSON.parse(event.body);
        const inputContent = body.content;
        const inputType = body.type; // 'text' or 'url'

        if (!inputContent || !inputType) {
            return {
                statusCode: 400,
                headers: headers,
                body: JSON.stringify({ error: 'Missing content or type in request body.' })
            };
        }

        let googleApiUrl = '';
        let queryParameter = '';

        // Construct the Google Fact Check Tools API URL based on input type
        if (inputType === 'text') {
            queryParameter = query=${encodeURIComponent(inputContent)};
        } else if (inputType === 'url') {
            queryParameter = uri=${encodeURIComponent(inputContent)};
        } else {
             return {
                statusCode: 400,
                headers: headers,
                body: JSON.stringify({ error: 'Invalid input type. Must be "text" or "url".' })
            };
        }

        // Append the API key securely from environment variables
        googleApiUrl = https://factchecktools.googleapis.com/v1alpha1/claims:search?${queryParameter}&key=${GOOGLE_API_KEY};

        // Make the actual call to Google's Fact Check Tools API
        const googleResponse = await fetch(googleApiUrl);
        const googleData = await googleResponse.json();

        // Handle non-OK responses from Google API
        if (!googleResponse.ok) {
            console.error('Google API Error:', googleData);
            return {
                statusCode: googleResponse.status,
                headers: headers,
                body: JSON.stringify({ error: googleData.error?.message || 'Error from Google Fact Check API' })
            };
        }

        // --- Process Google's response to derive your 'trust score' ---
        let trustScore = 50; // Default or neutral score if no specific claims are found
        let analysisDetails = "No direct fact-checks found for this specific content. Consider cross-referencing information.";
        const claims = googleData.claims || []; // Extract claims, default to empty array if none

        if (claims.length > 0) {
            let falseCount = 0;
            let trueCount = 0;
            let reviewText = [];

            // Iterate through found claims and their reviews
            claims.forEach(claim => {
                claim.claimReview.forEach(review => {
                    reviewText.push(- ${review.textualRating}: "${review.title}" by ${review.publisher.name}. Learn more: ${review.url});
                    const rating = review.textualRating.toLowerCase();
                    if (rating.includes('false') || rating.includes('misleading') || rating.includes('hoax')) {
                        falseCount++;
                    } else if (rating.includes('true') || rating.includes('mostly true') || rating.includes('accurate')) {
                        trueCount++;
                    }
                });
            });

            // Simple logic to adjust trust score based on findings
            if (falseCount > 0) {
                trustScore = Math.max(0, 50 - (falseCount * 15)); // Decrease score for false/misleading claims
                analysisDetails = Found ${falseCount} claim(s) rated as false/misleading. Trust score reduced. Details:\n + reviewText.join('\n');
            } else if (trueCount > 0) {
                trustScore = Math.min(100, 50 + (trueCount * 10)); // Increase score for true/accurate claims
                analysisDetails = Found ${trueCount} claim(s) rated as true/accurate. Details:\n + reviewText.join('\n');
            } else {
                 analysisDetails = "Fact-checks found, but no clear rating (e.g., 'no rating', 'needs context'). Details:\n" + reviewText.join('\n');
            }

            // Ensure score stays within 0-100 bounds
            trustScore = Math.max(0, Math.min(100, trustScore));

        } else {
            analysisDetails = "No specific fact-checks found in Google's database for this content. This does not necessarily mean it's true or false; it simply hasn't been widely fact-checked yet.";
        }

        // Prepare the response data for the frontend
        const responseData = {
            trust_score: trustScore,
            analysis_details: analysisDetails
        };

        return {
            statusCode: 200, // OK
            headers: headers,
            body: JSON.stringify(responseData) // Send data back as JSON
        };

    } catch (error) {
        // Catch any unexpected errors during function execution
        console.error('Function error:', error);
        return {
            statusCode: 500, // Internal Server Error
            headers: headers,
            body: JSON.stringify({ error: 'Internal server error: ' + error.message })
        };
    }
};