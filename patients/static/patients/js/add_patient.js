//Checked
var inputs = document.querySelectorAll('input')
var button = document.querySelector('button')


// Inputs
for (var i = 0; i<inputs.length; i++){
    inputs[i].addEventListener('mouseover', function(){
        this.classList.add('input-hover')
    })

    inputs[i].addEventListener('mouseout', function(){
        this.classList.remove('input-hover')
    })
}

// Button
button.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

button.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})