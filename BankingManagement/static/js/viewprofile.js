document.addEventListener("DOMContentLoaded", () => {
    const moreBtn = document.getElementById("moreBtn");
    const cardinfo = document.getElementById("cardInfo");
    const right = document.getElementById("right-arrowv");
    const down = document.getElementById("down-arrowv");

    moreBtn.addEventListener('click', () => {
        cardinfo.classList.toggle('hidden');
        right.classList.toggle('hidden');
        down.classList.toggle('hidden');
    })
})