const videoId = window.location.href.split('/').pop().split('?')[1].split('=')[1];
const comments = [];
alert(videoId);

function scrapeComments() {
    let commentList = [];
    let commentElements = document.querySelectorAll("#comment");

    commentElements.forEach((commentElement) => {
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
    });
    return commentList;
}

setInterval(() => {
    console.log(scrapeComments());
}, 1000);