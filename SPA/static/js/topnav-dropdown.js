document.querySelectorAll(".nav-dropdown").forEach((dropdown) => {
    const toggle = dropdown.querySelector("[data-nav-toggle]");
    const menu = dropdown.querySelector("[data-nav-submenu]");

    if (!toggle || !menu) {
        return;
    }

    const isInitiallyOpen = toggle.classList.contains("active");
    dropdown.classList.toggle("is-open", isInitiallyOpen);
    toggle.setAttribute("aria-expanded", isInitiallyOpen ? "true" : "false");

    toggle.addEventListener("click", () => {
        const willOpen = !dropdown.classList.contains("is-open");

        document.querySelectorAll(".nav-dropdown.is-open").forEach((item) => {
            if (item !== dropdown) {
                item.classList.remove("is-open");
                const itemToggle = item.querySelector("[data-nav-toggle]");
                if (itemToggle) {
                    itemToggle.setAttribute("aria-expanded", "false");
                }
            }
        });

        dropdown.classList.toggle("is-open", willOpen);
        toggle.setAttribute("aria-expanded", willOpen ? "true" : "false");
    });
});

document.addEventListener("click", (event) => {
    document.querySelectorAll(".nav-dropdown.is-open").forEach((dropdown) => {
        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove("is-open");
            const toggle = dropdown.querySelector("[data-nav-toggle]");
            if (toggle) {
                toggle.setAttribute("aria-expanded", "false");
            }
        }
    });
});

document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
        return;
    }

    document.querySelectorAll(".nav-dropdown.is-open").forEach((dropdown) => {
        dropdown.classList.remove("is-open");
        const toggle = dropdown.querySelector("[data-nav-toggle]");
        if (toggle) {
            toggle.setAttribute("aria-expanded", "false");
        }
    });
});

