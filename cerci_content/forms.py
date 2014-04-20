from django import forms
from django.db.models import get_model
from ckeditor.widgets import CKEditorWidget


class IssueContentAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = get_model('cerci_content', 'IssueContent')
