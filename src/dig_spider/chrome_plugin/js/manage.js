chrome.storage.local.getKeys().then((keys) => {
    search(keys)
    $('#search_count').text("find keys: " + keys.length)
});

function search(keys) {
    chrome.storage.local.get(keys).then((result) => {
        keys.forEach(function (key, i) {
            add_record(key, result[key])
        });
        $('.delete-key').click(function (e) {
            let key = $(this).attr('key')
            delete_key(key)
        });
    });
}

function delete_key(key) {
    let result = confirm("delete " + key + '?')
    if (result) {
        chrome.storage.local.remove(key)
        location.reload()
    }
}

function add_record(key, config) {
    let html = ''
        + '<div class="row">'
        + '  <div>'
        + '    <input class="pe-key" value="' + key + '" />'
        + '    <button class="delete-key" key="' + key + '" onclick="delete_key(\'' + key + '\')">delete</button>'
        + '  </div>'
        + '    <div><pre>' + syntaxHighlight(JSON.stringify(config, null, 2)) + '</pre></div>'
        + '</div>'
    $('.content-list').append(html)


}

$(document).ready(function () {
    $('#search').click(function (e) {
        let key = $('.search-key').val().trim();
        if (key) {
            $('.content-list').html('')
            search([key])
            $('#search_count').text('')
        }
    });
});


function syntaxHighlight(json) {
    if (typeof json != 'string') {
        json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
        function (match) {
            var cls = 'number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'key';
                } else {
                    cls = 'string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'boolean';
            } else if (/null/.test(match)) {
                cls = 'null';
            }
            return '<span class="' + cls + '">' + match + '</span>';
        }
    );
}