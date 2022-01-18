from group import Group, GroupSet, get_agg_func, check_data
from group_by import RangeGroupBy, ValueGroupBy
from lang import lang

def _filter_activity_type(data_row, keyword):
    return data_row[lang.data__activity_type].find(keyword) >= 0

def _filter_running_func(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_running)

def _filter_swimming_func(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_swimming)

def _filter_cycling_func(data_row):
    return _filter_activity_type(data_row, lang.data__keyword_cycling)

def _range_group_set(title, column, group_by, filter_func=None):
    agg_func = get_agg_func("count")
    group_set = GroupSet(title, column, group_by, agg_func, filter_func)
    group_set.set_ytitle(lang.activity_times)
    return group_set

@check_data('run_times')
def _run_pace_group_set():
    title = lang.average_run_pace
    col = lang.data__avg_pace

    def value_func(val): return val.tm_min

    group_by = RangeGroupBy(4, 9, 1, '%s:00').set_value_func(value_func)

    return _range_group_set(title, col, group_by, 
        _filter_running_func).set_xtitle(lang.run_pace_unit)

@check_data('run_times')
def _run_cadence_group_set():
    title = lang.average_run_cadence
    col = lang.data__avg_run_cadence

    group_by = RangeGroupBy(160, 200, 10)

    return _range_group_set(title, col, group_by, 
        _filter_running_func).set_xtitle(lang.steps_per_min)

@check_data('run_times')
def _run_stride_group_set():
    title = lang.average_stride_length
    col = lang.data__avg_stride_length

    series = [0.7, 0.8, 0.9, 1.0, 1.1]
    group_by = RangeGroupBy(0.7, 1.2, 0.1, '%2.1f', series)

    return _range_group_set(title, col, group_by, 
        _filter_running_func).set_xtitle(lang.m)

@check_data('data_rows_count')
def _activity_hour_group_set():
    title = lang.activity_hours
    col = lang.data__date

    def value_func(val): return val.tm_hour

    group_by = ValueGroupBy(range(0, 24), '%s' + lang.activity_h).set_value_func(value_func)

    return _range_group_set(title, col, group_by, None)


@check_data('data_rows_count')
def _activity_weekday_group_set():
    title = lang.activity_weekdays
    col = lang.data__date
    weekDays = lang.days_of_week
    series = map(lambda w: weekDays[w], range(0, 7))

    def value_func(val): return val.tm_wday  # Monday is 0, just OK

    group_by = ValueGroupBy(series).set_value_func(value_func)

    return _range_group_set(title, col, group_by)

@check_data('data_rows_count')
def _activity_month_group_set():
    title = lang.activity_months
    col = lang.data__date
    months = lang.months
    series = map(lambda m: months[m-1], range(1, 13))

    def value_func(val): return val.tm_mon - 1 # month starts 1

    return _range_group_set(title, col, ValueGroupBy(series).set_value_func(value_func))


@check_data('run_times')
def _run_distance_group_set():
    title = lang.running_distance
    col = lang.data__distance
    
    return _range_group_set(title, col, RangeGroupBy(5, 100, 5), 
        _filter_running_func).set_xtitle(lang.km)

@check_data('swim_times')
def _swimming_distance_group_set():
    title = lang.swimming_distance
    col = lang.data__distance

    return _range_group_set(title, col, RangeGroupBy(500, 5000, 500), 
        _filter_swimming_func).set_xtitle(lang.m)

@check_data('cycle_times')
def _cycling_distance_group_set():
    title = lang.cycling_distance
    col = lang.data__distance

    return _range_group_set(title, col, RangeGroupBy(20, 100, 20), 
        _filter_cycling_func).set_xtitle(lang.km)

@check_data('data_rows_count')
def _activity_time_group_set():
    title = lang.activity_time
    col = lang.data__time

    return _range_group_set(title, col, RangeGroupBy(30, 180, 30)).set_xtitle(lang.min_full)

def get_range_group_sets():
    return [
        _activity_time_group_set(),
        _activity_month_group_set(),
        _activity_weekday_group_set(),
        _activity_hour_group_set(),
        _run_distance_group_set(),
        _run_pace_group_set(),
        _run_cadence_group_set(),
        _run_stride_group_set(),
        _swimming_distance_group_set(),
        _cycling_distance_group_set()
    ]
