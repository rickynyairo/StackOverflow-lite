questionId = parseInt(document.getElementsByClassName("questionHeader")[0].id);
let postAnswerBtn = thisElem("postAnswer");
let asker = false;

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
    let unameElem = thisElem("askerUname");
    let username = "";
    if (unameElem){
        username = unameElem.innerHTML;
    }
    if (localStorage.getItem("username") == username){
        let answerButtons = answer.getElementsByTagName("button");
        let acceptBtn = answerButtons[answerButtons.length - 1];
        acceptBtn.style.display = "inline-block";
    } 
}

function mouseOut(answer){
    let answerButtons = answer.getElementsByTagName("button");
    let acceptBtn = answerButtons[answerButtons.length - 1];
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
    let questionId = element["question_id"];
    let text = element["text"];
    let username = element["username"];
    let dateCreated = element["date_created"];
    let upvotes = element["up_votes"];
    let downvotes = element["down_votes"];
    let user_preferred = element["user_preferred"];
    let ansElem = makeElement("div", "id", answerId, "answersDiv");
    ansElem.setAttribute("name", questionId);
    let accept = "Accept";
    if (user_preferred){
        ansElem.setAttribute("class", "preferred");
        accept = "Reject";
    }
    makeElement("p", "class", "answer", answerId, text);
    let meta = `Answered by <a href="/profile/${username}">${username}</a> on ${dateCreated}`;
    makeElement("p", "class", "answerMeta", answerId, meta);
    if (validatedUser){
        let upBtn = makeElement("button", "class", "buttons", answerId, `Upvote | ${upvotes}`);
        upBtn.setAttribute("onclick", "voteAnswer(this)");
        upBtn.setAttribute("name", "upvote");
        let downBtn = makeElement("button", "class", "buttons", answerId, `Downvote | ${downvotes}`); 
        downBtn.setAttribute("onclick", "voteAnswer(this)");
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

function getAnswers(path = `/api/v2/questions/${questionId}`){
    localStorage.setItem("refreshAnsPath", path);
    return getData(path)
    .then((response) => {
        if (response.status == 200){
            response.json().then((data) => {
                let answers = data["answers"];
                answers.forEach((element) => {
                    let username = localStorage.getItem("username");
                    if (username == element.username){
                        makeAnswer(element, true);
                    }else{
                        makeAnswer(element);
                    }
                });
                if (window.location.pathname.startsWith("/profile")){
                    thisElem("answersGiven").innerHTML = thisElem("answersDiv").children.length;
                    let quesIds = answers.map(ans => parseInt(ans["question_id"]));
                    let questionsAnswered = new Set(quesIds).size;
                    thisElem("questionsAnswered").innerHTML = questionsAnswered;
                    getAnswerQuestions();
                }
            });
        }
        else{
            response.json().then((data) => {
                showDialog(JSON.stringify(data));
            });
        }
    });
}

function refreshAnswers(){
    let path = localStorage.getItem("refreshAnsPath");
    let postAns = thisElem('postAnswerFieldset')
    if (postAns){
        postAns.style.display = 'none';
    }
    elems = thisElem("answersDiv").children;
    Array.from(elems).forEach((elem) => {
        if (Number.isInteger(parseInt(elem.id))){
            elem.parentNode.removeChild(elem);
        }
    });
    // refresh questions
    getAnswers(path)
    .then(()=>{
        if (validatedUser && postAns){
            postAns.style.display = 'block';
        }
    });
}

function postAnswer(answer){
    let path = `/api/v2/questions/${questionId}/answers`;
    postData(path, answer, token)
    .then((res) => {
        if (res.status == 201){
            res.json().then(data=>{
                thisElem("answer").value = "";
                refreshAnswers();
            });
        }
        else{
            res.json().then(data=>{
                showDialog(JSON.stringify(data));
            });
        }
    })
    .catch(error=>{
        showDialog(JSON.stringify(error));
    })
}

function voteAnswer(button){
    let questionId = parseInt(button.parentNode.getAttribute("name"));
    let answerId = parseInt(button.parentNode.id);
    let vote = button.getAttribute("name");
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
                refreshAnswers();
            });
        }
        else{
            res.json().then(data => {
                showDialog(JSON.stringify(data));
            });
        }
    })
    .catch(error => {
        showDialog(JSON.stringify(error));
    });
}

function showPostAnswer(resp){
    getAnswers();
    if (resp.message === "Valid"){
        thisElem("postAnswerFieldset").style.display = "block";
        thisElem("signOutLink").style.display = "block";
        thisElem("signInLink").style.display = "none";
        thisElem("signUpLink").style.display = "none";
        thisElem("profileLink").innerHTML = localStorage.getItem("username");
        thisElem("profileLink").style.display = "inline-block";
    }
}
if (window.location.pathname.startsWith("/question")){
    if (token){
        validateUser(token, showPostAnswer);
    }else{
        getAnswers();
    }
}
function editAnswer(question){
    let currAns = question.parentNode;
    let questionId = parseInt(currAns.getAttribute("name"));
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
                        thisElem("editWarnings").innerHTML = JSON.stringify(data.message);
                    });
                }
            })
            .catch((err) => {showDialog(JSON.stringify(err));});
        }
    });
    thisElem("cancel").addEventListener("click", () => {
        thisElem("myModal").style.display = "none";
    });
    thisElem("myModal").style.display = "block";
}