
const form = document.querySelector("form");
const fileInput = document.querySelector("#file");
const actionSelect = document.querySelector("#action");
const passwordInput = document.querySelector("#password");

form.addEventListener("submit", function (event) {
    const selectedFile = fileInput.files[0];
    const password = passwordInput.value;

    if (!selectedFile) {
        event.preventDefault();
        alert("Please select a file.");
        return;
    }

    if (password.length < 8) {
        event.preventDefault();
        alert("Password must be at least 8 characters long.");
        return;
    }

    if (actionSelect.value === "decrypt" &&
        !selectedFile.name.endsWith(".enc")) {
        const confirmDecrypt = confirm(
            "This file does not have an .enc extension. Do you want to continue?"
        );

        if (!confirmDecrypt) {
            event.preventDefault();
        }
    }
});
