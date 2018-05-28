from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import pytz
import consts


# 타임존 확인
def getTimezone():
    tz_list = []
    for tz in pytz.all_timezones:
        tz_list.append(tz)
    return tz_list


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


def getUtcStr2Local(strDate, fm):
    strDate = parse(strDate)
    local_tz = pytz.timezone(consts.LOCAL_TIMEZONE)
    local_dt = strDate.replace(tzinfo=pytz.UTC).astimezone(local_tz)
    local_dt = local_dt.strftime(fm)

    return local_dt



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
