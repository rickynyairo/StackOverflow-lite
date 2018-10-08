loginBtn = thisElem('loginButton')
loginBtn.addEventListener('click', (event) => {
  event.preventDefault();
  login();
});
thisElem("signUpBtn").addEventListener("click", ()=>{
  window.location.href  = "/";
})

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
        localStorage.setItem("AuthToken", data["AuthToken"]);
        window.location.href = "home";
      });
    }
    else{
      res.json().then((data) => {
        showDialog(JSON.stringify(data));
      });
    }
  })
  .catch((err) => {
    showDialog(JSON.stringify(err));
  });
}
