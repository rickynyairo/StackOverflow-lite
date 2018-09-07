let mostAnsweredBtn = thisElem("mostAnswered");
mostAnsweredBtn.addEventListener("click", (event)=>{
    console.log(event);
    getMostAnswered();
})


function getMostAnswered(){
    //load the question page with the id of the most answered question
    let path = "/api/v2/questions/answers/most";
    getData(path)
    .then((response) => {
        if (response.status == 200){
            response.json().then((data) => {
                let question_id = data["question_id"];
                window.location.href=`questions/${question_id}`
            });
        }
        else{
            response.json().then((data) => {
                console.log("Failed:\n" + data);
            });
        }
    });
}
