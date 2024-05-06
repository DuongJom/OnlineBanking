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

const closepopup = () => {
    const popups = document.querySelectorAll(".popup");

    popups.forEach(popup => {
        popup.classList.add('hidden');
    });
}

const openpopup = () => {
    const popups = document.querySelectorAll(".popup");

    popups.forEach(popup => {
        popup.classList.remove('hidden');
    });
}