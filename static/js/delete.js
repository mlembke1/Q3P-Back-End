$(document).ready(() => {
  $(".dropdown-trigger").dropdown()

  // HANDLE CLICK EVENT THAT DELETES AN ENTRY
  $('#confirm-delete-button').click((e) => {
    e.preventDefault()
    const id = $(e.target).data('id')
    $.ajax({
        url: `/delete/${id}`,
        type: 'DELETE',
        success: (data) => {
            if(data.message === 'success'){
              window.location = 'https://write-flask.herokuapp.com/read'
            }
        }
    })
  })

})
