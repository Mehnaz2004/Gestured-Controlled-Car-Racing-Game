document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const customAlert = document.getElementById("customAlert");
    const alertMessage = document.getElementById("alertMessage");
    const alertOkButton = document.getElementById("alertOkButton");

    loginForm.addEventListener("submit", (event) => {
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        if (!email || !password) {
            event.preventDefault();
            showAlert("Please fill in all fields.");
        }
    });

    function showAlert(message) {
        alertMessage.textContent = message;
        customAlert.classList.add("show");
        customAlert.style.display = "block";
    }

    alertOkButton.addEventListener("click", () => {
        customAlert.classList.remove("show");
        setTimeout(() => {
            customAlert.style.display = "none";
        }, 500);
    });
});