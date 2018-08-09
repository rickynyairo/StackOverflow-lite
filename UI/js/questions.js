function loadQuestions(){
    let container = document.getElementById("questionsDiv");
    let questions = test_data.questions;
    
    for (let x = 0;x<questions.length;x++){
        questionTextNode = document.createTextNode(questions[x].text);
        let pElem = document.createElement("P");
        let ulElem = document.createElement("UL");
        pElem.appendChild(questionTextNode);
        for(let y=0;y<questions[x].answers.length;y++){
            let answer =  questions[x].answers[y].slice(0,-4);
            let upvotes = questions[x].answers[y].slice(-3);
            let text = "".concat(answer, " : ", parseInt(upvotes), " up votes.");
            let answerNode = document.createTextNode(text);
            let liElem = document.createElement("LI");
            liElem.appendChild(answerNode);
            ulElem.appendChild(liElem);
        }
        pElem.appendChild(ulElem);
        let username = questions[x].askedBy;
        let askedByParagraphElement = document.createElement("P");
        let userAnswerParagraphElement = document.createElement("P");
        let askedByNode = document.createTextNode("".concat("Asked By ", username, " on ",  questions[x].date.toDateString()));
        let userAnswerNode = document.createTextNode("".concat(username, " up voted:\t", questions[x].userAnswer));
        askedByParagraphElement.appendChild(askedByNode);
        userAnswerParagraphElement.appendChild(userAnswerNode);
        pElem.appendChild(askedByParagraphElement);
        pElem.appendChild(userAnswerParagraphElement);
        pElem.className = "questions"
        textArea = document.createElement("textarea");
        button = document.createElement("button");
        button.innerHTML = "Post Answer";
        button.className = "postAnswer"
        button.id = "postAnswer"+x;
        button.setAttribute("onclick","postAnswer(this)");
        pElem.appendChild(textArea);
        pElem.appendChild(button);
        container.appendChild(pElem);
    }
}

function postAnswer(button){
    text = button.parentNode.children[3].value;
    button.parentNode.children[3].value = '';
    ulELement = button.parentNode.children[0];
    let textNode = document.createTextNode(text)
    //append the answer to the list of answers
    let liElement = document.createElement("LI");
    liElement.appendChild(textNode);
    ulELement.appendChild(liElement);
}
loadQuestions();
