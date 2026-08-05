const passwordInput = document.getElementById("passwordInput");
const togglePassword = document.getElementById("togglePassword");
const analyzeButton = document.getElementById("analyzeButton");

const analysisResult = document.getElementById("analysisResult");
const strengthFill = document.getElementById("strengthFill");
const strengthText = document.getElementById("strengthText");
const securityChecklist = document.getElementById("securityChecklist");
const improvedPasswords = document.getElementById("improvedPasswords");

const tipsDialog = document.getElementById("tipsDialog");
const tipsButton = document.getElementById("tipsButton");
const closeDialog = document.getElementById("closeDialog");

const generateButton = document.getElementById("generateButton");
const loading = document.getElementById("loading");
const generatedBox = document.getElementById("generatedBox");
const generatedPassword = document.getElementById("generatedPassword");
const copyPassword = document.getElementById("copyPassword");

const warningText = document.getElementById("warningText");
const errorMessage = document.getElementById("errorMessage");


/* --- Toggle Password --- */

togglePassword.addEventListener("click", () => {

    const isHidden = passwordInput.type === "password";

    passwordInput.type = isHidden ? "text" : "password";

    togglePassword.innerHTML = `
        <i data-lucide="${isHidden ? "eye-off" : "eye"}"></i>
    `;

    lucide.createIcons();

});


/* --- Password Tips --- */

tipsButton.addEventListener("click", () => {

    tipsDialog.showModal();

});

closeDialog.addEventListener("click", () => {

    tipsDialog.close();

});

tipsDialog.addEventListener("click", (event) => {

    if (event.target === tipsDialog) {

        tipsDialog.close();

    }

});


/* --- Analyze Password --- */

analyzeButton.addEventListener("click", async () => {

    const password = passwordInput.value.trim();

    errorMessage.style.display = "none";
    errorMessage.textContent = "";

    if (!password) {
        errorMessage.textContent = "Please enter a password.";
        errorMessage.style.display = "block";
        analysisResult.style.display = "none";
        return;
    }

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                password: password
            })

        });

        if (!response.ok) {

            const error = await response.json();

            errorMessage.textContent = error.error;
            errorMessage.style.display = "block";

            return;

        }

        const data = await response.json();

        errorMessage.style.display = "none";
        errorMessage.textContent = "";
        analysisResult.style.display = "block";

        updateStrength(data.score, data.strength);
        if (data.warning) {
            warningText.classList.add("show");
            warningText.innerHTML = `
        <i data-lucide="triangle-alert"></i>
        ${data.warning}
    `;
        } else {
            warningText.classList.remove("show");
            warningText.innerHTML = "";
        }

        lucide.createIcons();

        renderChecklist(data.checks);

        renderSuggestions(data.suggestions);

    } catch (error) {

        console.error(error);

        errorMessage.textContent = "Something went wrong. Please try again.";
        errorMessage.style.display = "block";
    }

});

passwordInput.addEventListener("keypress", function (event) {

    if (event.key === "Enter") {

        analyzeButton.click();

    }

});

/* --- UI Functions --- */

function updateStrength(score, strength) {

    strengthFill.style.width = `${score}%`;
    strengthFill.style.backgroundColor = strength.color;

    strengthText.innerHTML = `
        <strong>${strength.text}</strong><br>
        ${score}%
    `;
}


function renderChecklist(checks) {

    securityChecklist.innerHTML = "";

    const items = [

        {
            text: "At least 8 characters",
            valid: checks.length
        },

        {
            text: "Contains uppercase letters",
            valid: checks.uppercase
        },

        {
            text: "Contains lowercase letters",
            valid: checks.lowercase
        },

        {
            text: "Contains numbers",
            valid: checks.number
        },

        {
            text: "Contains special characters",
            valid: checks.special
        }

    ];

    items.forEach(item => {

        securityChecklist.innerHTML += `

            <div class="check-item">

                <i
                    data-lucide="${item.valid ? "check-circle" : "x-circle"}"
                    class="${item.valid ? "check-success" : "check-fail"}">
                </i>

                <span>${item.text}</span>

            </div>

        `;

    });

    lucide.createIcons();

}

function renderSuggestions(suggestions) {

    improvedPasswords.innerHTML = "";

    if (suggestions.length === 0) {
        improvedPasswords.parentElement.style.display = "none";
        return;
    }

    improvedPasswords.parentElement.style.display = "block";

    suggestions.forEach(password => {

        improvedPasswords.innerHTML += `

            <div class="password-suggestion">

                <code>${password}</code>

                <button
                    class="suggestion-copy"
                    data-password="${password}">

                    <i data-lucide="copy"></i>

                </button>

            </div>

        `;

    });

    lucide.createIcons();

    document.querySelectorAll(".suggestion-copy").forEach(button => {

        button.addEventListener("click", async () => {

            await navigator.clipboard.writeText(button.dataset.password);

            button.innerHTML = `
                <i data-lucide="check"></i>
            `;

            lucide.createIcons();

            setTimeout(() => {

                button.innerHTML = `
                    <i data-lucide="copy"></i>
                `;

                lucide.createIcons();

            }, 1500);

        });

    });

}
/* --- Password Generator --- */

generateButton.addEventListener("click", async () => {

    generatedBox.style.display = "none";
    loading.style.display = "flex";

    try {

        const response = await fetch("/generate", {
            method: "POST"
        });

        if (!response.ok) {

            throw new Error("Failed to generate password.");

        }

        const data = await response.json();

        setTimeout(() => {

            loading.style.display = "none";
            generatedBox.style.display = "flex";

            generatedPassword.value = data.password;

        }, 1200);

    } catch (error) {

        console.error(error);

        loading.style.display = "none";

        alert("Something went wrong. Please try again.");

    }

});


/* --- Copy Password --- */

copyPassword.addEventListener("click", async () => {

    if (!generatedPassword.value) return;

    await navigator.clipboard.writeText(generatedPassword.value);

    copyPassword.classList.add("copied");

    copyPassword.innerHTML = `
        <i data-lucide="check"></i>
        <span>Copied</span>
    `;

    lucide.createIcons();

    setTimeout(() => {

        copyPassword.classList.remove("copied");

        copyPassword.innerHTML = `
            <i data-lucide="copy"></i>
            <span>Copy</span>
        `;

        lucide.createIcons();

    }, 2000);

});


/* --- Lucide Icons --- */

lucide.createIcons();