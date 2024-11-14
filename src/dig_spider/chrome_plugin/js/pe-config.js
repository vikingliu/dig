// function

function get_url_patterns() {
    var urls = $('#url_patterns').val().split('\n');
    var url_patterns = []
    urls.forEach(function (url, i) {
        url = url.trim()
        if (url !== '') url_patterns.push(url)
    });
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
    if (name === '') name = $(item).find('.pe-name').text().trim();
    var path_type = $(item).find('.pe-type option:selected').text();
    var path = $(item).find('.pe-path').val().trim();
    var funcs = $(item).find('.pe-funcs').val();
    funcs = funcs !== undefined ? funcs.trim() : ''
    return {'name': name, 'path_type': path_type, 'path': path, 'funcs': funcs}
}

function get_config() {
    var page_config = {
        'page_type': $('.pe-page-type option:selected').text(),
        'url_patterns': get_url_patterns(),
        'list_rule': get_rule('#list_rule'),
        'next_page_rule': get_rule('#next_page_rule'),
        'item_rules': get_item_rules('#item_rules')
    }
    // if (page_config.page_type === 'Detail Page') {
    //     delete page_config.list_rule
    //     delete page_config.next_page_rule
    // }
    return page_config;
}

function add_rule() {
    var item_urle = $('.item-rule')[0].outerHTML;
    $('.item-rules').append(item_urle);
    $('.pe-remove-rule').click(function (e) {
        if ($('.item-rule').length > 1) {
            $(this).parent().parent().detach();
        }
    });
    $('select, input').change(function (e) {
        save_config()
    });
    return item_urle
}

function save_config() {
    let config = get_config()
    config.url_patterns.forEach(function (url_pattern, i) {
        let content = {}
        content[url_pattern] = config
        chrome.storage.local.set(content).then(() => {
            console.log("save config to " + url_pattern);
        });
    });
}

function download_config(text, name, type = 'text/plain') {
    var a = document.getElementById("downloadfile");
    var file = new Blob([text], {type: type});
    a.href = URL.createObjectURL(file);
    a.innerText = "Download Config: " + name;
    a.download = name;
    a.style.display = 'block';
}


function load_config(url, tabid) {
    chrome.scripting.executeScript({
        target: {tabId: tabid},
        files: ["js/content-script.js", "js/jsonpath.min.js", "css/content.css"]
    });
    $('#cur_url').text(url);
    $('#show_extract_result').text("check extract result")
    $('#downloadfile').hide()
    sendMessageToActiveTab({cmd: "hidden"})
    chrome.storage.local.getKeys().then((keys) => {
        let find = false
        for (let i in keys) {
            let url_pattern = keys[i]
            if (url.search(url_pattern) > -1) {
                chrome.storage.local.get(url_pattern).then((result) => {
                    let config = result[url_pattern]
                    show_config(config)
                    find = true
                });
                break
            }
        }
        if (!find) {
            clear_config()
        }
    });
}

function clear_config() {
    let config = {
        page_type: "List Page",
        url_patterns: [],
        list_rule: {name: "", path_type: "xpath", path: "", funcs: ""},
        next_page_rule: {name: "", path_type: "xpath", path: "", funcs: ""},
        item_rules: [{name: "", path_type: "xpath", path: "", funcs: ""}]
    }
    show_config(config)
}

function show_config(config) {
    function set_rule(item, rule) {
        if ($(item).find('input.pe-name').length > 0) {
            $(item).find('input.pe-name').val(rule.name);
        } else {
            $(item).find('.pe-name').text(rule.name);
        }
        $(item).find('.pe-type option[name="' + rule.path_type + '"]').attr("selected", "selected");
        $(item).find('.pe-path').val(rule.path);
        $(item).find('.pe-funcs').val(rule.funcs);
    }

    $('.pe-page-type option[name="' + config.page_type + '"]').attr("selected", "selected");
    $('#url_patterns').val(config.url_patterns.join('\n'))
    if (config.page_type === "List Page") {
        $("#list_rule").show()
        $("#next_page_rule").show()
        set_rule('#list_rule', config.list_rule)
        set_rule('#next_page_rule', config.next_page_rule)
    } else {
        $("#list_rule").hide()
        $("#next_page_rule").hide()
    }
    let item_rules = []
    let old_item_rules = $('.item-rules .item-rule')
    if (old_item_rules.length < config.item_rules.length) {
        for (let i = 0; i < config.item_rules.length - old_item_rules.length; i++) {
            add_rule()
        }
        item_rules = $('.item-rules .item-rule')
    } else if (old_item_rules.length > 1) {
        for (let i = config.item_rules.length; i < old_item_rules.length; i++) {
            $(old_item_rules[i]).detach()
        }
        item_rules = old_item_rules
    }
    for (let i = 0; i < item_rules.length; i++) {
        set_rule(item_rules[i], config.item_rules[i])
    }
}


function get_config_yaml(config) {
    function convert_rule(rule) {
        return rule.path_type + '{' + rule.path + '}' + rule.funcs
    }
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
    return jsyaml.dump(page_extract_config)
}

