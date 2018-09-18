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
function validProfileUser(resp){
    if (resp.message == "Valid"){
        validatedUser = true;
        thisElem("answerTab").style.display = "block";
        thisElem("signOutLink").style.display = "block";
        thisElem("signInLink").style.display = "none";
        thisElem("profileLink").innerHTML = localStorage.getItem("username");
        thisElem("profileLink").style.display = "inline-block";
    }
}
if (token){
    validateUser(token, validProfileUser);
}
getQuestions(`/api/v2/questions/${currUser}`)
.then(()=>{
    thisElem("questionsAsked").innerHTML = thisElem("questionsDiv").children.length;
});
