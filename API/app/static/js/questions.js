let mostAnsweredBtn = thisElem("mostAnswered");
let postQuestionBtn = thisElem("postQuestion");
mostAnsweredBtn.addEventListener("click", getMostAnswered);
postQuestionBtn.addEventListener("click", postQuestion);

function getMostAnswered(){
    //load the question page with the id of the most answered question
    let path = "/api/v2/questions/answers/most";
    getData(path)
    .then((response) => {
        if (response.status == 200){
            response.json().then((data) => {
                let question_id = data["question_id"];
                window.location.href=`questions/${question_id}`;
            });
        }
        else{
            response.json().then((data) => {
                showDialog(JSON.stringify(data));
            });
        }
    });
}

function postQuestion(){
    let text = thisElem("questionText").value;
    let description = thisElem("questionDescription").value;
    if (text.length < 10 || description.length < 10){
        //to short or unfilled
        thisElem("warnings").innerHTML = "The text/description is invalid";
    }
    else{
        thisElem("warnings").innerHTML = "";
        let question = {
            "text":`${text}`,
            "description":`${description}`
        };
        let path = "/api/v2/questions";
        postData(path, question, token)
        .then((result) => {
            if (result.status == 201){
                // question posted successfully
                result.json().then((resp) => {
                    thisElem("questionText").value = "";
                    thisElem("questionDescription").value = "";
                    refreshQuestions();
                });
            }else{
                result.json().then((data) => {
                    showDialog(JSON.stringify(data.message));
                });
            }
        })
        .catch((err) => {
            showDialog(JSON.stringify(err));
        });
    }
}

function editQuestion(question){
    let currQstn = question.parentNode.parentNode;
    let questionId = currQstn.id;
    let text = currQstn.children[0].innerHTML;
    let desc = currQstn.children[1].innerHTML;
    let editFieldset = `<fieldset id = "editQuestionFieldset">
                            <legend>Edit the Question:</legend>
                            <label for="question">Question:</label>
                            <textarea name="question" id="editText" minlength="10">${text}</textarea>
                            <label for="description">Description:</label>
                            <textarea name="description" id="editDescription" rows="10">${desc}</textarea>
                            <p id="editWarnings"></p>
                            <button id="editQuestion">Edit</button>
                            <button id="cancel">Cancel</button>
                        </fieldset>`;
    showDialog(editFieldset);
    thisElem("editQuestion").addEventListener("click", () => {
        let path = `/api/v2/questions/${questionId}`
        let editedText = thisElem("editText").value;
        let editedDesc = thisElem("editDescription").value;
        if (editedText.length < 10 || editedDesc.length < 10){
            thisElem("editWarnings").innerHTML = "Invalid length for question title or description";
        }
        else{
            let data = {
                "text":editedText,
                "description":editedDesc
            }
            putData({path, data, token})
            .then((res) => {
                if (res.status == 200){
                    thisElem("myModal").style.display = "none";
                    refreshQuestions();
                }else{
                    res.json().then((data) => {
                        thisElem("editWarnings").innerHTML = JSON.dumps(data.message);
                    });
                }
            })
            .catch((err) => {showDialog(JSON.stringify(err));});
        }
    });
    thisElem("cancel").addEventListener("click", () => {
        thisElem("myModal").style.display = "none";
    });
}

function deleteQuestion(question){
    let currQstn = question.parentNode.parentNode;
    let questionId = currQstn.id;
    let text = currQstn.children[0].innerHTML;
    let desc = currQstn.children[1].innerHTML;
    let deleteHTML = `<h3>Are you sure you want to delete the question?</h3>
                      <h4>${text}</h4>
                      <p>${desc}</p>
                      <button id="deleteQstn">Delete</button>
                      <button id="cancel">Cancel</button>`;
    
    showDialog(deleteHTML);
    thisElem("deleteQstn").addEventListener("click", () => {
        let path = `/api/v2/questions/${questionId}`
        deleteData({path, token})
        .then((res) => {
            if (res.status == 202){
                thisElem("myModal").style.display = "none";
                refreshQuestions();
            }else{
                res.json().then((data) => {
                    showDialog(JSON.stringify(data.message));
                });
            }
        })
        .catch((err) => {showDialog(JSON.stringify(err));});
    });
}