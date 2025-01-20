let timer = null;
let startTime = null;
let timeLimit = 60; // Time limit in seconds
let currentTextIndex = 0;

// List of sample texts
const sampleTexts = [
    "Typing speed tests can improve your efficiency at work.In a world driven by technology, the ability to type swiftly and accurately is a game-changer.",
    "Typing is an essential skill in the modern world. It helps you communicate quickly and efficiently. Whether you are writing an email, chatting with friends, or completing a school project, typing accurately saves time. With practice, you can become a faster and better typist.",
    "Technology has changed the way we live. Computers, smartphones, and the internet have made our lives easier and more connected. Typing is a crucial skill that allows us to use these tools effectively. Everyone can benefit from improving their typing speed.",
    "Technology evolves rapidly, shaping the future of humanity.A journey of a thousand miles begins with a single step."
];

const sampleTextElement = document.getElementById("sample-text");
const typingArea = document.getElementById("typing-area");
const wpmElement = document.getElementById("wpm");
const accuracyElement = document.getElementById("accuracy");
const timeElement = document.getElementById("time");
const startButton = document.getElementById("start-test");
const resetButton = document.getElementById("reset");

// Load the initial sample text
updateSampleText();

startButton.addEventListener("click", () => {
    typingArea.value = "";
    typingArea.disabled = false;
    typingArea.focus();

    startTime = new Date();
    timeLimit = 60; // Reset time limit
    timer = setInterval(updateTimer, 1000);

    wpmElement.innerText = "Words Per Minute (WPM): --";
    accuracyElement.innerText = "Accuracy: --%";
    timeElement.innerText = `Time: ${timeLimit} seconds`;
});

typingArea.addEventListener("input", () => {
    const typedText = typingArea.value;
    const sampleText = sampleTextElement.innerText;

    // Stop the test if the user finishes typing the text before time runs out
    if (typedText === sampleText) {
        clearInterval(timer);
        calculateResults();
        typingArea.disabled = true;
    }
});

resetButton.addEventListener("click", () => {
    clearInterval(timer);
    typingArea.value = "";
    typingArea.disabled = true;
    wpmElement.innerText = "Words Per Minute (WPM): --";
    accuracyElement.innerText = "Accuracy: --%";
    timeElement.innerText = "Time: -- seconds";

    // Move to the next sample text
    currentTextIndex = (currentTextIndex + 1) % sampleTexts.length;
    updateSampleText();
});

function updateTimer() {
    timeLimit--;
    timeElement.innerText = `Time: ${timeLimit} seconds`;

    // Stop the timer when the time reaches 0
    if (timeLimit <= 0) {
        clearInterval(timer);
        calculateResults();
        typingArea.disabled = true;

        // Move to the next sample text
        currentTextIndex = (currentTextIndex + 1) % sampleTexts.length;
        updateSampleText();
    }
}

function calculateResults() {
    const elapsedTime = 60 - timeLimit; // Time elapsed in seconds
    const timeInMinutes = elapsedTime / 60; // Convert to minutes
    const sampleText = sampleTextElement.innerText;
    const typedText = typingArea.value;

    // Calculate Words Per Minute (WPM)
    const wordCount = typedText.trim().split(/\s+/).length;
    const wpm = Math.round(wordCount / timeInMinutes);
    wpmElement.innerText = `Words Per Minute (WPM): ${wpm}`;

    // Calculate Accuracy
    const sampleWords = sampleText.trim().split(/\s+/);
    const typedWords = typedText.trim().split(/\s+/);
    let correctWords = 0;

    for (let i = 0; i < Math.min(sampleWords.length, typedWords.length); i++) {
        if (sampleWords[i] === typedWords[i]) {
            correctWords++;
        }
    }

    const accuracy = Math.round((correctWords / sampleWords.length) * 100);
    accuracyElement.innerText = `Accuracy: ${accuracy}%`;
}

function updateSampleText() {
    sampleTextElement.innerText = sampleTexts[currentTextIndex];
}
