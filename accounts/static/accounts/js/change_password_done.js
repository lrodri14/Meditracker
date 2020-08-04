var seconds = 6
var redirect = document.querySelector('#redirection')

setInterval(function(){
    seconds --
    redirect.textContent = 'You will be redirected in ' + seconds + ' seconds'
}, 1000)

setTimeout(function(){
    window.location = '/accounts/profile/'
}, 6000)