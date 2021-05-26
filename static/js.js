//document ready
$(document).ready(function () {
  $('#getcolors').click(function (){
    $( "#getcolors" ).slideUp( "fast", function() {
      $('#loading').show();
    });
    $.post("postjson",
    {
      'color': $('#colorPicker').val()
    },
    function(data, status){
      $('#colors').empty();
      console.log("Data: " + data + "\nStatus: " + status);
      data.forEach(element => {
        console.log(element);
        $('#colors').append('<li class="color" swatch='+ element + '><input type="text" style="background: #'+ element +';" /></li>');
      });
        $('#colors').append('<span id="target">Generated using AI , those are the recommended colors to fit your input.</span>');
        $('#colors').css('display','block');
        $( "#getcolors" ).slideDown( "slow", function() {
          $('#loading').hide();
        });
      });
  });
  $('ul').click(function (e) {
      var elem = e.target;
      if ($(elem).is('input')) {
          $(elem).val('#'+$(elem).parent().attr('swatch'));
          elem.focus();
          elem.select();
          setTimeout(function () { resetElem(elem) }, 3000);            
      }
  });
 

});

//functions
function resetElem(elem) {
  $(elem).val('');
  elem.blur();
}

document.querySelectorAll('input[type=color]').forEach(function(picker) {

  var targetLabel = document.querySelector('label[for="' + picker.id + '"]'),
  codeArea = document.createElement('span');
  codeArea.setAttribute("id", "colorspan");
  codeArea.innerHTML = picker.value;
  targetLabel.appendChild(codeArea);

  picker.addEventListener('change', function() {
    codeArea.innerHTML = picker.value;
    targetLabel.appendChild(codeArea);
  });
});



