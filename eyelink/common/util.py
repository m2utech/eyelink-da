from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
from consts import consts
from config import config


# 타임존 확인
def getTimezone():
    tz_list = []
    for tz in pytz.all_timezones:
        tz_list.append(tz)
    return tz_list

# EFSL, EFMM
def getToday(utcYN, fm):
    today = ""
    if utcYN is True:
        today = datetime.now(pytz.UTC)
        today = today.strftime(fm) + 'Z'
    else:
        today = datetime.now()
        today = today.strftime(fm)
    return today


def checkDatetime(strDate, fm):
    if 'Z' in strDate or 'z' in strDate:
        return strDate
    else:
        strDate = strDate + 'Z'
        strDate = getLocalStr2Utc(strDate, fm+'Z')
        return strDate


def getLocalStr2Utc(strDate, fm):
    strDate = datetime.strptime(strDate, fm)
    local_tz = pytz.timezone(consts.LOCAL_TIMEZONE)
    utc_dt = local_tz.localize(strDate).astimezone(pytz.UTC)
    utc_dt = utc_dt.strftime(fm)
    return utc_dt


def getIndexDateList(esIndex, sDate, eDate, fm):
    sDate = datetime.strptime(sDate.split('T')[0], consts.DATE).date()
    eDate = datetime.strptime(eDate.split('T')[0], consts.DATE).date()
    delta = eDate - sDate
    ind_list = []
    for i in range(delta.days + 1):
        dt = sDate + timedelta(days=i)
        dt = esIndex + dt.strftime(fm).replace('-', '.')
        ind_list.append(dt)
    return ind_list


def getStartEndDateByDay(timeRange, utcYN, fm):
    if utcYN is True:
        today = datetime.now(pytz.UTC)
    else:
        today = datetime.now()
    startDate = (today - relativedelta(days=timeRange)).strftime(fm)
    endDate = today.strftime(fm)
    return startDate, endDate

def getStartEndDateByHour(timeRange, utcYN, fm):
    if utcYN is True:
        today = datetime.now(pytz.UTC)
    else:
        today = datetime.now()
    startDate = (today - relativedelta(hours=timeRange)).strftime(fm)
    endDate = today.strftime(fm)
    return startDate, endDate

def convertDefaultDate(strDate):
    d = strDate.split('T')[0]
    t = strDate.split('T')[1]
    day = int(d.split('-')[2])
    day = '{0:02d}'.format(day % 10)
    if day == '00':
        day = '10'
    dt = "2018-01-{}T{}".format(day, t)
    return dt


def getStartEndDateByMinute(timeRange, utcYN, fm):
    if utcYN is True:
        today = datetime.now(pytz.UTC)
    else:
        today = datetime.now()
    startDate = (today - relativedelta(minutes=timeRange,seconds=-11)).strftime(fm)
    endDate = today.strftime(fm)
    return startDate, endDate

# EFSL
def getTimeRangeByDay(timeRange, fm):
    today = datetime.now()
    startDate = (today - relativedelta(days=timeRange)).strftime(fm)
    endDate = today.strftime(fm)
    return startDate, endDate

def datetime_range(start, end, delta):
    current = start
    if not isinstance(delta, timedelta):
        delta = timedelta(**delta)
    while current < end:
        yield current
        current += delta

if __name__ == '__main__':
    # s, e = getStartEndDateByMinute(60, False, consts.DATETIMEZERO)
    # s, e = getStartEndDateByHour(24, False, consts.DATETIMEZERO)
    #s, e = getTimeRangeByDay(1, consts.DATETIMEZERO)
    # dt = convertDefaultDate("2018-01-31T12:12:23")
    # print(dt)
    dt = getToday(True, consts.DATETIMEZERO)
    print(dt)
