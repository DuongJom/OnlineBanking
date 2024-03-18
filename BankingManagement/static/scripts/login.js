document.addEventListener('DOMContentLoaded', () => {
    const login_form = document.getElementById("login_form");
    login_form.addEventListener('submit', (e) => {
        e.preventDefault();
        const form = new FormData(login_form)

        fetch('/login', {
            method: "POST",
            body: form
        })
        .then(response => response.json())
        .then(data => {
           if(data.message == "Login successful") {
                window.location.href = "/"; 
           }else {
                const alert = document.getElementById("alert");
                alert.innerHTML = data.message;
                setTimeout(()=>{
                    alert.innerHTML = "";
                }, 2000)
           }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
)})