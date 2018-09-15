const questionId = parseInt(document.getElementsByTagName("h3")[0].getAttribute("id"));
const token = localStorage.getItem("AuthToken");
const postAnswerBtn = thisElem("postAnswer");
let validatedUser = false;

postAnswerBtn.addEventListener('click', ()=>{
    let text = thisElem("answer").value;
    if (text.length < 5){
        thisElem("warnings").innerHTML = "The value for the text is invalid";
    }
    else{
        thisElem("warnings").innerHTML = "";
        postAnswer({"text":text});
    }
});

function makeAnswer(element){
    let answerId = element["answer_id"];
    let text = element["text"];
    let username = element["username"];
    let dateCreated = element["date_created"];
    let upvotes = element["up_votes"];
    makeElement("div", "id", answerId, "answersDiv", "");
    makeElement("p", "class", "answer", answerId, text);
    let meta = `Total votes: ${upvotes}<br/>Answered by ${username} on ${dateCreated}`;
    makeElement("p", "class", "answerMeta", answerId, meta);
    let upBtn = makeElement("button", "class", "buttons", answerId, "Upvote");
    upBtn.setAttribute("onclick", "voteClicked(this)");
    let downBtn = makeElement("button", "class", "buttons", answerId, "Downvote"); 
    downBtn.setAttribute("onclick", "voteClicked(this)");
}
function getAnswers(){
    let path = `/api/v2/questions/${questionId}`;
    return getData(path)
    .then((response) => {
        if (response.status == 200){
            response.json().then((data) => {
                let answers = data["answers"];
                console.log(answers);
                answers.forEach((element) => {
                    makeAnswer(element);
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

function showPostAnswer(resp){
    if (resp.message === "Valid"){
        validatedUser = true;
        thisElem("postAnswerFieldset").style.display = "block";
    }
}
function refreshAnswers(){
    thisElem('postAnswerFieldset').style.display = 'none';
    elems = thisElem("answersDiv").children;
    Array.from(elems).forEach((elem) => {
        if (Number.isInteger(parseInt(elem.id))){
            elem.parentNode.removeChild(elem);
        }
    });
    // refresh questions
    getAnswers()
    .then(()=>{
        if (validatedUser){
            thisElem('postAnswerFieldset').style.display = 'block';
        }
    });
}

function postAnswer(answer){
    let path = `/api/v2/questions/${questionId}/answers`;
    postData(path, answer, token)
    .then((res) => {
        if (res.status == 201){
            res.json().then(data=>{
                console.log(data);
                thisElem("answer").value = "";
                refreshAnswers();
            });
        }
        else{
            res.json().then(data=>{
                console.log("Failed: ", data);
            });
        }
    })
    .catch(error=>{
        console.log("Error: ", error);
    })
}
function voteAnswer(answerId, vote){
    let path = `/api/v2/questions/${questionId}/answers/${answerId}/${vote}`;
    let params = {
        "path":path,
        "data":{},
        "token":token
    }
    putData(params)
    .then((res) => {
        if (res.status == 200){
            res.json().then(data => {
                console.log("Success: ", data);
                refreshAnswers();
            });
        }
        else{
            res.json().then(data => {
                console.log("Failed: ", data);
            });
        }
    })
    .catch(error => {
        console.log("Error: ", error)
    });
}

function voteClicked(button){
    let answerId = parseInt(button.parentNode.id);
    let vote = button.innerHTML.toLowerCase();
    voteAnswer(answerId, vote);
}

getAnswers();
if (token){
    validateUser(token, showPostAnswer);
}