var im = {};
im.submit = function() {
  var q1 = $('#question-1').val();
  window.console.log(q1);
  var data = {
    'q': q1
  };
  $.ajax({
    method: "POST",
    url: "phone_ins_form_completed",
    data: data
  })
  .done(function(msg) {
    window.console.log(msg);
  });
}