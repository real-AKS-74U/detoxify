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
    chrome.storage.local.set({ 'enabled': this.checked });
    // chrome.runtime.sendMessage({ 'enabled': this.checked });
});