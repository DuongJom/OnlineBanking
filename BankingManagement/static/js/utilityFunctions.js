function onClose(){
    document.getElementById("alert").style.display = "none";
}

function goBack() {
  window.history.back();
}

const toggle = () => {
    const mainDropdown = document.getElementById("mainDropdown");
    const right = document.getElementById("right-arrow");
    const down = document.getElementById("down-arrow");

    mainDropdown.classList.toggle('hidden');
    right.classList.toggle('hidden');
    down.classList.toggle('hidden');
}

document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggleButton');
    const dropdownList = document.getElementById('mainDropdown');
  
    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
      const targetElement = event.target;
  
      if (!dropdownList.contains(targetElement) && !toggleButton.contains(targetElement)) {
        dropdownList.classList.add('hidden');
      }
    });
  });