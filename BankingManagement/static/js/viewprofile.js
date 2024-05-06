const card_info_toggle = () => {
    const card_info = document.getElementById("cardInfo");
    const right = document.getElementById("card_right_arrow");
    const down = document.getElementById("card_down_arrow");

    card_info.classList.toggle('hidden');
    right.classList.toggle('hidden');
    down.classList.toggle('hidden');
}

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