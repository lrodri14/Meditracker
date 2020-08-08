//Checked
if (document.querySelectorAll('tr') !== 'undefined' && document.querySelectorAll('tr') !== 'null'){
    var rows = document.querySelectorAll('tr')
}
if (document.querySelector('.fa-filter') !== 'undefined' && document.querySelector('.fa-filter') !== 'null'){
    var i = document.querySelector('.fa-filter')
}
if (document.querySelector('button') !== 'undefined' && document.querySelector('form') !== 'null'){
    var button = document.querySelector('button')
}
if (document.querySelector('form') !== 'undefined' && document.querySelector('form') !== 'null'){
    var form = document.querySelector('form')
}

if (document.querySelector('.all-registers') !== 'undefined' && document.querySelector('.all-registers') !== 'null'){
    var allRegisters = document.querySelector('.all-registers')
}

//Table Rows
if (rows){
    for(let i = 0; i<rows.length; i++){
        let childNodes = rows[i].childNodes
        if (rows[i].id === ''){
            rows[i].addEventListener('mouseover', function(e){
                rows[i].style.backgroundColor = 'cyan'
                rows[i].classList.add('tr-hover')
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
            rows[i].classList.remove('tr-hover')
            for (let c = 0; c<childNodes.length; c++){
                if (childNodes[c].nodeName != '#text'){
                    childNodes[c].style.color = 'cyan'
                    if (childNodes[c].children){
                            var children = childNodes[c].children
                            for (var cc = 0; cc<children.length; cc++){
                                children[cc].style.color = ''
                                }
                            }
                        }
                    }
                })
        }
    }
}

// Show filter button
if (i){
    i.addEventListener('mouseover', function(){
        this.classList.add('button-hover')
    })

    i.addEventListener('mouseout', function(){
        this.classList.remove('button-hover')
    })

    i.addEventListener('click', function(){
        !form.classList.contains('show-form') ? form.classList.add('show-form') : form.classList.remove('show-form')
    })
}


// Button
if (button){
    button.addEventListener('mouseover', function(){
        this.classList.add('button-form-hover')
    })

    button.addEventListener('mouseout', function(){
        this.classList.remove('button-form-hover')
    })
}

// AllRegisters
if (allRegisters){
    allRegisters.addEventListener('mouseover', function(){
        this.classList.add('all-registers-hover')
    })

    allRegisters.addEventListener('mouseout', function(){
        this.classList.remove('all-registers-hover')
    })
}