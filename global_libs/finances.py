import datetime
from dateutil.relativedelta import relativedelta

from django.db.models import Max

from data_upload_system.models import Record
from projections.constants import months_str2num, months


def getCurrentMonth():
    actualMonth = datetime.date.today().strftime("%B")
    return months_str2num[actualMonth]

def getCurrentYear():
    actualYear = datetime.date.today().strftime("%Y")
    return int(actualYear)

def toActualMonth(fiscalMonth):
    long_month_name = months[fiscalMonth]
    datetime_object = datetime.datetime.strptime(long_month_name, "%B")
    month_number = datetime_object.month
    return month_number

def getMostRecentDateInformation() -> (int, int):
    """
    Returns the most recent month and most recent fiscal year
    :return: maxMonth and maxYear
    """
    maxYear = Record.objects.aggregate(Max('fiscal_year'))['fiscal_year__max']
    maxMonth = Record.objects.filter(fiscal_year=maxYear).aggregate(Max('month'))['month__max']
    return maxMonth, maxYear

def getMostRecentUploadDateInCalandar() -> (int, int):
    """
    Returns the most recent month and most recent fiscal year
    :return: maxMonth and maxYear
    """
    maxYear = Record.objects.aggregate(Max('fiscal_year'))['fiscal_year__max']
    maxMonth = Record.objects.filter(fiscal_year=maxYear).aggregate(Max('month'))['month__max']
    if maxMonth < 7:
        maxYear = maxYear - 1
    return maxMonth, maxYear

def getFiscalInformation() -> (int, int):
    """
    Returns the most recent month and most recent fiscal year
    :return: maxMonth and maxYear - 1
    """
    fiscalYear = Record.objects.aggregate(Max('fiscal_year'))['fiscal_year__max']
    fiscalMonth = Record.objects.filter(fiscal_year=fiscalYear).aggregate(Max('month'))['month__max']
    return fiscalMonth, fiscalYear
# def getLastUploadedFiscalMonth():
#
#     if not Record.objects.exists():
#         return None
#     #Look up until our current fiscal month for the last fiscal month that we have.
#     currentFiscalMonth = getCurrentFiscalMonth()
#     for currentMonth in range(1, currentFiscalMonth + 1):
#         if not Record.objects.filter(month=currentMonth).exists():
#             return currentMonth - 1
#
#     return currentFiscalMonth



