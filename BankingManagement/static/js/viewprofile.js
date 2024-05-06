document.addEventListener("DOMContentLoaded", () => {
    const moreBtn = document.getElementById("moreBtn");
    const card_info = document.getElementById("cardInfo");
    const right = document.getElementById("right-arrowv");
    const down = document.getElementById("down-arrowv");

    moreBtn.addEventListener('click', () => {
        card_info.classList.toggle('hidden');
        right.classList.toggle('hidden');
        down.classList.toggle('hidden');
    })
})

const close_popup = () => {
    const popups = document.querySelectorAll(".popup");

    popups.forEach(popup => {
        popup.classList.add('hidden');
    });
}

const open_popup = () => {
    const popups = document.querySelectorAll(".popup");

    popups.forEach(popup => {
        popup.classList.remove('hidden');
        popup.classList.add('flex');
    });
}