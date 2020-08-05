var tiles = document.querySelectorAll('.tile')

for (let i = 0; i<tiles.length; i++){
    tiles[i].addEventListener('mouseover', function(){
        tiles[i].classList.add('tile-hover')
        for (let x = 0; x<tiles.length; x++){
            if (tiles[x] !== tiles[i]){
                tiles[x].classList.add('tile-fade-out')
            }
        }
    })
    tiles[i].addEventListener('mouseout', function(){
        tiles[i].classList.remove('tile-hover')
        for (let x = 0; x<tiles.length; x++){
            if (tiles[x] !== tiles[i]){
                tiles[x].classList.remove('tile-fade-out')
            }
        }
    })
}