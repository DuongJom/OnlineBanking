function onClose(){
    document.getElementById("alert").style.display = "none";
}

function goBack() {
  window.history.back();
}

function toggle() {
    const toggledElement = document.getElementById('toggled_element');

    toggledElement.classList.toggle('flex');
    toggledElement.classList.toggle('hidden');
}

function navBarToggle () {
    const mainDropdown = document.getElementById("mainDropdown");
    const right = document.getElementById("navbar_right_arrow");
    const down = document.getElementById("navbar_down_arrow");

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

