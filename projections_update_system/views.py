import datetime
import json
import logging
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.contrib import messages
from django.utils.translation import gettext
from django.http import HttpRequest
from django.db.models import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from projections_update_system.forms import ProjectionUpdateForm
from data_upload_system.models import Record, Organization, AccountParentLevelE
from global_libs.finances import toActualMonth, getMostRecentDateInformation, getFiscalInformation, getCurrentMonth, \
    getCurrentYear, getMostRecentUploadDateInCalandar
from projections_update_system.models import CurrentProjections, ProjectionsUpdateLog
from projections_update_system.summary import RecordSummary, accumulateSummaries
from django.contrib.admin.views.decorators import staff_member_required

from projections.constants import months
from django.db.models import Max

SUMMARY = "summaryprojection"
logger = logging.getLogger('django')


@login_required
def selectOrgToUpdate(request):
    """
    Serves a web page that allows the user to choose their organization to update projections for
    :param request:
    :return:
    """
    myOrganizations = request.user.myorganizations.organizations.all()
    lastUpdated = {}
    hasUploadedData = set()
    for org in myOrganizations:
        lastUpdated[org.id] = wasLastUpdatedThisMonth(org)
        if len(Record.objects.filter(organization=org.id + "~" + org.name)) > 0:
            hasUploadedData.add(org.id)
    return render(request, "projections_update_system/selectOrganization.html", {"myOrganizations" : myOrganizations,
                                                                                 "lastUpdated" : lastUpdated,
                                                                                 "hasUploadedData": hasUploadedData})


@login_required
def getDetailRecord(request):
    return render(request, "projections_update_system/detailRecord.html", {"data": [3]})


def handleProjectionFormPOSTRequest(request, form, org_id):
    for key, val in form.items():
        # Optional fields
        if key in ["comments", "program", "location", "activity"]:
            continue
        # If there is a blank in a required field, invalid sent
        # this the only case a "send" will fail, but usually will not happen,
        # because ‘’ is casted to 0 before "send"
        if val == '' or val is None:
            return False


    org = Organization.objects.get(id=org_id)
    accEParts = form["accountParentLevelE"].split("~")
    account = form["account"]
    accE, _ = AccountParentLevelE.objects.get_or_create(id=accEParts[0], name=accEParts[1])
    program = form["program"] if 'program' in form.keys() else None
    location = form["location"] if 'location' in form.keys() else None
    activity = form["activity"] if 'activity' in form.keys() else None
    currentProjection, created = CurrentProjections.objects.get_or_create(org=org, accE=accE, account=account, program=program, location=location, activity=activity)
    newProjection = float(form["projection"])
    comments = form["comments"]

    # If the projection's value has been edited or the projection was just created for the first time, make a log
    if created or currentProjection.projection != newProjection:
        if created:
            oldValue = 0
        else:
            oldValue = currentProjection.projection
        ProjectionsUpdateLog.objects.create(accE=accE, org=org, byUserName=request.user.username, fromValue=oldValue, toValue=newProjection)

    currentProjection.projection = newProjection
    currentProjection.comments = comments
    month, year = getMostRecentDateInformation()

    currentProjection.lastUpdatedFiscalMonth = month
    currentProjection.lastUpdatedYear = year
    currentProjection.save()

    # if the account updated is a child account,
    # then we need to update the summary projection
    if account != 'summaryprojection':
        summaryProjection, created = CurrentProjections.objects.get_or_create(org=org, accE=accE, account='summaryprojection')
        allAccEProjections = CurrentProjections.objects.all().filter(accE=accE, org=org)
        newSumProjectionAmount = 0
        for projection in allAccEProjections:
            if projection.account != 'summaryprojection':
                newSumProjectionAmount += projection.projection
        summaryProjection.projection = newSumProjectionAmount
        summaryProjection.save()
    return True

@login_required
def handleProjectionUpdatePOSTRequest(request, org_id):
    """
    Handles a projection form that is delivered via post request to the server
    :param request:
    :param org_id: Organization ID of the provided
    :return:
    """
    form_data_list = request.POST.getlist("forms[]", [])
    success = True
    #print(form_data_list);
    # for form_data in form_data_list:
    #     form = ProjectionUpdateForm(form_data)
    #     if form.is_valid() != True:
    #         success = False

    forms = [json.loads(item) for item in form_data_list]
    for i, form in enumerate(forms):
        if handleProjectionFormPOSTRequest(request, form, org_id) != True:
            success = False
    return success


def createProjectionUpdateForm(accE_full_descriptor, account, org_id, isChild=False, isDisabled=False, record=None):
    """
    Creates a projection update form given the full accounptParentE descriptor of the form "[ID]~[NAME]" and the account
    name

    :param accE_full_descriptor: accounptParentE descriptor of the form "[ID]~[NAME]"
    :param account: account name
    :param isChild: marks the form as a child form
    :return:
    """
    accE_id = accE_full_descriptor.split("~")[0]


    prefix = "{0}_%s"
    accountCode = None
    programCode = None
    activityCode = None
    locationCode = None

    if account == SUMMARY:
        key = accE_id
    else:
        accountCode = record.account.split("~")[0]
        programCode = record.program.split("~")[0]
        activityCode = record.activity.split("~")[0]
        locationCode = record.location.split("~")[0]
        key = "child_{0}_{1}_{2}_{3}".format(accountCode, programCode, locationCode, activityCode)

    form = ProjectionUpdateForm(auto_id=prefix.format(key), key=key, isChild=isChild)
    form.initial['accountParentLevelE'] = accE_full_descriptor
    form.initial['account'] = account
    if isDisabled:
        form.fields['projection'].disabled = True
        form.fields['comments'].disabled = True
    # Attempt to find last projection to use as default value
    if account == SUMMARY:
        lastProjection = CurrentProjections.objects.filter(accE__id=accE_id, account=account, org__id=org_id, location=None, program=None, activity=None).first()
    else:
        lastProjection = CurrentProjections.objects.filter(accE__id=accE_id, account=account, org__id=org_id, location=record.location, program=record.program, activity=record.activity).first()

    # Default data to be loaded in the form fields. Should reflect information from last form
    # If a projection value is not present for this, the form will be blank
    if lastProjection is not None:
        form.initial['projection'] = int(lastProjection.projection)
        form.initial['comments'] = lastProjection.comments
    if lastProjection is None:
        form.initial['projection'] = 0

    return form


@login_required
def updateProjections(request, org_id):
    """
    Serves a page where the user can update the accounts for a parent
    :param request:
    :param org_id:
    :return:
    """

    #Handles form submissions
    if request.method == "POST":
        if handleProjectionUpdatePOSTRequest(request, org_id) == True:
            return JsonResponse({}, status=200) #success
            # return HttpResponseRedirect(reverse("selectOrgToUpdate"))
        else:
            # failure, happens only if a required field is left empty (but '' is casted to 0 when filling)
            return JsonResponse({}, status=400)

    #Serves the update page
    organization = Organization.objects.get(id=org_id)
    fullOrgName = organization.id + "~" + organization.name
    mostRecentMonth, mostRecentYear = getMostRecentDateInformation()
    records = Record.objects.filter(organization=fullOrgName, month=mostRecentMonth, fiscal_year=mostRecentYear)

    accounts = AccountParentLevelE.objects.all()


    accts = defaultdict(list)
    acc_list = []
    acc_list_except_sum = []

    accounts = defaultdict(list)
    forms = {}
    summaries = {}

    # Fetch all accounts for adding in a new row
    for acc in accounts:
        accts[acc.id].append(acc.name)
    for (key, val) in accts.items():
        join_accts = '~'.join((key, val[0]))
        acc_list.append(join_accts)

    # Groups the org's records by parent level E
    for record in records[:]:
        accounts[record.account_parent_level_E].append(record)

    #Creates the summary views to be displayed based on the account parent level E\

    for key, groupedAccounts in accounts.items():
        if len(groupedAccounts) > 0:
            summaries[key] = createSummaryData(key, groupedAccounts, groupedAccounts[0].month)
            # Disable any summary view that has editable child projections
            id, name = splitFullIdentifier(key)
            accountParentLevelE, _ = AccountParentLevelE.objects.get_or_create(id=id, name=name)
            if accountParentLevelE.allowChildProjections:
                forms[key] = createProjectionUpdateForm(key, SUMMARY, organization.id, isDisabled=True)
            else:
                forms[key] = createProjectionUpdateForm(key, SUMMARY, organization.id, isDisabled=False)
    for account in acc_list:
        if account in summaries.keys():
            continue
        else:
            acc_list_except_sum.append(account)
    bottomLine = createTotalsLine(list(summaries.values()))
    ts = ProjectionsUpdateLog.objects.filter(org_id=org_id).aggregate(Max('timestamp'))['timestamp__max']
    lastUploadedMonth, lastUploadedYear = getMostRecentUploadDateInCalandar()
    return render(request, "projections_update_system/updater.html", {"recordForms": forms, "summaries": summaries,
                                                                      "organization": organization, "org_id": org_id,
                                                                      "fullOrganizationLabel": fullOrgName,
                                                                      "bottomLine": bottomLine,
                                                                      "ProjectionLastUpdatedTime": ts,
                                                                      "lastUploadedYear": lastUploadedYear,
                                                                      "lastUploadedMonth": months[lastUploadedMonth],
                                                                      "acc_list_except_sum": acc_list_except_sum})


@login_required
def projectionsHomepage(request):
    return render(request, "projections_update_system/home.html", {})


# Helper methods
def createSummaryData(accountName, groupedAccounts : list[Record], fiscalMonth : int) -> RecordSummary:
    """
    Creates a Summary data object given a group of accounts
    :param accountName:
    :param groupedAccounts:
    :param fiscalMonth:
    :return:
    """
    budget_amount = 0
    ytd_end_of_period = 0
    ytd_spent = 0
    spend_rate = 0
    total_actuals = 0
    total_encumberences = 0
    for account in groupedAccounts:
        budget_amount += account.budget_amount
        ytd_end_of_period += account.actual_YTD_end_of_period
        ytd_spent += account.actual_YTD_end_of_period + account.PO_Req_other_encumbrances + account.salary_encumbrance
        total_actuals += account.actual_YTD_end_of_period
        total_encumberences += account.PO_Req_other_encumbrances + account.salary_encumbrance

    spend_rate = ((total_actuals / fiscalMonth) * 12) + total_encumberences

    summary = RecordSummary(budget_amount, accountName, ytd_end_of_period, spend_rate, ytd_spent, fiscalMonth)
    return summary

def createTotalsLine(summaries: list[RecordSummary]) -> RecordSummary:
    return accumulateSummaries(summaries)


@login_required
def viewRecordInformation(request):
    """
    Called via JQuery / Javascript and will return a table of details about the provided accountParentLevelE and
    Org
    :param request:
    :return:
    """
    organization_name = request.POST["org"]
    org_id = request.POST["org_id"]
    account_parent_level_E = request.POST["accountParentLevelE"]
    month = int(request.POST["month"])
    summaryFieldID = request.POST["summaryFieldID"] #The ID of the projection field on the summary table to be updated
    records = Record.objects.filter(organization=organization_name, account_parent_level_E=account_parent_level_E, month=month)
    recordForms = {}

    accEId, _ = splitFullIdentifier(account_parent_level_E)
    allowChildProjections = AccountParentLevelE.objects.get(id=accEId).allowChildProjections
    if allowChildProjections:
        for record in records:
            #Associate each record with a form. Template will render this form using the record's pk
            recordForms[record.pk] = createProjectionUpdateForm(record.account_parent_level_E, record.account, org_id, isChild=True, record=record)
    summary = createSummaryData(account_parent_level_E, records, month)

    return render(request, "projections_update_system/detailRecord.html", {"records":records, "recordForms":recordForms,
                                                                       "summary":summary, "summaryFieldID":summaryFieldID, "org_id": org_id})


def splitFullIdentifier(key):
    """
    Takes an identifier of the form id~name and returns the separated components
    :param key:
    :return: id and name
    """
    id = key.split("~")[0]
    name = key.split("~")[1]
    return id, name

@register.filter
def to_currency(rawFloat):
    value = '{0:,.0f}'.format(abs(float(rawFloat)))
    if rawFloat < 0:
        return '(' + value + ')'
    return value

@login_required
@staff_member_required
def viewLogs(request):
    user_orgs = request.user.myorganizations.organizations.all()
    logs = ProjectionsUpdateLog.objects.filter(org__in=user_orgs)
    return render(request, "projections_update_system/changeLogs.html", {
        "logs": logs
    })

def wasLastUpdatedThisMonth(org):
    """
    Returns whether or not the given organization has been updated this fiscal month
    :param org: Organizaiton to check
    :return: True if this Org's projections were updated this month, false otherwise
    """

    month, year = getCurrentMonth(), getCurrentYear();
    # Checks the ProjectionUpdateLogs model for any logs this fiscal month for this org
    return ProjectionsUpdateLog.objects.filter(org_id=org.id, timestamp__month=toActualMonth(month), timestamp__year=year).exists();


def getCountOfAccounts(full_org_id):
    expectedSummaryProjections = Record.objects.filter(organization=full_org_id).values("account_parent_level_E").annotate(dcount=Count('account_parent_level_E')).order_by()
    expectedSummaryProjectionsCount = len(expectedSummaryProjections)

    for accountParentLevelE in expectedSummaryProjections:
        fullNameOfAccountParentLevelE = list(accountParentLevelE.values())[0]
        account = AccountParentLevelE.objects.get(id=splitFullIdentifier(fullNameOfAccountParentLevelE)[0])
        if account.allowChildProjections:
            expectedSummaryProjectionsCount += len(Record.objects.filter(organization=full_org_id, account_parent_level_E=fullNameOfAccountParentLevelE).values("account")
                                                   .annotate(dcount=Count('account')).order_by())
    return expectedSummaryProjectionsCount

def getProjectionsCountForMonth(org_id, fiscalMonth):
    return len(CurrentProjections.objects.filter(org__id=org_id, lastUpdatedFiscalMonth=fiscalMonth))

