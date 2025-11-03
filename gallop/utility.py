#! python3


import csv
#  from datetime import date, datetime
import os
import re

#  from pandas import DataFrame, concat, to_numeric
#  from numpy import nan
#  from scipy.stats import norm

from brispy.singlefile import SingleFile  # SingleFileHorse, SingleFilePastPerformance, SingleFileRace, SingleFileRow
from pydrf.textchart import Header, RaceData, StarterPerformanceData, RecordType
#  from gallop.pacecontainer import PaceContainerPastPerformance


DEFAULT_PP_DATA_DIR: str = 'C:\\Users\\mathe\\OneDrive\\Documents\\horses\\pp_data\\2025'


#######################################################################
# regular ol' utils for us to use
#######################################################################
# def get_time_of_beaten_length(distance: float, time: float) -> float:
#     return round(1.0 / (distance * 660 / time / 10.0), 2)
#
#
# def summarize_post_positions(charts: list[Chart]) -> None:
#     chart_dfs: list[DataFrame] = []
#     for chart in charts:
#         for race in chart.races:
#             if race.course_type != Course.DIRT:
#                 wait = 1
#             for horse in race.horses:
#                 horse_df = horse_to_dataframe(horse)
#                 if horse.is_winner():
#                     horse_df['winner'] = 1
#                 else:
#                     horse_df['winner'] = 0
#                 chart_dfs.append(horse_df)
#     track_df: DataFrame = concat(chart_dfs, axis=0, ignore_index=True)
#     track_df = track_df[track_df['odds'] != 0.0]
#     track_df['odds'] = track_df['odds'] / 100.0
#     track_df['fair_odds'] = track_df['odds'] * (1 - 0.2)    # 20% takeout?
#     track_df['public_expected_wins'] = 1 / (1 + track_df['fair_odds'])
#     track_df['public_variance'] = track_df['public_expected_wins'] * (1 - track_df['public_expected_wins'])
#     post_positions = set(track_df['post_position'].to_list())
#     for post_position in post_positions:
#         pp_df = track_df[track_df['post_position'] == post_position]
#         pp_winner_df = pp_df[pp_df['winner'] == 1]
#         expected_wins = sum(pp_df['public_expected_wins'])
#         variance = sum(pp_df['public_variance'])
#         actual_wins = sum(pp_winner_df['winner'])
#         print(
#             post_position,
#             round(expected_wins, 2),
#             actual_wins,
#             round(variance, 2),
#             round(float(norm.cdf(actual_wins, loc=expected_wins, scale=variance)), 2)
#         )


#######################################################################
# chart_parser utils
#######################################################################
#  def get_chart_date(chart_path: str, track_code: str) -> date:
#      '''
#      YYYYmmdd
#      '''
#      chart_date = chart_path[len(track_code):].rstrip('.chart')
#      return datetime.strptime(chart_date, '%Y%m%d').date()
#
#
#  def get_charts(path: str, track_code: str) -> list[Chart]:
#      charts: list[Chart] = []
#      for dir in os.listdir(path):
#          dir_path = os.path.join(path, dir)
#          for chart in os.listdir(dir_path):
#              if chart[:len(track_code)] == track_code and \
#                      chart[len(track_code)].isdigit():
#                  chart_path = os.path.join(dir_path, chart)
#                  charts.append(parse_chart(chart_path))
#      return charts
#
#
#  def horse_to_dataframe(horse: Horse) -> DataFrame:
#      return DataFrame([dict(vars(horse).items())])
#
#
#  def race_to_dataframe(race: Race, skip_horses: bool = False) -> DataFrame:
#      if skip_horses:
#          filtered_dict = {k: v for k, v in vars(race).items() if v != 'horses'}
#      else:
#          filtered_dict = dict(vars(race).items())
#      return DataFrame([filtered_dict])
#
#
#  def chart_to_dataframe(chart: Chart, skip_races: bool) -> DataFrame:
#      if skip_races:
#          filtered_dict = {k: v for k, v in vars(chart).items() if v != 'races'}
#      else:
#          filtered_dict = dict(vars(chart).items())
#      return DataFrame([filtered_dict])
#
#
#  def check_if_pp_exists(track_code: str, race_date: date) -> bool:
#      if len(track_code) == 2:
#          track_code += 'X'
#      file_name = f'{track_code}{race_date.strftime('%m%d')}.drf'
#      if os.path.exists(os.path.join(DEFAULT_PP_DATA_DIR, file_name)):
#          return True
#      return False
#
#
#  def get_pp_path(track_code: str, race_date: date) -> str:
#      if len(track_code) == 2:
#          track_code += 'X'
#      file_name = f'{track_code}{race_date.strftime('%m%d')}.drf'
#      return os.path.join(DEFAULT_PP_DATA_DIR, file_name)


#######################################################################
# SingleFile(...) utils
#######################################################################
#  def is_maiden(race: SingleFileRace) -> bool:
#      if 'Md' in race.classification:
#          return True
#      return False
#
#
#  def remove_todays_scratches(single_file: SingleFile, todays_scratches: list[str] |
#  None = None) -> list[SingleFileRow]:
#      if not todays_scratches:
#          return single_file.rows
#      else:
#          todays_scratches = [scratch.casefold() for scratch in todays_scratches]
#      for row in single_file.rows:
#          if row.horse.name.casefold() in todays_scratches:
#              print(f'Removing a scratch: {row.horse.name}')
#      return [row for row in single_file.rows if row.horse.name.casefold() not in todays_scratches]
#
#
#  def singlefile_past_performance_to_dataframe(sfpp: SingleFilePastPerformance) -> DataFrame:
#      return DataFrame([dict(vars(sfpp).items())])
#
#
#  def singlefile_past_performance_to_pace_container_past_performance(sfpp: SingleFilePastPerformance) -> DataFrame:
#      return DataFrame([dict(vars(PaceContainerPastPerformance(sfpp)).items())])
#
#
#  def create_dataframe_from_singlefile(single_file: SingleFile, skip_maidens=False) -> list[DataFrame | None]:
#      return []
#
#
#  def get_combined_dataframe_from_singlefile_horse_past_performances(horse: SingleFileHorse) -> DataFrame | None:
#      pp_dfs: list[DataFrame | None] = []
#      for pp in horse.past_performances:
#          if not pp.date or pp.distance / 220 > 12 or int(pp.date[:4]) < 2025:
#              continue
#          if not horse.program_number:
#              continue
#          pp_df = singlefile_past_performance_to_dataframe(pp)
#          pc_df = singlefile_past_performance_to_pace_container_past_performance(pp)
#          combined_df = concat([pp_df, pc_df], axis=1, ignore_index=False)
#          combined_df.insert(0, 'horseid', int(horse.program_number))
#          combined_df.insert(0, 'name', horse.name)
#          pp_dfs.append(combined_df)
#      if pp_dfs != []:
#          pp_df = concat(pp_dfs, axis=0, ignore_index=True)
#      else:
#          pp_df = None
#      return pp_df
#
#
#  def singlefile_to_combined_dataframe(sf: SingleFile) -> DataFrame | None:
#      current_race_number: int = 0
#      todays_dfs: list[DataFrame | None] = []
#      race_dfs: list[DataFrame | None] = []
#      race_df: DataFrame | None = None
#      for row in sf.rows:
#          if is_maiden(row.race):
#              continue
#          if current_race_number != row.race.number:
#              if race_dfs:
#                  race_df = concat(race_dfs, axis=0, ignore_index=True)
#                  race_df.insert(0, 'todays_race_number', current_race_number)
#                  todays_dfs.append(race_df)
#              current_race_number = row.race.number
#              race_dfs: list[DataFrame | None] = []
#          if row.horse:
#              horse_df = get_combined_dataframe_from_singlefile_horse_past_performances(row.horse)
#              if horse_df is None:
#                  continue
#              horse_df.insert(2, "horseno", row.horse.program_number)
#              if row.trainer.current_year_starts:
#                  horse_df['trainer_win_pct'] = row.trainer.current_year_wins / row.trainer.current_year_starts
#              else:
#                  horse_df['trainer_win_pct'] = 0
#              if row.jockey.current_year_starts:
#                  horse_df['jockey_win_pct'] = row.jockey.current_year_wins / row.jockey.current_year_starts
#              else:
#                  horse_df['jockey_win_pct'] = 0
#              horse_df['todays_distance'] = abs(row.race.distance) / 220
#              horse_df['todays_surface'] = row.race.surface
#              horse_df['todays_all_weather_flag'] = row.race.todays_all_weather_surface_flag
#              race_dfs.append(horse_df)
#      if race_dfs:
#          # We need to do all this here to get the final race of the list
#          race_df = concat(race_dfs, axis=0, ignore_index=True)
#          race_df.insert(0, 'todays_race_number', current_race_number)
#          todays_dfs.append(race_df)
#      if todays_dfs:
#          # Create the day's dataframe with the PaceContainer entries added on the end
#          day_df = concat(todays_dfs, axis=0, ignore_index=True)
#          return day_df
#      else:
#          return None
#
#
#  def get_all_pace_data(charts_path: str, track_code: str) -> DataFrame | None:
#      charts: list[Chart] = get_charts(charts_path, track_code)
#      charts_dfs: list[DataFrame] = []
#      charts_df: DataFrame | None = None
#      # Now that we have the charts, we need to look and see if we have the DRF (SingleFile) data file
#      # for that day
#      for chart in charts:
#          chart_dfs: list[DataFrame] = []
#          if chart.header:
#              if check_if_pp_exists(track_code, chart.header.race_date):
#                  # Now that we have a chart that has a corresponding data file, we need to get the SingleFile
#                  # instance of the data file and then get the combined dataframe.
#                  singlefile: SingleFile = SingleFile.create(get_pp_path(track_code, chart.header.race_date))
#                  data_frame = singlefile_to_combined_dataframe(singlefile)
#                  for race in chart.races:
#                      if 'Md' in race.abbreviated_race_name or data_frame is None:
#                          # Skip maidens
#                          continue
#                      else:
#                          # It's a race we care about, find the ponies involved
#                          winner_name = race.get_winner().name
#                          race_df = data_frame[data_frame['todays_race_number'] == race.number]
#                          if not race_df.empty:
#                              race_df.insert(0, 'todays_winner', race_df['name'] == winner_name.upper())
#                              race_df.insert(0, 'key',
#                                             int(f'{chart.header.race_date.strftime('%Y%m%d')}{race.number:02}'))
#                              race_df = race_df.copy(True)
#                              race_df['todays_winner'] = race_df['todays_winner'].astype(int)
#                              # TODO: Filter out different surfaces and/or distances
#                              race_df = race_df[race_df['todays_distance'] > 7.5]  # Routes only
#                              # race_df = race_df[race_df['todays_distance'] > 5]  #
#                              race_df = race_df[race_df['todays_surface'] == 'D']
#                              race_df = race_df[race_df['todays_all_weather_flag'] == 'A']
#                              race_df = race_df.drop_duplicates(subset=['name'], keep='first')
#                              race_df = race_df.apply(to_numeric, errors='coerce').fillna(race_df)
#                              race_df = race_df.dropna()
#                              if race_df.shape[0] > 4 and 1 in race_df['todays_winner'].values:
#                                  race_df['rank_f1'] = race_df['f1'].rank(method='average', ascending=False)
#                                  race_df['rank_f2'] = race_df['f2'].rank(method='average', ascending=False)
#                                  race_df['rank_f3'] = race_df['f3'].rank(method='average', ascending=False)
#                                  race_df['rank_ep'] = race_df['ep'].rank(method='average', ascending=False)
#                                  race_df['rank_sp'] = race_df['sp'].rank(method='average', ascending=False)
#                                  race_df['rank_ap'] = race_df['ap'].rank(method='average', ascending=False)
#                                  race_df['rank_fx'] = race_df['fx'].rank(method='average', ascending=False)
#                                  if 1 in race_df['todays_winner'].values and \
#                                          '' not in race_df['second_call_position'].values:
#                                      chart_dfs.append(race_df)
#                                  else:
#                                      wait = 1
#          if chart_dfs:
#              chart_df = concat(chart_dfs, axis=0, ignore_index=True)
#              charts_dfs.append(chart_df)
#      if charts_dfs:
#          charts_df = concat(charts_dfs, axis=0, ignore_index=True)
#          return charts_df
#      return None
#
#
#  def filter_all_pace_data(dataframe: DataFrame) -> DataFrame:
#      ret = dataframe.copy()
#      ret = ret[ret['distance'] < 8]
#      ret = ret[ret['course'] == Course.DIRT]
#      return ret


#######################################################################
# pydrf.textchart(...) utils
#######################################################################
class Chart:
    def __init__(self, header: Header, race_data: list[RaceData],
                 starters: list[StarterPerformanceData]):
        self.header: Header = header
        self.race_data: list[RaceData] = race_data
        self.starters_performance_data: list[StarterPerformanceData] = starters

    def __str__(self):
        ret = ''
        for k, v in vars(self).items():
            ret += f'{k}={v}, '
        return f'Chart({ret[:-2]})'

    def __repr__(self):
        ret = ''
        for k, v in vars(self).items():
            ret += f'{k}={v}, '
        return f'Chart({ret[:-2]})'


def parse_chart(path: str) -> Chart | None:
    header: Header | None = None
    race_data: list[RaceData] = []
    starters_performance_data: list[StarterPerformanceData] = []
    try:
        with open(path) as chart_file:
            reader = csv.reader(chart_file.readlines())
            for line in reader:
                if line[0] == RecordType.HEADER:
                    header = Header.create(line)
                elif line[0] == RecordType.RACE:
                    race_data.append(RaceData.create(line))
                elif line[0] == RecordType.STARTER:
                    starters_performance_data.append(StarterPerformanceData.create(line))
                elif line[0] == RecordType.EXOTIC_WAGERING:
                    pass
                elif line[0] == RecordType.ATTENDANCE:
                    pass
                elif line[0] == RecordType.COMMENT:
                    pass
                elif line[0] == RecordType.FOOTNOTE:
                    pass
        if header and race_data and starters_performance_data:
            return Chart(
                header,
                race_data,
                starters_performance_data
            )
        return None
    except FileNotFoundError as e:
        print(f'[{e}]: could not find file {path}')
        return None


def get_charts(path: str) -> list[Chart | None]:
    charts: list[Chart | None] = []
    for dir in os.listdir(path):
        dir_path = os.path.join(path, dir)
        for chart in os.listdir(dir_path):
            chart_path = os.path.join(dir_path, chart)
            charts.append(parse_chart(chart_path))
    return charts


def chart_to_data_dict(chart: Chart, data_dir: str, track_code: str):
    '''
    Get the Brisnet SingleFile data files (as a dict) associated with the chart's date.

    :param chart: The chart to get Brisnet PP's for
    :type chart: Chart
    :param data_dir: The directory to search for the Brisnet SingleFile data files
    :type data_dir: str
    :param track_code: The DRF result chart track code
    :type track_code: str
    '''
    singlefiles_available = os.listdir(data_dir)
    singlefile_track_code = track_code + 'X' if len(track_code) == 2 else track_code
    chart_dict = {}
    singlefile_name = f'{singlefile_track_code}{chart.header.race_date[4:]}.DRF'
    if singlefile_name in singlefiles_available:
        singlefile_path = os.path.join(data_dir, singlefile_name)
        sf: SingleFile = SingleFile.create(singlefile_path)
        for row in sf.rows:
            key = f'Race {row.race.number}'
            if key not in chart_dict.keys():
                chart_dict[key] = {}
            if row.horse.name not in chart_dict[key].keys():
                chart_dict[key][row.horse.name] = {}
            row_horse_dict = dict(vars(row.horse))
            del row_horse_dict['name']
            del row_horse_dict['stats']
            del row_horse_dict['workouts']
            del row_horse_dict['past_performances']
            chart_dict[key][row.horse.name]['datekey'] = f'{row.race.date}{row.race.number:02d}'
            chart_dict[key][row.horse.name]['winner'] = 0
            chart_dict[key][row.horse.name]['race_type'] = row.race.race_type
            chart_dict[key][row.horse.name]['classification'] = row.race.classification
            chart_dict[key][row.horse.name]['claiming_price'] = row.race.claiming_price
            chart_dict[key][row.horse.name]['surface'] = row.race.surface
            chart_dict[key][row.horse.name]['all_weather_flag'] = row.race.todays_all_weather_surface_flag
            chart_dict[key][row.horse.name]['distance'] = round(abs(row.race.distance / 220), 2)
            for performance in chart.starters_performance_data:
                horse_name = re.sub(r'\([^()]*\)', '', performance.horse_name).rstrip().casefold()
                if row.race.number == performance.race_number and \
                        horse_name == row.horse.name.casefold():
                    if performance.program_number == 'SCR':
                        chart_dict[key][row.horse.name]['scratch'] = 1
                    else:
                        chart_dict[key][row.horse.name]['scratch'] = 0
                    chart_dict[key][row.horse.name]['post_position'] = performance.post_position
                    if performance.original_finish == 1:
                        chart_dict[key][row.horse.name]['winner'] = 1
            for k, v in row_horse_dict.items():
                if k not in chart_dict[key][row.horse.name].keys():
                    chart_dict[key][row.horse.name][f'horse_{k}'] = v
            row_jockey_dict = dict(vars(row.jockey))
            for k, v in row_jockey_dict.items():
                if k not in chart_dict[key][row.horse.name].keys():
                    chart_dict[key][row.horse.name][f'jockey_{k}'] = v
            row_trainer_dict = dict(vars(row.trainer))
            for k, v in row_trainer_dict.items():
                if k not in chart_dict[key][row.horse.name].keys():
                    chart_dict[key][row.horse.name][f'trainer_{k}'] = v
            row_trainer_jockey_combo_dict = dict(vars(row.trainer_jockey_combo))
            for k, v in row_trainer_jockey_combo_dict.items():
                if k not in chart_dict[key][row.horse.name].keys():
                    chart_dict[key][row.horse.name][f'trainer_jockey_combo_{k}'] = v
            row_owner_dict = dict(vars(row.owner))
            for k, v in row_owner_dict.items():
                if k not in chart_dict[key][row.horse.name].keys():
                    chart_dict[key][row.horse.name][f'owner_{k}'] = v
            for i, pp in enumerate(row.horse.past_performances[:4]):
                chart_dict[key][row.horse.name][f'past_performances{i + 1}'] = pp
    return chart_dict


def data_dict_to_rows(data_dict: dict):
    rows = []
    for race, race_dict in data_dict.items():
        for horse, horse_dict in race_dict.items():
            horse_pp_dict = {
                'race': race,
                'horse_name': horse,
            }
            for key, item in horse_dict.items():
                if 'past_performances' in key:
                    for k, v in dict(vars(item)).items():
                        new_key = f'pps_{k}_{key[-1]}'
                        horse_pp_dict[new_key] = v
                else:
                    horse_pp_dict[key] = item
            rows.append(horse_pp_dict)
    return rows


def clean_row(row: dict):
    ret = row
    del ret['trainer_key_stats']
    return ret


def calculate_horse_fractional_time1_1(df_row):
    if df_row['pps_distance_1'] == '':
        return ''
    elif df_row['pps_distance_1'] >= 12 or df_row['pps_distance_1'] < 5.5:
        return ''
    elif df_row['pps_distance_1'] < 8:
        return df_row['pps_fr1_1'] + df_row['pps_first_call_beaten_lengths_1'] * 0.2
    else:
        return df_row['pps_fr2_1'] + df_row['pps_first_call_beaten_lengths_1'] * 0.2


def calculate_horse_fractional_time2_1(df_row):
    if df_row['pps_distance_1'] == '':
        return ''
    elif df_row['pps_distance_1'] >= 12 or df_row['pps_distance_1'] < 5.5:
        return ''
    elif df_row['pps_distance_1'] < 8:
        return df_row['pps_fr2_1'] + df_row['pps_second_call_beaten_lengths_1'] * 0.2
    else:
        return df_row['pps_fr3_1'] + df_row['pps_second_call_beaten_lengths_1'] * 0.2


def calculate_horse_final_time_1(df_row):
    if df_row['pps_distance_1'] == '':
        return ''
    elif df_row['pps_distance_1'] >= 12 or df_row['pps_distance_1'] < 5.5:
        return ''
    else:
        return df_row['pps_final_time_1'] + df_row['pps_finish_beaten_lengths_1'] * 0.2


def calculate_horse_fractional_time1_2(df_row):
    if df_row['pps_distance_2'] == '':
        return ''
    elif df_row['pps_distance_2'] >= 12 or df_row['pps_distance_2'] < 5.5:
        return ''
    elif df_row['pps_distance_2'] < 8:
        return df_row['pps_fr1_2'] + df_row['pps_first_call_beaten_lengths_2'] * 0.2
    else:
        return df_row['pps_fr2_2'] + df_row['pps_first_call_beaten_lengths_2'] * 0.2


def calculate_horse_fractional_time2_2(df_row):
    if df_row['pps_distance_2'] == '':
        return ''
    elif df_row['pps_distance_2'] >= 12 or df_row['pps_distance_2'] < 5.5:
        return ''
    elif df_row['pps_distance_2'] < 8:
        return df_row['pps_fr2_2'] + df_row['pps_second_call_beaten_lengths_2'] * 0.2
    else:
        return df_row['pps_fr3_2'] + df_row['pps_second_call_beaten_lengths_2'] * 0.2


def calculate_horse_final_time_2(df_row):
    if df_row['pps_distance_2'] == '':
        return ''
    elif df_row['pps_distance_2'] >= 12 or df_row['pps_distance_2'] < 5.5:
        return ''
    else:
        return df_row['pps_final_time_2'] + df_row['pps_finish_beaten_lengths_2'] * 0.2


def calculate_horse_fractional_time1_3(df_row):
    if df_row['pps_distance_3'] == '':
        return ''
    elif df_row['pps_distance_3'] >= 12 or df_row['pps_distance_3'] < 5.5:
        return ''
    elif df_row['pps_distance_3'] < 8:
        return df_row['pps_fr1_3'] + df_row['pps_first_call_beaten_lengths_3'] * 0.2
    else:
        return df_row['pps_fr2_3'] + df_row['pps_first_call_beaten_lengths_3'] * 0.2


def calculate_horse_fractional_time2_3(df_row):
    if df_row['pps_distance_3'] == '':
        return ''
    elif df_row['pps_distance_3'] >= 12 or df_row['pps_distance_3'] < 5.5:
        return ''
    elif df_row['pps_distance_3'] < 8:
        return df_row['pps_fr2_3'] + df_row['pps_second_call_beaten_lengths_3'] * 0.2
    else:
        return df_row['pps_fr3_3'] + df_row['pps_second_call_beaten_lengths_3'] * 0.2


def calculate_horse_final_time_3(df_row):
    if df_row['pps_distance_3'] == '':
        return ''
    elif df_row['pps_distance_3'] >= 12 or df_row['pps_distance_3'] < 5.5:
        return ''
    else:
        return df_row['pps_final_time_3'] + df_row['pps_finish_beaten_lengths_3'] * 0.2


def calculate_horse_fractional_time1_4(df_row):
    if df_row['pps_distance_4'] == '':
        return ''
    elif df_row['pps_distance_4'] >= 12 or df_row['pps_distance_4'] < 5.5:
        return ''
    elif df_row['pps_distance_4'] < 8:
        return df_row['pps_fr1_4'] + df_row['pps_first_call_beaten_lengths_4'] * 0.2
    else:
        return df_row['pps_fr2_4'] + df_row['pps_first_call_beaten_lengths_4'] * 0.2


def calculate_horse_fractional_time2_4(df_row):
    if df_row['pps_distance_4'] == '':
        return ''
    elif df_row['pps_distance_4'] >= 12 or df_row['pps_distance_4'] < 5.5:
        return ''
    elif df_row['pps_distance_4'] < 8:
        return df_row['pps_fr2_4'] + df_row['pps_second_call_beaten_lengths_4'] * 0.2
    else:
        return df_row['pps_fr3_4'] + df_row['pps_second_call_beaten_lengths_4'] * 0.2


def calculate_horse_final_time_4(df_row):
    if df_row['pps_distance_4'] == '':
        return ''
    elif df_row['pps_distance_4'] >= 12 or df_row['pps_distance_4'] < 5.5:
        return ''
    else:
        return df_row['pps_final_time_4'] + df_row['pps_finish_beaten_lengths_4'] * 0.2


def calculate_horse_fractional_fps1_1(df_row):
    if df_row['pps_distance_1'] == '' or df_row['pps_distance_1'] == 0:
        return 0
    elif df_row['pps_distance_1'] >= 12 or df_row['pps_distance_1'] < 5.5:
        return 0
    elif df_row['pps_distance_1'] < 8:
        d = 2
        fr1 = df_row['pps_fr1_1']
        bl1 = df_row['pps_first_call_beaten_lengths_1']
        if fr1 == 0:
            return 0
        return round((d * 660) / (fr1 + bl1 * 0.2), 2)
    else:
        if df_row['pps_fr2_1'] == 0:
            return 0
        d = 4
        fr2 = df_row['pps_fr2_1']
        bl2 = df_row['pps_first_call_beaten_lengths_1']
        if fr2 == 0:
            return 0
        return round((d * 660) / (fr2 + bl2 * 0.2), 2)


def calculate_horse_fractional_fps2_1(df_row):
    if df_row['pps_distance_1'] == '' or df_row['pps_distance_1'] == 0:
        return ''
    elif df_row['pps_distance_1'] >= 12 or df_row['pps_distance_1'] < 5.5:
        return ''
    elif df_row['pps_distance_1'] < 8:
        d = 2
        fr2 = df_row['pps_fr2_1']
        bl2 = df_row['pps_second_call_beaten_lengths_1']
        fr1 = df_row['pps_fr1_1']
        bl1 = df_row['pps_first_call_beaten_lengths_1']
        if fr1 == 0 or fr2 == 0:
            return 0
        return round((d * 660) / ((fr2 + bl2 * 0.2) - (fr1 + bl1 * 0.2)), 2)
    else:
        d = 2
        fr3 = df_row['pps_fr3_1']
        bl3 = df_row['pps_second_call_beaten_lengths_1']
        fr2 = df_row['pps_fr2_1']
        bl2 = df_row['pps_first_call_beaten_lengths_1']
        if fr2 == 0 or fr3 == 0:
            return 0
        return round((d * 660) / ((fr3 + bl3 * 0.2) - (fr2 + bl2 * 0.2)), 2)


def calculate_horse_fractional_fps3_1(df_row):
    if df_row['pps_distance_1'] == '' or df_row['pps_distance_1'] == 0:
        return ''
    elif df_row['pps_distance_1'] >= 12 or df_row['pps_distance_1'] < 5.5:
        return ''
    elif df_row['pps_distance_1'] < 8:
        d = df_row['pps_distance_1'] - 4
        fr3 = df_row['pps_final_time_1']
        bl3 = df_row['pps_finish_beaten_lengths_1']
        fr2 = df_row['pps_fr2_1']
        bl2 = df_row['pps_second_call_beaten_lengths_1']
        if fr2 == 0 or fr3 == 0:
            return 0
        return round((d * 660) / ((fr3 + bl3 * 0.2) - (fr2 + bl2 * 0.2)), 2)
    else:
        d = df_row['pps_distance_1'] - 6
        fr4 = df_row['pps_final_time_1']
        bl4 = df_row['pps_finish_beaten_lengths_1']
        fr3 = df_row['pps_fr3_1']
        bl3 = df_row['pps_second_call_beaten_lengths_1']
        if fr3 == 0 or fr4 == 0:
            return 0
        return round((d * 660) / ((fr4 + bl4 * 0.2) - (fr3 + bl3 * 0.2)), 2)


def calculate_horse_fractional_fps1_2(df_row):
    if df_row['pps_distance_2'] == '' or df_row['pps_distance_2'] == 0:
        return ''
    elif df_row['pps_distance_2'] >= 12 or df_row['pps_distance_2'] < 5.5:
        return ''
    elif df_row['pps_distance_2'] < 8:
        d = 2
        fr1 = df_row['pps_fr1_2']
        bl1 = df_row['pps_first_call_beaten_lengths_2']
        if fr1 == 0:
            return 0
        return round((d * 660) / (fr1 + bl1 * 0.2), 2)
    else:
        d = 4
        fr2 = df_row['pps_fr2_2']
        bl2 = df_row['pps_first_call_beaten_lengths_2']
        if fr2 == 0:
            return 0
        return round((d * 660) / (fr2 + bl2 * 0.2), 2)


def calculate_horse_fractional_fps2_2(df_row):
    if df_row['pps_distance_2'] == '' or df_row['pps_distance_2'] == 0:
        return ''
    elif df_row['pps_distance_2'] >= 12 or df_row['pps_distance_2'] < 5.5:
        return ''
    elif df_row['pps_distance_2'] < 8:
        d = 2
        fr2 = df_row['pps_fr2_2']
        bl2 = df_row['pps_second_call_beaten_lengths_2']
        fr1 = df_row['pps_fr1_2']
        bl1 = df_row['pps_first_call_beaten_lengths_2']
        if fr1 == 0 or fr2 == 0:
            return 0
        return round((d * 660) / ((fr2 + bl2 * 0.2) - (fr1 + bl1 * 0.2)), 2)
    else:
        d = 2
        fr3 = df_row['pps_fr3_2']
        bl3 = df_row['pps_second_call_beaten_lengths_2']
        fr2 = df_row['pps_fr2_2']
        bl2 = df_row['pps_first_call_beaten_lengths_2']
        if fr2 == 0 or fr3 == 0:
            return 0
        return round((d * 660) / ((fr3 + bl3 * 0.2) - (fr2 + bl2 * 0.2)), 2)


def calculate_horse_fractional_fps3_2(df_row):
    if df_row['pps_distance_2'] == '' or df_row['pps_distance_2'] == 0:
        return ''
    elif df_row['pps_distance_2'] >= 12 or df_row['pps_distance_2'] < 5.5:
        return ''
    elif df_row['pps_distance_2'] < 8:
        d = df_row['pps_distance_2'] - 4
        fr3 = df_row['pps_final_time_2']
        bl3 = df_row['pps_finish_beaten_lengths_2']
        fr2 = df_row['pps_fr2_2']
        bl2 = df_row['pps_second_call_beaten_lengths_2']
        if fr2 == 0 or fr3 == 0:
            return 0
        return round((d * 660) / ((fr3 + bl3 * 0.2) - (fr2 + bl2 * 0.2)), 2)
    else:
        d = df_row['pps_distance_2'] - 6
        fr4 = df_row['pps_final_time_2']
        bl4 = df_row['pps_finish_beaten_lengths_2']
        fr3 = df_row['pps_fr3_2']
        bl3 = df_row['pps_second_call_beaten_lengths_2']
        if fr3 == 0 or fr4 == 0:
            return 0
        return round((d * 660) / ((fr4 + bl4 * 0.2) - (fr3 + bl3 * 0.2)), 2)


def calculate_horse_fractional_fps1_3(df_row):
    if df_row['pps_distance_3'] == '' or df_row['pps_distance_3'] == 0:
        return ''
    elif df_row['pps_distance_3'] >= 12 or df_row['pps_distance_3'] < 5.5:
        return ''
    elif df_row['pps_distance_3'] < 8:
        d = 2
        fr1 = df_row['pps_fr1_3']
        bl1 = df_row['pps_first_call_beaten_lengths_3']
        if fr1 == 0:
            return 0
        return round((d * 660) / (fr1 + bl1 * 0.2), 2)
    else:
        d = 4
        fr2 = df_row['pps_fr2_3']
        bl2 = df_row['pps_first_call_beaten_lengths_3']
        if fr2 == 0:
            return 0
        return round((d * 660) / (fr2 + bl2 * 0.2), 2)


def calculate_horse_fractional_fps2_3(df_row):
    if df_row['pps_distance_3'] == '' or df_row['pps_distance_3'] == 0:
        return ''
    elif df_row['pps_distance_3'] >= 12 or df_row['pps_distance_3'] < 5.5:
        return ''
    elif df_row['pps_distance_3'] < 8:
        d = 2
        fr2 = df_row['pps_fr2_3']
        bl2 = df_row['pps_second_call_beaten_lengths_3']
        fr1 = df_row['pps_fr1_3']
        bl1 = df_row['pps_first_call_beaten_lengths_3']
        if fr1 == 0 or fr2 == 0:
            return 0
        return round((d * 660) / ((fr2 + bl2 * 0.2) - (fr1 + bl1 * 0.2)), 2)
    else:
        d = 2
        fr3 = df_row['pps_fr3_3']
        bl3 = df_row['pps_second_call_beaten_lengths_3']
        fr2 = df_row['pps_fr2_3']
        bl2 = df_row['pps_first_call_beaten_lengths_3']
        if fr2 == 0 or fr3 == 0:
            return 0
        return round((d * 660) / ((fr3 + bl3 * 0.2) - (fr2 + bl2 * 0.2)), 2)


def calculate_horse_fractional_fps3_3(df_row):
    if df_row['pps_distance_3'] == '' or df_row['pps_distance_3'] == 0:
        return ''
    elif df_row['pps_distance_3'] >= 12 or df_row['pps_distance_3'] < 5.5:
        return ''
    elif df_row['pps_distance_3'] < 8:
        d = df_row['pps_distance_3'] - 4
        fr3 = df_row['pps_final_time_3']
        bl3 = df_row['pps_finish_beaten_lengths_3']
        fr2 = df_row['pps_fr2_3']
        bl2 = df_row['pps_second_call_beaten_lengths_3']
        if fr2 == 0 or fr3 == 0:
            return 0
        return round((d * 660) / ((fr3 + bl3 * 0.2) - (fr2 + bl2 * 0.2)), 2)
    else:
        d = df_row['pps_distance_3'] - 6
        fr4 = df_row['pps_final_time_3']
        bl4 = df_row['pps_finish_beaten_lengths_3']
        fr3 = df_row['pps_fr3_3']
        bl3 = df_row['pps_second_call_beaten_lengths_3']
        if fr3 == 0 or fr4 == 0:
            return 0
        return round((d * 660) / ((fr4 + bl4 * 0.2) - (fr3 + bl3 * 0.2)), 2)


def calculate_horse_fractional_fps1_4(df_row):
    if df_row['pps_distance_4'] == '' or df_row['pps_distance_4'] == 0:
        return ''
    elif df_row['pps_distance_4'] >= 12 or df_row['pps_distance_4'] < 5.5:
        return ''
    elif df_row['pps_distance_4'] < 8:
        d = 2
        fr1 = df_row['pps_fr1_4']
        bl1 = df_row['pps_first_call_beaten_lengths_4']
        if fr1 == 0:
            return 0
        return round((d * 660) / (fr1 + bl1 * 0.2), 2)
    else:
        d = 4
        fr2 = df_row['pps_fr2_4']
        bl2 = df_row['pps_first_call_beaten_lengths_4']
        if fr2 == 0:
            return 0
        return round((d * 660) / (fr2 + bl2 * 0.2), 2)


def calculate_horse_fractional_fps2_4(df_row):
    if df_row['pps_distance_4'] == '' or df_row['pps_distance_4'] == 0:
        return ''
    elif df_row['pps_distance_4'] >= 12 or df_row['pps_distance_4'] < 5.5:
        return ''
    elif df_row['pps_distance_4'] < 8:
        d = 2
        fr2 = df_row['pps_fr2_4']
        bl2 = df_row['pps_second_call_beaten_lengths_4']
        fr1 = df_row['pps_fr1_4']
        bl1 = df_row['pps_first_call_beaten_lengths_4']
        if fr1 == 0 or fr2 == 0:
            return 0
        return round((d * 660) / ((fr2 + bl2 * 0.2) - (fr1 + bl1 * 0.2)), 2)
    else:
        d = 2
        fr3 = df_row['pps_fr3_4']
        bl3 = df_row['pps_second_call_beaten_lengths_4']
        fr2 = df_row['pps_fr2_4']
        bl2 = df_row['pps_first_call_beaten_lengths_4']
        if fr2 == 0 or fr3 == 0:
            return 0
        return round((d * 660) / ((fr3 + bl3 * 0.2) - (fr2 + bl2 * 0.2)), 2)


def calculate_horse_fractional_fps3_4(df_row):
    if df_row['pps_distance_4'] == '' or df_row['pps_distance_4'] == 0:
        return ''
    elif df_row['pps_distance_4'] >= 12 or df_row['pps_distance_4'] < 5.5:
        return ''
    elif df_row['pps_distance_4'] < 8:
        d = df_row['pps_distance_4'] - 4
        fr3 = df_row['pps_final_time_4']
        bl3 = df_row['pps_finish_beaten_lengths_4']
        fr2 = df_row['pps_fr2_4']
        bl2 = df_row['pps_second_call_beaten_lengths_4']
        if fr2 == 0 or fr3 == 0:
            return 0
        return round((d * 660) / ((fr3 + bl3 * 0.2) - (fr2 + bl2 * 0.2)), 2)
    else:
        d = df_row['pps_distance_4'] - 6
        fr4 = df_row['pps_final_time_4']
        bl4 = df_row['pps_finish_beaten_lengths_4']
        fr3 = df_row['pps_fr3_4']
        bl3 = df_row['pps_second_call_beaten_lengths_4']
        if fr3 == 0 or fr4 == 0:
            return 0
        return round((d * 660) / ((fr4 + bl4 * 0.2) - (fr3 + bl3 * 0.2)), 2)
