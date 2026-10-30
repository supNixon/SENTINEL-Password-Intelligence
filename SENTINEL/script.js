
// ==========================================
// SENTINEL - CYBERSECURITY INTELLIGENCE
// Frontend password analysis engine
// ==========================================

let history = [];

const commonPasswords = [
    "password", "password123", "123456",
    "12345678", "qwerty", "admin",
    "welcome", "letmein", "abc123",
    "iloveyou", "sunshine"
];

const sequences = [
    "1234", "abcd", "qwerty",
    "asdf", "zxcv", "9876"
];

// ==========================================
// PAGE NAVIGATION
// ==========================================

function showPage(pageId) {

    document.querySelectorAll(".page").forEach(page => {
        page.classList.remove("active");
    });

    document.querySelectorAll(".nav-item").forEach(button => {
        button.classList.remove("active");
    });

    document.getElementById(pageId).classList.add("active");

    const activeButton = document.querySelector(
        `[data-page="${pageId}"]`
    );

    if (activeButton) {
        activeButton.classList.add("active");
    }

    const names = {
        dashboard: "DASHBOARD",
        analyzer: "PASSWORD ANALYZER",
        learning: "CYBER LEARNING",
        about: "ABOUT PROJECT"
    };

    document.getElementById("pageName").textContent =
        names[pageId];

    document.getElementById("welcomeTitle").textContent =
        pageId === "dashboard" ? "Security Overview" :
        pageId === "analyzer" ? "Password Analysis" :
        pageId === "learning" ? "Cyber Learning Hub" :
        "Project Information";
}

document.querySelectorAll(".nav-item").forEach(button => {

    button.addEventListener("click", () => {
        showPage(button.dataset.page);
    });

});

// ==========================================
// SHOW / HIDE PASSWORD
// ==========================================

document.getElementById("togglePassword")
.addEventListener("click", function() {

    const input = document.getElementById("password");

    if (input.type === "password") {
        input.type = "text";
        this.textContent = "HIDE";
    } else {
        input.type = "password";
        this.textContent = "SHOW";
    }

});

// ==========================================
// PASSWORD ANALYSIS
// ==========================================

function analyzePassword() {

    const password = document.getElementById("password").value;

    if (!password) {
        alert("Please enter a sample password.");
        return;
    }

    const result = calculateStrength(password);

    displayResults(result);

    saveActivity(result);

    updateDashboard();

}

// ==========================================
// FEATURE EXTRACTION
// ==========================================

function calculateStrength(password) {

    const length = password.length;

    const lowercase = /[a-z]/.test(password);
    const uppercase = /[A-Z]/.test(password);
    const numbers = /[0-9]/.test(password);
    const special = /[^A-Za-z0-9]/.test(password);

    const characterClasses = [
        lowercase, uppercase, numbers, special
    ].filter(Boolean).length;

    const repeated = /(.)\1{2,}/.test(password);

    const lowerPassword = password.toLowerCase();

    const common = commonPasswords.includes(lowerPassword);

    const sequence = sequences.some(item =>
        lowerPassword.includes(item)
    );

    const uniqueRatio =
        new Set(password).size / Math.max(length, 1);

    // Character pool estimation
    let pool = 0;

    if (lowercase) pool += 26;
    if (uppercase) pool += 26;
    if (numbers) pool += 10;
    if (special) pool += 33;

    // Shannon-style maximum search-space estimate
    const entropy = pool > 0
        ? length * Math.log2(pool)
        : 0;

    // ======================================
    // RULE-BASED SCORE
    // ======================================

    const lengthPoints = Math.min(30, length * 2.5);

    const varietyPoints = characterClasses * 8;

    let patternPoints = 20;

    if (repeated) patternPoints -= 18;
    if (sequence) patternPoints -= 16;
    if (common) patternPoints -= 25;

    const entropyPoints = Math.min(22, entropy / 3);

    const score = Math.round(
        Math.max(0, Math.min(100,
            lengthPoints +
            varietyPoints +
            patternPoints +
            entropyPoints
        ))
    );

    // ======================================
    // CLASSIFICATION
    // ======================================

    let strength;

    if (score < 25) {
        strength = "Very Weak";
    }
    else if (score < 42) {
        strength = "Weak";
    }
    else if (score < 62) {
        strength = "Moderate";
    }
    else if (score < 82) {
        strength = "Strong";
    }
    else {
        strength = "Very Strong";
    }

    // ======================================
    // ML-STYLE DEMONSTRATION
    // ======================================
    // This is a feature-based heuristic, not
    // a trained machine-learning classifier.

    let prediction = strength;

    let confidence = Math.min(
        99,
        65 + Math.abs(score - 50) * 0.5
    );

    // ======================================
    // SECURITY CHECKS
    // ======================================

    const checks = [
        {
            name: "Minimum 12 characters",
            passed: length >= 12
        },
        {
            name: "Lowercase letters",
            passed: lowercase
        },
        {
            name: "Uppercase letters",
            passed: uppercase
        },
        {
            name: "Numbers",
            passed: numbers
        },
        {
            name: "Special characters",
            passed: special
        },
        {
            name: "No repeated character runs",
            passed: !repeated
        },
        {
            name: "No predictable sequence",
            passed: !sequence
        },
        {
            name: "Not an exact common password",
            passed: !common
        }
    ];

    // ======================================
    // RISK DETECTION
    // ======================================

    const risks = [];

    if (length < 12)
        risks.push("Password is shorter than 12 characters.");

    if (common)
        risks.push("Password matches a common password.");

    if (sequence)
        risks.push("Predictable sequence detected.");

    if (repeated)
        risks.push("Repeated character pattern detected.");

    if (characterClasses < 3)
        risks.push("Low character category diversity.");

    // ======================================
    // RECOMMENDATION ENGINE
    // ======================================

    const recommendations = [];

    if (length < 12) {
        recommendations.push(
            "Increase password length to at least 12-16 characters."
        );
    }

    if (characterClasses < 3) {
        recommendations.push(
            "Use a wider mix of character types where practical."
        );
    }

    if (common || sequence) {
        recommendations.push(
            "Avoid common words, dates and predictable sequences."
        );
    }

    if (repeated) {
        recommendations.push(
            "Replace repeated characters with unpredictable characters."
        );
    }

    if (uniqueRatio < 0.5) {
        recommendations.push(
            "Reduce excessive character repetition."
        );
    }

    recommendations.push(
        "Use a unique password for every account."
    );

    recommendations.push(
        "Enable multi-factor authentication (MFA)."
    );

    recommendations.push(
        "Use a reputable password manager."
    );

    return {
        score,
        strength,
        entropy: entropy.toFixed(1),
        prediction,
        confidence: confidence.toFixed(0),
        checks,
        risks,
        recommendations
    };

}

// ==========================================
// DISPLAY RESULTS
// ==========================================

function displayResults(result) {

    document.getElementById("results")
        .classList.remove("hidden");

    document.getElementById("score").textContent =
        result.score;

    document.getElementById("strength").textContent =
        result.strength;

    document.getElementById("entropy").textContent =
        result.entropy;

    document.getElementById("prediction").textContent =
        result.prediction;

    document.getElementById("confidence").textContent =
        "Heuristic estimate: " + result.confidence + "% (not ML probability)";

    const bar = document.getElementById("scoreBar");

    bar.style.width = result.score + "%";

    if (result.score < 42) {
        bar.style.background = "#ff7185";
    }
    else if (result.score < 62) {
        bar.style.background = "#ffc76a";
    }
    else {
        bar.style.background = "#41e0b5";
    }

    // Security checks
    const checksContainer = document.getElementById("checks");

    checksContainer.innerHTML = "";

    result.checks.forEach(check => {

        const row = document.createElement("div");

        row.className = "check-row " +
            (check.passed ? "good" : "bad");

        row.textContent =
            (check.passed ? "✓ " : "✕ ") + check.name;

        checksContainer.appendChild(row);

    });

    // Risk indicators
    const risksContainer = document.getElementById("risks");

    risksContainer.innerHTML = "";

    if (result.risks.length === 0) {

        const safe = document.createElement("p");
        safe.className = "good";
        safe.textContent = "✓ No obvious risks detected.";

        risksContainer.appendChild(safe);

    } else {

        result.risks.forEach(risk => {

            const row = document.createElement("div");

            row.className = "risk-row warning";
            row.textContent = "⚠ " + risk;

            risksContainer.appendChild(row);

        });

    }

    // Recommendations
    const recommendationContainer =
        document.getElementById("recommendations");

    recommendationContainer.innerHTML = "";

    result.recommendations.forEach(rec => {

        const row = document.createElement("div");

        row.className = "rec-row";
        row.textContent = "✧ " + rec;

        recommendationContainer.appendChild(row);

    });

}

// ==========================================
// ACTIVITY LOG
// ==========================================

function saveActivity(result) {

    history.push({
        time: new Date().toLocaleTimeString(),
        strength: result.strength,
        score: result.score
    });

}

// ==========================================
// UPDATE DASHBOARD
// ==========================================

function updateDashboard() {

    document.getElementById("totalAnalyses")
        .textContent = history.length;

    const strongCount = history.filter(item =>
        item.score >= 62
    ).length;

    document.getElementById("strongCount")
        .textContent = strongCount;

    const average = history.length
        ? Math.round(
            history.reduce((sum, item) =>
                sum + item.score, 0
            ) / history.length
        )
        : 0;

    document.getElementById("averageScore")
        .textContent = history.length ? average : "--";

    const activity = document.getElementById("activityList");

    activity.innerHTML = "";

    if (history.length === 0) {

        activity.innerHTML =
            '<p class="empty">No analysis performed yet.</p>';

        return;

    }

    history.slice(-5).reverse().forEach(item => {

        const row = document.createElement("div");

        row.className = "activity-row";

        const left = document.createElement("span");
        left.textContent = item.time + " | " + item.strength;

        const right = document.createElement("b");
        right.textContent = item.score + "/100";

        row.append(left, right);
        activity.appendChild(row);

    });

}

// Initial dashboard state
updateDashboard();
