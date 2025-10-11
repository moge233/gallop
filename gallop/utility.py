#! python3


from datetime import date, datetime
import os

from pandas import DataFrame, concat
from scipy.stats import norm

from chart_parser.chart import Chart
from chart_parser.horse import Horse
from chart_parser.race import Race
from chart_parser.utils import parse_chart


#######################################################################
# regular ol' utils for us to use
#######################################################################
def get_time_of_beaten_length(distance: float, time: float) -> float:
    return round(1.0 / (distance * 660 / time / 10.0), 2)


def summarize_post_positions(charts: list[Chart]) -> None:
    chart_dfs: list[DataFrame] = []
    for chart in charts:
        for race in chart.races:
            for horse in race.horses:
                horse_df = horse_to_dataframe(horse)
                if horse.is_winner():
                    horse_df['winner'] = 1
                else:
                    horse_df['winner'] = 0
                chart_dfs.append(horse_df)
    track_df: DataFrame = concat(chart_dfs, axis=0, ignore_index=True)
    track_df = track_df[track_df['odds'] != 0.0]
    track_df['odds'] = track_df['odds'] / 100.0
    track_df['fair_odds'] = track_df['odds'] * (1 - 0.2)    # 20% takeout?
    track_df['public_expected_wins'] = 1 / (1 + track_df['fair_odds'])
    track_df['public_variance'] = track_df['public_expected_wins'] * (1 - track_df['public_expected_wins'])
    post_positions = set(track_df['post_position'].to_list())
    for post_position in post_positions:
        pp_df = track_df[track_df['post_position'] == post_position]
        pp_winner_df = pp_df[pp_df['winner'] == 1]
        expected_wins = sum(pp_df['public_expected_wins'])
        variance = sum(pp_df['public_variance'])
        actual_wins = sum(pp_winner_df['winner'])
        print(
            post_position,
            round(expected_wins, 2),
            actual_wins,
            round(variance, 2),
            round(norm.cdf(actual_wins, loc=expected_wins, scale=variance), 2)
        )


#######################################################################
# chart_parser utils
#######################################################################
def get_chart_date(chart_path: str, track_code: str) -> date:
    '''
    YYYYmmdd
    '''
    chart_date = chart_path[len(track_code):].rstrip('.chart')
    return datetime.strptime(chart_date, '%Y%m%d').date()


def get_charts(path: str, track_code: str) -> list[Chart]:
    charts: list[Chart] = []
    for dir in os.listdir(path):
        dir_path = os.path.join(path, dir)
        for chart in os.listdir(dir_path):
            if chart[:len(track_code)] == track_code and \
                    chart[len(track_code)].isdigit():
                chart_path = os.path.join(dir_path, chart)
                charts.append(parse_chart(chart_path))
    return charts


def horse_to_dataframe(horse: Horse) -> DataFrame:
    return DataFrame([dict(vars(horse).items())])


def race_to_dataframe(race: Race, skip_horses: bool = False) -> DataFrame:
    if skip_horses:
        filtered_dict = {k: v for k, v in vars(race).items() if v != 'horses'}
    else:
        filtered_dict = dict(vars(race).items())
    return DataFrame([filtered_dict])


def chart_to_dataframe(chart: Chart, skip_races: bool) -> DataFrame:
    if skip_races:
        filtered_dict = {k: v for k, v in vars(chart).items() if v != 'races'}
    else:
        filtered_dict = dict(vars(chart).items())
    return DataFrame([filtered_dict])
