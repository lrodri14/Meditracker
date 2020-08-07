var button = document.querySelector('button')

button.addEventListener('mouseover', function(){
    this.classList.add('button-hover')
})

button.addEventListener('mouseout', function(){
    this.classList.remove('button-hover')
})