function makeElement(elementType, attr, value, parentId){
    elem = document.createElement(elementType);
    elem.setAttribute(attr, value);
    parentElem = document.getElementById(parentId);
    parentElem.append(elem);
    //console.log(parentElem);
    return elem;
}

function getQuestions(){
    path = "/api/v2/questions"
    getData(path)
    .then((response) => {
        if (response.status == 200){
            response.json().then((data) => {
                let questions = data["questions"];
                console.log(questions);
                questions.forEach((element) => {
                    //console.log(element)
                    let questionId = element["question_id"];
                    let text = element["text"];
                    let username = element["username"];
                    let description = element["description"];
                    let dateCreated = element["date_created"];
                    makeElement("div", "id", questionId, "questionsDiv");
                    let title = makeElement("p", "class", "questionTitle", questionId);
                    title.innerHTML = text;
                    let desc = makeElement("p", "class", "questionDesc", questionId);
                    desc.innerHTML = description;
                    let meta = `Asked by ${username} on ${dateCreated}`
                    let metaElem = makeElement("p", "class", "questionMeta", questionId);
                    metaElem.innerHTML = meta;
                    let ansLink = makeElement("p", "class", "linkSpan", questionId);
                    ansLink.innerHTML = `<a href="questions/${questionId}">See Answer</a>`;
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
getQuestions();