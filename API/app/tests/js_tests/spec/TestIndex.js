describe("IndexJS Functions", function() {
  describe("when thisElem('id') is called", function(){
    let domElem;
    beforeEach(function(){
      domElem = $("div");
      domElem.attr("id", "domElemId");
      $("#testElements").append(domElem);
    });
    it("should return the element when the id is passed", function() {
      let elem = document.getElementById("domElemId");
      expect(thisElem("domElemId")).toEqual(elem);
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
      // test that the element with the id can be
      let elem = document.getElementById("testMakeElem");
      expect(elem.id).toBeTruthy();
      expect($("#testMakeElem").html()).toEqual("test");
    });
  });

});
