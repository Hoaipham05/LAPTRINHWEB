const body = document.body;
const backdrop = document.querySelector("[data-backdrop]");
const modals = document.querySelectorAll(".modal");

function openModal(modalId) {
    modals.forEach((modal) => modal.classList.add("hidden"));
    const target = document.getElementById(modalId);
    if (!target) {
        return;
    }
    target.classList.remove("hidden");
    backdrop.classList.remove("hidden");
    body.classList.add("modal-open");
}

function closeAllModals() {
    modals.forEach((modal) => modal.classList.add("hidden"));
    backdrop.classList.add("hidden");
    body.classList.remove("modal-open");
}

document.querySelectorAll("[data-modal-target]").forEach((button) => {
    button.addEventListener("click", () => {
        openModal(button.dataset.modalTarget);
    });
});

document.querySelectorAll("[data-close-modal]").forEach((button) => {
    button.addEventListener("click", closeAllModals);
});

if (backdrop) {
    backdrop.addEventListener("click", closeAllModals);
}

function normalizePrice(value) {
    return Number(value.replace(/\./g, "").replace(/\s/g, ""));
}

function validateForm(form) {
    const formType = form.dataset.formType;

    if (formType === "add-service" || formType === "edit-service") {
        const name = form.querySelector('[name="name"]').value.trim();
        const description = form.querySelector('[name="description"]').value.trim();
        const price = normalizePrice(form.querySelector('[name="price"]').value.trim());

        if (!name) {
            return "error-empty-name";
        }
        if (!description) {
            return "error-empty-description";
        }
        if (!Number.isFinite(price) || price <= 0) {
            return "error-invalid-price";
        }
        return "success-save-service";
    }

    if (formType === "update-price") {
        const newPrice = normalizePrice(form.querySelector('[name="new_price"]').value.trim());
        if (!Number.isFinite(newPrice) || newPrice <= 0) {
            return "error-invalid-price";
        }
        return "success-save-service";
    }

    return "success-save-service";
}

document.querySelectorAll("form[data-form-type]").forEach((form) => {
    form.addEventListener("submit", (event) => {
        event.preventDefault();

        if (form.dataset.formType === "reply-feedback") {
            const value = form.querySelector('[name="reply"]').value.trim();
            if (!value) {
                openModal("reply-empty-modal");
                return;
            }
            if (value.toLowerCase().includes("fail")) {
                openModal("reply-failed-modal");
                return;
            }
            openModal("reply-success-modal");
            return;
        }

        openModal(validateForm(form));
    });
});

const feedbackActionRoot = document.querySelector("[data-feedback-action]");

if (feedbackActionRoot) {
    const toggle = feedbackActionRoot.querySelector("[data-action-toggle]");
    const menu = feedbackActionRoot.querySelector("[data-action-menu]");
    const statusBadge = document.querySelector("[data-feedback-status]");
    const saveButton = document.querySelector("[data-save-feedback]");
    let selectedAction = "";

    function setMenuState(open) {
        menu.classList.toggle("hidden", !open);
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }

    function applySelectedAction(value) {
        selectedAction = value;

        feedbackActionRoot.querySelectorAll("[data-selected-chip]").forEach((chip) => {
            chip.classList.toggle("hidden", chip.dataset.selectedChip !== value);
        });

        if (statusBadge) {
            if (value === "violation") {
                statusBadge.className = "status-badge pink";
                statusBadge.textContent = "Vi phạm";
            } else if (value === "deleted") {
                statusBadge.className = "status-badge gray";
                statusBadge.textContent = "Đã xóa";
            } else {
                statusBadge.className = "status-badge yellow";
                statusBadge.textContent = "Chưa phản hồi";
            }
        }
    }

    toggle.addEventListener("click", () => {
        setMenuState(menu.classList.contains("hidden"));
    });

    menu.querySelectorAll("[data-action-value]").forEach((option) => {
        option.addEventListener("click", () => {
            applySelectedAction(option.dataset.actionValue);
            setMenuState(false);
        });
    });

    document.addEventListener("click", (event) => {
        if (!feedbackActionRoot.contains(event.target)) {
            setMenuState(false);
        }
    });

    if (saveButton) {
        saveButton.addEventListener("click", () => {
            if (!selectedAction) {
                openModal("process-denied-modal");
                return;
            }

            if (selectedAction === "deleted") {
                openModal("process-failed-modal");
                return;
            }

            openModal("process-success-modal");
        });
    }
}

const appointmentRows = document.querySelectorAll("[data-appointment-item]");

if (appointmentRows.length) {
    const detailStatus = document.querySelector("[data-detail-status]");
    const detailFields = {
        customer: document.querySelector("[data-detail-customer]"),
        phone: document.querySelector("[data-detail-phone]"),
        service: document.querySelector("[data-detail-service]"),
        date: document.querySelector("[data-detail-date]"),
        time: document.querySelector("[data-detail-time]"),
        note: document.querySelector("[data-detail-note]"),
    };

    function fillAppointmentDetail(row) {
        detailFields.customer.textContent = row.dataset.customer;
        detailFields.phone.textContent = row.dataset.phone;
        detailFields.service.textContent = row.dataset.service;
        detailFields.date.textContent = row.dataset.date;
        detailFields.time.textContent = row.dataset.time;
        detailFields.note.textContent = row.dataset.note;
        detailStatus.className = `status-pill ${row.dataset.statusClass}`;
        detailStatus.textContent = row.dataset.status;
    }

    appointmentRows.forEach((row) => {
        row.addEventListener("click", () => {
            fillAppointmentDetail(row);
            openModal("appointment-detail-modal");
        });
    });

    const initialModal = body.dataset.initialModal;
    if (initialModal === "list-error") {
        openModal("appointment-list-error-modal");
    } else if (initialModal === "detail-error") {
        openModal("appointment-detail-error-modal");
    }
}

const consultationForm = document.querySelector('form[data-form-type="consultation-send"]');

if (consultationForm) {
    const input = consultationForm.querySelector('[name="message"]');
    const emptyWarning = document.querySelector("[data-chat-empty-warning]");
    const initialModal = body.dataset.initialModal;

    if (initialModal === "send-error") {
        openModal("consultation-send-error-modal");
    }

    consultationForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const value = input.value.trim();

        if (!value) {
            emptyWarning.classList.remove("hidden");
            return;
        }

        emptyWarning.classList.add("hidden");

        if (value.toLowerCase().includes("fail")) {
            openModal("consultation-send-error-modal");
            return;
        }

        input.value = "";
    });

    input.addEventListener("input", () => {
        if (input.value.trim()) {
            emptyWarning.classList.add("hidden");
        }
    });
}
