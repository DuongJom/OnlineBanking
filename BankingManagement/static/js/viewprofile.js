document.addEventListener("DOMContentLoaded", () => {
    const moreBtn = document.getElementById("moreBtn");
    const cardinfo = document.getElementById("cardInfo");
    const right = document.getElementById("right-arrow");
    const down = document.getElementById("down-arrow");

    moreBtn.addEventListener('click', () => {
        cardinfo.classList.toggle('hidden');
        right.classList.toggle('hidden');
        down.classList.toggle('hidden');
    })
})