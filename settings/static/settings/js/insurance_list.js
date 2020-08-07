//Checked
var sound = new Audio()
sound.src = "/static/settings/js/sound-effect.mp3"
if (document.querySelectorAll('tr') !== 'undefined' && document.querySelectorAll('tr') !== 'null'){
    var tr = document.querySelectorAll('tr')
}

// tr
if (tr){
    for (let i = 0; i<tr.length; i++){
        let childNodes = tr[i].childNodes
        if (tr[i].id === ''){
            tr[i].addEventListener('mouseover', function(){
                tr[i].style.backgroundColor = 'cyan'
                sound.play()
                for (let c = 0; c<childNodes.length; c++){
                    if (childNodes[c].nodeName != '#text'){
                        childNodes[c].style.color = '#12212b'
                        childNodes[c].style.cursor = 'pointer'
                        childNodes[c].style.transition = '0.5s'
                    }
                }
            })
            tr[i].addEventListener('mouseout', function(){
                tr[i].style.backgroundColor = ''
                for (let c = 0; c<childNodes.length; c++){
                    if (childNodes[c].nodeName != '#text'){
                        childNodes[c].style.color = ''
                        childNodes[c].style.cursor = ''
                        childNodes[c].style.transition = '0.5s'

                    }
                }
            })
        }
    }
}


