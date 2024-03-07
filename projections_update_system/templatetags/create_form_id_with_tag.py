from django.template.defaulttags import register

from projections_update_system.summary import RecordSummary


@register.simple_tag
def create_form_id_with_tag(summaryObject:RecordSummary, tagName):
    """
    Creates an id for use by the javascript on the Projections Update page that will conform to the format:

    #{{AccountParentLevelEID}}_tagname
    :param summaryObject:
    :param tagName:
    :return:
    """
    return summaryObject.getAccountParentLevelEID() + "_" + tagName
