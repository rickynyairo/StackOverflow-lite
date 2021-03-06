const token = localStorage.getItem("AuthToken");
let validatedUser = false;

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
  return fetch(path, {
    method:"GET",
    headers:{
      "Content-Type":"application/json",
      "Authorization":`Bearer ${token}`
    }
  });
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
function deleteData(params){
  let path = params.path;
  let token = params.token;
  return fetch(path, {
    method:"DELETE",
    headers:{
      "Content-Type":"application/json",
      "Authorization":`Bearer ${token}`
    }
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
function toggleDisplay(id){
  let currStyle = thisElem(id).style.display;
  if (currStyle == ""){
    currStyle = "block";
  }else{
    currStyle = "none";
  }
  return currStyle;
}

function signUp(){
  let newUser = {
    "first_name":thisElem("fname").value,
    "last_name":thisElem("lname").value,
    "username":thisElem("username").value,
    "email":thisElem("email").value,
    "password":thisElem("password").value
  };
  let path = "/api/v2/auth/signup";
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
        showDialog(JSON.stringify(data.message));
      });
    }
  })
  .catch((err) => {
    showDialog(JSON.stringify(err));
  });
}

function signOut(){
  let token = localStorage.getItem("AuthToken");
  let path = "/api/v2/auth/logout";
  postData(path, {}, token)
  .then((res) => {
    if (res.status == 200){
      window.location.href = "/home";
    }
    else{
      res.json().then((data)=>{showDialog(JSON.stringify(data));}); 
    }
  })
  .catch((err)=>{showDialog(JSON.stringify(err));});
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
        localStorage.setItem('username', user.username);
        localStorage.setItem('user_id', user.user_id);
        if (data.message == "Valid"){
          validatedUser = true;
        }
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

if (document.getElementsByClassName("close")[0]){
  let span = document.getElementsByClassName("close")[0];
  span.onclick = () => {
    thisElem("myModal").style.display = "none";
  }
  thisElem('submitButton').addEventListener('click', (event) => {
    event.preventDefault();
    signUp();
  });
}

window.onclick = function(event) {
  if (event.target == thisElem("myModal")) {
    thisElem("myModal").style.display = "none";
  }
}

function showDialog(html){
  if (thisElem("modalDiv")){
    thisElem("modalDiv").remove();
  }
  makeElement("div", "id", "modalDiv", "modalContent", html);
  if (thisElem("cancel")){
    thisElem("cancel").addEventListener("click", () => {
      thisElem("myModal").style.display = "none";
    });
  }
  thisElem("myModal").style.display = "block";
}

function loadProfile(){
  let username = localStorage.getItem("username");
  window.location.href = `/profile/${username}`;
}