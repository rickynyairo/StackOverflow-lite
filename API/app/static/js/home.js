function makeQuestion(element, isOwner=false){
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
    let links = `<a href="/questions/${questionId}">See Answer(s)</a>`;
    if (isOwner){
        links = `${links}<br/><a onclick=editQuestion(this)>Edit</a>  <a onclick=deleteQuestion(this)>Delete</a>`
    }
    makeElement("p", "class", "linkSpan", questionId, links);
    return question;
}

async function getQuestions(path = "/api/v2/questions"){
    return getData(path)
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
                            if(validatedUser){
                                let username = localStorage.getItem("username");
                                if(question["username"] == username){
                                    makeQuestion(question, true);
                                }else{
                                    makeQuestion(question);
                                }
                            }else{
                                makeQuestion(question);
                            }
                        });
                    }
                });        
            });
        }
        else{
            response.json().then((data) => {
                console.log("Failed:\n" + data);
            });
        }
    })
    .catch(err => {console.error("Error: ", err);});
}
function validUser(resp){
    if (resp.message === "Valid"){
        validatedUser = true;
        thisElem("postQuestionFieldset").style.display = "block";
        thisElem("signOutLink").style.display = "block";
        thisElem("signInLink").style.display = "none";
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
if (window.location.pathname == "/home"){
    getQuestions();
}

if (token){
    validateUser(token, validUser);
}