from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
import consts


# 타임존 확인
def confirmTimezone():
    for tz in pytz.all_timezones:
        print(tz)


def getToday(utcYN, fm):
    if utcYN is True:
        today = datetime.now(pytz.UTC)
    else:
        today = datetime.now()
    today = today.strftime(fm)

    return today


def getLocalStr2Utc(strDate, fm):
    strDate = datetime.strptime(strDate, fm)
    local_tz = pytz.timezone(consts.LOCAL_TIMEZONE)
    utc_dt = local_tz.localize(strDate).astimezone(pytz.UTC)
    utc_dt = utc_dt.strftime(fm)
    return utc_dt


def getStartEndDateByHour(timeRange, utcYN, fm):
    if utcYN is True:
        today = datetime.now(pytz.UTC)
    else:
        today = datetime.now()
    startDate = (today - relativedelta(hours=timeRange)).strftime(fm)
    endDate = today.strftime(fm)

    return startDate, endDate


def getStartEndDateByMinute(timeRange, utcYN, fm):
    if utcYN is True:
        today = datetime.now(pytz.UTC)
    else:
        today = datetime.now()
    startDate = (today - relativedelta(minutes=timeRange)).strftime(fm)
    endDate = today.strftime(fm)

    return startDate, endDate


def getStartEndDateByDay(timeRange, utcYN, fm):
    if utcYN is True:
        today = datetime.now(pytz.UTC)
    else:
        today = datetime.now()
    startDate = (today - relativedelta(days=timeRange)).strftime(fm)
    endDate = today.strftime(fm)

    return startDate, endDate
