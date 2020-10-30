// Checked
let newPassword1 = document.querySelector('#id_new_password1')
let newPassword2 = document.querySelector('#id_new_password2')
let reset = document.querySelector('button')
let body = document.querySelector('body')

body.addEventListener('input', (e) => {
    if (e.target === newPassword1 || e.target === newPassword2){
        if (newPassword1.value.length > 0 && newPassword2.value.length > 0){
            reset.classList.add('button-fadeIn')
        }else{
            reset.classList.remove('button-fadeIn')
        }
    }
})

body.addEventListener('mouseover', (e) => {
    if (e.target === reset){
        reset.classList.add('button-hover')
    }
})

body.addEventListener('mouseout', (e) => {
    if (e.target === reset){
        reset.classList.remove('button-hover')
    }
})