const questionId = parseInt(document.getElementsByTagName("h3")[0].getAttribute("id"));
const token = localStorage.getItem("AuthToken");
const postAnswerBtn = thisElem("postAnswer");
let asker = false;
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

function mouseIn(answer){
    if (localStorage.getItem("username") == thisElem("askerUname").innerHTML){
        let acceptBtn = answer.children[answer.children.length-1];
        acceptBtn.style.display = "inline-block";
    } 
}

function mouseOut(answer){
    let acceptBtn = answer.children[answer.children.length-1];
    acceptBtn.style.display = "none";
}

function acceptAnswer(answer){
    let answerId = answer.parentNode.id
    let path = `/api/v2/questions/${questionId}/answers/${answerId}`;
    let data = {};
    putData({path, data, token})
    .then((res) => {
        if (res.status == 200){
            res.json().then((data)=>{console.info(data)});
            refreshAnswers();
        }else if (res.status == 400){
            res.json().then(() => {
                let html = `<h4>Error: </h4>
                            <p>You cannot accept your own answer</p>
                            <button id="cancel">Exit</button>`;
                showDialog(html);
            });
        }
        else{
            res.json().then((resp) => {
                resp = JSON.stringify(resp)
                let html = `<h4>Error: </h4>
                            <p>${resp}</p>
                            <button id="cancel">Exit</button>`;
                showDialog(html);
            });
        }
    })
    .catch((error)=>{console.error("Error: ", error)});
}
function makeAnswer(element, isOwner=false){
    let answerId = element["answer_id"];
    let text = element["text"];
    let username = element["username"];
    let dateCreated = element["date_created"];
    let upvotes = element["up_votes"];
    let user_preferred = element["user_preferred"];
    let ansElem = makeElement("div", "id", answerId, "answersDiv");
    let accept = "Accept";
    if (user_preferred){
        ansElem.setAttribute("class", "preferred");
        accept = "Reject";
    }
    makeElement("p", "class", "answer", answerId, text);
    let meta = `Total votes: ${upvotes}<br/>Answered by ${username} on ${dateCreated}`;
    makeElement("p", "class", "answerMeta", answerId, meta);
    if (validatedUser){
        let upBtn = makeElement("button", "class", "buttons", answerId, "Upvote");
        upBtn.setAttribute("onclick", "voteClicked(this)");
        upBtn.setAttribute("name", "upvote");
        let downBtn = makeElement("button", "class", "buttons", answerId, "Downvote"); 
        downBtn.setAttribute("onclick", "voteClicked(this)");
        downBtn.setAttribute("name", "downvote");
        if (isOwner){
            let editBtn = makeElement("button", "class", "buttons", answerId, "Edit");
            editBtn.setAttribute("onclick", "editAnswer(this)");
        }
        let acceptBtn = makeElement("button", "class", "buttons acceptAnsBtn", answerId, accept);
        acceptBtn.setAttribute("onclick", "acceptAnswer(this)");
        ansElem.addEventListener("mouseenter", ()=>{mouseIn(ansElem);});
        ansElem.addEventListener("mouseleave", ()=>{mouseOut(ansElem);});
    }
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
                    let username = localStorage.getItem("username");
                    if (username == element.username){
                        makeAnswer(element, true);
                    }else{
                        makeAnswer(element);
                    }
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
        thisElem("signOutLink").style.display = "block";
        thisElem("signInLink").style.display = "none";
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
function editAnswer(question){
    let currAns = question.parentNode;
    let answerId = currAns.id;
    let text = currAns.children[0].innerHTML;
    let editFieldset = `<fieldset id>
                            <legend>Edit the Answer:</legend>
                            <label for="answer">Question:</label>
                            <textarea name="answer" id="editText" minlength="10">${text}</textarea>
                            <p id="editWarnings"></p>
                            <button id="editAnswer">Edit</button>
                            <button id="cancel">Cancel</button>
                        </fieldset>`;
    if (thisElem("modalDiv")){
        thisElem("modalDiv").remove();
    }
    makeElement("div", "id", "modalDiv", "modalContent", editFieldset);
    thisElem("editAnswer").addEventListener("click", () => {
        let path = `/api/v2/questions/${questionId}/answers/${answerId}`
        let editedText = thisElem("editText").value;
        if (editedText.length < 10){
            thisElem("editWarnings").innerHTML = "Invalid length for answer text";
        }
        else{
            let data = {
                "text":editedText
            }
            putData({path, data, token})
            .then((res) => {
                if (res.status == 200){
                    res.json().then((data) => {console.info(data);});
                    thisElem("myModal").style.display = "none";
                    refreshAnswers();
                }else{
                    res.json().then((data) => {
                        console.info("Failed: ", data);
                        thisElem("editWarnings").innerHTML = JSON.stringify(data.message);
                    });
                }
            })
            .catch((err) => {console.error("Error: ", err);});
        }
    });
    thisElem("cancel").addEventListener("click", () => {
        thisElem("myModal").style.display = "none";
    });
    thisElem("myModal").style.display = "block";
}