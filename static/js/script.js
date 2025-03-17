document.addEventListener("DOMContentLoaded", () => {
    const saveButton = document.getElementById("save-button");
    const runButton = document.getElementById("run-button");
    const stopButton = document.getElementById("stop-button");

    saveButton.addEventListener("click", () => handleRequest(saveMappings, saveButton));
    runButton.addEventListener("click", () => handleRequest(runPrototype, runButton));
    stopButton.addEventListener("click", () => handleRequest(stopPrototype, stopButton));
});

function handleRequest(action, button) {
    button.disabled = true;
    action().finally(() => {
        button.disabled = false;
    });
}

function saveMappings() {
    const mappings = {};
    const rows = document.querySelectorAll("tbody tr");

    rows.forEach(row => {
        const gesture = row.cells[0].textContent.trim();
        const rightKey = row.querySelector(`input[id="right_${gesture}"]`).value;
        const leftKey = row.querySelector(`input[id="left_${gesture}"]`).value;

        if (!rightKey || !leftKey) {
            showAlert(`Invalid input for gesture: ${gesture}`);
            return;
        }

        mappings[gesture] = { right: rightKey, left: leftKey };
    });

    return fetch("/update_mappings", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(mappings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            showAlert("Mappings updated successfully!");
        } else {
            showAlert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showAlert("Failed to save mappings.");
    });
}

function runPrototype() {
    return fetch("/run_prototype", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.status === "running") {
            showAlert("Click Ok to start the program!");
        } else {
            showAlert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showAlert("Failed to run prototype.");
    });
}

function stopPrototype() {
    return fetch("/stop_prototype", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.status === "stopped") {
            showAlert("Prototype stopped.");
        } else {
            showAlert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        showAlert("Failed to stop prototype.");
    });
}

function showAlert(message) {
    const alertBox = document.getElementById("custom-alert");
    const alertMessage = document.getElementById("alert-message");
    const alertOk = document.getElementById("alert-ok");

    alertMessage.textContent = message;
    alertBox.classList.remove("hide");
    alertBox.classList.add("show");

    alertOk.onclick = () => {
        alertBox.classList.remove("show");
        alertBox.classList.add("hide");

        // Ensure it stays hidden after animation ends
        setTimeout(() => {
            alertBox.classList.remove("hide");
        }, 300);
    };
}