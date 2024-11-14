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
    });

    $('.pe-add-rule').click(function (e) {
        add_rule()
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
        let config = get_config()
        let text = get_config_yaml(config)
        let file_name = $('#cur_url').text().split('/')[2] + '.yaml'
        download_config(text, file_name)
    });

    $('select, input').change(function (e) {
        save_config()
    });

    $('#manage').click(function (e) {
        chrome.tabs.create({url: '../manage.html'});
    });
});

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.cmd === 'path') console.log(request.value)
        sendResponse({status: "Got it."});
        return false
    }
);

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
    if (tab) load_config(tab.url, tab.id);
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