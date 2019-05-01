from django import forms


class MediaForm(forms.Form):
    def media(language):
        if language  == 'frontend-editor':
            return forms.Media(js={
        'codemirror/mode/xml/xml.js':'codemirror/mode/xml/xml.js',
        'codemirror/mode/css/css.js':'codemirror/mode/css/css.js',
        'codemirror/mode/javascript/javascript.js':'codemirror/mode/javascript/javascript.js'})
        else:
            if language == 'java':
                language+='script'
            if language == 'cpp' or language ==  'c':
                language='clike'
            return forms.Media(js={'codemirror/mode/'+language+'/'+language+'.js':
        'codemirror/mode/'+language+'/'+language+'.js'})
