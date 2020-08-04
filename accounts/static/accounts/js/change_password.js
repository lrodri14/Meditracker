//Checked
var inputs = document.querySelectorAll('input')
var button = document.querySelector('button')

//Inputs
for (let i = 0; i<inputs.length; i++){
    inputs[i].addEventListener('mouseover', function(){
        inputs[i].classList.add('input-hover')
    })

    inputs[i].addEventListener('mouseout', function(){
        inputs[i].classList.remove('input-hover')
    })

    inputs[i].addEventListener('input', function(){
        var filled = 0
        for(let i = 0; i<inputs.length; i++){
           if (inputs[i].value !== ''){
               filled++
           }
        }
        filled === inputs.length ? button.classList.add('button-fadeIn') : button.classList.remove('button-fadeIn')
    })
}



//Button

button.addEventListener('mouseover', function(){
    button.classList.add('button-hover')
})

button.addEventListener('mouseout', function(){
    button.classList.remove('button-hover')
})