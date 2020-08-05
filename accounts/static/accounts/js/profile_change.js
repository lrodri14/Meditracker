//Checked
var button = document.querySelector('button')
var changeProfileButton = document.querySelector('#id_profile_pic')
var inputs = document.querySelectorAll('input')
var img = document.querySelector('img')


// Img
img.addEventListener('mouseover', function(){
    this.classList.add('img-hover')
})

img.addEventListener('mouseout', function(){
    this.classList.remove('img-hover')
})

// Profile change button
changeProfileButton.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

changeProfileButton.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})

// Inputs
for (let i = 0; i<inputs.length; i++){
    inputs[i].addEventListener('mouseover', function(){
        this.classList.add('input-hover')
    })
    inputs[i].addEventListener('mouseout', function(){
        this.classList.remove('input-hover')
    })
}

//Button
button.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

button.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})

