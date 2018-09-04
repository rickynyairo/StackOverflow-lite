const hostname = window.location.hostname

submitBtn = document.getElementById('submitButton')
submitBtn.addEventListener('click', function(event){
  event.preventDefault();
  signUp();
});
function thisElem(id){
  return document.getElementById(id);
}
function postData(path, data, token="token"){
  return fetch(path, {
    method:"POST",
    headers:{
      "Content-Type":"application/json", 
      "Authorization":"Bearer " + token
    },
    body:JSON.stringify(data)
    });
}

function getData(path){
  return fetch(path);
}

function makeElement(elementType, attr, value, parentId, inner){
  let elem = document.createElement(elementType);
  elem.setAttribute(attr, value);
  elem.innerHTML = inner;
  parentElem = document.getElementById(parentId);
  parentElem.append(elem);
  
  return elem;
}

function signUp(){
  let email = thisElem("email").value;
  let fname = thisElem("fname").value;
  let lname = thisElem("lname").value;
  let username = thisElem("username").value;
  let password = thisElem("password").value;

  let newUser = {
    "first_name":fname,
    "last_name":lname,
    "username":username,
    "email":email,
    "password":password
  };

  path = "/api/v2/auth/signup";
  postData(path, newUser)
  .then((res) => {
   if (res.status == 201){
      res.json().then((data) => {
          console.log(data);
          localStorage.setItem("AuthToken", data["AuthToken"]);
          window.location.href = "questions";
      });
    }
    else{
      res.json().then((data) => {
        console.log("Failed: \n"+data);
        return "Failed";
      });
    }
  })
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
    return "Failed";
  });
}
