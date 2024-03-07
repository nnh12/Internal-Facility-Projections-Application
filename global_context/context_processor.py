from data_upload_system.forms import AddUserInfoForm
from django.urls import reverse

#This provider is called in the context_processor section in the settings
def add_variable_to_context(request):

    form = AddUserInfoForm()

    return {
        'AddUserInfoForm': form,
        'ajax_url': reverse('updateLogin')
    }