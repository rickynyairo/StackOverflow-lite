const hostname = window.location.hostname

function makeRequest(method, path, data){
  let xhr = new XMLHttpRequest();
  url = hostname + path;
  xhr.open(method, url, true);
  xhr.onload = function(e){
    if (xhr.readyState === 4){
      console.log(xhr.responseText);
    }else{
      console.log(xhr.statusText);
    }
  };
  xhr.onerror = function(e){
    console.log(xhr.statusText);
    console.log(xhr.responseText);
  };
  xhr.send(data);
  return xhr.response;
}

function signUp(form){
  form.preventDefault()

  let email = form.email.value;
  let fname = form.fname.value;
  let lname = form.lname.value;
  let username = form.username.value;
  let password = form.password

  data = {
    "first_name":fname,
    "last_name":lname,
    "username":username,
    "email":email,
    "password":password
  }

  path = "/api/v2/auth/signup"

  resp = makeRequest("POST", path, data)
  console.log(resp)

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


let test_data = {
  "users":{
    "john_doe@gmail.com":{
      "username":"johndoe",
      "password":"¥«,Â\u008aÝ"
      },
    "user@name.com":{
      "username":"user",
      "password":"¥«,Â\u008aÝ"
      }
  },
  "questions":[
      {
        "text":"What is the distance from the earth to the moon?",
        "askedBy":"Jimmy",
        "answers":["100000km-000","384000km-020"],
        "userAnswer":"384000km",
        "date":new Date("December 17, 2017 03:24:00")
      },
      {
        "text":"Who was the first Kenyan president?",
        "askedBy":"Nancy",
        "answers":["Jomo Kenyatta-100","Uhuru Kenyatta-020","Mwai Kibaki-060", "Raila Odinga-000"],
        "userAnswer":"Jomo Kenyatta",
        "date":new Date("August 17, 2017 13:44:28")
      }

  ]
};