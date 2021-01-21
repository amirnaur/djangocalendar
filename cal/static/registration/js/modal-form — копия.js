'use strict'

var events
var overlay_options = {
    closable: false,
    opened: false
    }
        
var overlay_day_events = new Overlay(overlay_options)
var overlay_new_event = new Overlay(overlay_options)
buildList()
function getData(url){
    let get_data
//            var url = 'http://127.0.0.1:8000/api/events/'
    fetch(url)
    .then((resp) => resp.json())
    .then(function(data){
         get_data = data
        console.log("getdata", get_data)
      });
    console.log("check", get_data)
    return get_data
}

function buildList(){
    //var wrapper = document.getElementById('list-wrapper')
    //wrapper.innerHTML = ''

    var url = 'http://127.0.0.1:8000/api/events/'

    fetch(url)
    .then((resp) => resp.json())
    .then(function(data){
//				console.log('Data:', data)
        events = data
        for(let i in events){
            let event_date = events[i].date_time
            $(`#${event_date} ul`).append(`<li data-id="${events[i].id}">${events[i].title}</li>`)
        }
      });
}

function newEvent(date){
    overlay_new_event.content.innerHTML = ''
    console.log("newEvent", date)
    let new_event_render = ''
    let icons_list
    let icons_render = ''
    let url = 'http://127.0.0.1:8000/api/icons/'
    icons_list = getData(url)
    console.log("icons list", icons_list)
    for (let icon in icons_list){
        icons_render += `
        <option style="background-image:url(${icon.icon});" value='${icon.name}'>${icon.name}</option>
`
        console.log("icon", icon)
    }
    console.log("icons render",icons_render)
    var data_check = $(`#${date}`)
    console.log(data_check.data.id)
    new_event_render += `
    <select name='options'>
      ${icons_render}
    </select>
    <label for="event-title" class="col-form-label">Название:</label>
    <input type="text" class="form-control" id="event-title">
    <label for="event-desc" class="col-form-label">Описание:</label>
    <textarea class="form-control" id="event-desc"></textarea>
`
    overlay_new_event.content.innerHTML += `
<div class="modal-header">
    <h5 class="modal-title" id="exampleModalLabel">${date}</h5>
    <button type="button" class="close" data-dismiss="modal" onclick="overlay_new_event.close()" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
</div>
<div class="modal-body">
    <form id="form-event-edit">

        ${new_event_render}

    </form>
    <div class="modal-footer">
        <button type="button" class="btn btn-primary" onclick="newEvent();">Сохранить</button>
    </div>
</div>
`
    overlay_new_event.open()

}

//
function editEvent(obj){
    let form = document.getElementById('form-edit-event')
    console.log('Form submitted')
    console.log(obj)
    let url = 'http://127.0.0.1:8000/api/events/'
}

//on date click events render
function dayEvents(data){
    let url = 'http://127.0.0.1:8000/api/events/'
    events = getData(url)
    console.log("events", events)
//        let overlay_content = document.createElement("div");
    let day_events_render = ''
    overlay_day_events.content.innerHTML = ''
    for(let i in events){
        console.log("Events", events)
        if(data.id == events[i].date_time){
            day_events_render += `
            <div class="event-container">
                <label for="recipient-name" class="col-form-label">Title:</label>
                <input type="text" data-id="${events[i].id}" class="form-control" id="recipient-name" value="${events[i].title}">
                <p>${events[i].title}</p>
            </div>
`
        }

//                overlay.content.innerHTML +=`
//            <div class="modal-header">
//                <h5 class="modal-title" id="exampleModalLabel">${data.id}</h5>
//                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
//                    <span aria-hidden="true">&times;</span>
//                </button>
//            </div>
//            <div class="modal-body">
//                <form id="form-event-edit">
//                    <div class="form-group">
//                        <label for="recipient-name" class="col-form-label">Title:</label>
//                        <input type="text" class="form-control" id="recipient-name" value="${events[i].title}">
//                    </div>
//                    <div class="form-group">
//                        <label for="message-text" class="col-form-label">Description:</label>
//                        <textarea class="form-control" id="message-text"></textarea>
//                    </div>
//                </form>
//                <div class="modal-footer">
//                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
//                    <!--                    <input id="submit" class="btn btn-primary" type="submit" value="Измен"/>-->
//                    <button type="button" class="btn btn-primary" onclick="editEvent(this)">Send message</button>
//                </div>
//            <button class="new-event-button btn">Новое событие</button>
//            </div>
//    </div>
//`
    }
    overlay_day_events.content.innerHTML +=`
    <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">${data.id}</h5>
        <button type="button" class="close" data-dismiss="modal" onclick="overlay_day_events.close()" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    <div class="modal-body">
        <form id="form-event-edit">

            ${day_events_render}

        </form>
        <div class="modal-footer">
            <button type="button" class="btn btn-primary" onclick="overlay_day_events.close(); newEvent('${data.id}');">Новое событие</button>
        </div>
    </div>
`

//         var btn_close = document.createElement("button")
//btn_close.innerHTML = "Close"
//btn_close.onclick = overlay.close
//overlay.content.appendChild(btn_close)
    overlay_day_events.open()

}