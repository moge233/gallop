#! python3


from fractions import Fraction
from pandas import DataFrame, concat

# from chart_parser.chart import Chart
from chart_parser.race import Race

from gallop.utility import get_time_of_beaten_length, horse_to_dataframe


def get_speed_table(race: Race, date: str) -> DataFrame:
    horse_dfs: list[DataFrame] = []
    time_of_beaten_length = get_time_of_beaten_length(race.distance, race.final)
    for horse in race.horses:
        if not horse:
            continue
        if horse.odds and horse.odds < 100:
            f = Fraction(horse.odds / 100.0)
            print(horse.odds / 100, f.denominator / (f.denominator + f.numerator))
        horse_df = horse_to_dataframe(horse)
        horse_df.insert(0, 'datekey', f'{date}{race.number:02d}')
        horse_df.insert(2, 'class', race.class_codes)
        horse_df.insert(3, 'sex_restriction', race.sex_restriction)
        horse_df.insert(4, 'age_restriction', race.age_restriction)
        horse_df.insert(5, 'distance', race.distance)
        horse_df.insert(6, 'surface', race.course_type.name)
        horse_df.insert(7, 'track_condition', race.track_condition)
        horse_df.insert(41, 'final_time', round(time_of_beaten_length * horse.blf + race.final, 2))
        horse_df.insert(42, 'winner', horse.is_winner())
        horse_df = horse_df[['datekey', 'class', 'sex_restriction', 'age_restriction', 'distance', 'surface',
                             'track_condition', 'final_time', 'finish', 'winner']]
        horse_dfs.append(horse_df)
    return concat(horse_dfs, axis=0, ignore_index=True)


# def get_speed_table(chart: Chart) -> DataFrame:
#     if not chart.header:
#         raise ValueError
#     race_dfs: list[DataFrame] = []
#     for race in chart.races:
#         if not race or not race.horses:
#             continue
#         horse_dfs: list[DataFrame] = []
#         time_of_beaten_length = get_time_of_beaten_length(race.distance, race.final)
#         for horse in race.horses:
#             if not horse:
#                 continue
#             horse_df = horse_to_dataframe(horse)
#             horse_df.insert(0, 'datekey', f'{chart.header.race_date.strftime('%Y%m%d')}{race.number:02d}')
#             horse_df.insert(2, 'class', race.class_codes)
#             horse_df.insert(3, 'sex_restriction', race.sex_restriction)
#             horse_df.insert(4, 'age_restriction', race.age_restriction)
#             horse_df.insert(5, 'distance', race.distance)
#             horse_df.insert(6, 'surface', race.course_type.name)
#             horse_df.insert(7, 'track_condition', race.track_condition)
#             horse_df.insert(41, 'final_time', round(time_of_beaten_length * horse.blf + race.final, 2))
#             horse_df.insert(42, 'winner', horse.is_winner())
#             horse_dfs.append(horse_df)
#         race_dfs.append(concat(horse_dfs, axis=0, ignore_index=True))
#     return concat(race_dfs, axis=0, ignore_index=True)
