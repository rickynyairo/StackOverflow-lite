const hostname = window.location.hostname

submitBtn = document.getElementById('submitButton')
if (submitBtn){
  submitBtn.addEventListener('click', (event) => {
    event.preventDefault();
    signUp();
  });
}

function thisElem(id){
  return document.getElementById(id);
}

function postData(path, data, token="token"){
  return fetch(path, {
    method:"POST",
    headers:{
      "Content-Type":"application/json", 
      "Authorization":`Bearer ${token}`
    },
    body:JSON.stringify(data)
    });
}

function getData(path){
  return fetch(path);
}

function putData(params){
  let path = params.path;
  let data = params.data;
  let token = params.token;
  return fetch(path, {
    method:"PUT",
    headers:{
      "Content-Type":"application/json",
      "Authorization":`Bearer ${token}`
    },
    body:JSON.stringify(data)
  });
}

function makeElement(elementType, attr, value, parentId, inner=""){
  let elem = document.createElement(elementType);
  elem.setAttribute(attr, value);
  elem.innerHTML = inner;
  parentElem = document.getElementById(parentId);
  parentElem.append(elem);
  
  return elem;
}

function signUp(){
  let newUser = {
    "first_name":thisElem("fname").value,
    "last_name":thisElem("lname").value,
    "username":thisElem("username").value,
    "email":thisElem("email").value,
    "password":thisElem("password").value
  };
  path = "/api/v2/auth/signup";
  postData(path, newUser)
  .then((res) => {
   if (res.status == 201){
      res.json().then((data) => {
          localStorage.setItem("AuthToken", data["AuthToken"]);
          window.location.href = "home";
      });
    }
    else{
      res.json().then((data) => {
        console.log("Failed: \n"+data);
      });
    }
  })
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  });
}

function validateUser(token, callBack){
  let path ="/api/v2/auth/validate";
  let user = {
    "username":"",
    "user_id":""
  };
  postData(path, {}, token)
  .then((res) => {
    if (res.status == 200){
      res.json().then((data) => {
        user.username = data.username;
        user.user_id = data.user_id;
        localStorage.setItem('user', user);
        callBack({"message":data.message,"user":user});
      });
      }
    else{
      res.json().then((data) => {
        callBack({"message":data.message});
      });
      }
    })
    .catch((err) => {
      callBack({"message":"error","error":err});
    });
}