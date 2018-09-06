loginBtn = thisElem('loginButton')
loginBtn.addEventListener('click', (event) => {
  event.preventDefault();
  login();
});

function login(){
  let username = thisElem("username").value;
  let password = thisElem("password").value;
  let user = {
    "username":username,
    "password":password
  };
  path = "/api/v2/auth/login";
  postData(path, user)
  .then((res) => {
   if (res.status == 200){
      res.json().then((data) => {
        console.log(data);
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
