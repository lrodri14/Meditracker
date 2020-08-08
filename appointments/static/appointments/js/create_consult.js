//Checked
var button = document.querySelector('button')
var anchor = document.querySelectorAll('a')
console.log(anchor)

button.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

button.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})

anchor[anchor.length - 1].addEventListener('mouseover', function(){
    this.style.fontSize = '16px'
})

anchor[anchor.length - 1].addEventListener('mouseout', function(){
    this.style.fontSize = ''
})