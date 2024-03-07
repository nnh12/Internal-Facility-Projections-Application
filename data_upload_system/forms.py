from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row
from django import forms

from data_upload_system.models import Record
from crispy_forms.layout import Field


class TableInput(Field):
    template = 'forms/tableData.html'
    number = 1



class ProjectionForm(forms.Form):
    account_parent_level_E = forms.CharField()
    budget_amount = forms.FloatField()
    actual_YTD_end_of_period = forms.FloatField()
    adjusted_budget = forms.FloatField()
    ytd_spent = forms.FloatField()
    spend_rate = forms.FloatField()
    projection = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(ProjectionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        field_names = [field for field in self.base_fields]
        oneRow = [TableInput(field) for field in field_names]
        self.helper.layout = Layout(*oneRow)


class RecordModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecordModelForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)
        field_names = [field for field in self.base_fields]
        self.helper.form_show_labels = False
        #Account(description, Budget, Amount,	Actual YTD Beginning of Period,	Period Net, Actual YTD End of Period

        oneRow = [Column(field) for field in field_names]
        self.helper.layout = Layout(Row(*oneRow))

    class Meta:
        model = Record
        fields = ["account_parent_level_E", "budget_amount", "actual_YTD_beginning_of_period", "period_net", "actual_YTD_end_of_period"]


class AddUserInfoForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    emailVerify = forms.CharField(label="Confirm Email")

    def __init__(self,*args,**kwargs):
        super(AddUserInfoForm,self).__init__(*args,**kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'addUserInfo'
        self.helper.form_method = 'post'
        # self.helper.form_action = 'addUserInfo'

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-12'
        self.helper.field_class = 'col-lg-12'

