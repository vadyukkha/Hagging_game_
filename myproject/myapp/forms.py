from django import forms

class UploadFileForm(forms.Form):
    # folder_name = forms.CharField(max_length=100)
    cpp_file = forms.FileField()
