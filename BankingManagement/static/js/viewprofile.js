const toggleCardInfo = () => {
    const cardInfo = document.getElementById("cardInfo");
    const right = document.getElementById("card_right_arrow");
    const down = document.getElementById("card_down_arrow");

    cardInfo.classList.toggle('hidden');
    right.classList.toggle('hidden');
    down.classList.toggle('hidden');
}

const closePopup = () => {
    const popups = document.querySelectorAll(".popup");

    popups.forEach(popup => {
        popup.classList.add('hidden');
    });
}

const openPopup = () => {
    const popups = document.querySelectorAll(".popup");

    popups.forEach(popup => {
        popup.classList.remove('hidden');
        popup.classList.add('flex');
    });
}