let userNameIsTaken = true
let emailIsTaken = true
let passwordsMatch = false

const checkUsernameSignup = () => {
  return $.get('/start/users')
    .done((result) => {
      const enteredUsername = $('#username-signup').val()
      const usernames = result.allUsers.map(x => x.username)
      console.log(usernames)
      userNameIsTaken = usernames.includes(enteredUsername) ? true : false
      if (userNameIsTaken) {
        $('.signup-form-username-error').empty()
        $('.signup-form-username-error').text(` Whoops. ${enteredUsername} already exists.`)
      } else if (enteredUsername.length > 30) {
        $('.signup-form-username-error').empty()
        $('.signup-form-username-error').text(' Whoops. Please keep it under 30 characters.')
      } else if (enteredUsername.length < 8) {
        $('.signup-form-username-error').empty()
        $('.signup-form-username-error').text(' Whoops. Please make it longer than 8 characters.')
      } else {
        $('.signup-form-username-error').empty()
      }
    })
    .fail(err => err)
}

const checkEmail = () => {
  return $.get('/start/users')
    .done((result) => {
      const emailRegex = RegExp(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)
      const enteredEmail = $('#email-signup').val().toLowerCase()
      const emails = result.allUsers.map(x => x.email)
      emailIsTaken = emails.includes(enteredEmail) ? true : false
      if (emailIsTaken) {
        $('.signup-form-email-error').empty()
        $('.signup-form-email-error').text(` Whoops. ${enteredEmail} already exists.`)
      } else if (!emailRegex.test(enteredEmail)){
        $('.signup-form-email-error').empty()
        $('.signup-form-email-error').text('Please enter a valid email')
      } else {
        $('.signup-form-email-error').empty()
      }
    })
    .fail(err => err)
}
//
//
const checkPasswords = () => {
  const firstPass = $('#password-signup').val()
  const secondPass = $('#confirm-password-signup').val()
  if (firstPass !== secondPass) {
    $('.signup-form-password-error').empty()
    $('.signup-form-password-error').text('Whoops, these passwords don\'t match.')
    passwordsMatch = false
  } else if (firstPass.length < 8 || secondPass.length < 8) {
    $('.signup-form-password-error').empty()
    $('.signup-form-password-error').text('Please make it longer than 8 characters.')
  } else if (firstPass.length > 30 || secondPass.length > 30) {
    $('.signup-form-password-error').empty()
    $('.signup-form-password-error').text('Please keep it shorter than 30 characters.')
  } else {
    $('.signup-form-password-error').empty()
    $('#general-signup-error').empty()
    passwordsMatch = true
  }
}

const isSignupFormValid = () => {
  if(userNameIsTaken || emailIsTaken || !passwordsMatch){
    return $('#signup-submit-button').attr('disabled', true)
  } else {
    return $('#signup-submit-button').attr('disabled', false)
  }
}

$(document).ready(() => {
  // MAKE SIGNUP/LOGIN BUTTONS FUNCTIONAL.
  $('.collapsible').collapsible()
  if (window.location.hash === '#login-collapsible') {
    $('#login-collapsible').trigger('click')
  } else if (window.location.hash === '#signup-collapsible') {
    $('#signup-collapsible').trigger('click')
  }

  // BY DEFAULT, DO NOT ALLOW THEM TO SUBMIT THE FORM
  $('#signup-submit-button').attr('disabled', true)

  // WHEN USER FOCUSES OUT OF USERNAME INPUT,
  // CHECK DATABASE TO SEE IF USERNAME IS ALREADY TAKEN
  $('#username-signup').focusout((event) => {
    checkUsernameSignup()
    isSignupFormValid()
  })

  // WHEN USER FOCUSES OUT OF EMAIL INPUT,
  // CHECK DATABASE TO SEE IF EMAIL IS ALREADY TAKEN
  $('#email-signup').focusout((event) => {
    checkEmail()
    isSignupFormValid()
  })

  // WHEN USER FOCUSES OUT OF CONFRIM PASSWORD INPUT,
  // CHECK DATABASE TO SEE IF EMAIL IS ALREADY TAKEN
    $('#confirm-password-signup').keyup((event) => {
      checkPasswords()
      isSignupFormValid()
    })

    $('#password-signup').keyup((event) => {
      checkPasswords()
      isSignupFormValid()
    })

    $('#confirm-password-signup').focusout((event) => {
      isSignupFormValid()
    })

    $('#password-signup').focusout((event) => {
      isSignupFormValid()
    })
}) // End document ready
