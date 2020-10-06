//Checked
var tiles = document.querySelectorAll('.tile')
var icons = document.querySelectorAll('i')
var title = document.querySelectorAll('h3')
var sound = document.querySelector('audio')

for (let i = 0; i<tiles.length; i++){
    tiles[i].addEventListener('mouseover', function(){
        tiles[i].classList.add('tile-hover')
        icons[i].classList.add('i-hover')
        title[i].classList.add('h3-hover')
        sound.play()
    })
    tiles[i].addEventListener('mouseout', function(){
        tiles[i].classList.remove('tile-hover')
        icons[i].classList.remove('i-hover')
        title[i].classList.remove('h3-hover')
    })
}