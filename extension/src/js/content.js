const videoId = window.location.href.split('/').pop().split('?')[1].split('=')[1];
const comments = [];

function scrapeComments() {
    let commentList = [];
    let commentElements = document.querySelectorAll("#comment");

    for (let i = comments.length; i < commentElements.length; i++) {
        let commentElement = commentElements[i];
        let body = commentElement.querySelector("#body");
        let main = body.querySelector("#main");

        let header = main.querySelector("#header");
        let author = header.querySelector("#header-author");
        let authorName = author.querySelector("#author-text").innerText.trim();

        let expander = main.querySelector("#expander");
        let commentText = expander.querySelector("#content-text").innerText

        let comment = {
            author: authorName,
            text: commentText,
            element: commentElement
        };
        commentList.push(comment);
    }
    return commentList;
}

isExtensionOff = false;
chrome.storage.local.get('enabled', function (data) {
    isExtensionOff = !data.enabled;
});

if (!isExtensionOff) {
    setInterval(() => {
        if (comments.length < document.querySelectorAll("#comment").length) {
            let scrapedComments = scrapeComments();
            comments.push(...scrapedComments);
            console.log(comments);
        }
    }, 1000);
}