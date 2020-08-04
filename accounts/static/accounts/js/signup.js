var inputs = document.querySelectorAll('input')
var roll = document.querySelector('#id_roll')
var signUp = document.querySelector('button')

//Inputs
for (let i = 0; i<inputs.length; i++){

    inputs[i].addEventListener('mouseover', function(){
        inputs[i].classList.add('input-hover')
    })

    inputs[i].addEventListener('mouseout', function(){
        inputs[i].classList.remove('input-hover')
    })
}

// Roll
roll.addEventListener('change', function(){
    if(roll.value === 'Assistant'){
        document.querySelector('#id_speciality').style.display = 'none'
        for (let i = 0; i < document.querySelectorAll('p').length; i++){
            if (document.querySelectorAll('p')[i].textContent === 'Speciality'){
               document.querySelectorAll('p')[i].style.display = 'none'
            } else{
               document.querySelectorAll('p')[i].style.display = ''
            }
        }
    } else {
        document.querySelector('#id_speciality').style.display = ''
    }
})

// SignUp Button
for (let i = 0; i<inputs.length; i++){
    inputs[i].addEventListener('input', function(){
    var filled = 0
        for (let i = 0; i<inputs.length; i++){
            if (inputs[i].value !== ''){
                filled = filled + 1
            }
        }
    if (filled===inputs.length){
       signUp.classList.add('button-fade-in')
    } else {
       signUp.classList.remove('button-fade-in')
    }
    })
}

signUp.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

signUp.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})