$(document).ready(function () {

    $("#load-repo").click(function (e) {
    e.preventDefault();

    let repoUrl = $("#repo-url").val().trim();

    if (repoUrl === "") return;

        $("#chat-container").append(`
            <div class="message bot" id="loading-msg">
                <em>Loading and indexing repository, please wait...</em>
            </div>
        `);
        $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight);

        $.ajax({
            url: "/chatbot",
            type: "POST",
            data: { question: repoUrl },
            success: function () {
                $("#loading-msg").remove();
                $("#chat-container").append(`
                    <div class="message bot" style="color: #2e7d32; font-weight: bold;">
                        ✅ Repository Loaded Successfully! You can now ask questions.
                    </div>
                `);
                $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight);
            },
            error: function (xhr) {
                $("#loading-msg").remove();
                let errorMsg = "Error loading repository";
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = "Error: " + xhr.responseJSON.error;
                }
                $("#chat-container").append(`
                    <div class="message bot" style="color: #c62828; font-weight: bold;">
                        ❌ ${errorMsg}
                    </div>
                `);
                $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight);
            }
        });
    });

    

    $("#send").click(function () {

        let userMessage = $("#message").val();

        if (userMessage.trim() === "") {
            return;
        }

        $("#chat-container").append(`
            <div class="message user">
                ${userMessage}
            </div>
        `);

        $.ajax({
            url: "/get",
            type: "POST",
            data: {
                msg: userMessage
            },
            success: function (data) {

                let formattedResponse = data;
                if (typeof marked !== 'undefined') {
                    formattedResponse = marked.parse(data);
                }

                $("#chat-container").append(`
                    <div class="message bot">
                        ${formattedResponse}
                    </div>
                `);

                $("#message").val("");

                $("#chat-container").scrollTop(
                    $("#chat-container")[0].scrollHeight
                );
            },
            error: function () {

                $("#chat-container").append(`
                    <div class="message bot" style="color: #c62828;">
                        Error generating response
                    </div>
                `);
            }
        });

    });

});