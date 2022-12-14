from bottle import route, run, template
from urllib.request import urlopen
from dateutil import parser
from datetime import timedelta
import json
import hashlib
import os
from pathlib import Path

sript_path = os.path.dirname(os.path.realpath(__file__))

@route('/')
def utils():
    return template('utils/index')

@route('/ical/<user_id>/<token>')
def ical(user_id, token):
    year = 2022
    date_from = '{0}-09-01'.format(year)
    date_to = '{0}-08-31'.format(int(year) +1)
    
    url = 'https://foxford.ru/api/calendar?date_from={0}&date_to={1}&token={2}&user_id={3}'.format(date_from,date_to, token, user_id)
    response = urlopen(url)
    data = response.read()

    schedule_hash = hashlib.md5(data).hexdigest()
    storage_path = sript_path + '/var/ics/'
    ics_file_path = '{0}{1}.ics'.format(storage_path, schedule_hash)

    if False and os.path.exists(ics_file_path):
        result = Path(ics_file_path).read_text()
    else:
        dict = json.loads(data.decode("utf-8"))
        user_id = dict['user']['id']
        vevents = []

        prior_date = None

        home_work_summary = 'Сделать ДЗ'
        home_work_description = 'Знание свет'
        home_work_location = ''
        home_work_timedelta = 30
        home_work_duration = 60

        for course_lesson in dict['course_lessons']:
            starts_at_str = course_lesson['starts_at']
            starts_at = parser.parse(starts_at_str)
            starts_at = starts_at - starts_at.utcoffset()
            ends_at = starts_at + timedelta(minutes=course_lesson['duration'])

            dtstart = starts_at.strftime("%Y%m%dT%H%M%SZ")
            dtend = ends_at.strftime("%Y%m%dT%H%M%SZ")
            dtstamp = dtstart
            uid = '{0}@{1}'.format(user_id, course_lesson['url'])
            summary = course_lesson['discipline_name']
            description = "{0}  {1}".format(
                course_lesson['title'], course_lesson['agent_name'])

            location = 'https://foxford.ru{0}'.format(course_lesson['url'])

            vevent = template('isc/vevent', dtstart=dtstart, dtend=dtend,
                              dtstamp=dtstamp, uid=uid, description=description, summary=summary, location=location)

            vevents.append(vevent)

            if prior_date != None:
                truncated_prior_date = prior_date.replace(hour=0, minute=0, second=0, microsecond=0)
                truncated_starts_at = starts_at.replace(hour=0, minute=0, second=0, microsecond=0)
                
                if truncated_prior_date < truncated_starts_at:
                    home_work_starts_at = prior_date + \
                        timedelta(minutes=home_work_timedelta)
                    home_work_ends_at = home_work_starts_at + \
                        timedelta(minutes=home_work_duration)

                    home_work_date = home_work_starts_at.strftime("%Y%m%d")
                    home_work_dtstart = home_work_starts_at.strftime(
                        "%Y%m%dT%H%M%SZ")
                    home_work_dtend = home_work_ends_at.strftime("%Y%m%dT%H%M%SZ")
                    home_work_dtstamp = home_work_dtstart

                    home_work_uid = '{0}@{1}'.format(user_id, home_work_date)

                    vevent = template('isc/vevent', dtstart=home_work_dtstart, dtend=home_work_dtend,
                                    dtstamp=home_work_dtstamp, uid=home_work_uid, description=home_work_description, summary=home_work_summary, location=home_work_location)

                    vevents.append(vevent)

            prior_date = ends_at

        result = template('isc/vevents', vevents=vevents)

        file = open(ics_file_path, 'w')
        file.write(result)
        file.close()

    return result


if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)
