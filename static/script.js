// 🔍 Scan Emails Button
function startScan() {
    const btn = document.getElementById("scanBtn");
    const loader = document.getElementById("loader");

    btn.disabled = true;
    btn.innerHTML = "Scanning...";
    if (loader) loader.style.display = "block";

    fetch("/scan", { method: "POST" })
        .then(res => {
            if (!res.ok) {
                throw new Error("Scan failed");
            }
            return res.json();
        })
        .then(data => {
            btn.disabled = false;
            btn.innerHTML = "Scan Emails";
            if (loader) loader.style.display = "none";

            alert(data.status || "Scan completed successfully");
            location.reload();
        })
        .catch(err => {
            btn.disabled = false;
            btn.innerHTML = "Scan Emails";
            if (loader) loader.style.display = "none";

            alert("Scan failed. Please try again.");
            console.error(err);
        });
}

// 🗑 Delete Mail
function deleteMail(id) {
    if (!confirm("Are you sure you want to delete this email?")) return;

    fetch(`/delete/${id}`, { method: "POST" })
        .then(res => {
            if (!res.ok) {
                throw new Error("Delete failed");
            }
            return res.json();
        })
        .then(() => {
            alert("Mail deleted successfully");
            location.reload();
        })
        .catch(err => {
            alert("Failed to delete mail");
            console.error(err);
        });
}

// 👁 View Mail Modal
function viewMail(body, from, status) {
    document.getElementById("modalFrom").innerText = from;
    document.getElementById("modalStatus").innerText = status;
    document.getElementById("modalBody").innerText = body;

    const modal = document.getElementById("mailModal");
    modal.style.display = "flex";   // ✅ ensures center alignment
}

// ❌ Close Modal
function closeModal() {
    document.getElementById("mailModal").style.display = "none";
}

function viewMailFromBtn(btn) {
    const body = btn.getAttribute("data-body");
    const from = btn.getAttribute("data-from");
    const status = btn.getAttribute("data-status");

    document.getElementById("modalFrom").innerText = from;
    document.getElementById("modalStatus").innerText = status;
    document.getElementById("modalBody").innerText = body;

    document.getElementById("mailModal").style.display = "flex";
}
