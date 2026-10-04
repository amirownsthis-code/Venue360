document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const adminId = form.querySelector('input[name="admin_id"]');
    const password = form.querySelector('input[name="password"]');

    form.addEventListener("submit", function (e) {
        if (adminId.value.trim() === "" || password.value.trim() === "") {
            e.preventDefault();
            alert("Please enter admin ID and password!");
        }
    });
});
