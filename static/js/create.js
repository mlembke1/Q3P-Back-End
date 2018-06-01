let createtitleIsFilledOut = false
let createauthorIsFilledOut = false
let createjeIsFilledOut = false

const validateCreate = () => {
  console.log('validate has been called')
  const updateAuthorInput = $('#create-author-input').val()
  const updateTitleInput = $('#create-title-input').val()
  const updateJournalEntryInput = $('#create-journal_entry-input').val()
  createauthorIsFilledOut = updateAuthorInput.length > 0  ? true : false
  createtitleIsFilledOut = updateTitleInput.length > 0 ? true : false
  createjeIsFilledOut = updateJournalEntryInput.length > 0 ? true : false
  createauthorIsFilledOut && createtitleIsFilledOut && createjeIsFilledOut ?
  $('#create-entry-button').removeAttr('disabled') :
  $('#create-entry-button').attr('disabled')
}

$(document).ready(() => {
  $('#create-author-input').keyup(validateCreate)
  $('#create-title-input').keyup(validateCreate)
  $('#create-journal_entry-input').keyup(validateCreate)
})
