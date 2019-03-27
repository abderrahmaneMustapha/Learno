from django import forms


class MediaForm(forms.Form):
    def media(language):
        if language  == 'frontend-editor':
            return forms.Media(js={
        'codemirror/mode/xml/xml.js':'codemirror/mode/xml/xml.js',
        'codemirror/mode/css/css.js':'codemirror/mode/css/css.js',
        'codemirror/mode/javascript/javascript.js':'codemirror/mode/javascript/javascript.js'})
        else:
            import re
            language_re = "".join(re.findall("[a-zA-Z]+", language))
            print(language_re)
            return forms.Media(js={'codemirror/mode/'+language_re+'/'+language_re+'.js':
        'codemirror/mode/'+language+'/'+language+'.js'})
