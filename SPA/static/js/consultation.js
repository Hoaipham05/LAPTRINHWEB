(function () {
    const launcher = document.getElementById("chat-launcher");
    const panel = document.getElementById("chat-panel");
    const closeButton = document.getElementById("chat-close");
    const messages = document.getElementById("chat-messages");

    if (!launcher || !panel) {
        return;
    }

    const setOpen = (open) => {
        panel.classList.toggle("is-open", open);
        panel.setAttribute("aria-hidden", open ? "false" : "true");
        if (open && messages) {
            messages.scrollTop = messages.scrollHeight;
        }
    };

    launcher.addEventListener("click", () => {
        setOpen(!panel.classList.contains("is-open"));
    });

    if (closeButton) {
        closeButton.addEventListener("click", () => {
            setOpen(false);
        });
    }

    if (document.body.dataset.chatOpen === "1") {
        setOpen(true);
    }
})();
