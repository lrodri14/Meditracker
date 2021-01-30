/* This main.js file contains all the variable declarations, async functions and sync functions needed for the main.html
   template to perform correctly.*/


///////////////////////////////////////////////// Variables ////////////////////////////////////////////////////////////

var body = document.querySelector('body')
var quoteContainer = document.querySelector('.quote-container')
var loginBtn = document.querySelector('#login-btn')
var signUpBtn = document.querySelector('#signup-btn')
var modal = document.querySelector('.modal')
var modalContent = document.querySelector('.modal-content')
var accountType = document.querySelector('.account-type-selector')

// Login Inputs
let username
let password
let passwordResetEmail

// Sign Up Inputs
let signUpInputs = []

// Submit Button
let submitBtn

///////////////////////////////////////////////// Functions ////////////////////////////////////////////////////////////


// Async Functions
async function loginFormAW(url){
    /* This loginFormAW function is used to display the login form dynamically, it takes a single argument: url which is
       used to make the request to the server, the response will be returned in JSON Format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function passwordResetFormAW(url){
    /* This passwordResetFormAw function is used to display the password reset form dynamically,  it takes a single
       argument: url which is used to make the request to the server, the response will be returned in JSON Format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function loginAW(formData, url, method, csrfmiddlewaretoken){
    /* This loginAW function is used to login the user and to display errors dynamically, this function expects 4 args
       formData, url, method, csrfmiddlewaretoken, these are the arguments we will use to make the POST request to the
       server, once we receive our response, we will return it in JSON Format.*/
    const result = await fetch(url, {method: method, headers: {'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = result.json()
    return data
}

async function signUpFormAW(url){
    /* This loginFormAW function is used to display the login form dynamically, it takes a single argument: url which is
       used to make the request to the server, the response will be returned in JSON Format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function signUpAW(formData, url, method, csrfmiddlewaretoken){
    /* This signUpAW function is used to signup the user and to display errors dynamically, this function expects 4 args
       formData, url, method, csrfmiddlewaretoken, these are the arguments we will use to make the POST request to the
       server, once we receive our response, we will return it in JSON Format.*/
    const result = await fetch(url, {method:method, headers:{'X-CSRFToken': csrfmiddlewaretoken}, body:formData})
    const data = result.json()
    return data
}

///////////////////////////////////////////////// Event Listeners //////////////////////////////////////////////////////

// Body Event Listeners
if (body){

    // Mouseover events
    body.addEventListener('mouseover', (e) => {
        /* This event will be fired every time the target contains the login or sign-up class in it's classList, it will
           add the hover-over class */
        if (e.target === loginBtn || e.target === signUpBtn){
            e.target.classList.add('auth-btn-hover')
        }

        /* This event will be fired every time the target contains the doctor-type or assistant-type class in it's
           classList, it will add the account-type-selector-hover class */
        if (e.target.classList.contains('doctor-type') || e.target.classList.contains('assistant-type')){
            e.target.classList.add('account-type-selector-hover')
        }
    })

    body.addEventListener('mouseout', (e) => {
        /* This event will be fired every time the target contains the login or sign-up class in it's classList, it will
           remove the hover-over class */
        if (e.target === loginBtn || e.target === signUpBtn){
            e.target.classList.remove('auth-btn-hover')
        }

        /* This event will be fired every time the target contains the doctor-type or assistant-type class in it's
           classList, it will remove the account-type-selector-hover class */
        if (e.target.classList.contains('doctor-type') || e.target.classList.contains('assistant-type')){
            e.target.classList.remove('account-type-selector-hover')
        }
    })

    body.addEventListener('click', (e) => {

        if (e.target === container){
            /* This event will be fired every time the target is the container, this event will show up all the hidden elements */
            loginBtn.classList.remove('auth-btn-hide')
            signUpBtn.classList.remove('auth-btn-hide')
            quoteContainer.classList.remove('quote-container-hide')
            accountType.classList.remove('account-type-selector-show')
        }

        /* This event will be fired every time the target contains the login class in its classList, it will hide the
           sign-up button and collect the url from the data-url attribute and make a request through the loginFormAW func,
           the response will be added to the modalContent and finally the modal will be displayed */
        if (e.target === loginBtn){
            loginBtn.classList.add('auth-btn-hide')
            signUpBtn.classList.add('auth-btn-hide')
            quoteContainer.classList.add('quote-container-hide')
            accountType.classList.remove('account-type-selector-show')
            const url = e.target.getAttribute('data-url')
            loginFormAW(url)
            .then(data => {
                modalContent.innerHTML = data['html']
                modal.classList.add('modal-show')
                username = document.querySelector('#id_username')
                password = document.querySelector('#id_password')
                submitBtn = document.querySelector('.login-submit-btn')
            })
        }

        /* This event will be fired every time the target contains the sign-up class in its classList, it will hide the
           login button, finally the accountType modal will be displayed */
        if (e.target === signUpBtn){
            signUpBtn.classList.add('auth-btn-hide')
            loginBtn.classList.add('auth-btn-hide')
            quoteContainer.classList.add('quote-container-hide')
            accountType.classList.add('account-type-selector-show')
        }
//        /* This event will be fired every time the target contains either the doctor-type or assistant-type class in its
//           classList, we collect the type from the data-type attribute and the url from the data-url attribute, we build
//           up our url and call the signUpFormAW function to make the request to the server, finally the response will be
//           added to the modalContent.innerHTML and the modal will be displayed.*/
        if (e.target.classList.contains('doctor-type') || e.target.classList.contains('assistant-type')){
            let type = e.target.getAttribute('data-type')
            let url = e.target.getAttribute('data-url') + '?account_type=' + type
            signUpFormAW(url)
            .then(data => {
                accountType.classList.remove('account-type-selector-show')
                modalContent.innerHTML = data['html']
                modal.classList.add('modal-show')
                signUpInputs = document.querySelectorAll('input,select')
                submitBtn = document.querySelector('.signup-submit-btn')
            })
        }
    })
}

// Modal Event Listeners
if (modal){

    // Click Event
    modal.addEventListener('click', (e) =>{
        /* This event will be fired every time the target is the modal, this event will hide the modal, and display the
           buttons.*/
        if (e.target === modal){
            modal.classList.remove('modal-show')
            loginBtn.classList.remove('auth-btn-hide')
            signUpBtn.classList.remove('auth-btn-hide')
            quoteContainer.classList.remove('quote-container-hide')
            accountType.classList.remove('account-type-selector-show')
        }

        /* This event will be fired every time the target contains the password-reset class in it's classList, this event
           will display the reset password form, we will collect the url from the anchor href attribute to make the request,
           the response will be added to the modalContent.innerHTMl*/
        if (e.target.classList.contains('password-reset')){
            e.preventDefault()
            e.stopPropagation()
            passwordResetFormAW(e.target.href)
            .then(data => {
                modalContent.innerHTML = data['html']
                passwordResetEmail = document.querySelector('#id_email')
                submitBtn = document.querySelector('.password-reset-submit-btn')
            })
        }

        /* This event will be fired every time the target contains the continue class in it's classList, this event
           will display the login form, we will collect the url from the data-url attribute to make the request,
           the response will be added to the modalContent.innerHTMl, this procedure will only be performed once a pass-
           word reset form has taken place.*/
        if (e.target.classList.contains('continue')){
            let url = e.target.getAttribute('data-url')
            loginFormAW(url)
            .then(data => {
                modalContent.innerHTML = data['html']
                username = document.querySelector('#id_username')
                password = document.querySelector('#id_password')
                submitBtn = document.querySelector('.login-submit-btn')
            })
        }

    })

    // Input Events
    modal.addEventListener('input', (e) => {

        /* This event will be fired every time an input is typed in the username or password elements, it will check if
           none of the elements.value is empty, if the condition is fulfilled, then the submit button will be displayed
           if not, it will be hidden.*/
        if (e.target === username || e.target === password){
            if (username.value.length > 0 && password.value.length > 0){
                submitBtn.classList.add('submit-btn-fade-in')
            }else{
                submitBtn.classList.remove('submit-btn-fade-in')
            }
        }

        /* This event will be fired every time an input is typed in the passwordResetEmail element, it will check if
           none of the elements.value is empty, if the condition is fulfilled, then the submit button will be displayed
           if not, it will be hidden.*/
        if (e.target === passwordResetEmail){
            if (passwordResetEmail.value.length > 0 && passwordResetEmail.value.search('@') !== -1){
                submitBtn.classList.add('submit-btn-fade-in')
            }else{
                submitBtn.classList.remove('submit-btn-fade-in')
            }
        }

        /* This event will be fired every time the target is an input or select field, this will check if all the inputs
           are not empty, if the condition is fulfilled the submit button will be displayed, otherwise it will be hidden.*/
        if (e.target.nodeName === 'INPUT' || e.target.nodeName === 'SELECT'){
            for (let i = 0; i<signUpInputs.length; i++){
                if (signUpInputs[i].value && signUpInputs.length - i === 1){
                    submitBtn.classList.add('submit-btn-fade-in')
                }else{
                   submitBtn.classList.remove('submit-btn-fade-in')
                }
            }
        }

    })

    // MouseOver events
    modal.addEventListener('mouseover', (e) => {

        // This event will be fired when the target is submit, the button-hover class will be added.
        if (e.target === submitBtn){
            submitBtn.classList.add('submit-btn-hover')
        }

        // This event will be fired when the target's nodeName is 'INPUT', the input-hover class will be added.
        if (e.target.nodeName === 'INPUT'){
            e.target.classList.add('input-hover')
        }

        // This event will be fired when the target's classList contains new-password-hover class, the new-password-hover class will be added.
        if (e.target.classList.contains('password-reset')){
            e.target.classList.add('password-reset-hover')
        }

        // This event will be fired when the target's classList contains continue class, the continue class will be added.
        if (e.target.classList.contains('continue')){
            e.target.classList.add('continue-hover')
        }
    })

    // MouseOut events
    modal.addEventListener('mouseout', (e) => {

        // This event will be fired when the target is submit, the button-hover class will be removed.
        if (e.target === submitBtn){
            submitBtn.classList.remove('submit-btn-hover')
        }

        // This event will be fired when the target's nodeName is 'INPUT', the input-hover class will be removed.
        if (e.target.nodeName === 'INPUT'){
            e.target.classList.remove('input-hover')
        }


        // This event will be fired when the target's classList contains new-password-hover class, the new-password-hover class will be removed.
        if (e.target.classList.contains('password-reset')){
            e.target.classList.remove('password-reset-hover')
        }

        // This event will be fired when the target's classList contains continue class, the continue class will be removed.
        if (e.target.classList.contains('continue')){
            e.target.classList.remove('continue-hover')
        }
    })

    // Submit Events
    modal.addEventListener('submit', (e) => {

        e.preventDefault()
        e.stopPropagation()

        // This event will be fired every time the target is a form, and the form data will be collected.
        if (e.target.nodeName === 'FORM'){
            let form = e.target
            let formData = new FormData(form)
            let url = form.action
            let method = form.method
            let csrfmiddlewaretoken = document.querySelector('input[type=hidden]').value
            /* If the target contains the login-form classList, the loginAW function will be called, if the data is
               authentic then the user will be logged in, if not, an error will be displayed.*/
             if (e.target.id === 'login-form'){
                 loginAW(formData, url, method, csrfmiddlewaretoken)
                .then(data => {
                    if (data['html']){
                        modalContent.innerHTML = data['html']
                        username = document.querySelector('#id_username')
                        password = document.querySelector('#id_password')
                        submitBtn = document.querySelector('.submit-btn')
                        passwordReset = document.querySelector('.password-reset')
                    }else{
                        window.location.href = '/home/'
                    }
                })
             }

            /* If the target contains the password-reset-form class in it's classList, the loginAW function will be called,
               and the response will be added to the modalContent.innerHTML*/
             if (e.target.id === 'password-reset-form'){
                loginAW(formData, url, method, csrfmiddlewaretoken)
                .then(data => {
                    if (data['html']){
                        modalContent.innerHTML = data['html']
                    }
                })
             }

            /* If the target's classList contains the signup-form class in its classList, the signUpAW function will be
               called and depending if we received errors or not, they will be displayed, else, the login form will
               be displayed.*/
            if (e.target.id === 'signup-form'){
                signUpAW(formData, url, method, csrfmiddlewaretoken)
                .then(data => {
                    if (data['error']){
                        modalContent.innerHTML = data['html']
                        signUpInputs = document.querySelectorAll('input,select')
                        submitBtn = document.querySelector('.submit-btn')
                    }else{
                        modal.classList.remove('modal-show')
                        loginBtn.click()
                    }
                })
            }
        }
    })
}