const manage = 'sidepanel.html';

chrome.runtime.onInstalled.addListener(() => {
    chrome.sidePanel.setPanelBehavior({openPanelOnActionClick: true});
});

chrome.tabs.onActivated.addListener(async ({tabId}) => {
    const {path} = await chrome.sidePanel.getOptions({tabId});
    chrome.sidePanel.setOptions({path: mainPage});
});
