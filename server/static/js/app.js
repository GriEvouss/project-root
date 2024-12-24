document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("#login-form");
    const registerForm = document.querySelector("#register-form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(loginForm);
            fetch("/login", {
                method: "POST",
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = "/dashboard";
                    } else {
                        alert(data.error || "Login failed. Please try again.");
                    }
                })
                .catch(err => console.error("Error:", err));
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(registerForm);
            fetch("/register", {
                method: "POST",
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = "/login";
                    } else {
                        alert(data.error || "Registration failed. Please try again.");
                    }
                })
                .catch(err => console.error("Error:", err));
        });
    }
});
