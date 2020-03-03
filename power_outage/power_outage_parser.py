from html_table_parser.parser import HTMLTableParser
import datetime
import urllib.request

URL = 'http://www.koe.vsei.ua/poweroff/default/planed?SearchPlanovi[region_id]={}&SearchPlanovi[dt]='

#<option value="6">Броварський</option>
REGION_BROVARY = 6
#<option value="7">Васильківський</option>
REGION_VASYLKIV = 7

FIELD_REGION = 0
FIELD_TOWN = 1
FIELD_STREET = 2
FIELD_EQUIPMENT = 3
FIELD_WORK_TYPE = 4
FIELD_DT_START = 5
FIELD_DT_STOP = 6
FIELD_PERIOD = 7

# search settings
REGION = REGION_VASYLKIV
SEARCH_TOWN = 'глеваха'
SEARCH_STREET = 'космонавтів'


req = urllib.request.Request(url=URL.format(REGION))
f = urllib.request.urlopen(req)
xhtml = f.read().decode('utf-8')

p = HTMLTableParser()
p.feed(xhtml)

events_active = ''
events_upcoming = ''
events_old = ''

for row in p.tables[0]:
    if not SEARCH_TOWN in row[FIELD_TOWN].lower():
        continue
    if not SEARCH_STREET in row[FIELD_STREET].lower():
        continue

    result = '{} - {}, {}, {};\\n\\n{}\\n\\n'.format(
        row[FIELD_DT_START],
        row[FIELD_DT_STOP],
        row[FIELD_PERIOD],
        row[FIELD_WORK_TYPE],
        row[FIELD_STREET]
    )

    event_date_start = datetime.datetime.strptime(row[FIELD_DT_START],
            '%Y-%m-%d').date()
    event_date_stop = datetime.datetime.strptime(row[FIELD_DT_STOP],
            '%Y-%m-%d').date()
    date_today = datetime.date.today()

    if event_date_start <= date_today <= event_date_stop:
        events_active += result
    elif date_today < event_date_start:
        events_upcoming += result
    else:
        events_old += result

result = '{ "state": '
if events_active:
    result += '"planned"'
else:
    result += '"not planned"'

if events_active:
    result += ', "active" : "{}"'.format(events_active.strip())
if events_upcoming:
    result += ', "upcoming" : "{}"'.format(events_upcoming.strip())
if events_old:
    result += ', "past" : "{}"'.format(events_old.strip())

result += '}'

print(result)
