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
            alert(`Invalid input for gesture: ${gesture}`);
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
            alert("Mappings updated successfully!");
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to save mappings.");
    });
}

function runPrototype() {
    return fetch("/run_prototype", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.status === "running") {
            alert("Prototype running...");
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to run prototype.");
    });
}

function stopPrototype() {
    return fetch("/stop_prototype", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.status === "stopped") {
            alert("Prototype stopped.");
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to stop prototype.");
    });
}
