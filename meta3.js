const homeLink = document.getElementById('home-link');
const aboutLink = document.getElementById('about-link');
const contactLink = document.getElementById('contact-link');
const mainContent = document.getElementById('main-content');

// Function to load home content
function loadHomeContent() {
    mainContent.innerHTML = `
        <h1>Fake News Detector</h1>
        <p>Enter text to detect fake news</p>
        <input type="text" id="news-input" placeholder="Enter news text">
        <button id="detect-btn">Detect</button>
        <div id="result"></div>
    `;

    const detectBtn = document.getElementById('detect-btn');
    const newsInput = document.getElementById('news-input');
    const resultDiv = document.getElementById('result');

    detectBtn.addEventListener('click', () => {
        const newsText = newsInput.value.trim();
        resultDiv.textContent = `You entered: ${newsText}`;
    });
}

// Function to load about content
function loadAboutContent() {
    mainContent.innerHTML = `
        <h1>About Us</h1>
        <p>This is a fake news detector application.</p>
    `;
}

// Function to load contact content
function loadContactContent() {
    mainContent.innerHTML = `
        <h1>Contact Us</h1>
        <p>Get in touch with us for more information.</p>
    `;
}

// Load home content by default
loadHomeContent();

// Add event listeners to navigation links
homeLink.addEventListener('click', loadHomeContent);
aboutLink.addEventListener('click', loadAboutContent);
contactLink.addEventListener('click', loadContactContent);