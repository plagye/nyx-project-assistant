// Function to handle form submission
document.getElementById("send-btn").addEventListener("click", async () => {
    const userInput = document.getElementById("user-input").value;

    if (!userInput.trim()) {
        return; // Ignore empty input
    }

    // Display user's message in the chat window
    addMessageToChat(userInput, "user-message");

    // Send input to Flask backend via POST request
    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input_text: userInput }),
    });

    // Parse and display the AI's response in the chat window
    const data = await response.json();
    const aiMessage = data.generated_text || "Error generating response.";
    
    addMessageToChat(aiMessage, "ai-message");

    // Clear the input field after sending
    document.getElementById("user-input").value = "";
});

// Function to add a message to the chat window
function addMessageToChat(message, messageType) {
    const outputBox = document.getElementById("output-box");

    // Create a new div for the message
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", messageType);
    
    // Set the text content of the message
    messageDiv.innerText = message;

    // Append the message to the output box
    outputBox.appendChild(messageDiv);

    // Scroll to the bottom of the chat window
    outputBox.scrollTop = outputBox.scrollHeight;
}
