
const tag_input = document.getElementById('tag-input');
const tag_container = document.getElementById('tag-container')

var timerId;

let tags = new Set();

tag_input.addEventListener('keyup', function (event) {
    if (event.key === ' ') {
        if (event.target.value === "")
            return;
        let value = event.target.value.trim();
        if (confirm(`This will create tag '${value}' once the form is submitted. Are you sure?`)) {
            add_tag(value);
            tags.add(value);
        }
    }
});

tag_input.addEventListener('input', async function (event) {
    value = event.target.value;

    if (value.length < 3) {
        if (timerId !== undefined)
            clearTimeout(timerId);
        return;
    }

    if (timerId !== undefined)
        clearTimeout(timerId);

    timerId = setTimeout(() => searchTag(value), 300);
});

async function searchTag(value) {
    // TODO: Show 'Searching tags...'

    const res = await fetch(`/documents/tags?text=${value}`);
    const json = await res.json();

    let available_tags = JSON.parse(json.tags);

    tag_container.innerHTML = "";
    let newHTML = "";

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
}

function remove_tag(tag_name) {
    if (confirm("Delete tag '"+tag_name+"' from this document?")) {
        tags.delete(tag_name);
        show_tags();
    }
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