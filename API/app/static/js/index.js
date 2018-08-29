const hostname = window.location.hostname

submitBtn = document.getElementById('submitButton')
submitBtn.addEventListener('click', function(event){
  event.preventDefault();
  const form = document.getElementById("signUpForm")
  signUp(form);
});

function getRequest(path){
  url = "http://" + hostname + path;
  fetch(url, {
    method:"GET",
    headers:{
      "Content-Type":"application/json"
    }})
  .then(
    function(response) {
      if (response.status == 200) {
        console.log('Status Code: ' + response.status);
        return response;
      }
      else{
        response.json().then(function(data) {
          console.log(data);
        });
      }
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  });
}

function postRequest(path, data, token="token"){
  url = path;
  fetch(url, {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      "Authorization":"Bearer " + token
    },
    body:JSON.stringify(data)
    })
  .then(
    //success function
    function(response) {
      if (response.status == 201) {
        console.log('Status Code: ' + response.status);
        return response;
      }
      else{
        response.json().then(function(data) {
          console.log(data);
          return "Failed"
        });
      }
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
  });
}
function thisElem(id){
  return document.getElementById(id);
}
function signUp(form){
  //form.preventDefault()
  //alert("Errrrrrrorrrorororororo")
  let email = thisElem("email").value;
  let fname = thisElem("fname").value;
  let lname = thisElem("lname").value;
  let username = thisElem("username").value;
  let password = thisElem("password").value

  data = {
    "first_name":fname,
    "last_name":lname,
    "username":username,
    "email":email,
    "password":password
  }

  path = "/api/v2/auth/signup"

  resp = postRequest(path, data)
  console.log(resp)
  if (resp.json['AuthToken']){
    localStorage.setItem('AuthToken', resp.json['AuthToken'])
  }
  alert(resp)
  return false
}

function signIn(form){
  let email = form.email.value;
  let password = form.password.value;
  //check if email exists
  if (email in test_data.users){
    //check if password is correct
    if (password === btoa(test_data.users[email].password)){
      console.log("login successful");
      document.getElementById("signInForm").action="questions.html"
      return true;
    }
    else{
      //password is incorrect
      document.getElementById("signInForm").action="questions.html"
      //alert("incorrect password");
      return true;
    }
  }
  else{
    document.getElementById("signInForm").action="questions.html"
    //alert("incorrect email");
    return true;
  }
}
