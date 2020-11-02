//Checked
var tiles = document.querySelectorAll('.tile')
var icons = document.querySelectorAll('i')
var title = document.querySelectorAll('h3')
var logoutTile = document.querySelector('#logout')
var sound = document.querySelector('audio')
var modal = document.querySelector('.modal')

document.querySelector('body').click()

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

logoutTile.addEventListener('click', (e) => {
    modal.classList.add('modal-show')
})

if (modal){

    modal.addEventListener('click', (e) => {

        if (e.target === modal){
            modal.classList.remove('modal-show')
        }

        if (e.target.nodeName === 'BUTTON'){
            if (e.target.textContent === 'No'){
                modal.classList.remove('modal-show')
            }
        }
    })

    modal.addEventListener('mouseover', (e) => {
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.add('button-hover')
        }
    })

    modal.addEventListener('mouseout', (e) => {
        if (e.target.nodeName === 'BUTTON'){
            e.target.classList.remove('button-hover')
        }
    })

}