const currUser = thisElem("username").innerHTML;

function openTab(evt, tabName) {
    let tabContent = document.getElementsByClassName("tabcontent");
    Array.from(tabContent).forEach((tab) => {
        tab.style.display = "none";
    });
    let tabLinks = document.getElementsByClassName("tablinks");
    Array.from(tabLinks).forEach((tabLink) => {
        tabLink.className = tabLink.className.replace(" active", "");
    })
    thisElem(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

getQuestions(`/api/v2/questions/${currUser}`)
.then(()=>{
    thisElem("questionsAsked").innerHTML = thisElem("questionsDiv").children.length;
});
