document.addEventListener("DOMContentLoaded", () => {
    const showMenuBtn = document.getElementById("showMenuBtn");
    const mainMenu = document.getElementById("mainMenu");

    showMenuBtn.addEventListener('click', () => {
        mainMenu.classList.toggle('hidden');
    })
})