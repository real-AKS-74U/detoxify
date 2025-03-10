document.addEventListener('DOMContentLoaded', function () {
    chrome.storage.local.get('enabled', function (data) {
        if (data.enabled === undefined) {
            chrome.storage.local.set({ 'enabled': true });
            document.getElementById('toggle').checked = true;
        } else {
            document.getElementById('toggle').checked = data.enabled;
        }
    });
});

document.getElementById('toggle').addEventListener('change', function () {
    // if toggle is checked then set enabled to true and vice versa
    chrome.storage.local.set({ 'enabled': this.checked });
    // send message to background.js to enable or disable the extension
    chrome.runtime.sendMessage({ 'enabled': this.checked });
});