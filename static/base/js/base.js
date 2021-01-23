/*
    This base.js file contains all the variable declarations, async and sync functions and event listeners for the base
    template to work properly.
*/

///////////////////////////////////////////////// Variables ////////////////////////////////////////////////////////////

var loaderModal = document.querySelector('.loader-modal')
var bars = document.querySelector('.fa-bars')
var globalNavigator = document.querySelector('.global-navigator')
var contacts = document.querySelector('.fa-users')
var socialSection = document.querySelector('.social-section')
var socialSectionSearch = document.querySelector('#social-section-search')
var socialSectionData = document.querySelector('#social-section-data')
var socialSectionTabs = document.querySelectorAll('.social-section-tab')
var closeSocialSection = document.querySelector('#close-social-section')

// Variables used for the chat functionality
let identity
let chatWindow
let chatClient
let chatChannel

//if (document.querySelector('.navigator') !== 'undefined' || document.querySelector('.navigator') !== 'null'){
//}
//if (document.querySelector('.social-section') !== 'undefined' && document.querySelector('.social-section') !== 'null'){
//}

///////////////////////////////////////////////// Functions ////////////////////////////////////////////////////////////

// Async functions

async function displayContactsAW(url){
    /*The displayContactsAW async function is used to display all the contacts the user is linked with, it takes
      a single argument: url, used to perform the request to the server, the response will be return in json format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function displayChatAW(url){
    /*The displayChatAW async function is used to display all the chats the user has opened, it takes a single
      argument: url, used to perform the request to the server, the response will be return in json format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function displayRequestsAW(url){
    /*The displayRequestsAW async function is used to display all the requests the user has received, it takes a
      single argument: url, used to perform the request to the server, the response will be return in json format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

async function requestResponseAW(url){
    /*The requestResponseAW async function is used to accept or deny any requests the user has received, it receives
      a single argument: url, which contains the request reply along with it. The response will be returned in json
      format.*/
    const result = await fetch(url)
    const data = result.json()
    return data
}

// Sync functions

function displayMessage(fromUser, message){
    /* This displayMessage function is used to display the messages inside the chatWindow, it takes two arguments, the
       sender and the message itself, we will create a div element to store our message, and add the message body, we
       will check if the identity variable contains the same user as the fromUser parameter, if the condition is fulfilled
       the 'message' class will be added, else the 'reply' class will be added, afterwards, the message will be added to
       the chatWindow and the chatWindow scroll will be set to the bottom.*/
    let messageContent = document.createElement('div')
    messageContent.textContent = message
    fromUser === identity ? messageContent.classList.add('message') : messageContent.classList.add('reply')
    chatWindow.appendChild(messageContent)
    chatWindow.scrollTop = chatWindow.scrollHeight
}

function setupChannel(name){
    /* The setUpChannel function takes a single argument name, which the channel object we we collect from the response
       when we either retrieved from the subscribed channels or we created, we will check if the channel.status attribute
       is 'joined'... if this condition is fulfilled then we will directly retrieve all the messages from the channel, we
       will receive a promise object we will consume, we call the processPage function to display the messages we collected
       from the server. If the condiiton is not fulfilled then we will call the .join() method to join the channel and
       follow the same procedure, retrieve the messages and process them.*/
    if (chatChannel.status === 'joined'){
        chatChannel.getMessages(pageSize=30, anchor=0, direction='forward')
        .then( messages => {
            processPage(messages)
        })
    }else{
        chatChannel.join()
        .then(channel => {
            channel.getMessages(pageSize=30, anchor=0, direction='forward')
            .then(messages => {
                processPage(messages)
            })
        })
    }

    /* We will assign a messageAdded event listener to the chatChannel this way every time we capture this event, the
       displayMessage function will be called passing the author and body message as parameters, this will display our
       message in the chatWindow*/
    chatChannel.on('messageAdded', message => {
        displayMessage(message.author, message.body)
    })

}

function processPage(page){
    /* The processPage function is used to display all the messages that have been sent previously in the channel, it
       takes one single argument: page, which expects a Paginator Object, this will print each and every single message
       sent, it will check if the Paginator contains any other pages to render them too.*/
    page.items.forEach(message => {
        displayMessage(message.author, message.body)
    })
    if (page.hasNextPage){
        page.nextPage().then(processPage)
    }
}

function createOrJoinChannel(){
    /* This createOrJoinChannel function, is used to retrieve the channel with the channelName we received in our
       server response, we will make use of the getChannelByUniqueName function to retrieve this channel, this function
       will return us a promise we will consume which contains the channel itself, we will store this channel inside
       the chatChannel variable for future uses, afterwards we will setup or start our channel using the setupChannel
       function we defined. If that channel does not exist, we will create it making use of the chatClient.createChannel
       function, this function receives an object as parameter which contains the uniqueName and friendlyName of the channel,
       this function will return a promise with the channel itself, we do the same procedure, store the channel inside
       the chatChannel variable and make use of the setupChannel function to set it up.*/
    chatClient.getChannelByUniqueName(channelName)
    .then(channel => {
        chatChannel = channel
        setupChannel(channelName)
    })
    .catch(() => {
        chatClient.createChannel({
            uniqueName: channelName,
            friendlyName: channelName + 'Channel'
        })
        .then(channel => {
            chatChannel = channel
            setupChannel(channelName)
        })
    })
}

///////////////////////////////////////////////// Event Listeners //////////////////////////////////////////////////////

// Bars Event Listeners
if (bars){

    // Bars Click Event
    // This event will be triggered every time a click over the bars occur, this will open the global navigator section.
    bars.addEventListener('click', () => {
       globalNavigator.classList.add('global-navigator-show')
    })

}

// Contacts Event Listeners
if (contacts){

    // Contacts click events
    /* This event will be triggered every time a click over the contacts occur, this will open the social section and display
       the contacts automatically */
    contacts.addEventListener('click', (e) => {
       socialSectionTabs[0].classList.add('social-section-tab-active')
       let url = e.target.getAttribute('data-url') + '?query=' + socialSectionSearch.value
        displayContactsAW(url)
        .then(data => {
            socialSectionData.innerHTML = data['html']
        })
       socialSection.classList.add('social-section-show')
    })

}

// Global Navigator Event Listeners
if (globalNavigator){

    // Mouseover Events
    globalNavigator.addEventListener('mouseover', (e) => {

        /* This event will be triggered any time the target contains either the global-navigator-tab, fas or fa-times class,
           the global-navigator-tab-hover class will be added*/
        if (e.target.classList.contains('global-navigator-tab') || e.target.classList.contains('fas') && !e.target.classList.contains('fa-times')){
            let tab = e.target.classList.contains('global-navigator-tab') ? e.target : e.target.parentNode.parentNode
            tab.classList.add('global-navigator-tab-hover')
        }

    })

    // Mouseout Events
    globalNavigator.addEventListener('mouseout', (e) => {

        /* This event will be triggered any time the target contains either the global-navigator-tab, fas or fa-times class,
           the global-navigator-tab-hover class will be removed*/
        if (e.target.classList.contains('global-navigator-tab') || e.target.classList.contains('fas') && !e.target.classList.contains('fa-times')){
            let tab = e.target.classList.contains('global-navigator-tab') ? e.target : e.target.parentNode.parentNode
            tab.classList.remove('global-navigator-tab-hover')
        }

    })

    // Click Events
    globalNavigator.addEventListener('click', (e) => {

        /* This event will be triggered any time the target contains either the close-global-navigator class,
           the global navigator will be hidden */
        if (e.target.parentNode.classList.contains('close-global-navigator')){
           globalNavigator.classList.remove('global-navigator-show')
        }

    })

}

// Social Section Event Listeners
if (socialSection){

    // Mouseover events
    socialSection.addEventListener('mouseover', (e) => {

        /* This event will be triggered whenever the target contains the cell class, some styles will be edited and added.*/
        if (e.target.classList.contains('cell') || e.target.parentNode.classList.contains('cell')){
            let cell = e.target.classList.contains('cell') ? e.target : e.target.parentNode
            cell.style.backgroundColor = '#C7E8F3'
            cell.style.color = '#496897'
        }

        // This event will be triggered every time the target contains the 'social-section-tab' class, social-section-tab-hover class will be added
         if (e.target.classList.contains('social-section-tab')){
            e.target.classList.add('social-section-tab-hover')
         }

        // This event will be triggered every time the target contains the delete-contact class, delete-contact-hover class will be added
        if (e.target.classList.contains('delete-contact')){
            e.target.classList.add('delete-contact-hover')
        }

        // This event will be triggered every time the target contains the accept-contact-request class, accept-contact-request-hover class will be added
        if (e.target.classList.contains('accept-contact-request')){
            e.target.classList.add('accept-contact-request-hover')
        }

        // This event will be triggered every time the target contains the deny-contact-request class, deny-contact-request-hover class will be added
        if (e.target.classList.contains('deny-contact-request')){
            e.target.classList.add('deny-contact-request-hover')
        }

        // This event will be triggered every time the target contains the send-message-btn class, send-message-btn-hover class will be added
        if (e.target.id === 'send-message-btn'){
            e.target.classList.add('send-message-btn-hover')
        }

    })

    socialSection.addEventListener('mouseout', (e) => {

        /* This event will be triggered whenever the target contains the cell class, some styles will be edited and removed.*/
        if (e.target.classList.contains('cell') ||  e.target.parentNode.classList.contains('cell')){
            let cell = e.target.classList.contains('cell') ? e.target : e.target.parentNode
            cell.style.backgroundColor = ''
            cell.style.color = ''
        }

        // This event will be triggered every time the target contains the 'social-section-tab' class, social-section-tab-hover class will be removed
        if (e.target.classList.contains('social-section-tab')){
            e.target.classList.remove('social-section-tab-hover')
        }

        // This event will be triggered every time the target contains the delete-contact class, delete-contact-hover class will be removed
        if (e.target.classList.contains('delete-contact')){
            e.target.classList.remove('delete-contact-hover')
        }

        // This event will be triggered every time the target contains the accept-contact-request class, accept-contact-request-hover class will be removed
        if (e.target.classList.contains('accept-contact-request')){
            e.target.classList.remove('accept-contact-request-hover')
        }

        // This event will be triggered every time the target contains the deny-contact-request-hover class, deny-contact-request-hover class will be removed
        if (e.target.classList.contains('deny-contact-request')){
            e.target.classList.remove('deny-contact-request-hover')
        }

        // This event will be triggered every time the target contains the send-message-btn class, send-message-btn-hover class will be removed
        if (e.target.id === 'send-message-btn'){
            e.target.classList.remove('send-message-btn-hover')
        }


    })

    // Click Events
    socialSection.addEventListener('click', (e) => {

        /* This event will be fired whenever the target contains the close-social-section classList,
           the social section will be closed.*/
        if (e.target.id == 'close-social-section'){
            socialSection.classList.remove('social-section-show')
            for (let i = 0; i<socialSectionTabs.length; i++){
                socialSectionTabs[i].classList.remove('social-section-tab-active')
            }
       }

        /* This event will be fired whenever the target contains the social-section-tab class in it's
           classList, when the event is fired all the tabs will have the social-section-tab-active class
           removed, and the target will have the same class added, afterwards the url will be collected
           from the data-url attribute in the target and the parameters will be added, we will make use
           of the displayContactsAW to request the information from the server, the response will be added
           to the socialSectionData.innerHTML */
        if (e.target.classList.contains('social-section-tab')){
            for (let i = 0; i<socialSectionTabs.length; i++){
                socialSectionTabs[i].classList.remove('social-section-tab-active')
            }
            e.target.classList.add('social-section-tab-active')
            let url = e.target.getAttribute('data-url') + '?query=' + socialSectionSearch.value
            displayContactsAW(url)
            .then(data => {
                socialSectionData.innerHTML = data['html']
            })
        }

        /* This event will be fired every time the classList contains the accept-contact request or deny-contact-request
           class, we will grab the url from the data-url attribute, and the response from the data-response
           attribute, these are the parts that will shape our URL, we will make use the requestResponseAW async
           function to send the user response to the server, the server response with the updated content will be
           added to the socialSectionData.innerHTML*/
        if (e.target.classList.contains('accept-contact-request') || e.target.classList.contains('deny-contact-request')){
            e.preventDefault()
            e.stopPropagation()
            let url = e.target.getAttribute('data-url') + '?response=' + e.target.getAttribute('data-response')
            requestResponseAW(url)
            .then(data => {
                socialSectionData.innerHTML = data['html']
            })
        }

        /* This event will be fired whenever the target contains the chat class in its classList, we will
           collect the url from the data-url attribute, we need this to make the request to the server, the response
           contains the token and extra elements we need to create our instance of the Twilio Chat Client. The
           ['html'] response will be added to the socialSectionData.innerHTML, the response also contains an
           ['identity'] key and a ['channel_name'] key, these will be stored inside inside the identity and
           and channelName variables, we also set the chatWindow variable to the div which will contain the messages,
           To create our chat client we use the create function in Twilio.Chat.Client and we pass the token we received
           from the response inside the ['token'] key, this function will make a request to the Twilio servers and return
           a promise we will consume, it will return the client instance, so we store it inside the chatClient class.
           after the collect our chatClient instance we get it's subscribed channels, making use of the
           getSubscribedChannels function. This will return a promise we will consume, and we will call the
           createOrJoinChannel function.*/
        if (e.target.classList.contains('chat') || e.target.parentNode.classList.contains('chat')){
            let chatUrl = e.target.classList.contains('chat') ? e.target.getAttribute('data-url') : e.target.parentNode.getAttribute('data-url')
            displayChatAW(chatUrl)
            .then(data => {
                socialSectionData.innerHTML = data['html']
                chatWindow = document.querySelector('#chat-content')
                identity = data['identity']
                channelName = data['channel_name']
                Twilio.Chat.Client.create(data['token'])
                .then(client => {
                    chatClient = client
                    chatClient.getSubscribedChannels()
                    .then(createOrJoinChannel)
                })
            })
        }

        /* This event will be fired every time the target contains fa-paper-plane in it's classList, this event will collect
           the value from the #id_message element, and check if there is a channel available, if the condition is
           fulfilled, the channel sendMessage function will be called, passing the message as it's parameter. Finally
           the #id_message element will be cleared.*/
        if (e.target.classList.contains('fa-paper-plane')){
            let message = document.querySelector('#id_message').value
            if (chatChannel && message.length > 0){
                chatChannel.sendMessage(message)
                document.querySelector('#id_message').value = ''
            }
        }

    })
}

// Window Event Listeners
// This event will be fired every time the DOM content has been fully loaded, the loaderModal will be hidden.
window.addEventListener('DOMContentLoaded', () => {
    loaderModal.classList.add('loader-modal-hide')
})
