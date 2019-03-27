var editor = CodeMirror.fromTextArea(document.getElementById("code_id"),{
lineNumbers: true,
mode : 'python',
theme : 'dracula'
});

editor.setSize(500, 300);
