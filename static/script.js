document.addEventListener("DOMContentLoaded", () => {
    const chatForm = document.getElementById("chatForm");
    if (chatForm) {
        chatForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const formData = new FormData(chatForm);
            const response = await fetch("/chat/", {
                method: "POST",
                body: formData,
            });
            const result = await response.json();
            document.getElementById("responseBox").innerText = result.response;
        });
    }
});
