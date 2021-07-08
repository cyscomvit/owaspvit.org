document.addEventListener('DOMContentLoaded', () => {
  // TODO: Implement getParameterByName()

  const queryString = window.location.search;
  const getParameterByName = new URLSearchParams(queryString);
  

  // Get the action to complete.
  var mode = getParameterByName.get('mode');
  // Get the one-time code from the query parameter.
  var actionCode = getParameterByName.get('oobCode');
  // (Optional) Get the continue URL from the query parameter if available.
  var continueUrl = getParameterByName.get('continueUrl');
  // (Optional) Get the language code if available.
  var lang = getParameterByName.get('lang') || 'en';

  // Configure the Firebase SDK.
  // This is the minimum configuration required for the API to be used.
  var config = {
    'apiKey': "AIzaSyB1a_4OKRPxg_B12QWEyTmzeipA0T12PdA" 
    // Copy this key from the web initialization
    // snippet found in the Firebase console.
  };
  var app = firebase.initializeApp(config);
  var auth = app.auth();

  // Handle the user management action.
  switch (mode) {

    case 'verifyEmail':
      document.getElementById("reset").style.display='none';
      document.getElementById("verify").style.display='flex';

      // Display email verification handler and UI.
      console.log(mode + actionCode + continueUrl + lang);
      handleVerifyEmail(auth, actionCode, continueUrl, lang);
      break;
    
      case 'resetPassword':
        document.getElementById("verify").style.display='none';
        document.getElementById("reset").style.display='flex';
        var btn = document.getElementById('submit');
        btn.addEventListener('click', event =>{
          event.preventDefault();
          handleResetPassword(auth, actionCode, continueUrl, lang);
        });
        break;
    default:
      // Error: invalid mode.
  }
}, false);

function handleVerifyEmail(auth, actionCode, continueUrl, lang) {
  // Localize the UI to the selected language as determined by the lang
  // parameter.
  // Try to apply the email verification code.
  auth.applyActionCode(actionCode).then((resp) => {
    console.log("email verified.")
    // Email address has been verified.

    // TODO: Display a confirmation message to the user.
    // You could also provide the user with a link back to the app.

    // TODO: If a continue URL is available, display a button which on
    // click redirects the user back to the app via continueUrl with
    // additional state determined from that URL's parameters.
  }).catch((error) => {
    console.log("email is invalid");
    // Code is invalid or expired. Ask the user to verify their email address
    // again.
  });
}
  
  function handleResetPassword(auth, actionCode, continueUrl, lang) {
    // Localize the UI to the selected language as determined by the lang
    // parameter.
  
    // Verify the password reset code is valid.
    auth.verifyPasswordResetCode(actionCode).then((email) => {
      var accountEmail = email;
      console.log(accountEmail)
  
      // TODO: Show the reset screen with the user's email and ask the user for
      // the new password.

      var newPassword = document.getElementById("new_password").value;
      //var newPassword = 'hello';
      //var newPassword = form.inputbox.value;
      // Save the new password.
      auth.confirmPasswordReset(actionCode, newPassword).then((resp) => {
          console.log("password has been changed");
          window.location.href="login";
        // Password reset has been confirmed and new password updated.
  
        // TODO: Display a link back to the app, or sign-in the user directly
        // if the page belongs to the same domain as the app:
        // auth.signInWithEmailAndPassword(accountEmail, newPassword);
  
        // TODO: If a continue URL is available, display a button which on
        // click redirects the user back to the app via continueUrl with
        // additional state determined from that URL's parameters.
      }).catch((error) => {
          console.log("password too weak");
          console.log(error);
        // Error occurred during confirmation. The code might have expired or the
        // password is too weak.
      });
    }).catch((error) => {
        console.log("expired");
        console.log(error);
      // Invalid or expired action code. Ask user to try to reset the password
      // again.
    });
  }

  let btnOn = document.getElementById("submit");
  let btnOff = document.getElementById("submit_disabled");
  let ele = document.getElementById("new_password");
  btnOn.style.display = "none";
  btnOff.style.display = "flex";
  ele.addEventListener('input', () => {
      console.log('called');
      let result = zxcvbn(ele.value).score
      if (result > 2) {
          btnOn.style.display = "flex";
          btnOff.style.display = "none";
      }
      else {
          btnOn.style.display = "none";
          btnOff.style.display = "flex";
      }
  })