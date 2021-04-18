const cities_ul = document.querySelector('#cities-list ul');
const filters = document.querySelector('.filters');
const cafes_list = document.querySelector('.cafe-list');
const cafe_quantity = document.querySelector('.cafe-quantity');
const cafe_form = document.querySelector('.edit_form form');

const cafe_url = {};
const cafe_names = {};
const cafe_markers = {};
const cafe_popups = {};
let map = {};
let current_id = "0";


function populate_cities() {
    let response = get_request('/cities');
    response.then(data => {
        let li_html = ``;
        for (let i = 0; i < data.length; i++) {
            let data_item = data[i];
            li_html = li_html + `<li class="nav-city"><a href="${data_item.link}">${data_item.city}</a></li>`
        }
        cities_ul.innerHTML = li_html;
    });
}

function add_cafe(e) {
    e.preventDefault();

    let form_data = new FormData(cafe_form);
    let form_data_object = Object.fromEntries(form_data.entries());

    let request = get_request('/cafes', {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(form_data_object)
    })

    request.then(data => {
        cafe_form.innerHTML = `<h1>${data.Status}</h1>`
    })
}

async function get_request(url, params = {}) {
    let response = await fetch(url, params);
    return await response.json();
}

function processFilters() {
    let filers_elements = filters.querySelectorAll('input');
    let has_wifi = false;
    let has_sockets = false;
    let has_phone = false;
    let has_toilet = false;

    filers_elements.forEach(el => {
        if (el.checked) {
            if (el.id === 'has-wifi') {
                has_wifi = true;
            } else if (el.id === 'has-sockets') {
                has_sockets = true;
            } else if (el.id === 'has-phone') {
                has_phone = true;
            } else if (el.id === 'has-toilet') {
                has_toilet = true;
            }
        }
    });

    let cafes_elements = cafes_list.querySelectorAll('.cafe-info');
    let quantity = 0;
    cafes_elements.forEach(el => {
        let visibility = true;
        if (has_wifi) {
            if (!el.classList.contains('has-wifi')) {
                visibility = false
            }
        }
        if (has_sockets) {
            if (!el.classList.contains('has-sockets')) {
                visibility = false
            }
        }
        if (has_phone) {
            if (!el.classList.contains('has-phone')) {
                visibility = false
            }
        }
        if (has_toilet) {
            if (!el.classList.contains('has-toilet')) {
                visibility = false
            }
        }
        if (visibility) {
            el.style.display = 'flex';
            quantity++;
        } else {
            el.style.display = 'none';
        }
    });

    cafe_quantity.textContent = `${quantity} WORK-FRIENDLY PLACES`
}

function initMap() {
    let city = document.querySelector('.city').textContent;
    let zoom

    if (city === 'ALL CITIES') {
        city = 'Paris';
        zoom = 3;
    } else {
        zoom = 10;
    }

    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({address: city}, (results, status) => {
        if (status === 'OK') {
            // map.setCenter(results[0].geometry.location);
            let city_coords = {}
            city_coords.lat = results[0].geometry.location.lat();
            city_coords.lng = results[0].geometry.location.lng();
            let mapProp = {
                center: city_coords,
                zoom: zoom,
            };
            map = new google.maps.Map(document.getElementById("google-map"), mapProp);

            create_markers(map);
        }
    });

}

function collect_cafe_data() {
    if (cafes_list !== null){
        let cafe_infos = cafes_list.querySelectorAll('.cafe-info');
        cafe_infos.forEach(cafe_info => {
            let url_a = cafe_info.querySelector('.cafe-data .location a');
            let name_p = cafe_info.querySelector('.cafe-data .cafe-name');
            cafe_url[cafe_info.getAttribute('cafe_id')] = url_a.getAttribute('href');
            cafe_names[cafe_info.getAttribute('cafe_id')] = name_p.textContent;
        });
    }
}

function create_markers(map) {
    for (let cafe_id in cafe_url) {
        //REQUEST TO PYTHON API
        let response = get_request('/unpack_google_url?short_url=' + cafe_url[cafe_id]);
        response.then(data => {
            if (data.status === 'OK') {
                let pos = {lat: Number(data.lat), lng: Number(data.lng)};
                // CREATE MARKERS
                cafe_markers[cafe_id] = new google.maps.Marker({
                    position: pos,
                    map,
                    title: cafe_names[cafe_id],
                });
                //CREATE POPUPS
                cafe_popups[cafe_id] = new google.maps.InfoWindow({
                    content: cafe_names[cafe_id],
                });

            }
        });
    }
}

function cafe_list_mouse_event(e) {
    let cafe_info = e.target.closest('.cafe-info');
    let new_id;
    if (cafe_info === null) {
        new_id = "0"
    } else {
        new_id = cafe_info.getAttribute('cafe_id');
    }
    if (new_id !== current_id) {
        if (current_id !== "0" && current_id in cafe_popups){
            cafe_popups[current_id].close();
        }

        if (new_id !== "0" && new_id in cafe_markers){
            cafe_popups[new_id].open(map, cafe_markers[new_id]);
        }
        current_id = new_id;
    }
}

collect_cafe_data();
populate_cities();
