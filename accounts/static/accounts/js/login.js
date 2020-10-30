//Checked
var loginBtn = document.querySelector('button')
if (document.querySelector('a') !== 'undefined' && document.querySelector('a') !== 'null'){
    var passwordChange = document.querySelector('a')
}

username.addEventListener('mouseover', usernameFocusHover)
username.addEventListener('mouseout', usernameFocusHoverOut)
password.addEventListener('mouseover', usernameFocusHover)
password.addEventListener('mouseout', usernameFocusHoverOut)


// Change password link
if (passwordChange){
    passwordChange.addEventListener('mouseover', function(){
        this.classList.add('update-password-hover')
    })

    passwordChange.addEventListener('mouseout', function(){
        this.classList.remove('update-password-hover')
    })
}

// Login Button
loginBtn.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

loginBtn.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})

for (var i = 0; i<inputs.length; i++){
    inputs[i].addEventListener('input', function(){
        if (username.value.length > 0 && password.value.length > 0){
            loginBtn.classList.add('button-fadeIn')
        } else{
            loginBtn.classList.remove('button-fadeIn')
        }
    })
}