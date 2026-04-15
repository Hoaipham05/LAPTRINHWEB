document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.querySelector("[data-chat-toggle]");
    const closeButton = document.querySelector("[data-chat-close]");
    const widget = document.querySelector("[data-chat-widget]");
    const form = document.querySelector("[data-chat-form]");

    if (!toggleButton || !widget) {
        return;
    }

    toggleButton.addEventListener("click", function () {
        widget.classList.toggle("hidden");
    });

    if (closeButton) {
        closeButton.addEventListener("click", function () {
            widget.classList.add("hidden");
        });
    }

    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            const input = form.querySelector("input[name='message']");
            if (!input || !input.value.trim()) {
                return;
            }

            const body = widget.querySelector(".chat-body");
            const row = document.createElement("div");
            row.className = "chat-row right";
            row.innerHTML =
                '<p class="chat-bubble"></p>' +
                '<span class="chat-stamp">Vừa xong</span>';
            row.querySelector(".chat-bubble").textContent = input.value.trim();
            body.appendChild(row);
            body.scrollTop = body.scrollHeight;
            input.value = "";
        });
    }
});

