'use strict'

var events
var colors = [
    {
        "id": 1,
        "color": "757575",
        "rgba": "rgba(117,117,117,0.6)"
    },
    {
        "id": 2,
        "color": "F2994A",
        "rgba": "rgba(242,153,74,0.6)"
    },
    {
        "id": 3,
        "color": "F2C94C",
        "rgba": "rgba(242,201,76,0.6)"
    },
    {
        "id": 4,
        "color": "00CCA7",
        "rgba": "rgba(0,204,167,0.6)"
    },
    {
        "id": 5,
        "color": "2D9CDB",
        "rgba": "rgba(45,156,219,0.6)"
    },
    {
        "id": 6,
        "color": "EB5757",
        "rgba": "rgba(235,87,87,0.6)"
    },
    {
        "id": 7,
        "color": "4F4F4F",
        "rgba": "rgba(79,79,79,0.6)"
    }
]
var overlay_options = {
    closable: false,
    opened: false
}

var overlay_day_events = new Overlay(overlay_options)
var overlay_new_event = new Overlay(overlay_options)
var csrftoken = getCookie('csrftoken')
function getFormData($form){
    var unindexed_array = $form.serializeArray();
    var indexed_array = {};

    $.map(unindexed_array, function(n, i){
        indexed_array[n['name']] = n['value'];
    });

    return indexed_array;
}

function getCookie(name) {
		    var cookieValue = null;
		    if (document.cookie && document.cookie !== '') {
		        var cookies = document.cookie.split(';');
		        for (var i = 0; i < cookies.length; i++) {
		            var cookie = cookies[i].trim();
		            // Does this cookie string begin with the name we want?
		            if (cookie.substring(0, name.length + 1) === (name + '=')) {
		                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                break;
		            }
		        }
		    }
		    return cookieValue;
		}

buildList()

function getData() {
    var url = '/api/events/'
    fetch(url)
        .then((resp) => resp.json())
        .then(function (data) {
            events = data
            //                console.log(events)
        });
    return events
}
//function getIcons(){
//    
//}

function icon_render(data, id, color_id){
    $(`#form-event-edit-${id} .title-icon-container`).append(data.inline_svg)
    $(`#form-event-edit-${id} .title-icon-container`).find('svg path').css({fill: '#'+colors[color_id].color, 'fill-opacity': 1})
}
function buildList() {
    //var wrapper = document.getElementById('list-wrapper')
    //wrapper.innerHTML = ''

    var url = '/api/events/'
    
    fetch(url)
        .then((resp) => resp.json())
        .then(function (data) {
            //				console.log('Data:', data)
            events = data
            for (let i in events) {
                let event_date = events[i].date_time
                if($(`#${event_date} ul li`).length){
                    console.log(event_date)
                    $(`#${event_date} ul`)[0].innerHTML = ''
                }
            }
            for (let i in events) {
                let event_color = colors[+events[i].event_color-1]
                let event_date = events[i].date_time
                if($(`#${event_date} ul`).length){
                    $(`#${event_date} ul`).append(
                        `<li style="background:${event_color.rgba}; color:#ffffff" class="event" data-id="${events[i].id}">${events[i].title}</li>`)
                }
            }
        });
}

function newEvent(date) {
    overlay_new_event.content.innerHTML = ''
//    console.log("newEvent", date)
    let new_event_render = ''
    let icons_list = []//[{value: '', selected: true, description: '', imageSrc: ''}]
    let colors_list = []
    let icons_render = ''
    let colors_render = ''
    let url_icons = '/api/icons/'
    let url_colors = '/api/colors/'
    let date_this = new Date(date)
    let year = date_this.getFullYear()
    let day_month = date_this.toLocaleString('ru', {
        day: 'numeric',
        month: 'long',
        });
    fetch(url_icons)
        .then((resp) => resp.json())
        .then(function (data) {
            for (let i in data) {
                icons_list.push({
                    value: data[i].id,
                    selected: false,
                    description: '',
                    imageSrc: data[i].icon,
                    svgInline: data[i].inline_svg
                })
            }
//             for (let i in colors) {
//                 colors_render += `
// <label id="${colors[i].color}">
//   <input type="radio" name="event_color" value="${colors[i].id}">
//   <div class="button"><span></span></div>
// </label>`
            // }
            for (let i in colors) {
                colors_list.push({
                    value: +i+1,
                    selected: false,
                    description: '',
                    imageSrc: '',
                    svgInline: `<label id="${colors[i].color}">
                    <input type="radio" name="event_color" value="${colors[i].id}">
                    <div class="button"><span></span></div>
                  </label>`
                })
                colors_render += `
<label id="${colors[i].color}">
  <input type="radio" name="event_color" value="${colors[i].id}">
  <div class="button"><span></span></div>
</label>`

            }
            //            for (let i in data){
            ////                console.log("AAA",icons_list[i])
            //                icons_render += `
            //                <option value='${data[i].id}' data-imagesrc='${data[i].icon}'></option>
            //`           }
            new_event_render += `
    <input type="hidden" name="date_time" id="date-input-hidden" value=${date}>
    <div class="title-icon-container">
    <input type="text" class="form-control event-input" name="title" id="event-title" placeholder="Выберите тему...">
    <div id="icons-select"></div>
    <div id="colors-select"></div>
    </div>
    <textarea class="event-description" name="description" id="event-desc" placeholder="Введите описание.."></textarea>
`
            overlay_new_event.content.innerHTML += `
<div class="modal-header">
    <h5 class="modal-title" id="exampleModalLabel"><span class="modal-year">${year}</span></br>${day_month}</h5>
    <button type="button" class="close" data-dismiss="modal" onclick="overlay_new_event.close()" aria-label="Close">
        <span aria-hidden="true">&times;</span>
    </button>
</div>
<div class="modal-body">
    <form id="form-event-create">

        ${new_event_render}
    <div class="modal-footer">
        <input id="submit" class="btn btn-submit" type="submit" value="Сохранить">
        <i class="arrow"></i>
    </div>

    </form>
</div>
`
            overlay_new_event.open()
            $('#icons-select').ddslick({
                data: icons_list,
                input_name: "icon",
                width: 75,
                selectText: "",
                imagePosition: "right",
                onSelected: function (selectedData) {
                }
            });
            $('#colors-select').ddslick({
                data: colors_list,
                input_name: "event_color",
                width: 75,
                selectText: "",
                imagePosition: "right",
                onSelected: function (selectedData) {
                    let i = selectedData.selectedIndex
                    $('#icons-select svg path').css({ fill: '#'+colors[i].color, 'fill-opacity': 1, })
                }
            });
            // $('.dd-options.dd-click-off-close').append(colors_render)
            let form = $('#form-event-create')
            form.on('submit', function (e) {
                e.preventDefault()
                var url = '/api/events/'
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-type': 'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body: JSON.stringify(getFormData(form))
                    }).then(function (response) {
//                        console.log("response", response)
                        console.log(JSON.stringify(getFormData(form)))
                        buildList()
                        form[0].reset()
                        overlay_new_event.close()
                    })

                //                var title = document.getElementById('title').value
                //                fetch(url, {
                //                    method: 'POST',
                //                    headers: {
                //                        'Content-type': 'application/json',
                //                        'X-CSRFToken': csrftoken,
                //                    },
                //                    body: JSON.stringify({
                //                        'title': title
                //                    })
                //                }).then(function (response) {
                //                    buildList()
                //                    document.getElementById('form').reset()
                //                })
            })
    })
    var data_check = $(`#${date}`)
}

//
function editEvent(event_id) {
//    let form = document.getElementById('form-edit-event')
   let url = `/api/events/${event_id}/`
   let form = $(`#form-event-edit-${event_id}`)
   fetch(url, {
       method: 'PUT',
       headers: {
           'Content-type': 'application/json',
           'X-CSRFToken': csrftoken,
       },
       body: JSON.stringify(getFormData(form))
   }).then(function (response) {
        buildList()
//        form[0].reset()
//        overlay_new_event.close()
})
}
//
function deleteEvent(event_id) {
       let url = `/api/events/${event_id}/`
       let form = $(`#form-event-edit-${event_id}`)
       fetch(url, {
           method: 'DELETE',
           headers: {
               'Content-type': 'application/json',
               'X-CSRFToken': csrftoken,
           },
           body: JSON.stringify(getFormData(form))
       }).then(function (response) {
            if(response.ok){
                $(`#form-event-edit-${event_id}`).remove()
            }
            buildList()
    //        form[0].reset()
    //        overlay_new_event.close()
    })
    }
//
//on date click events render
function dayEvents(date_data) {
    let url = '/api/events/'
    fetch(url)
        .then((resp) => resp.json())
        .then(function (data) {
            var icon_url = ''
            events = data
            let day_events_render = ''
            overlay_day_events.content.innerHTML = ''
            let date_this = new Date(date_data.id)
            let year = date_this.getFullYear()
            let day_month = date_this.toLocaleString('ru', {
                day: 'numeric',
                month: 'long',
              });
            for (let i in events) {
//                console.log("Events", events)
                if (date_data.id == events[i].date_time) {
                    $.ajax({
                        url: `/api/icons/${events[i].icon}`,
                        type: "GET", // Что бы воспользоваться POST методом, меняем данную строку на POST
//                        data: {
//                            id: jsonCommon[i]["ID"],
//                            comment_o: JSON.stringify(jsonCommon[i]["comment_o"])
//                        },
                        success: function (response) {
                            // console.log(response.icon)
                            icon_render(response, events[i].id, events[i].event_color-1)
                            
                        }
                    })
                    console.log(icon_url)
                    day_events_render += `
                <form id="form-event-edit-${events[i].id}">
                    <div class="event-container">
                        <button type="button" class="close" onclick="deleteEvent(${events[i].id})">
                        <span aria-hidden="true">×</span>
                    </button>
                        <div class="title-icon-container">
                            <input type="text" name="title" data-id="${events[i].id}" onblur="editEvent(${events[i].id});" id="event-title" class="form-control event-title" value="${events[i].title}">
                        </div>
                        <input type="text" data-id="${events[i].id}" onblur="editEvent(${events[i].id});" placeholder="Введите описание.." id="event-desc" class="form-control event-desc" name="description" value="${events[i].description}">
                        <input type="hidden" name="date_time" data-id="${events[i].id}" value="${events[i].date_time}">
                        <input type="hidden" name="icon" data-id="${events[i].id}" value="${events[i].icon}">
                        <input type="hidden" name="event_color" data-id="${events[i].id}" value="${events[i].event_color}">
                    </div>
                    <hr>
                </form>
    `
                }
            }
            overlay_day_events.content.innerHTML += `
    <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel"><span class="modal-year">${year}</span></br>${day_month}</h5>
        <button type="button" class="close" data-dismiss="modal" onclick="overlay_day_events.close()" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
    <div class="modal-body">

        ${day_events_render}

    </div>
    <div class="modal-footer">
            <button type="button" class="btn btn-submit" onclick="overlay_day_events.close(); newEvent('${date_data.id}');">Новое событие</button>
    </div>
`
//            $('#icons-select').ddslick({
//                data: icons_list,
//                width: 75,
//                selectText: "",
//                imagePosition: "right",
//                onSelected: function (selectedData) {
//                    //callback function: do something with selectedData;
//                }
//            });
            overlay_day_events.open()
        });
}

//appearence
$('#config svg').click(function(){
    if ($(this).hasClass('active')) {
        $('#config .config-modal-form').height('');
        $(this).removeClass('active');
    } else {
        // console.log(+$(this).find('form').height()+50)
        $('#config .config-modal-form').height(+$('#config .config-modal-form').find('form').height()+80);
        $(this).addClass('active');

    }
});