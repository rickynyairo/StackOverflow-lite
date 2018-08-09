function loadQuestions(){
    //this function loads questions into the page
    let container = document.getElementById("questionsDiv");
    let questions = test_data.questions;
    
    //collect questions from the JS object "test_data" in index.js
    for (let x = 0;x<questions.length;x++){
        //create a p element for every question
        questionTextNode = document.createTextNode(questions[x].text);
        let pElem = document.createElement("P");
        let ulElem = document.createElement("UL");
        pElem.appendChild(questionTextNode);
        
        //collect the answers to the questions as well as the upvotes
        for(let y=0;y<questions[x].answers.length;y++){
            let answer =  questions[x].answers[y].slice(0,-4);
            let upvotes = questions[x].answers[y].slice(-3);
            let text = "".concat(answer, " :\t", parseInt(upvotes), " up votes");
            let answerNode = document.createTextNode(text);
            let liElem = document.createElement("LI");
            liElem.appendChild(answerNode);
            ulElem.appendChild(liElem);
        }

        //append answers to each question appropriately
        //append username and date 
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

        //create a test area and button for submitting answers
        textArea = document.createElement("textarea");
        button = document.createElement("button");
        button.innerHTML = "Post Answer";
        button.className = "postAnswer"
        button.id = "postAnswer"+x;

        //add onclick attribute for every button
        button.setAttribute("onclick","postAnswer(this)");
        pElem.appendChild(textArea);
        pElem.appendChild(button);
        container.appendChild(pElem);
    }
}

function postAnswer(button){
    text = button.parentNode.children[3].value.concat(" :\t0 up votes");
    button.parentNode.children[3].value = '';
    ulELement = button.parentNode.children[0];
    let textNode = document.createTextNode(text)
    //append the answer to the list of answers
    let liElement = document.createElement("LI");
    liElement.appendChild(textNode);
    ulELement.appendChild(liElement);
}
loadQuestions();
