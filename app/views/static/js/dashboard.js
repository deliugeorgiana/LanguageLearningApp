document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    const savedTheme = localStorage.getItem("theme") || "light";
    body.classList.add(savedTheme + "-mode");

    const toggleBtn = document.createElement("button");
    toggleBtn.textContent = savedTheme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
    toggleBtn.className = "btn btn-sm btn-secondary position-fixed";
    toggleBtn.style.top = "1rem";
    toggleBtn.style.right = "1rem";
    toggleBtn.style.zIndex = "9999";

    toggleBtn.onclick = () => {
        const newTheme = body.classList.contains("dark-mode") ? "light" : "dark";
        body.classList.remove("dark-mode", "light-mode");
        body.classList.add(newTheme + "-mode");
        toggleBtn.textContent = newTheme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
        localStorage.setItem("theme", newTheme);
    };

    document.body.appendChild(toggleBtn);
});
