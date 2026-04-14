(function () {
    const slotSource = document.getElementById("booking-slots-data");
    const packageSource = document.getElementById("booking-packages-data");
    const slotMap = slotSource ? JSON.parse(slotSource.textContent) : {};
    const packagesByService = packageSource ? JSON.parse(packageSource.textContent) : {};

    const boardTabs = Array.from(document.querySelectorAll("[data-panel-target]"));
    const boardPanels = Array.from(document.querySelectorAll(".booking-panel"));
    const serviceCards = Array.from(document.querySelectorAll("[data-service-card]"));
    const calendarDays = Array.from(document.querySelectorAll("[data-calendar-day]"));
    const stepPanels = Array.from(document.querySelectorAll("[data-step]"));
    const stepIndicators = Array.from(document.querySelectorAll("[data-step-indicator]"));
    const nextButton = document.getElementById("next-step-btn");
    const prevButton = document.getElementById("prev-step-btn");
    const timeslotGrid = document.getElementById("timeslot-grid");
    const packageGrid = document.getElementById("package-grid");
    const submitForm = document.getElementById("booking-submit-form");
    const serviceField = document.getElementById("booking-service-id");
    const packageField = document.getElementById("booking-package-id");
    const dateField = document.getElementById("booking-appointment-date");
    const timeField = document.getElementById("booking-appointment-time");

    const summaryService = document.getElementById("summary-service");
    const summaryPackage = document.getElementById("summary-package");
    const summarySessions = document.getElementById("summary-sessions");
    const summaryDate = document.getElementById("summary-date");
    const summaryTime = document.getElementById("summary-time");
    const summaryPrice = document.getElementById("summary-price");
    const summaryResult = document.getElementById("summary-result");

    const state = {
        step: 1,
        service: null,
        package: null,
        date: null,
        time: null,
    };

    const formatDate = (isoDate) => {
        if (!isoDate) {
            return "Chưa chọn";
        }
        const value = new Date(`${isoDate}T00:00:00`);
        return new Intl.DateTimeFormat("vi-VN", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
        }).format(value);
    };

    const updateBoardPanel = (panelId) => {
        boardTabs.forEach((tab) => {
            tab.classList.toggle("is-active", tab.dataset.panelTarget === panelId);
        });
        boardPanels.forEach((panel) => {
            panel.classList.toggle("is-active", panel.id === panelId);
        });
    };

    const updateHiddenFields = () => {
        if (serviceField) {
            serviceField.value = state.service ? state.service.id : "";
        }
        if (packageField) {
            packageField.value = state.package ? state.package.id : "";
        }
        if (dateField) {
            dateField.value = state.date || "";
        }
        if (timeField) {
            timeField.value = state.time || "";
        }
    };

    const updateSummary = () => {
        updateHiddenFields();
        if (summaryService) {
            summaryService.textContent = state.service ? state.service.name : "Chưa chọn";
        }
        if (summaryPackage) {
            summaryPackage.textContent = state.package ? state.package.name : "Chưa chọn";
        }
        if (summarySessions) {
            summarySessions.textContent = state.package ? state.package.sessions : "Chưa chọn";
        }
        if (summaryDate) {
            summaryDate.textContent = formatDate(state.date);
        }
        if (summaryTime) {
            summaryTime.textContent = state.time || "Chưa chọn";
        }
        if (summaryPrice) {
            summaryPrice.textContent = state.package ? state.package.price : "Chưa chọn";
        }
        if (summaryResult) {
            summaryResult.textContent = state.package ? state.package.result : "Chưa chọn";
        }
    };

    const updateActions = () => {
        let disabled = false;
        if (state.step === 1) {
            disabled = !state.service;
        } else if (state.step === 2) {
            disabled = !state.package;
        } else if (state.step === 3) {
            disabled = !(state.date && state.time);
        }

        prevButton.disabled = state.step === 1;
        nextButton.disabled = disabled;
        nextButton.textContent = state.step === 4 ? "Xác nhận" : "Tiếp theo →";
    };

    const setActiveStep = (step) => {
        state.step = step;
        stepPanels.forEach((panel) => {
            panel.classList.toggle("is-active", Number(panel.dataset.step) === step);
        });
        stepIndicators.forEach((indicator) => {
            const current = Number(indicator.dataset.stepIndicator);
            indicator.classList.toggle("is-active", current === step);
            indicator.classList.toggle("is-complete", current < step);
        });
        updateActions();
    };

    const renderSlots = (dateKey) => {
        timeslotGrid.innerHTML = "";
        const slots = slotMap[dateKey] || [];

        if (!dateKey || !slots.length) {
            const empty = document.createElement("div");
            empty.className = "timeslot-chip is-empty";
            empty.textContent = "Hãy chọn ngày để xem khung giờ.";
            timeslotGrid.appendChild(empty);
            updateSummary();
            updateActions();
            return;
        }

        slots.forEach((slot) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "timeslot-chip";
            button.textContent = slot.label;
            if (slot.disabled) {
                button.disabled = true;
                button.classList.add("is-disabled");
            }
            if (state.time === slot.label) {
                button.classList.add("is-selected");
            }
            button.addEventListener("click", () => {
                state.time = slot.label;
                renderSlots(state.date);
            });
            timeslotGrid.appendChild(button);
        });

        updateSummary();
        updateActions();
    };

    const renderPackages = (serviceId) => {
        if (!packageGrid) {
            return;
        }

        packageGrid.innerHTML = "";
        const packages = packagesByService[serviceId] || [];

        if (!packages.length) {
            const empty = document.createElement("div");
            empty.className = "package-empty";
            empty.textContent = "Hãy chọn một dịch vụ ở bước trước để xem các gói phù hợp.";
            packageGrid.appendChild(empty);
            updateSummary();
            updateActions();
            return;
        }

        packages.forEach((pkg) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = `package-card accent-${pkg.accent}`;
            button.innerHTML = `
                <span class="package-card__name">${pkg.name}</span>
                <span class="package-card__line">${pkg.sessions}</span>
                <span class="package-card__line">${pkg.steps}</span>
                <span class="package-card__price">${pkg.price}</span>
                <span class="package-card__foot">${pkg.result}</span>
            `;

            if (state.package && state.package.id === pkg.id) {
                button.classList.add("is-selected");
            }

            button.addEventListener("click", () => {
                Array.from(packageGrid.querySelectorAll(".package-card")).forEach((item) => {
                    item.classList.remove("is-selected");
                });
                button.classList.add("is-selected");
                state.package = {
                    id: pkg.id,
                    name: pkg.name,
                    sessions: pkg.sessions,
                    price: pkg.price,
                    result: pkg.result,
                };
                updateSummary();
                updateActions();
            });

            packageGrid.appendChild(button);
        });
    };

    boardTabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            updateBoardPanel(tab.dataset.panelTarget);
        });
    });

    serviceCards.forEach((card) => {
        card.addEventListener("click", () => {
            serviceCards.forEach((item) => item.classList.remove("is-selected"));
            card.classList.add("is-selected");
            state.service = {
                id: card.dataset.serviceId,
                name: card.dataset.serviceName,
            };
            state.package = null;
            renderPackages(state.service.id);
            updateSummary();
            updateActions();
        });
    });

    calendarDays.forEach((day) => {
        day.addEventListener("click", () => {
            if (day.disabled) {
                return;
            }
            calendarDays.forEach((item) => item.classList.remove("is-selected"));
            day.classList.add("is-selected");
            state.date = day.dataset.date;
            state.time = null;
            renderSlots(state.date);
        });
    });

    prevButton.addEventListener("click", () => {
        if (state.step > 1) {
            setActiveStep(state.step - 1);
        }
    });

    nextButton.addEventListener("click", () => {
        if (state.step < 4) {
            setActiveStep(state.step + 1);
            return;
        }
        if (submitForm) {
            submitForm.submit();
        }
    });

    updateBoardPanel("booking-flow");
    updateSummary();
    renderPackages(null);
    renderSlots(null);
    setActiveStep(1);
})();
