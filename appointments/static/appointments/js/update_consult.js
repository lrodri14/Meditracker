var medicalBook = document.querySelector('.fa-book-medical')
var button = document.querySelector('button')
var label = document.querySelector('#medical_exams')

medicalBook.addEventListener('mouseover', function(){
    this.classList.add('fa-book-medical-hover')
})

medicalBook.addEventListener('mouseout', function(){
    this.classList.remove('fa-book-medical-hover')
})

button.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

button.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})

label.addEventListener('mouseover', function(){
    this.classList.add('medical-exams-hover')
})

label.addEventListener('mouseout', function(){
    this.classList.remove('medical-exams-hover')
})