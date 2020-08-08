//Checked
if (document.querySelectorAll('tr') !== 'undefined' && document.querySelectorAll('tr') !== 'null'){
    var rows = document.querySelectorAll('tr')
}

if (document.querySelectorAll('button') !== 'undefined' && document.querySelectorAll('button') !== 'null'){
    var button = document.querySelectorAll('button')
}

if (document.querySelector('#add-consult') !== 'undefined' && document.querySelector('#add-consult') !== 'null'){
    var addConsult = document.querySelector('#add-consult')
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


// Button
if (button){
    for (let i = 0; i<button.length; i++){
        button[i].addEventListener('mouseover', function(){
            this.classList.add('button-hover')
        })

        button[i].addEventListener('mouseout', function(){
            this.classList.remove('button-hover')
        })
    }
}

//Add consult
if (addConsult){
    setInterval(function(){
        if (addConsult.style.top == '90%'){
            addConsult.style.top = '88%'
        } else {
            addConsult.style.top = '90%'
        }
    },500)
}