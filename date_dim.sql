create table date_dim
(
    date_dim_id           integer            not null
        primary key,
    dt                    date               not null,
    epoch                 integer            not null
        constraint date_dim_epoch_check
            check (epoch >= 1451606400),
    day                   smallint           not null
        constraint date_dim_day_check
            check ((day >= 1) AND (day <= 31)),
    weekday               smallint           not null
        constraint date_dim_weekday_check
            check ((weekday >= 0) AND (weekday <= 6)),
    weekday_iso           smallint           not null
        constraint date_dim_weekday_iso_check
            check ((weekday_iso >= 1) AND (weekday_iso <= 7)),
    weekday_name_en       varchar            not null
        constraint date_dim_weekday_name_en_check
            check ((weekday_name_en)::text = ANY
                   ((ARRAY ['Friday'::character varying, 'Sunday'::character varying, 'Saturday'::character varying, 'Tuesday'::character varying, 'Thursday'::character varying, 'Monday'::character varying, 'Wednesday'::character varying])::text[])),
    weekday_name_ru       varchar            not null
        constraint date_dim_weekday_name_ru_check
            check ((weekday_name_ru)::text = ANY
                   ((ARRAY ['Суббота'::character varying, 'Вторник'::character varying, 'Понедельник'::character varying, 'Четверг'::character varying, 'Пятница'::character varying, 'Среда'::character varying, 'Воскресенье'::character varying])::text[])),
    is_weekend            smallint           not null
        constraint date_dim_is_weekend_check
            check (is_weekend = ANY (ARRAY [0, 1])),
    is_holiday            smallint           not null
        constraint date_dim_is_holiday_check
            check (is_holiday = ANY (ARRAY [0, 1])),
    holiday_name_en       varchar            not null,
    holiday_name_ru       varchar            not null,
    day_of_year           smallint           not null
        constraint date_dim_day_of_year_check
            check ((day_of_year >= 1) AND (day_of_year <= 366)),
    week_of_month         smallint           not null
        constraint date_dim_week_of_month_check
            check ((week_of_month >= 1) AND (week_of_month <= 5)),
    week_of_year          smallint           not null
        constraint date_dim_week_of_year_check
            check ((week_of_year >= 1) AND (week_of_year <= 53)),
    week_of_year_iso      smallint           not null
        constraint date_dim_week_of_year_iso_check
            check ((week_of_year_iso >= 1) AND (week_of_year_iso <= 53)),
    month                 smallint           not null
        constraint date_dim_month_check
            check ((month >= 1) AND (month <= 12)),
    month_name_en         varchar            not null
        constraint date_dim_month_name_en_check
            check ((month_name_en)::text = ANY
                   ((ARRAY ['October'::character varying, 'November'::character varying, 'December'::character varying, 'January'::character varying, 'May'::character varying, 'April'::character varying, 'July'::character varying, 'March'::character varying, 'August'::character varying, 'February'::character varying, 'June'::character varying, 'September'::character varying])::text[])),
    month_name_ru         varchar            not null
        constraint date_dim_month_name_ru_check
            check ((month_name_ru)::text = ANY
                   ((ARRAY ['Май'::character varying, 'Август'::character varying, 'Март'::character varying, 'Декабрь'::character varying, 'Январь'::character varying, 'Июнь'::character varying, 'Октябрь'::character varying, 'Июль'::character varying, 'Апрель'::character varying, 'Сентябрь'::character varying, 'Февраль'::character varying, 'Ноябрь'::character varying])::text[])),
    month_name_for_rep_ru varchar            not null
        constraint date_dim_month_name_for_rep_ru_check
            check ((month_name_for_rep_ru)::text = ANY
                   ((ARRAY ['Апреля'::character varying, 'Октября'::character varying, 'Мая'::character varying, 'Июня'::character varying, 'Ноября'::character varying, 'Марта'::character varying, 'Августа'::character varying, 'Февраля'::character varying, 'Июля'::character varying, 'Января'::character varying, 'Сентября'::character varying, 'Декабря'::character varying])::text[])),
    quarter               smallint           not null
        constraint date_dim_quarter_check
            check ((quarter >= 1) AND (quarter <= 4)),
    quarter_name_en       varchar            not null
        constraint date_dim_quarter_name_en_check
            check ((quarter_name_en)::text = ANY
                   ((ARRAY ['Third'::character varying, 'Fourth'::character varying, 'First'::character varying, 'Second'::character varying])::text[])),
    quarter_name_ru       varchar            not null
        constraint date_dim_quarter_name_ru_check
            check ((quarter_name_ru)::text = ANY
                   ((ARRAY ['Третий'::character varying, 'Четвертый'::character varying, 'Второй'::character varying, 'Первый'::character varying])::text[])),
    year                  smallint           not null
        constraint date_dim_year_check
            check ((year >= 2016) AND (year <= 9999)),
    mmyyyy                varchar(6)         not null,
    ddmmyyyy              varchar(8)         not null,
    first_day_of_week     date               not null,
    last_day_of_week      date               not null,
    first_day_of_month    date               not null,
    last_day_of_month     date               not null,
    first_day_of_quarter  date               not null,
    last_day_of_quarter   date               not null,
    first_day_of_year     date               not null,
    last_day_of_year      date               not null,
    is_working_day        smallint           not null
        constraint date_dim_is_working_day_check
            check (is_working_day = ANY (ARRAY [0, 1])),
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