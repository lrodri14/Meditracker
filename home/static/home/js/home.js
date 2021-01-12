//Checked
var searchBar = document.querySelector('#search-bar')
var topMenuElements = document.querySelector('.wrapper-one')
var bottomMenuElements = document.querySelector('.wrapper-two')
var menuTitle = document.querySelector('h1')
var queryResults = document.querySelector('.query-results')
var tiles = document.querySelectorAll('.tile')
var icons = document.querySelectorAll('i')
var title = document.querySelectorAll('h3')
var logoutTile = document.querySelector('#logout')
var sound = document.querySelector('audio')
var modal = document.querySelector('.modal')

document.querySelector('body').click()

// Async FUnctions

async function userLookupAW(url){
    const result = await fetch(url)
    const data = result.json()
    return data
}

searchBar.addEventListener('input', (e) => {

    let url = e.target.getAttribute('data-url') + '?query=' + e.target.value
    if (e.target.value !== ''){
        topMenuElements.classList.add('hide-menu')
        bottomMenuElements.classList.add('hide-menu')
        menuTitle.classList.add('hide-menu')
        userLookupAW(url)
        .then(data => {
            queryResults.innerHTML = data['html']
        })
        queryResults.classList.add('query-results-show')
    }else{
        topMenuElements.classList.remove('hide-menu')
        bottomMenuElements.classList.remove('hide-menu')
        menuTitle.classList.remove('hide-menu')
        queryResults.innerHTML = ''
        queryResults.classList.remove('query-results-show')
    }
})

if (queryResults){

    queryResults.addEventListener('mouseover', (e) => {
        /* This event will be fired every time a hover occurs in the icons or a td cell, this will change many style
           properties from the row and add tr-hover and td-hover class*/
        if (e.target.nodeName === 'TD'){
            let row
            e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = '#C7E8F3'
            row.style.color = '#496897'
        }

        if (e.target.classList.contains('fa-user-plus')){
            e.target.classList.add('fa-user-plus-hover')
        }

        if (e.target.classList.contains('fa-user-slash')){
            e.target.classList.add('fa-user-slash-hover')
        }

    })

    queryResults.addEventListener('mouseout', (e) => {

      /* This event will be fired every time a hover occurs in the icons or a td cell, this will change many style
         properties from the row and removed tr-hover and td-hover class*/
      if (e.target.nodeName === 'TD'){
        let row
        e.target.nodeName === 'TD' ? row = e.target.parentNode : row = e.target.parentNode.parentNode
            row.style.backgroundColor = ''
            row.style.color = ''
      }
    })

}

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