const videoId = window.location.href.split('/').pop().split('?')[1].split('=')[1];
const comments = [];
const isFiltered = false;
// const apiEndpoint = "http://api.ayushch.xyz";
const apiEndpoint = "http://127.0.0.1:5000"

function filterComments() {
    let unfilteredComments = [];

    comments.forEach(comment => {
        if (!comment.filtered) {
            unfilteredComments.push(
                {
                    author: comment.author,
                    text: comment.text
                }
            );
        }
    });

    return fetch(apiEndpoint + "/filter", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(unfilteredComments)
    }).then((response) => {
        return response.json();
    })
}

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
            element: commentElement,
            videoId,
            filtered: false
        };
        commentList.push(comment);
    }
    return commentList;
}

chrome.storage.local.get('enabled', function (data) {
    if (data.enabled === undefined) {
        chrome.storage.local.set({ 'enabled': true });
    }
    if (data.enabled) {
        setInterval(() => {
            if (comments.length < document.querySelectorAll("#comment").length) {
                let scrapedComments = scrapeComments();
                comments.push(...scrapedComments);
                console.log(comments);
                (async () => {
                    let cmts = await filterComments();
                    // response = {data: [{author: "author", text: "text", spam: true/false}...], success: true}
                    cmts = cmts.data;
                    cmts.forEach((cmt, index) => {
                        comments[index].filtered = true;
                        if (cmt.spam) {
                            comments[index]['spam'] = true;
                            comments[index].element.style.display = "none";
                            console.log(comments[index]['text']);
                        }
                    });
                })();
            }
        }, 1000);
    }
});