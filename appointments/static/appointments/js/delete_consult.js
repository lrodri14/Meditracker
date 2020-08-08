// Checked
var button = document.querySelectorAll('button')

for (var i = 0; i<button.length; i++){
    button[i].addEventListener('mouseover', function(){
        this.classList.add('button-hover')
    })

    button[i].addEventListener('mouseout', function(){
        this.classList.remove('button-hover')
    })
}