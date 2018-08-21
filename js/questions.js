

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
