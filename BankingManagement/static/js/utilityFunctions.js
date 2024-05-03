function onClose(){
    document.getElementById("alert").style.display = "none";
}

toggle = () => {
    console.log("click");
    const mainDropdown = document.getElementById("mainDropdown");
    const right = document.getElementById("right-arrow");
    const down = document.getElementById("down-arrow");

    mainDropdown.classList.toggle('hidden');
    right.classList.toggle('hidden');
    down.classList.toggle('hidden');
}