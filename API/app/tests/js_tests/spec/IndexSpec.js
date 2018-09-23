describe("IndexJS Functions", function() {
  let server;
  beforeEach(()=>{
    server = sinon.fakeServer.create();
    let inner = `<div id="myModal" class="modal">
                  <div id = "modalContent" class="modal-content">
                    <span class="close">&times;</span>
                    <!-- The content of the dialog box will go here -->
                  </div>
                </div>`;
    if(!thisElem("testElements")){
      let testElem = document.createElement("div");
      testElem.style.display = "none";
      testElem.id = "testElements";
      testElem.innerHTML = inner;
      document.getElementsByTagName("body")[0].appendChild(testElem);
    }
  });
  afterEach(()=>{
    server.restore();
  });
  describe("when thisElem('id') is called", function(){
    it("should return the element when the id is passed", function() {
      let elem = document.getElementById("testElements");
      expect(thisElem("testElements")).toEqual(elem);
    });
  });
  describe("when postData is called", function(){
    let postPromise = postData("path", {});
    it("should return a promise object", function(){
      expect(typeof(postPromise)).toEqual("object");
    });
  });
  describe("when makeElement is called", function(){ 
    it("should return an element with the passed paramaters", function(){
      makeElement("div", "id", "testMakeElem", "testElements", "test");
      // test that the element with the id can be created
      let elem = document.getElementById("testMakeElem");
      expect(elem.id).toBeTruthy();
      expect($("#testMakeElem").html()).toEqual("test");
    });
  });
  describe("when signUp is called", function(){
    let fname, lname, password, username, email, submitBtn;
    beforeEach(() => {
      makeElement("input", "id", "fname", "testElements").value = "john";
      makeElement("input", "id", "lname", "testElements").value = "doe";
      makeElement("input", "id", "password", "testElements").value = "password";
      makeElement("input", "id", "email", "testElements").value = "jdoe@gm.com";
      makeElement("input", "id", "username", "testElements").value = "testUname";
      makeElement("button", "id", "submitBtn", "testElements", "Submit");
      thisElem("submitBtn").addEventListener("click", signUp);
    });

    it("should collect values from the respective DOM elements and make a POST request", function(){
      server.respondWith("POST", "api/v2/auth/signup",
                       [201, { "Content-Type": "application/json" },
                        '{ "message": "success", "AuthToken": "testToken", "username":"testUname", "user_id":"1" }']);
      thisElem("submitBtn").click();
      expect(thisElem("modalContent").children.length).toBeGreaterThan(1);
    });
  });

});
