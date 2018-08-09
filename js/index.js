function signUp(form){
  let email = form.email.value;
  let username = form.username.value;
  let password = atob(form.password.value);
  if (email in test_data.users){
    console.log("account creation unsuccessful");
    document.getElementById("signUpForm").action=""
    alert("Email is already taken");
    return false;
  }
  else{
    //email does not exist therefore user can sign up
    //save user details
    test_data.users[email] = {
      "username":username,
      "password":password
    };
    document.getElementById("signUpForm").action="questions.html"
    return true;
  } 
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
      document.getElementById("signInForm").action=""
      alert("incorrect password");
      return false;
    }
  }
  else{
    //document.getElementById("signInForm").action=""
    alert("incorrect email");
    return false;
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