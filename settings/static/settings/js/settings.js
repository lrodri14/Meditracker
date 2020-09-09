// Checked
//Checked

if (document.querySelector('.wrapper') !== 'undefined' && document.querySelector('.wrapper') !== 'null'){
    var wrapper = document.querySelector('.wrapper')
}

if (document.querySelectorAll('tr') !== 'undefined' && document.querySelectorAll('tr') !== 'null'){
    var rows = document.querySelectorAll('tr')
}

var body = document.querySelector('body')

// Body Event Listeners


body.addEventListener('click', (e) => {
        if (e.target.nodeName === 'A' || e.target.nodeName === 'LI'){
        items = document.querySelectorAll('ul > li')
        for (let i = 0; i<items.length; i++){
            if (items[i].classList.contains('li-active') && items[i] !== e.target){
                items[i].classList.remove('li-active')
                wrapper.innerHTML = ''
            }
        }
        item = e.target.nodeName === 'A' ? e.target.parentNode : e.target
        item.classList.contains('li-active') ? item.classList.remove('li-active') : item.classList.add('li-active')
    }
})

body.addEventListener('mouseover', (e) => {

    if (e.target.nodeName === 'A' || e.target.nodeName === 'LI'){
        item = e.target.nodeName === 'A' ? e.target.parentNode : e.target
        item.classList.add('li-hover')
    }

})

body.addEventListener('mouseout', (e) => {

    if (e.target.nodeName === 'A' || e.target.nodeName === 'LI'){
        item = e.target.nodeName === 'A' ? e.target.parentNode : e.target
        item.classList.remove('li-hover')
    }

})

if (wrapper){

    var backedUpContent = wrapper.innerHTML

    wrapper.addEventListener('mouseover', (e) => {

    })

    wrapper.addEventListener('mouseout', (e) => {

    })

    wrapper.addEventListener('click', (e) => {

    })
}

//Table Rows
if (rows){
    for(let i = 0; i<rows.length; i++){
        let childNodes = rows[i].childNodes
        if (rows[i].id === ''){
            rows[i].addEventListener('mouseover', function(e){
                rows[i].style.backgroundColor = 'cyan'
                rows[i].style.cursor = 'pointer'
                for (let c = 0; c<childNodes.length; c++){
                    if (childNodes[c].nodeName != '#text'){
                        childNodes[c].style.color = '#12212b'
                        if (childNodes[c].children){
                            var children = childNodes[c].children
                            for (var cc = 0; cc<children.length; cc++){
                                children[cc].style.color = '#12212b'
                                children[cc].style.transition = '0.5s'
                            }
                        }
                        }
                    }
        })

        rows[i].addEventListener('mouseout', function(){
            rows[i].style.backgroundColor = ''
            rows[i].style.cursor = 'pointer'
            for (let c = 0; c<childNodes.length; c++){
                if (childNodes[c].nodeName != '#text'){
                    childNodes[c].style.color = 'cyan'
                    if (childNodes[c].children){
                            var children = childNodes[c].children
                            for (var cc = 0; cc<children.length; cc++){
                                children[cc].style.color = 'cyan'
                            }
                        }
                    }
                }
        })
        }
    }
}


