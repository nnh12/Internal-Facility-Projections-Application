from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms

from data_upload_system.forms import TableInput


class ProjectionUpdateForm(forms.Form):
    projection = forms.CharField()
    comments = forms.CharField(required=False)
    accountParentLevelE = forms.CharField(widget=forms.HiddenInput)
    account = forms.CharField(widget=forms.HiddenInput)
    lastValue = forms.FloatField(widget=forms.HiddenInput)
    netBudget = forms.CharField(required=False, disabled=True)

    def __init__(self, *args, **kwargs):
        key = kwargs.pop("key")
        if "isChild" in kwargs:
            isChild = kwargs.pop("isChild")
        else:
            isChild = False
        super(ProjectionUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = "projectionForm"
        self.helper.form_method = "POST"
        self.helper.attrs = {'data_key': key, "data_isChild": isChild}
        self.helper.form_show_labels = False
        self.key = key

        self.layout = Layout(TableInput('projection', css_class="right-align"),
                             TableInput('netBudget', css_class="right-align"), TableInput('comments'),
                             Field('accountParentLevelE'), Field('lastValue'), Field('account'), )
        self.helper.layout = self.layout

        # self.accountParentLevelE.initial = accE
        # if len(args == 0):
        #     raise Exception("Did not specify an account")
        pass

    def getKey(self):
        """
        Returns the key that identifies this form. Useful for referencing a form in a template
        :return:
        """
        return self.key