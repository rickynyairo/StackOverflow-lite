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
        container.appendChild(pElem);
    }
}

loadQuestions();