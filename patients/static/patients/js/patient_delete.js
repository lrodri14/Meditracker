// Checked
var inputs = document.querySelectorAll('input')

for (let i = 0; i<inputs.length; i++){

    inputs[i].addEventListener('mouseover', function(){
        this.classList.add('input-hover')
    })

    inputs[i].addEventListener('mouseout', function(){
        this.classList.remove('input-hover')
    })
}

