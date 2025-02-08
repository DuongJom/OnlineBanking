let current_step = 1;
let hightlight_color = 'bg-green-200';

const form_step1 = document.getElementById("form-step1");
const form_step2 = document.getElementById("form-step2");
const form_step3 = document.getElementById("form-step3");
const form_step4 = document.getElementById("form-step4");
const form_step5 = document.getElementById("form-step5");

const process_bar_step1 = document.getElementById("process_bar_step1");
const process_bar_step2 = document.getElementById("process_bar_step2");
const process_bar_step3 = document.getElementById("process_bar_step3");
const process_bar_step4 = document.getElementById("process_bar_step4");
const process_bar_step5 = document.getElementById("process_bar_step5");

function isValidEmail(email) {
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return regex.test(email);
}

function isValidInternationalPhone(phone) {
    const regex = /^\+?[0-9]{7,15}$/;
    return regex.test(phone);
}

function isRadioSelected(name) {
    return !!document.querySelector(`input[name="${name}"]:checked`);
}

function checkRequiredField(step) {
    let isValid = true;
    const inputFields = document.querySelectorAll(`.step-${step}`);
    inputFields.forEach(inputField => {
        const errorAlert = document.getElementById(`${inputField.name}Error`);
        if(inputField.value.trim() === "") {
            errorAlert.textContent = `Please provide your ${inputField.name}`;
            isValid = false;
        }else {
            errorAlert.textContent = "";
        }
    });

    if(step === 2) {
        const genderError = document.getElementById('genderError');
        genderError.textContent = "";
        if(!isRadioSelected('gender')) {
            isValid = false;
            genderError.textContent = "Please select your gender.";
        }
    }

    if(step === 4) {
        const loginMethodError = document.getElementById('loginMethodError');
        const transferMethodError = document.getElementById('transferMethodError');
        const branchError = document.getElementById('branchError');

        loginMethodError.textContent = "";
        transferMethodError.textContent = "";
        branchError.textContent = "";

        if(document.querySelectorAll('input[name="loginMethod"]:checked').length == 0) {
            isValid = false;
            loginMethodError.textContent = "*";
        }

        if(document.querySelectorAll('input[name="transferMethod"]:checked').length == 0) {
            isValid = false;
            transferMethodError.textContent = "*";
        }

        if(document.getElementById('branch').value == -1) {
            isValid = false;
            branchError.textContent = "Please select your account branch";
        }
    }

    return isValid;
}

function validateStep(step) {
    let isValid = true;
    if(checkRequiredField(step)) {
        if(step === 1) {     
            const confirmPasswordError = document.getElementById('confirmPasswordError'); 
            confirmPasswordError.textContent = "";
            if (document.getElementById('password').value != document.getElementById('confirmPassword').value) {
                isValid = false;
                confirmPasswordError.textContent = "Those passwords didn't match. Try again.";
            }
        }

        if(step === 2) {
            const emailError = document.getElementById('emailError');
            const phoneError = document.getElementById('phoneError');
            emailError.textContent = "";
            phoneError.textContent = "";
            if(!isValidEmail(document.getElementById('email').value)) {
                isValid = false;
                emailError.textContent = "Your email is invalid. Try again.";
            }

            if(!isValidInternationalPhone(document.getElementById('phone').value)) {
                isValid = false;
                phoneError.textContent = "Your phone is invalid. Try again.";
            }
        }
    }else {
        isValid = false
    }

    return isValid;
}

function fillStepFiveContent () {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const branchSelect = document.getElementById('branch');
    const branchName = branchSelect.options[branchSelect.selectedIndex].innerHTML;

    const reUsername = document.getElementById('reUsername');
    const reEmail = document.getElementById('reEmail');
    const rePhone = document.getElementById('rePhone');
    const reBranchName = document.getElementById('reBranch');

    reUsername.innerHTML = username;
    reEmail.innerHTML = email;
    rePhone.innerHTML = phone;
    reBranchName.innerHTML = branchName;
}

function goNextStep() {
    if(current_step === 1) {
        if(validateStep(current_step)) {
            form_step1.classList.remove('flex');
            form_step1.classList.add('hidden');
            form_step2.classList.add('opacity-100');
            form_step2.classList.remove('hidden');
            form_step2.classList.add('flex');
            process_bar_step1.classList.remove(hightlight_color);
            process_bar_step2.classList.add(hightlight_color);
            current_step++;
        }
    }else if (current_step === 2) {
        if(validateStep(current_step)) {
            form_step2.classList.remove('flex');
            form_step2.classList.add('hidden');
            form_step2.classList.remove('opacity-100');
            form_step3.classList.add('opacity-100');
            form_step3.classList.remove('hidden');
            form_step3.classList.add('flex');
            process_bar_step2.classList.remove(hightlight_color);
            process_bar_step3.classList.add(hightlight_color);
            current_step++;
        }
    }else if (current_step === 3) {
        if(validateStep(current_step)) {
            form_step3.classList.remove('flex');
            form_step3.classList.add('hidden');
            form_step3.classList.remove('opacity-100');
            form_step4.classList.add('opacity-100');
            form_step4.classList.remove('hidden');
            form_step4.classList.add('flex');
            process_bar_step3.classList.remove(hightlight_color);
            process_bar_step4.classList.add(hightlight_color);
            current_step++;
        }
    }else {
        if(validateStep(current_step)) {
            form_step4.classList.remove('flex');
            form_step4.classList.add('hidden');
            fillStepFiveContent ();
            form_step3.classList.remove('opacity-100');
            form_step4.classList.add('opacity-100');
            form_step5.classList.remove('hidden');
            form_step5.classList.add('flex');
            process_bar_step4.classList.remove(hightlight_color);
            process_bar_step5.classList.add(hightlight_color);
            current_step++;
        }
    }
}

function goPreviousStep() {
    if(current_step === 5) {
        form_step5.classList.remove('flex');
        form_step5.classList.add('hidden');
        form_step4.classList.remove('hidden');
        form_step4.classList.add('flex');
        process_bar_step5.classList.remove(hightlight_color);
        process_bar_step4.classList.add(hightlight_color);
        current_step--;
    }else if (current_step === 4) {
        form_step4.classList.remove('flex');
        form_step4.classList.add('hidden');
        form_step3.classList.remove('hidden');
        form_step3.classList.add('flex');
        process_bar_step4.classList.remove(hightlight_color);
        process_bar_step3.classList.add(hightlight_color);
        current_step--;
    }else if (current_step === 3) {
        form_step3.classList.remove('flex');
        form_step3.classList.add('hidden');
        form_step2.classList.remove('hidden');
        form_step2.classList.add('flex');
        process_bar_step3.classList.remove(hightlight_color);
        process_bar_step2.classList.add(hightlight_color);
        current_step--;
    }else {
        form_step2.classList.remove('flex');
        form_step2.classList.add('hidden');
        form_step1.classList.remove('hidden');
        form_step1.classList.add('flex');
        process_bar_step2.classList.remove(hightlight_color);
        process_bar_step1.classList.add(hightlight_color);
        current_step--;
    } 
}