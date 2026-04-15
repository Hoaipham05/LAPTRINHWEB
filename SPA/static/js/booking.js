document.addEventListener("DOMContentLoaded", function () {
    const panelTabs = document.querySelectorAll(".booking-board__tab");
    const panels = document.querySelectorAll(".booking-panel");
    const steps = Array.from(document.querySelectorAll(".booking-step"));
    const indicators = Array.from(document.querySelectorAll("[data-step-indicator]"));
    const prevBtn = document.getElementById("prev-step-btn");
    const nextBtn = document.getElementById("next-step-btn");
    const packageGrid = document.getElementById("package-grid");
    const timeslotGrid = document.getElementById("timeslot-grid");

    if (!steps.length) return;

    const packageData = JSON.parse(document.getElementById("booking-packages-data").textContent || "{}");
    const slotData = JSON.parse(document.getElementById("booking-slots-data").textContent || "{}");

    const state = {
        step: 1,
        service: null,
        serviceName: "",
        package: null,
        packageName: "",
        packageSessions: "",
        packagePrice: "",
        packageResult: "",
        date: "",
        time: "",
    };

    function resetFromService() {
        state.package = null;
        state.packageName = "";
        state.packageSessions = "";
        state.packagePrice = "";
        state.packageResult = "";
        state.date = "";
        state.time = "";
        packageGrid.innerHTML = "";
        timeslotGrid.innerHTML = "";
        document
            .querySelectorAll("[data-calendar-day]")
            .forEach((btn) => btn.classList.remove("is-selected"));
    }

    function activatePanel(targetId) {
        panels.forEach((panel) => panel.classList.toggle("is-active", panel.id === targetId));
        panelTabs.forEach((tab) => tab.classList.toggle("is-active", tab.getAttribute("data-panel-target") === targetId));
    }

    panelTabs.forEach((tab) => {
        tab.addEventListener("click", function () {
            activatePanel(this.getAttribute("data-panel-target"));
        });
    });

    function renderStep() {
        steps.forEach((stepEl) => {
            stepEl.classList.toggle("is-active", Number(stepEl.getAttribute("data-step")) === state.step);
        });
        indicators.forEach((item) => {
            item.classList.toggle("is-active", Number(item.getAttribute("data-step-indicator")) === state.step);
        });
        prevBtn.disabled = state.step === 1;
        nextBtn.textContent = state.step === 4 ? "Xác nhận đặt lịch" : "Tiếp theo →";
        updateSummary();
    }

    function updateSummary() {
        const map = {
            "summary-service": state.serviceName || "Chưa chọn",
            "summary-package": state.packageName || "Chưa chọn",
            "summary-sessions": state.packageSessions || "Chưa chọn",
            "summary-date": state.date || "Chưa chọn",
            "summary-time": state.time || "Chưa chọn",
            "summary-price": state.packagePrice || "Chưa chọn",
            "summary-result": state.packageResult || "Chưa chọn",
        };
        Object.keys(map).forEach((id) => {
            const el = document.getElementById(id);
            if (el) el.textContent = map[id];
        });
    }

    function renderPackages(serviceId) {
        packageGrid.innerHTML = "";
        const items = packageData[String(serviceId)] || [];
        if (!items.length) {
            packageGrid.innerHTML = '<p class="empty-inline">Chưa có gói cho dịch vụ này.</p>';
            return;
        }
        items.forEach((item) => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "package-card";
            if (item.theme) {
                btn.classList.add("is-" + item.theme);
            }
            const benefitList = (item.benefits || [])
                .map((text) => "<li>\u2713 " + text + "</li>")
                .join("");
            btn.innerHTML =
                "<h3>" + item.name + "</h3>" +
                "<p class=\"package-sessions\">" + item.sessions + " buoi dieu tri</p>" +
                "<ul class=\"package-benefits\">" + benefitList + "</ul>" +
                '<p class="package-price">' + item.price + "</p>";
            if (item.result) {
                btn.innerHTML += '<p class="package-note">' + item.result + "</p>";
            }
            btn.addEventListener("click", function () {
                document.querySelectorAll(".package-card").forEach((x) => x.classList.remove("is-selected"));
                btn.classList.add("is-selected");
                state.package = item.id;
                state.packageName = item.name;
                state.packageSessions = item.sessions + " buổi";
                state.packagePrice = item.price;
                state.packageResult = item.result;
                updateSummary();
            });
            packageGrid.appendChild(btn);
        });
    }

    function renderSlots(dayIso) {
        timeslotGrid.innerHTML = "";
        (slotData[dayIso] || ["09:00", "10:30", "14:00", "16:00"]).forEach((slot) => {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.textContent = slot;
            btn.addEventListener("click", function () {
                timeslotGrid.querySelectorAll("button").forEach((x) => x.classList.remove("is-selected"));
                btn.classList.add("is-selected");
                state.time = slot;
                updateSummary();
            });
            timeslotGrid.appendChild(btn);
        });
    }

    document.querySelectorAll("[data-service-card]").forEach((card) => {
        card.addEventListener("click", function () {
            document.querySelectorAll("[data-service-card]").forEach((x) => x.classList.remove("is-selected"));
            card.classList.add("is-selected");
            resetFromService();
            state.service = card.getAttribute("data-service-id");
            state.serviceName = card.getAttribute("data-service-name") || "";
            renderPackages(state.service);
            updateSummary();
        });
    });

    const firstServiceCard = document.querySelector("[data-service-card]");
    if (firstServiceCard) {
        firstServiceCard.click();
    }

    document.querySelectorAll("[data-calendar-day]").forEach((dayBtn) => {
        dayBtn.addEventListener("click", function () {
            document.querySelectorAll("[data-calendar-day]").forEach((x) => x.classList.remove("is-selected"));
            dayBtn.classList.add("is-selected");
            state.date = dayBtn.getAttribute("data-date") || "";
            state.time = "";
            renderSlots(state.date);
            updateSummary();
        });
    });

    const todayBtn = document.querySelector("[data-calendar-day].is-today") || document.querySelector("[data-calendar-day]");
    if (todayBtn) {
        todayBtn.classList.add("is-selected");
        state.date = todayBtn.getAttribute("data-date") || "";
        renderSlots(state.date);
    }

    function canMoveForward() {
        if (state.step === 1) return !!state.service;
        if (state.step === 2) return !!state.package;
        if (state.step === 3) return !!state.date && !!state.time;
        return true;
    }

    prevBtn.addEventListener("click", function () {
        if (state.step > 1) {
            state.step -= 1;
            renderStep();
        }
    });

    nextBtn.addEventListener("click", function () {
        if (state.step < 4) {
            if (!canMoveForward()) {
                alert("Vui long chon thong tin truoc khi tiep tuc.");
                return;
            }
            state.step += 1;
            renderStep();
            return;
        }

        if (!canMoveForward()) {
            alert("Vui long chon day du thong tin dat lich.");
            return;
        }

        document.getElementById("booking-service-id").value = state.service || "";
        document.getElementById("booking-package-id").value = state.package || "";
        document.getElementById("booking-appointment-date").value = state.date || "";
        document.getElementById("booking-appointment-time").value = state.time || "";
        document.getElementById("booking-submit-form").submit();
    });

    renderStep();
});

