$(document).ready(function () {
    $("#url_patterns").on('input', function (e) {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });

    $('.pe-page-type').change(function (e) {
        var page_type = $('.pe-page-type option:selected').text();
        if (page_type === 'Detail Page') {
            $('#list_rule').hide()
            $('#next_page_rule').hide()
        } else {
            $('#list_rule').show()
            $('#next_page_rule').show()
        }
        console.log(page_type);
    });

    $('.pe-add-rule').click(function (e) {
        var item_urle = $('.item-rule')[0].outerHTML;
        $('.item-rules').append(item_urle);
        $('.pe-remove-rule').click(function (e) {
            if ($('.item-rule').length > 1) {
                $(this).parent().parent().detach();
            }
        });
    });

    $('#show_extract_result').click(function (e) {
        var value = $('#show_extract_result').text()
        if (value === 'check extract result') {
            $('#show_extract_result').text("hidden extract result")
            sendMessageToActiveTab({cmd: "show", config: get_config()})
        } else {
            $('#show_extract_result').text("check extract result")
            sendMessageToActiveTab({cmd: "hidden"})
        }
    });
    $('#export_config').click(function (e) {
        function convert_rule(rule) {
            return rule.path_type + '{' + rule.path + '}' + rule.funcs
        }
        let config = get_config()
        console.log(config['url_patterns'])
        config['list_rule'] = convert_rule(config['list_rule'])
        config['next_page_rule'] = convert_rule(config['next_page_rule'])
        let item_rules = {}
        config['item_rules'].forEach(function (v, i) {
            if (v.name)
                item_rules[v.name] = convert_rule(v)
        });
        if (Object.keys(item_rules).length > 0)
            config['item_rules'] = item_rules
        else
            delete config['item_rules']
        let page_extract_config = {
            'extract': [
                {'page': config}
            ]
        }
        let text = jsyaml.dump(page_extract_config)
        let url = $('#cur_url').text()
        let file_name = url.split('/')[2] + '.yaml'
        download(text, file_name)
    });
});

function get_config() {
    var page_config = {
        'page_type': $('.pe-page-type option:selected').text(),
        'url_patterns': get_url_patterns(),
        'list_rule': get_rule('#list_rule'),
        'next_page_rule': get_rule('#next_page_rule'),
        'item_rules': get_item_rules('#item_rules')
    }
    return page_config;
}

function get_url_patterns() {
    var urls = $('#url_patterns').val().split('\n');
    var url_patterns = []
    for (var i = 0; i < urls.length; i++) {
        var url = urls[i].trim();
        if (url !== '') {
            url_patterns.push(url)
        }
    }
    return url_patterns;
}

function get_item_rules(items) {
    var items_rules = [];
    $(items).find('.item-rule').each(function (i, v) {
        items_rules.push(get_rule(v));
    });
    return items_rules
}

function get_rule(item) {
    var name = $(item).find('.pe-name').val().trim();
    if (name === '') {
        name = $(item).find('.pe-name').text().trim();
    }
    var path_type = $(item).find('.pe-type option:selected').text();
    var path = $(item).find('.pe-path').val().trim();
    var funcs = $(item).find('.pe-funcs').val();
    if (funcs !== undefined) {
        funcs = funcs.trim()
    }else{
        funcs = ''
    }
    return {'name': name, 'path_type': path_type, 'path': path, 'funcs': funcs}
}

function load_config(url, tabid) {
    chrome.scripting.executeScript({
        target: {tabId: tabid},
        files: ["js/content-script.js", "css/content.css"]
    });
    $('#cur_url').text(url);
    $('#show_extract_result').text("check extract result")
    $('#downloadfile').hide()
    sendMessageToActiveTab({cmd: "hidden"})
}


function download(text, name, type = 'text/plain') {
    var a = document.getElementById("downloadfile");
    var file = new Blob([text], {type: type});
    a.href = URL.createObjectURL(file);
    a.innerText = "Download Config: " + name;
    a.download = name;
    a.style.display = 'block';
}

chrome.tabs.onUpdated.addListener(function (number, changeInfo, tab) {
    load_config(tab.url, tab.id)
});
chrome.tabs.onActivated.addListener(function (activeInfo) {
    chrome.tabs.get(activeInfo.tabId, async (tab) => {
        load_config(tab.url, tab.id);
    });
});

(async () => {
    // see the note below on how to choose currentWindow or lastFocusedWindow
    const [tab] = await chrome.tabs.query({active: true, lastFocusedWindow: true});
    if (tab) {
        load_config(tab.url, tab.id);
    }
})();

function sendMessageToActiveTab(message) {
    (async () => {
        // see the note below on how to choose currentWindow or lastFocusedWindow
        const [tab] = await chrome.tabs.query({active: true, lastFocusedWindow: true});
        if (tab) {
            console.log('send msg to active tab: ', message);
            chrome.tabs.sendMessage(tab.id, message, function (e) {
                console.log(e)
            });
        }
    })();
}

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.cmd === 'path') {
            console.log(request.value)
        }
        sendResponse({status: "Got it."});
        return false
    }
);