import xml.etree.ElementTree as ET
import glob
import datetime
import calendar
import csv

import pendulum

DDL = """create table date_dim
(
    date_dim_id           integer    not null
        constraint date_dim_pkey
            primary key,
    dt                    date       not null,
    epoch                 integer    not null
        constraint date_dim_epoch_check
            check (epoch >= 1451606400),
    day                   smallint   not null
        constraint date_dim_day_check
            check ((day >= 1) AND (day <= 31)),
    weekday               smallint   not null
        constraint date_dim_weekday_check
            check ((weekday >= 0) AND (weekday <= 6)),
    weekday_iso           smallint   not null
        constraint date_dim_weekday_iso_check
            check ((weekday_iso >= 1) AND (weekday_iso <= 7)),
    weekday_name_en       varchar    not null
        constraint date_dim_weekday_name_en_check
            check ((weekday_name_en)::text = ANY
                   ((ARRAY ['Friday'::character varying, 'Sunday'::character varying, 'Saturday'::character varying, 'Tuesday'::character varying, 'Thursday'::character varying, 'Monday'::character varying, 'Wednesday'::character varying])::text[])),
    weekday_name_ru       varchar    not null
        constraint date_dim_weekday_name_ru_check
            check ((weekday_name_ru)::text = ANY
                   ((ARRAY ['Суббота'::character varying, 'Вторник'::character varying, 'Понедельник'::character varying, 'Четверг'::character varying, 'Пятница'::character varying, 'Среда'::character varying, 'Воскресенье'::character varying])::text[])),
    is_weekend            smallint   not null
        constraint date_dim_is_weekend_check
            check (is_weekend = ANY (ARRAY [0, 1])),
    is_holiday            smallint   not null
        constraint date_dim_is_holiday_check
            check (is_holiday = ANY (ARRAY [0, 1])),
    holiday_name_en       varchar    not null,
    holiday_name_ru       varchar    not null,
    day_of_year           smallint   not null
        constraint date_dim_day_of_year_check
            check ((day_of_year >= 1) AND (day_of_year <= 366)),
    week_of_month         smallint   not null
        constraint date_dim_week_of_month_check
            check ((week_of_month >= 1) AND (week_of_month <= 5)),
    week_of_year          smallint   not null
        constraint date_dim_week_of_year_check
            check ((week_of_year >= 1) AND (week_of_year <= 53)),
    week_of_year_iso      smallint   not null
        constraint date_dim_week_of_year_iso_check
            check ((week_of_year_iso >= 1) AND (week_of_year_iso <= 53)),
    month                 smallint   not null
        constraint date_dim_month_check
            check ((month >= 1) AND (month <= 12)),
    month_name_en         varchar    not null
        constraint date_dim_month_name_en_check
            check ((month_name_en)::text = ANY
                   ((ARRAY ['October'::character varying, 'November'::character varying, 'December'::character varying, 'January'::character varying, 'May'::character varying, 'April'::character varying, 'July'::character varying, 'March'::character varying, 'August'::character varying, 'February'::character varying, 'June'::character varying, 'September'::character varying])::text[])),
    month_name_ru         varchar    not null
        constraint date_dim_month_name_ru_check
            check ((month_name_ru)::text = ANY
                   ((ARRAY ['Май'::character varying, 'Август'::character varying, 'Март'::character varying, 'Декабрь'::character varying, 'Январь'::character varying, 'Июнь'::character varying, 'Октябрь'::character varying, 'Июль'::character varying, 'Апрель'::character varying, 'Сентябрь'::character varying, 'Февраль'::character varying, 'Ноябрь'::character varying])::text[])),
    month_name_for_rep_ru varchar    not null
        constraint date_dim_month_name_for_rep_ru_check
            check ((month_name_for_rep_ru)::text = ANY
                   ((ARRAY ['Апреля'::character varying, 'Октября'::character varying, 'Мая'::character varying, 'Июня'::character varying, 'Ноября'::character varying, 'Марта'::character varying, 'Августа'::character varying, 'Февраля'::character varying, 'Июля'::character varying, 'Января'::character varying, 'Сентября'::character varying, 'Декабря'::character varying])::text[])),
    quarter               smallint   not null
        constraint date_dim_quarter_check
            check ((quarter >= 1) AND (quarter <= 4)),
    quarter_name_en       varchar    not null
        constraint date_dim_quarter_name_en_check
            check ((quarter_name_en)::text = ANY
                   ((ARRAY ['Third'::character varying, 'Fourth'::character varying, 'First'::character varying, 'Second'::character varying])::text[])),
    quarter_name_ru       varchar    not null
        constraint date_dim_quarter_name_ru_check
            check ((quarter_name_ru)::text = ANY
                   ((ARRAY ['Третий'::character varying, 'Четвертый'::character varying, 'Второй'::character varying, 'Первый'::character varying])::text[])),
    year                  smallint   not null
        constraint date_dim_year_check
            check ((year >= 2016) AND (year <= 9999)),
    mmyyyy                varchar(6) not null,
    ddmmyyyy              varchar(8) not null,
    first_day_of_week     date       not null,
    last_day_of_week      date       not null,
    first_day_of_month    date       not null,
    last_day_of_month     date       not null,
    first_day_of_quarter  date       not null,
    last_day_of_quarter   date       not null,
    first_day_of_year     date       not null,
    last_day_of_year      date       not null,
    constraint date_dim_check
        check (first_day_of_week < last_day_of_week),
    constraint date_dim_check1
        check (first_day_of_week < last_day_of_week),
    constraint date_dim_check2
        check (first_day_of_month < last_day_of_month),
    constraint date_dim_check3
        check (first_day_of_month < last_day_of_month),
    constraint date_dim_check4
        check (first_day_of_quarter < last_day_of_quarter),
    constraint date_dim_check5
        check (first_day_of_quarter < last_day_of_quarter),
    constraint date_dim_check6
        check (first_day_of_year < last_day_of_year),
    constraint date_dim_check7
        check (first_day_of_year < last_day_of_year)
);
"""

QUARTERS_NAMES = {'en': {1: 'First', 2: 'Second', 3: 'Third', 4: 'Fourth'},
                  'ru': {1: 'Первый', 2: 'Второй', 3: 'Третий', 4: 'Четвертый'}
                  }

MONTH_NAMES = {'ru': {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
                      9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',
                      }}

NA = 'n/a'

START_DATE = '31-12-2022'
END_DATE = '01-01-2023'


def generate_row(dt: datetime, calend_ru, calend_en):
    row = {
        'date_dim_pk': dt.strftime('%Y%m%d'),
        'dt': dt.strftime('%Y-%m-%d'),
        'epoch': calendar.timegm(dt.timetuple()),
        'day': dt.day,
        'weekday': dt.weekday(),
        'weekday_iso': dt.isoweekday(),
        'weekday_name_en': dt.strftime('%A'),
        'weekday_name_ru': pendulum.instance(dt).format('dddd', locale='ru').capitalize(),
        'is_weekend': 1 if dt.isoweekday() in (6, 7) else 0,
        'is_working_day': calend_ru.get(dt.strftime('%Y-%m-%d'), (0 if dt.isoweekday() in (6, 7) else 1, NA))[0],
        'is_holiday': 1 if calend_en.get(dt.strftime('%Y-%m-%d'), (0 if dt.isoweekday() in (6, 7) else 1, NA))[
                               1] != NA else 0,
        'holiday_name_en': calend_en.get(dt.strftime('%Y-%m-%d'), (0 if dt.isoweekday() in (6, 7) else 1, NA))[1],
        'holiday_name_ru': calend_ru.get(dt.strftime('%Y-%m-%d'), (0 if dt.isoweekday() in (6, 7) else 1, NA))[1],
        'day_of_year': dt.timetuple().tm_yday,
        'week_of_month': pendulum.instance(dt).day // 7 + 1,
        'week_of_year': pendulum.instance(dt).week_of_year,
        'week_of_year_iso': dt.isocalendar()[1],
        'month': dt.month,
        'month_name_en': dt.strftime("%B"),
        'month_name_ru': MONTH_NAMES['ru'][dt.month],
        'month_name_for_rep_ru': pendulum.instance(dt).format('MMMM', locale='ru').capitalize(),
        'quarter': pendulum.instance(dt).quarter,
        'quarter_name_en': QUARTERS_NAMES['en'][pendulum.instance(dt).quarter],
        'quarter_name_ru': QUARTERS_NAMES['ru'][pendulum.instance(dt).quarter],
        'year': dt.year,
        'mmyyyy': dt.strftime('%m%Y'),
        'ddmmyyyy': dt.strftime('%d%m%Y'),
        'first_day_of_week': pendulum.instance(dt).start_of('week').strftime('%Y-%m-%d'),
        'last_day_of_week': pendulum.instance(dt).end_of('week').strftime('%Y-%m-%d'),
        'first_day_of_month': pendulum.instance(dt).start_of('month').strftime('%Y-%m-%d'),
        'last_day_of_month': pendulum.instance(dt).end_of('month').strftime('%Y-%m-%d'),
        'first_day_of_quarter': pendulum.instance(dt).first_of('quarter').strftime('%Y-%m-%d'),
        'last_day_of_quarter': pendulum.instance(dt).last_of('quarter').strftime('%Y-%m-%d'),
        'first_day_of_year': pendulum.instance(dt).start_of('year').strftime('%Y-%m-%d'),
        'last_day_of_year': pendulum.instance(dt).end_of('year').strftime('%Y-%m-%d')
    }

    return row


def generate_dt():
    start = datetime.datetime.strptime(START_DATE, "%d-%m-%Y")
    end = datetime.datetime.strptime(END_DATE, "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    calend_ru, calend_en = get_calendar()
    for dt in date_generated:
        yield generate_row(dt, calend_ru, calend_en)


def parse_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    year, lang = root.attrib['year'], root.attrib['lang']

    res = {}

    holidays = {'0': 'n/a'}
    for holiday in root.iter('holiday'):
        holidays[holiday.attrib['id']] = holiday.attrib['title']

    for day in root.iter('day'):
        dt = datetime.datetime.strptime(f'{year}.{day.attrib["d"]}', '%Y.%m.%d').strftime('%Y-%m-%d')
        is_workday = 0 if day.attrib["t"] == '1' else 1
        holiday_name = holidays[day.attrib.get('h', '0')]
        res[dt] = (is_workday, holiday_name)

    return res


def get_calendar():
    calend_ru = {}
    calend_en = {}
    for f in glob.glob('xmlcalendar/**/calendar.xml', recursive=True):
        calend_ru.update(parse_xml(f))

    for f in glob.glob('xmlcalendar/**/calendar.en.xml', recursive=True):
        calend_en.update(parse_xml(f))

    return calend_ru, calend_en


def generate_sql():
    with open('datedm.csv', 'w', newline='') as csvfile:
        fn = next(generate_dt())
        fieldnames = fn.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in generate_dt():
            writer.writerow(row)


if __name__ == '__main__':
    generate_sql()
