const RegisterSteps = Object.freeze({
    LOGIN_INFO: 1,
    PERSONAL_INFO: 2,
    ADDRESS_INFO: 3,
    ACCOUNT_INFO: 4
});

let current_step = RegisterSteps.LOGIN_INFO;
const high_light_color = 'bg-green-200';
const form_lst = Array.from(
    { length: 5 },
    (_, i) => document.getElementById(`form-step${i + 1}`)
);
const process_bar_lst = Array.from(
    { length: 5 },
    (_, i) => document.getElementById(`process_bar_step${i + 1}`)
);
const isValidEmail = (email) => /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email);
const isValidInternationalPhone = (phone) => /^\+?[0-9]{7,15}$/.test(phone);
const isRadioSelected = (name) => !!document.querySelector(`input[name="${name}"]:checked`);

const checkRequiredField = (step) => {
    let isValid = true;
    const fields = document.querySelectorAll(`.step-${step}`);

    fields.forEach(field => {
        const errorEl = document.getElementById(`${field.name}Error`);
        if (!field.value.trim()) {
            errorEl.textContent = `Please provide your ${field.name}`;
            isValid = false;
        } else {
            errorEl.textContent = "";
        }
    });

    switch (step){
        case RegisterSteps.PERSONAL_INFO:
            const genderError = document.getElementById('genderError');
            genderError.textContent = isRadioSelected('gender') ? "" : "Please select your gender.";
            if (!isRadioSelected('gender')) isValid = false;
            break;
        case RegisterSteps.ACCOUNT_INFO:
            const loginSelected = document.querySelectorAll('input[name="loginMethod"]:checked').length > 0;
            const transferSelected = document.querySelectorAll('input[name="transferMethod"]:checked').length > 0;
            const branchValid = document.getElementById('branch').value !== "-1";

            document.getElementById('loginMethodError').textContent = loginSelected ? "" : "*";
            document.getElementById('transferMethodError').textContent = transferSelected ? "" : "*";
            document.getElementById('branchError').textContent = branchValid ? "" : "Please select your account branch";

            if (!loginSelected || !transferSelected || !branchValid) isValid = false;
            break;
    }

    return isValid;
};

// ===== Step Validation =====
const validateStep = (step) => {
    let isValid = true;

    if (!checkRequiredField(step)) return false;

    switch (step){
        case RegisterSteps.LOGIN_INFO:
            const pw = document.getElementById('password').value;
            const cpw = document.getElementById('confirmPassword').value;
            const errorEl = document.getElementById('confirmPasswordError');
            errorEl.textContent = (pw === cpw) ? "" : "Those passwords didn't match. Try again.";
            if (pw !== cpw) isValid = false;
            break;
        case RegisterSteps.PERSONAL_INFO:
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;

            const emailError = document.getElementById('emailError');
            const phoneError = document.getElementById('phoneError');

            emailError.textContent = isValidEmail(email) ? "" : "Your email is invalid. Try again.";
            phoneError.textContent = isValidInternationalPhone(phone) ? "" : "Your phone is invalid. Try again.";

            if (!isValidEmail(email) || !isValidInternationalPhone(phone)) isValid = false;
            break;
    }

    return isValid;
};

const fillStepFiveContent = () => {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const branchName = document.getElementById('branch').selectedOptions[0].innerHTML;

    document.getElementById('reUsername').innerHTML = username;
    document.getElementById('reEmail').innerHTML = email;
    document.getElementById('rePhone').innerHTML = phone;
    document.getElementById('reBranch').innerHTML = branchName;
};

const goNextStep = () => {
    if (!validateStep(current_step)) return;

    if (current_step === RegisterSteps.ACCOUNT_INFO) fillStepFiveContent();

    toggleStep(current_step, current_step + 1);
    current_step++;
};

const goPreviousStep = () => {
    toggleStep(current_step, current_step - 1);
    current_step--;
};

const toggleStep = (fromStep, toStep) => {
    const fromForm = form_lst[fromStep - 1];
    const toForm = form_lst[toStep - 1];
    const fromBar = process_bar_lst[fromStep - 1];
    const toBar = process_bar_lst[toStep - 1];

    fromForm.classList.remove("opacity-100", "scale-100", "flex");
    fromForm.classList.add("opacity-0", "scale-90");

    setTimeout(() => {
        fromForm.classList.add("hidden");
        toForm.classList.remove("opacity-0", "scale-90", "hidden");
        toForm.classList.add("flex");
    }, 300);

    fromBar.classList.remove(high_light_color);
    toBar.classList.add(high_light_color);
};