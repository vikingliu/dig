var extract_result = document.getElementById("show_extract_result");
if (extract_result == null) {
    var div = document.createElement('div');
    div.setAttribute('id', 'show_extract_result');
    div.innerHTML = ''
        + '<div id="popupContainer">'
        + '    <div id="popupContent">'
        + '    </div>'
        + '</div>';
    document.body.append(div);
    chrome.runtime.onMessage.addListener(
        function (request, sender, sendResponse) {
            var msg = 'Yes, Commander.';
            if (request.cmd === 'show') {
                msg += ' I have show it.'
                show_extract_result(request.config)
            } else if (request.cmd === 'hidden') {
                msg += ' I have hidden it.'
                hidden_extract_result()
            }
            sendResponse({msg: msg});
            return false
        }
    );
}

var ERROR_HEAD = '「PATH ERROR!!!」'

function show_extract_result(config) {
    console.log(config);

    function get_page_type(page_type) {
        var html = ''
            + '  <div class="pe-row">'
            + '    <div class="pe-name">Page Type</div>'
            + '    <div class="pe-content">' + config.page_type + '    </div>'
            + '  </div>'
        return html
    }

    function get_url_patterns(url_patterns) {
        var html = ''
            + '  <div class="pe-row">'
            + '    <div class="pe-name">Url Patterns</div>'

        if (url_patterns.length > 0) {
            html += '    <div class="pe-content">'
            url_patterns.forEach(function (value, index) {
                var find = location.href.search(value)
                html += '<p>'
                if (find === -1) {
                    html += '<span class="not-match">not match: </span>'
                } else {
                    html += '<span class="match">match: </span>'
                }
                html += value + '</p>'
            });
            html += '    </div>'
        }

        html += '  </div>'
        return html
    }

    function get_list_result(list_rule, item_rules) {
        let html = ''
        let items = []
        let list_result = extract_result_by_rule(list_rule, document);
        if (list_result.length > 0) {
            list_result.forEach(function (value, index) {
                items.push(extract_item_result(item_rules, value))
            });
            html += ''
                + '  <div class="pe-row">'
                + '    <div class="pe-name">Item List</div>'
            if (typeof list_result[0] == 'string' && list_result[0].startsWith(ERROR_HEAD))
                html += '    <div class="pe-content pe-error">' + list_result[0] + '</div>'
            else
                html += '    <div class="pe-content"> Find ' + list_result.length + ' items</div>'
            html += '  </div>'
        } else {
            let item = extract_item_result(item_rules, document)
            console.log("only one: ", item)
            if (Object.keys(item).length > 0) items.push(item)
        }
        if (items.length > 0) {
            html += ''
                + '<div class="pe-row">'
                + '  <div class="pe-items">'
            items.forEach(function (value, index) {
                html += ''
                    + '  <div class="pe-row pe-item">'
                    + '   <div> item - ' + (index + 1) + '</div>'
                for (let key in value) {
                    let error_class = ''
                    html += ''
                        + '   <div class="pe-name">' + key + '</div>'
                    if (value[key].length > 0 && value[key][0].startsWith(ERROR_HEAD))
                        error_class = 'pe-error'
                    html += '   <div class="pe-content ' + error_class + '">' + htmlencode(value[key]) + '</div>'

                }
                html += ' </div>'
            });
            html += ''
                + '    </div>'
                + '  </div>'
        }
        return html
    }

    function extract_item_result(item_rules, response) {
        let item = {}
        item_rules.forEach(function (item_rule, index) {
            item_values = extract_result_by_rule(item_rule, response)
            item_values_str = []
            item_values.forEach(function (item_value) {
                if (item_value instanceof HTMLElement) {
                    item_values_str.push(item_value.innerHTML)
                } else {
                    item_values_str.push(item_value)
                }
            });
            if (item_rule.name || item_rule.path) {
                item[item_rule.name] = item_values_str
            }
        });
        return item
    }

    function get_next_page_url(next_page_rule) {
        var html = ''
        if (next_page_rule.path) {
            html += ''
                + '  <div class="pe-row">'
                + '    <div class="pe-name">Next Page Url</div>'
            let next_page_url = extract_result_by_rule(next_page_rule, document)
            let error_class = ''
            if (next_page_url.length > 0 && next_page_url[0].startsWith(ERROR_HEAD))
                error_class = 'pe-error'
            html += '   <div class="pe-content ' + error_class + '">' + next_page_url + '</div>'
                + '  </div>'
        }
        return html
    }

    var html = ''
        + get_page_type(config.page_type)
        + get_url_patterns(config.url_patterns)
    if (config.page_type === 'List Page') {
        html += get_next_page_url(config.next_page_rule)
    }
    html += get_list_result(config.list_rule, config.item_rules)
    var popupContent = document.getElementById("popupContent")
    popupContent.innerHTML = html
    var popupContainer = document.getElementById("popupContainer");
    popupContainer.style.display = "block";
}


function extract_result_by_rule(rule, response = document) {
    if (rule.path === '') return []
    try {
        var result = []
        if (rule.path_type === 'xpath') {
            var nodes = document.evaluate(rule.path, response)
            do {
                var node = nodes.iterateNext()
                if (node) {
                    result.push(node)
                }
            } while (node)
        } else if (rule.path_type === 'css') {
            var paths = rule.path.split('::')
            var css = paths[0]
            var attrib = paths.length === 2 ? paths[1].trim() : ''
            response.querySelectorAll(css).forEach(function (node, index) {
                var value = node
                if (attrib === 'text')
                    value = node.innerText
                else if (attrib === 'html')
                    value = node.innerHTML
                else if (attrib.startsWith('attr')) {
                    var key = attrib.replace('attr(', '').replace(')', '').trim()
                    value = node.getAttribute(key)
                }
                result.push(value);
            });
        } else if (rule.path_type === 'jpath') {

        } else if (rule.path_type === 're') {

        }
    } catch (error) {
        result.push(ERROR_HEAD + error.message)
    }
    return result
}


function htmlencode(html) {
    let div = document.createElement('div')
    div.innerText = html
    return div.innerHTML
}

function hidden_extract_result() {
    var popupContainer = document.getElementById("popupContainer");
    popupContainer.style.display = "none";
}

function sendmsg(msg) {
    chrome.runtime.sendMessage(msg, function (e) {
        console.log(e)
    });
}




