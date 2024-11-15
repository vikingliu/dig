function search_all() {
    chrome.storage.local.getKeys().then((keys) => {
        search(keys)
    });
}


function search(keys) {
    chrome.storage.local.get(keys).then((result) => {
        add_records(keys, result)
        $('#search_count').text("find keys: " + Object.keys(result).length)
        $('.delete-key').click(function (e) {
            let key = $(this).attr('key')
            delete_key(key)
        });
        $('.pe-type:first').attr("class", "pe-type selected")
        $('.pe-type').click(function (e) {
            let key = $(this).attr('key')
            $('.pe-type').attr("class","pe-type")
             $(this).attr("class", "pe-type selected")
            chrome.storage.local.get(key).then((result) => {
                let config = syntaxHighlight(JSON.stringify(result[key], null, 2))
                $('.pe-config pre').html(config)
            });
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

function add_records(keys, result) {
    let keys_html = ''
    let domain_keys = {}
    keys.forEach(function (key, i) {
        let domain = key.split('/')[2]
        if (!(domain in domain_keys)) {
            domain_keys[domain] = ''
        }

        let key_html = ''
            + '<div>'
            + '   &nbsp; -<input class="pe-key" disabled value="' + key + '" />'
            + '   <button class="delete-key" key="' + key + '">delete</button>'
            + '   <button class="pe-type"  key="' + key + '">' + result[key].page_type + '</button>'
            + '</div>'
        domain_keys[domain] += key_html
    });
    for (let domain in domain_keys) {
        keys_html += '<span>' + domain + '</span>'
        keys_html += domain_keys[domain]
        keys_html += '<hr />'
    }
    let config_html = ''
        + '  <pre>'
        + syntaxHighlight(JSON.stringify(result[keys[0]], null, 2))
        + ' </pre>'

    let html = ''
        + '<div class="row">'
        + '  <div class="pe-keys">' + keys_html + '  </div>'
        + '  <div class="pe-config">' + config_html + '  </div>'
        + '</div>'
    $('.content-list').html(html)
}

$(document).ready(function () {
    $('#search').click(function (e) {
        let key = $('.search-key').val().trim();
        if (key) {
            $('.content-list').html('')
            search([key])
        } else {
            search_all()
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

search_all()