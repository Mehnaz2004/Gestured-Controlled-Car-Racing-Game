$(document).ready(function () {
    $("#save-btn").click(function () {
        let data = {};
        $(".gesture-select").each(function () {
            let func = $(this).data("function");
            let gesture = $(this).val();
            data[func] = gesture;
        });

        $.ajax({
            url: "/update",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function (response) {
                $("#message").text("Gesture mappings updated successfully!").css("color", "green");
            }
        });
    });

    $("#run-btn").click(function () {
        $.ajax({
            url: "/run",
            type: "POST",
            success: function (response) {
                if (response.status === "running") {
                    $("#message").text("Game is running...").css("color", "green");
                } else {
                    $("#message").text("Error: " + response.message).css("color", "red");
                }
            }
        });
    });

    $("#exit-btn").click(function () {
        $.ajax({
            url: "/exit",
            type: "POST",
            success: function (response) {
                if (response.status === "stopped") {
                    $("#message").text("Game has been stopped.").css("color", "red");
                } else {
                    $("#message").text("Error stopping the game: " + response.message).css("color", "red");
                }
            }
        });
    });
});
