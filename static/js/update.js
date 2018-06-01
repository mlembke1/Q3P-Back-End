let titleIsFilledOut = false
let authorIsFilledOut = false
let jeIsFilledOut = false

const validate = () => {
  console.log('validate has been called')
  const updateAuthorInput = $('#update-author-input').val()
  const updateTitleInput = $('#update-title-input').val()
  const updateJournalEntryInput = $('#update-journal_entry-input').val()
  authorIsFilledOut = updateAuthorInput.length > 0  ? true : false
  titleIsFilledOut = updateTitleInput.length > 0 ? true : false
  jeIsFilledOut = updateJournalEntryInput.length > 0 ? true : false
  authorIsFilledOut && titleIsFilledOut && jeIsFilledOut ?
  $('#confirm-update-button').removeAttr('disabled') :
  $('#confirm-update-button').attr('disabled')
}

$(document).ready(() => {
  $(".dropdown-trigger").dropdown()

  // HANDLE CLICK EVENT THAT UPDATES A JOURNAL ENTRY
  $('#confirm-update-button').click((e) => {
    e.preventDefault()
    const id = $(e.target).data('id')
    const formInput = {
      author: $('#update-author-input').val(),
      title: $('#update-title-input').val(),
      journal_entry: $('#update-journal_entry-input').val()
    }
    $.ajax({
        url: `/update/${id}`,
        type: 'PUT',
        data: formInput,
        success: (result) => {
          if(result.message === 'success'){
            window.location = 'https://write-flask.herokuapp.com/read'
          }
        }
    })
  })


  $('#update-author-input').keyup(validate)
  $('#update-title-input').keyup(validate)
  $('#update-journal_entry-input').keyup(validate)

})
