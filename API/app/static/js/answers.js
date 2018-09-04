const questionId = parseInt(document.getElementsByTagName("h3")[0].getAttribute("id"));

function getAnswers(){
    let path = `/api/v2/questions/${questionId}`;
    getData(path)
    .then((response) => {
        if (response.status == 200){
            response.json().then((data) => {
                let answers = data["answers"];
                console.log(answers);
                answers.forEach((element) => {
                    let answerId = element["answer_id"];
                    let text = element["text"];
                    let username = element["username"];
                    let dateCreated = element["date_created"];
                    let upvotes = element["up_votes"];
                    makeElement("div", "id", answerId, "answersDiv", "");
                    makeElement("p", "class", "answer", answerId, text);
                    let votes = `Total votes: ${upvotes}`;
                    makeElement("p", "class", "votes", answerId, votes);
                    makeElement("button", "class", "buttons", answerId, "Upvote");
                    makeElement("button", "class", "buttons", answerId, "Downvote");
                    let meta = `Answered by ${username} on ${dateCreated}`;
                    makeElement("p", "class", "answerMeta", answerId, meta);
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
getAnswers();