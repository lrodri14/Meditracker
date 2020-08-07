//Checked
var a = document.querySelector('.fa-trash')

a.addEventListener('mouseover', function(){
    this.classList.add('link-hover')
})

a.addEventListener('mouseout', function(){
    this.classList.remove('link-hover')
})