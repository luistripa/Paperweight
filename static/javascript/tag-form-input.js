
const SEARCH_AFTER_N_LETTERS = 3;
const SEARCH_DELAY = 300; // ms

const tag_input = document.getElementById('tag-input');
const tag_container = document.getElementById('tag-container')

var timerId;

let tags = new Set();

tag_input.addEventListener('input', function (event) {
    let value = event.target.value;
    let trimmed_value = value.trim();

    if (trimmed_value.length === 0)
        return;

    if (value[value.length-1] === " ") { // If user pressed the space bar
        clearTimeout(timerId);
        add_tag(trimmed_value);
        tags.add(trimmed_value);

    } else {
        if (trimmed_value.length < SEARCH_AFTER_N_LETTERS) {
            if (timerId !== undefined)
                clearTimeout(timerId);
            clear_tag_display();
            return;
        }
        if (timerId !== undefined)
            clearTimeout(timerId);

        timerId = setTimeout(() => searchTag(trimmed_value), SEARCH_DELAY);
    }
});

async function searchTag(value) {
    let p = document.createElement('p');
    p.innerText = "Searching tags...";
    tag_container.appendChild(p);

    const res = await fetch(`/documents/tags?text=${value}`);
    const json = await res.json();

    let available_tags = JSON.parse(json.tags);

    tag_container.innerHTML = "";

    if (available_tags.length === 0) {
        let p = document.createElement('p');
        p.innerText = 'No tags with that name where found.';
        tag_container.appendChild(p);
        return;
    }

    for (let i = 0; i < available_tags.length; i++) {
        let div = document.createElement('div');
        div.className = "tag"

        let description = document.createElement('div');
        description.className = 'description';
        description.innerText = available_tags[i].fields.name;

        let add_button = document.createElement('div');
        add_button.className = 'add-button';
        add_button.innerText = '+';
        add_button.onclick = function () {
            add_tag(available_tags[i].fields.name);
        }

        div.appendChild(description);
        div.appendChild(add_button);

        tag_container.appendChild(div);
    }
}

function add_tag(tag_name) {
    tags.add(tag_name);
    show_tags();
    clear_tag_input();
}

function remove_tag(tag_name) {
    tags.delete(tag_name);
    show_tags();
}

function clear_tag_input() {
    tag_input.value = "";
    clear_tag_display();
}

function clear_tag_display() {
    tag_container.innerHTML = "";
}

function show_tags() {
    const form_input = document.getElementById('id_tags');
    const tag_list_container = document.getElementById('document-tags-container');

    tag_list_container.innerHTML = "";

    let form_input_str = "";

    tags.forEach(tag => {
        let div = document.createElement("div");
        div.className = "tag";

        let description = document.createElement("div");
        description.className = 'description';
        description.innerText = tag;

        let remove_button = document.createElement("div");
        remove_button.className = 'remove-button';
        remove_button.innerText = 'X';
        remove_button.onclick = function () {
            remove_tag(tag);
        }

        div.appendChild(description);
        div.appendChild(remove_button);

        tag_list_container.appendChild(div);
        form_input_str += tag+" ";
    })

    form_input.value = form_input_str;
}