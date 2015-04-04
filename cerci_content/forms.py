from django import forms
from cerci_content.models import IssueContent
from ckeditor.widgets import CKEditorWidget


class IssueContentAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        fields = '__all__'
        model = IssueContent
