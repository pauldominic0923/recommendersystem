visitNumber = 0;

function createCookie(length) {
   var result           = '';
   var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}

function checkCookie() {
    if (document.cookie.indexOf('uuid') === -1) { //cookie does not exsist
        document.cookie = "uuid="+createCookie(10);
        document.cookie = "visitNumber="+visitNumber;
    }
}

function findCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

function updateVisitCookie(updatedVisitNum) {
	document.cookie = "visitNumber="+updatedVisitNum;
}

var visitNum = findCookie("visitNumber");
var visitNumInt = parseInt(visitNum);
var updatedVisitNum = visitNumInt + 1;

if (visitNumInt > 0) {
  document.getElementById("recommendation").innerHTML = "Our recommendations especially for you";
}

updateVisitCookie(updatedVisitNum);
checkCookie()
