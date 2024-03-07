class RecordSummary():
    def __init__(self, budget, account_parent_level_e, actual_ytd, spend_rate, ytd_spent, month):
        self.budget_amount = round(budget, 2)
        self.account_parent_level_E = account_parent_level_e
        self.actual_YTD_end_of_period = round(actual_ytd, 2)
        self.spend_rate = round(spend_rate, 2)
        self.ytd_spent = round(ytd_spent, 2)
        self.fiscal_month = month

    def getAccountParentLevelEID(self):
        return self.account_parent_level_E.split("~")[0]


def accumulateSummaries(summaries : list[RecordSummary]) -> RecordSummary:
    """
    Returns an accumulated total of the RecordSummary objects provided
    :param summaries:
    :return:
    """
    total = RecordSummary(0, "TOTALS", 0, 0, 0, 0)

    for summary in summaries:
        if summary:
            total.budget_amount += summary.budget_amount
            total.actual_YTD_end_of_period += summary.actual_YTD_end_of_period
            total.spend_rate += summary.spend_rate
            total.ytd_spent += summary.ytd_spent

    return total
