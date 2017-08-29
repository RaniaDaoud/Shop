// Used in Attachement image
// Used in profile picture
function readURL(input, frame, id=0) {
  if (input.files && input.files[id]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      frame.attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[id]);
  }
}

// Preview multiple images using one file input
function previewMultiple(input, frame, template) {
    var length = input.files.length;
    for (var i=0; i<length; i++) {
        var clone = template.clone();
        frame.append(clone);
        readURL(input, clone.children('img'), i);
    }
}