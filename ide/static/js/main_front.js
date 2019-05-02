var htmlEditor = CodeMirror.fromTextArea(document.getElementById("html"),{
lineNumbers: true,
mode : 'xml',
theme : 'dracula',

});

var cssEditor = CodeMirror.fromTextArea(document.getElementById("css"),{
lineNumbers: true,
mode : 'css',
theme : 'dracula',
});

var jsEditor = CodeMirror.fromTextArea(document.getElementById("js"),{
lineNumbers: true,
mode : 'javascript',
theme : 'dracula',

});



$(document).ready(function(){

  $('textarea').keydown(function(e){


    if( e.keyCode === 9){
      //get caret position/selection
      var start = this.selectionStart;
      var end = this.selectionEnd;

      var $this = $(this);
      var value = $this.val();
        console.log(value)

      //set textarea value to : text before caret + tab + text after caret
      $this.val(value.substr(0, start) + '\t' + value.substr(end));

      //put caret at right position again (add one for the tab)
      this.selectionStart = this.selectionEnd = start - 1;

      //prevent the focus lose
      e.preventDefault();
    }
  });

  //getting input from textarea ' s
  function getHTML(){
    var html = htmlEditor.getValue();

    return html;
  }

  function getCSS(){
    var css = cssEditor.getValue();
    return css;
  }

  function getJS(){
    var js = jsEditor.getValue();
    return js;
  }

  //append input to iframe body
  var execute = function(){
      var targetIframe = $('#preview')[0].contentWindow.document;
      targetIframe.open();
      targetIframe.close();
      var html = getHTML();

      var css = '<style>' + getCSS() + '</style>';
      var js = '<script >' + getJS() + '</script>';
      window.onerror = true;
      $('body', targetIframe).append(html);
      $('head', targetIframe).append(css);
      $('body', targetIframe).append(js);

    }
var interval = setTimeout(execute, 1);
$('textarea').keyup(execute)

});
