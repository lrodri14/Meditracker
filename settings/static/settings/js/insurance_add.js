//Checked
var input = document.querySelector('#id_company')
var button = document.querySelectorAll('button')

//Input
input.addEventListener('mouseover', function(){
    this.classList.add('input-hover')
})

input.addEventListener('mouseout', function(){
    this.classList.remove('input-hover')
})

//Button

for (var i = 0; i<button.length; i++){
    button[i].addEventListener('mouseover', function(){
        this.classList.add('button-hover')
    })

    button[i].addEventListener('mouseout', function(){
        this.classList.remove('button-hover')
    })
}