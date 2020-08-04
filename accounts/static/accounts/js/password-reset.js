// Checked
var emailInput = document.querySelector('#id_email')
var submit = document.querySelector('button')

// Email Input
emailInput.addEventListener('mouseover', function(){
    this.classList.add('input-hover')
})

emailInput.addEventListener('mouseout', function(){
    this.classList.remove('input-hover')
})

emailInput.addEventListener('input', function(){
   if (emailInput.value !== ''){
        submit.classList.add('button-fade-in')
   }else {
        submit.classList.add('button-fade-in')
   }
})

// Submit
submit.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

submit.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})

