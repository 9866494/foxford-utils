from bottle import route, run, template
from urllib.request import urlopen
from dateutil import parser
from datetime import timedelta
import json
import hashlib
import os
from pathlib import Path

sript_path = os.path.dirname(os.path.realpath(__file__))

@route('/ical')
def index():
    url = 'https://foxford.ru/api/calendar?date_from=2022-08-29&date_to=2022-12-31&token=f58b27c809e5e45f91b78871cf51da0799899a0e&user_id=8917764'
    response = urlopen(url)
    data = response.read()

    schedule_hash = hashlib.md5(data).hexdigest()
    storage_path = sript_path + '/var/ics/'
    ics_file_path = '{0}{1}.ics'.format(storage_path, schedule_hash)

    if os.path.exists(ics_file_path):
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

            vevent = template('vevent', dtstart=dtstart, dtend=dtend,
                              dtstamp=dtstamp, uid=uid, description=description, summary=summary, location=location)

            vevents.append(vevent)

            if prior_date != None and prior_date.date() < starts_at.date():
                home_work_starts_at = starts_at + \
                    timedelta(minutes=home_work_timedelta)
                home_work_ends_at = home_work_starts_at + \
                    timedelta(minutes=home_work_duration)

                home_work_date = home_work_starts_at.strftime("%Y%m%d")
                home_work_dtstart = home_work_starts_at.strftime(
                    "%Y%m%dT%H%M%SZ")
                home_work_dtend = home_work_ends_at.strftime("%Y%m%dT%H%M%SZ")
                home_work_dtstamp = home_work_dtstart

                home_work_uid = '{0}@{1}'.format(user_id, home_work_date)

                vevent = template('vevent', dtstart=home_work_dtstart, dtend=home_work_dtend,
                                  dtstamp=home_work_dtstamp, uid=home_work_uid, description=home_work_description, summary=home_work_summary, location=home_work_location)

                vevents.append(vevent)

            prior_date = starts_at

        result = template('vevents', vevents=vevents)

        file = open(ics_file_path, 'w')
        file.write(result)
        file.close()

    return result


if __name__ == "__main__":
    run(host='localhost', port=8080)
