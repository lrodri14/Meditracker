//Checked
var inputs = document.querySelectorAll('input')
var button = document.querySelector('button')
var extraInfo = document.querySelector('.extra-info')


if (extraInfo){
    extraInfo.addEventListener('mouseover', (e) =>{
        if (e.target.classList.contains('fa-plus')){
            e.target.classList.add('fa-plus-hover')
        }

        if (e.target.classList.contains('fa-trash')){
            e.target.classList.add('fa-trash-hover')
        }
    })

    extraInfo.addEventListener('mouseout', (e) =>{
        if (e.target.classList.contains('fa-plus')){
            e.target.classList.remove('fa-plus-hover')
        }

        if (e.target.classList.contains('fa-trash')){
            e.target.classList.remove('fa-trash-hover')
        }
    })
}

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