// Checked
var li = document.querySelectorAll('li')
var loginBtn = document.querySelector('.login')
var signUpBtn = document.querySelector('.sign-up')
var modal = document.querySelector('.modal')
var modalContent = document.querySelector('.modal-content')

// Login Inputs
let username
let password
let submit
let passwordResetEmail

// Async Functions
async function loginFormAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function passwordResetFormAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function loginAW(formData, url, method, csrfmiddlewaretoken){
    const result = await fetch(url, {method: method, headers: {'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = result.json()
    return data
}

// Functions

function usernameFocusHover(){
    this.classList.add('input-hover')
}

function usernameFocusHoverOut(){
    this.classList.remove('input-hover')
}

// Links
for (let i = 0; i < li.length; i++) {
    li[i].addEventListener('mouseover', function(){
        this.classList.add('hover-over')
})
    li[i].addEventListener('mouseout', function(){
        this.classList.remove('hover-over')
    })
  }



if (loginBtn){
    loginBtn.addEventListener('click', (e) => {
        e.preventDefault()
        e.stopPropagation()
        e.target.classList.add('login-btn-hide')
        const url = e.target.getAttribute('data-url')
        loginFormAW(url)
        .then(data => {
            modal.classList.add('modal-show')
            modalContent.innerHTML = data['html']
            username = document.querySelector('#id_username')
            password = document.querySelector('#id_password')
            submit = document.querySelector('button[type=submit]')
        })
    })
}



if (modal){
    modal.addEventListener('click', (e) =>{
        if (e.target == modal){
            modal.classList.remove('modal-show')
            loginBtn.classList.remove('login-btn-hide')
        }

        if (e.target.classList.contains('password-reset')){
            e.preventDefault()
            e.stopPropagation()
            passwordResetFormAW(e.target.href)
            .then(data => {
                modalContent.innerHTML = data['html']
                passwordResetEmail = document.querySelector('#id_email')
                submit = document.querySelector('button[type=submit]')
            })
        }

        if (e.target.classList.contains('new-password-reset')){
            e.preventDefault()
            e.stopPropagation()
            passwordResetFormAW(e.target.href)
            .then(data => {
                modalContent.innerHTML = data['html']
                passwordResetEmail = document.querySelector('#id_email')
                submit = document.querySelector('button[type=submit]')
            })
        }

        if (e.target.classList.contains('continue')){
            let url = e.target.getAttribute('data-url')
            loginFormAW(url)
            .then(data => {
                modalContent.innerHTML = data['html']
                username = document.querySelector('#id_username')
                password = document.querySelector('#id_password')
                submit = document.querySelector('button[type=submit]')
            })
        }

    })

    modal.addEventListener('input', (e) => {
        if (e.target === username || e.target === password){
            if (username.value.length > 0 && password.value.length > 0){
                submit.classList.add('button-fadeIn')
            }else{
                submit.classList.remove('button-fadeIn')
            }
        }

        if (e.target === passwordResetEmail){
            if (passwordResetEmail.value.length > 0 && passwordResetEmail.value.search('@') !== -1){
                submit.classList.add('button-fadeIn')
            }else{
                submit.classList.remove('button-fadeIn')
            }
        }
    })

    modal.addEventListener('mouseover', (e) => {
        if (e.target == submit){
            submit.classList.add('button-hover')
        }

        if (e.target.nodeName === 'A'){
            e.target.classList.add('update-password-hover')
        }

        if (e.target.classList.contains('new-password-reset')){
            e.target.classList.add('new-password-reset-hover')
        }

        if (e.target.classList.contains('continue')){
            e.target.classList.add('continue-hover')
        }
    })

    modal.addEventListener('mouseout', (e) => {
        if (e.target == submit){
            submit.classList.remove('button-hover')
        }

        if (e.target.nodeName === 'A'){
            e.target.classList.remove('update-password-hover')
        }

        if (e.target.classList.contains('new-password-reset')){
            e.target.classList.remove('new-password-reset-hover')
        }

        if (e.target.classList.contains('continue')){
            e.target.classList.remove('continue-hover')
        }
    })

    modal.addEventListener('submit', (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.target.nodeName === 'FORM' && e.target.classList.contains('login-form')){
            let form = e.target
            let formData = new FormData(form)
            let url = form.action
            let method = form.method
            let csrfmiddlewaretoken = document.querySelector('input[type=hidden]').value
            loginAW(formData, url, method, csrfmiddlewaretoken)
            .then(data => {
                if (data['html']){
                    modalContent.innerHTML = data['html']
                    username = document.querySelector('#id_username')
                    password = document.querySelector('#id_password')
                    submit = document.querySelector('button[type=submit]')
                }else{
                    window.location.href = '/home/'
                }
            })
        }

        if (e.target.nodeName === 'FORM' && e.target.classList.contains('password-reset-form')){
            let form = e.target
            let formData = new FormData(form)
            let url = form.action
            let method = form.method
            let csrfmiddlewaretoken = document.querySelector('input[type=hidden]').value
            loginAW(formData, url, method, csrfmiddlewaretoken)
            .then(data => {
                if (data['html']){
                    modalContent.innerHTML = data['html']
                }
            })
        }

    })
}