document.addEventListener("DOMContentLoaded", () => {
    const saveButton = document.getElementById("save-button");
    const runButton = document.getElementById("run-button");
    const stopButton = document.getElementById("stop-button");

    saveButton.addEventListener("click", saveMappings);
    runButton.addEventListener("click", runPrototype);
    stopButton.addEventListener("click", stopPrototype);
});

function saveMappings() {
    const mappings = {};
    const rows = document.querySelectorAll("tbody tr");

    rows.forEach(row => {
        const gesture = row.cells[0].textContent.trim();
        const rightKey = row.querySelector(`input[id="right_${gesture}"]`).value;
        const leftKey = row.querySelector(`input[id="left_${gesture}"]`).value;

        mappings[gesture] = { right: rightKey, left: leftKey };
    });

    fetch("/update_mappings", {
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
    .catch(error => console.error("Error:", error));
}

function runPrototype() {
    fetch("/run_prototype", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.status === "running") {
            alert("Prototype running...");
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => console.error("Error:", error));
}

function stopPrototype() {
    fetch("/stop_prototype", { method: "POST" })
    .then(response => response.json())
    .then(data => {
        if (data.status === "stopped") {
            alert("Prototype stopped.");
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => console.error("Error:", error));
}
