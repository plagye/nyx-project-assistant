// Function to handle form submission
document.getElementById("send-btn").addEventListener("click", async () => {
    const userInput = document.getElementById("user-input").value;

    if (!userInput.trim()) {
        alert("Input cannot be empty!"); // Provide user feedback
        return;
    }

    addMessageToChat(userInput, "user-message");

    try {
        const response = await fetch("/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ input_text: userInput }),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch response from server");
        }

        const data = await response.json();
        const aiMessage = data.generated_text || "Error generating response.";
        addMessageToChat(aiMessage, "ai-message");
    } catch (error) {
        console.error("Error:", error);
        addMessageToChat("An error occurred while generating text.", "ai-message");
    }

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
