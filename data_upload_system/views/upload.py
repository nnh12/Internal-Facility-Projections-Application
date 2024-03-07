from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from accounts.access_list import user_orgs

from data_upload_system.models import UploadHistory, Record, AccountParentLevelE
from projections.constants import months_str2num
import pandas as pd
import logging

logger = logging.getLogger('django')

FILE_KEY = r'data_file'
MONTH_KEY = r'month'


@login_required
@staff_member_required
def upload(request):
    if request.method == 'POST' and FILE_KEY in request.FILES:
        uploadResult = newUpload(request)
        request.session["uploadResult"] = uploadResult

    return HttpResponseRedirect("/data/")




def get_valid_account_parent_levels():
    valid_account_parent_levels = AccountParentLevelE.objects.values_list('id', flat=True)

    valid_account_parent_levels_set = set(valid_account_parent_levels)

    return valid_account_parent_levels_set


def newUpload(request):
    file = request.FILES[FILE_KEY]
    if not file:
        return "File not found."

    month = months_str2num[request.POST[MONTH_KEY]]
    if not month:
        return "Month not specified."

    if doesUploadExist(month):
        Record.objects.filter(month=month).delete()
        UploadHistory.objects.filter(month=month).delete()

    try:
        data = pd.read_excel(file)
    except Exception as e:
        logger.error(e)
        return "Error when reading file: " + str(e)

    username = "admin"
    if request.user is not None:
        user = request.user
        username = user.first_name + " " + user.last_name + ' (' + user.username + ')'

    thisUpload = UploadHistory(byUsername=username, month=month, rows=0)

    valid_account_parent_levels_set = get_valid_account_parent_levels()

    # Check if all accounts in the uploaded data are valid
    invalid_accounts = set()
    for account in data['Account Parent Level E']:
        try:
            account_parent_level_e = account.split('~')[0]

            if account_parent_level_e not in valid_account_parent_levels_set:
                invalid_accounts.add(account)

        except Exception as e:
            print(f"Error occurred while processing data: {e}")


    if invalid_accounts:
        # TODO: Send email notification for unauthorized account
        print(invalid_accounts)

        # send_mail(
        #     'Unauthorized Account Uploaded',
        #     f'The account "{invalid_accounts}" were uploaded by {username} but is not authorized.',
        #     'alisonqiu4@gmail.com',
        #     ['zq6@rice.edu'],  # TODO: Replace with admin email address
        #     fail_silently=False,
        # )
    try:
        num_records = insert(data, thisUpload.id)
    except Exception as e:
        logger.error(e)
        Record.objects.filter(upload_id=thisUpload.id).delete()
        return "Error when inserting data: " + str(e)
    else:
        thisUpload.rows = num_records
        thisUpload.save()
        return "Upload success!"


def doesUploadExist( month):
    return Record.objects.filter(month=month).exists()


def insert(data, upload_id):
    num_records = 0
    for i, row in data.iterrows():
        try:
            Record(
                fiscal_year=row["Fiscal Year"],
                month=row["Month"][:2],
                upload_id=upload_id,

                fund_type_parent_level_A=row["Fund Type Parent Level A"],
                fund_type_parent_level_B=row["Fund Type Parent Level B"],
                fund_type=row["Fund Type"],

                fund_source_parent_level_C=row["Fund Source Parent Level C"],
                fund_source_parent_level_D=row["Fund Source Parent Level D"],
                fund_source=row["Fundsource"],

                organization_parent_level_B=row["Organization Parent Level  B"],
                organization_parent_level_C=row["Organization Parent Level C (Division)"],
                organization_parent_level_D=row["Organization Parent Level D"],
                organization_parent_level_E=row["Organization Parent Level  E"],
                organization=row["Organization"],

                account_parent_level_B=row["Account Parent Level B"],
                account_parent_level_C=row["Account Parent Level C"],
                account_parent_level_D=row["Account Parent Level D"],
                account_parent_level_E=row["Account Parent Level E"],
                account=row["Account"],

                budget_amount=row["Budget Amount"],
                actual_YTD_beginning_of_period=row["Actual YTD Beginning of Period"],
                period_net=row["Period Net"],
                actual_YTD_end_of_period=row["Actual YTD End of Period"],
                PO_Req_other_encumbrances=row["PO, Req & Other Encumbrances"],
                salary_encumbrance=row["Salary Encumbrance"],
                remaining_budget=row["Remaining Budget"],

                program=row["Program"],
                activity=row["Activity"],
                location=row["Location"]).save()
        except Exception as e:
            logger.error(e)
        else:
            num_records += 1

    return num_records
