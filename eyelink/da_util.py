from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz
import da_consts as consts


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


def getStartEndDateByMinute(timeRange, utcYN, fm):
    if utcYN is True:
        today = datetime.now(pytz.UTC)
    else:
        today = datetime.now()
    startDate = (today - relativedelta(minutes=timeRange,seconds=-11)).strftime(fm)
    endDate = today.strftime(fm)
    return startDate, endDate


if __name__ == '__main__':
    s, e = getStartEndDateByMinute(60, False, consts.DATETIMEZERO)
    print(s, e)
