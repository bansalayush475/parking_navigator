// ====== Admin Dashboard JS ======
// Handles inline updates and deletions without full page reload.

document.addEventListener("DOMContentLoaded", () => {
    // Attach update listeners
    document.querySelectorAll(".update-form").forEach(form => {
        form.addEventListener("submit", e => {
            e.preventDefault();
            const formData = new FormData(form);
            const areaId = form.dataset.areaId;

            fetch(`/admin/update/${areaId}`, {
                method: "POST",
                body: formData
            })
            .then(res => res.ok ? location.reload() : alert("❌ Update failed"))
            .catch(() => alert("⚠ Error updating area"));
        });
    });

    // Attach delete listeners
    document.querySelectorAll(".delete-form").forEach(form => {
        form.addEventListener("submit", e => {
            if (!confirm("Delete this area?")) {
                e.preventDefault();
            }
        });
    });
});
