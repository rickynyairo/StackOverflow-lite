let mostAnsweredBtn = thisElem("mostAnswered");
let postQuestionBtn = thisElem("postQuestion");
mostAnsweredBtn.addEventListener("click", (event)=>{
    console.log(event);
    getMostAnswered();
})

postQuestionBtn.addEventListener("click", (event)=>{
    console.log(event);
    let text = thisElem("questionText").value;
    let description = thisElem("questionDescription").value;
    if (text.length < 10 || description.length < 10){
        //to short or unfilled
        thisElem("warnings").innerHTML = "The text or description is invalid";
    }
    else{
        thisElem("warnings").innerHTML = "";
        let question = {
            "text":text,
            "description":description
        };
        postQuestion(question);
    }
})


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
                console.log("Failed:\n" + data);
            });
        }
    });
}

function postQuestion(question){
    let token = localStorage.getItem("AuthToken");
    let path = "/api/v2/questions";
    postData(path, question, token)
    .then((result) => {
        if (result.status == 201){
            // question posted successfully
            result.json().then((resp) => {
                console.log("question posted: ", resp);
                thisElem("questionText").value = "";
                thisElem("questionDescription").value = "";
                refreshQuestions();
            });
        }else{
            console.log(result);
        }
    })
    .catch((err) => {
        console.log(err);
    });
}

let loginRequest = (loginurl= "http://127.0.0.1:5000/api/v2/auth/login") => {
    fetch(loginurl, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "username": "asdsa",
        "password": "password"
      })
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
      })
      .catch(err => {
        console.log(`Fetch Error: ${err}`);
      });
}