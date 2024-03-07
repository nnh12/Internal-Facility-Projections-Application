from django.template.defaulttags import register

from data_upload_system.models import Record
from projections_update_system.summary import RecordSummary


@register.simple_tag
def create_child_form_id_with_tag(summaryObject: Record, tagName):
    """
    Creates an id for use by the javascript on the Projections Update page that will conform to the format:

    #{{AccountParentLevelEID}}_tagname
    :param summaryObject:
    :param tagName:
    :return:
    """
    accountCode = summaryObject.account.split("~")[0]
    programCode = summaryObject.program.split("~")[0]
    activityCode = summaryObject.activity.split("~")[0]
    locationCode = summaryObject.location.split("~")[0]
    return "child_" + accountCode + "_" + programCode + "_" + locationCode + "_" + activityCode + "_" + tagName
