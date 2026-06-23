const passwordInput =
    document.getElementById("password");

const toggleButton =
    document.getElementById("togglePassword");

const strengthMessage =
    document.getElementById("strengthMessage");


if (passwordInput && toggleButton) {

    toggleButton.addEventListener("click", function () {

        if (passwordInput.type === "password") {

            passwordInput.type = "text";
            toggleButton.textContent = "Hide";

        } else {

            passwordInput.type = "password";
            toggleButton.textContent = "Show";

        }

    });

}

if (passwordInput && strengthMessage) {

    passwordInput.addEventListener("input", function () {

        const password = passwordInput.value;

        if (password.length < 8) {

            strengthMessage.textContent =
                "🔴 Weak Password";

        }

        else if (
            password.match(/[A-Z]/) &&
            password.match(/[a-z]/) &&
            password.match(/[0-9]/) &&
            password.match(/[^A-Za-z0-9]/)
        ) {

            strengthMessage.textContent =
                "🟢 Strong Password";

        }

        else {

            strengthMessage.textContent =
                "🟡 Medium Password";

        }

    });

}