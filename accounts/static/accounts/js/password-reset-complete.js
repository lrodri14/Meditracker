//Checked

var a = document.querySelector('a')

a.addEventListener('mouseover', function(){
    this.classList.add('link-hover')
})

a.addEventListener('mouseout', function(){
    this.classList.remove('link-hover')
})