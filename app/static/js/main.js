// Polyfill for element.closest: http://devdocs.io/dom/element/closest
// Per http://stackoverflow.com/questions/15329167/closest-ancestor-matching-selector-using-native-dom
if (window.Element && !Element.prototype.closest) {
  Element.prototype.closest =
  function(s) {
      var matches = (this.document || this.ownerDocument).querySelectorAll(s),
          i,
          el = this;
      do {
          i = matches.length;
          while (--i >= 0 && matches.item(i) !== el) {};
      } while ((i < 0) && (el = el.parentElement));
      return el;
  };
}

function hide(elementList) {
    elementList.forEach(function(el) {
        if (!el.className.match(/\bhidden\b/)) {
            el.className = el.className.concat(' hidden');
        }
    })
}

/*
 * When editing or deleting a comment, clicking on the 'cancel' button
 * should hide the active comment form (edit or delete) and display the
 * original comment once again.
 */
function cancelEdit(e) {
    e.preventDefault();
    var commentRoot = this.closest('.post-comment');
    var editForm = commentRoot.querySelector('form.update-comment-form')
    var deleteForm = commentRoot.querySelector('form.delete-comment-form')
    var commentBody = commentRoot.querySelector('q');

    if (commentBody.className.match(/\bhidden\b/)) {
        hide([editForm, deleteForm]);
        commentBody.className = commentBody.className.replace(/\bhidden\b/, '').trim();
    }
}

/*
 * Checks if the comment is currently being edited; if not, it means that the
 * comment or the delete form is currently displayed so they need to be hidden
 * first before the edit comment form is shown.
 */
function editComment() {
    var commentRoot = this.closest('.post-comment');
    var editForm = commentRoot.querySelector('form.update-comment-form')
    var deleteForm = commentRoot.querySelector('form.delete-comment-form')
    var commentBody = commentRoot.querySelector('q');

    if (editForm.className.match(/\bhidden\b/)) {
        hide([commentBody, deleteForm]);
        editForm.className = editForm.className.replace(/\bhidden\b/, '').trim();
    }
}

/*
 * Checks if the delete comment form is currently displayed; if not, it means
 * that the comment or the edit comment form is displayed so they need to be
 * hidden first before the delete comment form is shown.
 */
function deleteComment() {
    var commentRoot = this.closest('.post-comment');
    var editForm = commentRoot.querySelector('form.update-comment-form')
    var deleteForm = commentRoot.querySelector('form.delete-comment-form')
    var commentBody = commentRoot.querySelector('q');

    if (deleteForm.className.match(/\bhidden\b/)) {
        hide([commentBody, editForm]);
        deleteForm.className = deleteForm.className.replace(/\bhidden\b/, '').trim();
    }
}

window.addEventListener('load', function() {
    // Add event listeners to the edit and delete comment buttons in each of the
    // comment action sections
    var commentActionSections = document.querySelectorAll('#read-post .comment-actions');

    // Add event listeners to the cancel buttons in the comment forms
    var cancelCommentChangeBtns = document.querySelectorAll('#read-post .post-comment form button.cancel');

    commentActionSections.forEach(function(section) {
        var editBtn = section.querySelector('button.edit-comment');
        var deleteBtn = section.querySelector('button.delete-comment');

        editBtn.addEventListener('click', editComment, true);
        deleteBtn.addEventListener('click', deleteComment, true);
    })

    cancelCommentChangeBtns.forEach(function(cancelBtn) {
        cancelBtn.addEventListener('click', cancelEdit, true);
    })
})
