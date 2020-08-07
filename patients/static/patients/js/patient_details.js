//Checked
var medicalBook = document.querySelector('.fa-book-medical')

//Medical Icon
medicalBook.addEventListener('mouseover', function(){
    this.classList.add('medical-hover')
})

medicalBook.addEventListener('mouseout', function(){
    this.classList.remove('medical-hover')
})