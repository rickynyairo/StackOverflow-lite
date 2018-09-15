const token = localStorage.getItem("AuthToken");

function makeQuestion(element){
    let questionId = element["question_id"];
    let text = element["text"];
    let username = element["username"];
    let description = element["description"];
    let dateCreated = element["date_created"];
    let question = makeElement("div", "id", questionId, "questionsDiv");
    makeElement("p", "class", "questionTitle", questionId, text);
    makeElement("p", "class", "questionDesc", questionId, description);
    let meta = `Asked by ${username} on ${dateCreated}`;
    makeElement("p", "class", "questionMeta", questionId, meta);
    let ansLink = `<a href="/questions/${questionId}">See Answer(s)</a>`;
    makeElement("p", "class", "linkSpan", questionId, ansLink);
    return question;
}

function getQuestions(){
    let path = "/api/v2/questions";
    getData(path)
    .then((response) => {
        if (response.status == 200){
            response.json().then((data) => {
                let questions = data["questions"];
                console.log(questions);
                $("#paginationDiv").pagination({
                    dataSource:questions,
                    callback:(data, pagination)=>{
                        $("#questionsDiv").empty();
                        data.forEach((question) => {
                            makeQuestion(question);
                        });
                    },
                    position:"bottom"
                });        
            });
        }
        else{
            response.json().then((data) => {
                console.log("Failed:\n" + data);
            });
        }
    });
}
function showPostQuestion(resp){
    if (resp.message === "Valid"){
        thisElem("postQuestionFieldset").style.display = "block";
    }
}
function refreshQuestions(){
    // clear the current questions
    elems = thisElem("questionsDiv").children;
    Array.from(elems).forEach((elem) => {
        elem.parentNode.removeChild(elem);
    });
    // refresh questions
    getQuestions();
}
getQuestions();
if (token){
    validateUser(token, showPostQuestion);
}