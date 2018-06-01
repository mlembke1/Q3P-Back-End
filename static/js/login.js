let usernameExists = false

const checkUsernameLogin = () => {
  return $.get('/start/users')
    .done((result) => {
      const enteredUsername = $('#username-login').val()
      const usernames = result.allUsers.map(x => x.username)
      usernameExists = usernames.includes(enteredUsername) ? true : false
      if (!usernameExists) {
        $('.login-form-username-error').empty()
        $('.login-form-username-error').text(` Whoops. "${enteredUsername}" doesn't currently exist as a username.`)
      } else if (enteredUsername.length > 30) {
        $('.login-form-username-error').empty()
        $('.login-form-username-error').text(' Whoops. Please keep it under 30 characters.')
      } else if (enteredUsername.length < 8) {
        $('.login-form-username-error').empty()
        $('.login-form-username-error').text(' Whoops. Please make it longer than 8 characters.')
      } else {
        $('.login-form-username-error').empty()
        $('#login-submit-button').attr('disabled', false)
      }
    })
    .fail(err => err)
}

$(document).ready(() => {

  // BY DEFAULT, DO NOT ALLOW THEM TO SUBMIT THE FORM
  $('#login-submit-button').attr('disabled', true)

  // WHEN USER FOCUSES OUT OF USERNAME INPUT,
  // CHECK DATABASE TO SEE IF USERNAME IS ALREADY TAKEN
  $('#username-login').focusout((event) => {
    checkUsernameLogin()
  })

}) // End document ready
