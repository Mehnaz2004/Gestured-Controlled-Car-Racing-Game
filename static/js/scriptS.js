document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.getElementById("signupForm");
    const customAlert = document.getElementById("customAlert");
    const alertMessage = document.getElementById("alertMessage");
    const alertOkButton = document.getElementById("alertOkButton");

    signupForm.addEventListener("submit", (event) => {
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();
        const confirmPassword = document.getElementById("confirm_password").value.trim();

        if (!email || !password || !confirmPassword) {
            event.preventDefault();
            showAlert("Please fill in all fields.");
        } else if (password !== confirmPassword) {
            event.preventDefault();
            showAlert("Passwords do not match.");
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
        }, 300);
    });
});
