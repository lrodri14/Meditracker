//Checked
var input = document.querySelectorAll('input')

//Inputs
for (let i = 0; i<input.length; i++){
    input[i].addEventListener('mouseover', function(){
        this.classList.add('input-hover')
    })

    input[i].addEventListener('mouseout', function(){
        this.classList.remove('input-hover')
    })
}