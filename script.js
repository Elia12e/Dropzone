const input = document.getElementById("file-input");
const status = document.getElementById("status");

input.addEventListener("change", function () {
    const selected = input.files[0];
    if (!selected) {
        status.textContent = "No file selected.";
        return;
    }

    if (!selected.name.toLowerCase().endsWith(".zip")) {
        status.textContent = "Please select a .zip file.";
        return;
    }
    const formattedSize = formatFileSize(selected.size);

    status.textContent = `Selected: ${selected.name} (${formattedSize})`;
});

function formatFileSize(bytes) {
    const sizeMB = bytes / 1_000_000;
    return `${sizeMB.toFixed(2)} MB`;
}
