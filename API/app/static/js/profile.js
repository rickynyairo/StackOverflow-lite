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

function getAnswerQuestions(){
    let answers = thisElem("answersDiv").children;
    Array.from(answers).forEach((answer) => {
        let qId = parseInt(answer.getAttribute("name"));
        let aId = answer.id
        let questionLink = `<a href="/questions/${qId}">See Question</a>`;
        makeElement("p", "class", "answerMeta", aId, questionLink);
    });
}
function validProfileUser(resp){
    if (resp.message == "Valid"){
        thisElem("answerTab").style.display = "block";
        thisElem("signOutLink").style.display = "block";
        thisElem("signInLink").style.display = "none";
        thisElem("signUpLink").style.display = "none";
        thisElem("profileLink").innerHTML = localStorage.getItem("username");
        thisElem("profileLink").style.display = "inline-block";
        let userId = localStorage.getItem("profileId");
        getAnswers(`/api/v2/answers/users/${userId}`);
    }
    getQuestions(`/api/v2/questions/${currUser}`);
}
if (token){
    validateUser(token, validProfileUser);
}else{
    getQuestions(`/api/v2/questions/${currUser}`);
}


