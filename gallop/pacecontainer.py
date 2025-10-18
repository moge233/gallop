#! python3


from datetime import date
from math import ceil, floor

from brispy.singlefile import SingleFileHorse, SingleFilePastPerformance
from chart_parser.special_types import Course
from horsedb2.variants import get_average_variant


DEFAULT_MIN_ROUTE_DISTANCE: float = 8.0


class PaceContainerPastPerformance:
    def __init__(self, sfpp: SingleFilePastPerformance):
        self.distance = round(abs(sfpp.distance) / 220.0, 2)
        if (sfpp.surface == 'D' or (sfpp.surface == 'T' and 'x' in sfpp.start_code)) and \
                sfpp.all_weather_surface_flag != 'A':
            self.course: Course | None = Course.DIRT
        elif sfpp.surface == 'D' and sfpp.all_weather_surface_flag == 'A':
            self.course: Course | None = Course.ALL_WEATHER_TRACK
        elif sfpp.surface == 'T':
            self.course: Course | None = Course.TURF
        elif sfpp.surface == 'd':
            self.course: Course | None = Course.INNER_TURF
        elif sfpp.surface == 't':
            self.course: Course | None = Course.OUTER_TURF
        else:
            print(sfpp.surface)
            self.course: Course | None = None
        self.t1 = sfpp.two_furlong_fraction if self.distance < DEFAULT_MIN_ROUTE_DISTANCE \
            else sfpp.four_furlong_fraction
        self.t2 = sfpp.four_furlong_fraction if self.distance < DEFAULT_MIN_ROUTE_DISTANCE \
            else sfpp.six_furlong_fraction
        self.t3 = sfpp.final_time
        self.track_variant = sfpp.track_variant
        if sfpp.track_code:
            try:
                self.average_variant = int(get_average_variant(sfpp.track_code, sfpp.distance, sfpp.surface,
                                                               sfpp.all_weather_surface_flag))
            except Exception as e:
                print(e)
                self.average_variant = 17
        else:
            self.average_variant = 0
        self.bl1 = sfpp.first_call_beaten_lengths
        self.bl2 = sfpp.second_call_beaten_lengths
        self.bl3 = sfpp.finish_beaten_lengths
        self.winner = 1 if sfpp.finish_position == '1' else 0

        if abs(self.average_variant - self.track_variant) > 1:  # type: ignore
            if self.average_variant - self.track_variant > 4:
                adj3 = self.average_variant - 3 - self.track_variant
            else:
                if self.track_variant > self.average_variant:
                    diff = self.average_variant + 1 - self.track_variant
                    adj3 = floor(diff / 2)
                else:
                    adj3 = ceil((self.average_variant - 1 - self.track_variant) / 2)
        else:
            adj3 = 0
        if adj3 > 0:
            adj2 = floor(adj3 / 2)
        else:
            adj2 = ceil(adj3 / 2)
        if self.distance < DEFAULT_MIN_ROUTE_DISTANCE:
            if abs(adj3) > 3:
                adj1 = round(adj2 / 2, 0)
            else:
                adj1 = 0
        else:
            adj1 = round(2 * adj2 / 3, 0)

        # Leader's times adjusted for DRF Track Variant
        adj_t1 = self.t1 + 0.2 * adj1
        adj_t2 = self.t2 + 0.2 * adj2
        adj_t3 = self.t3 + 0.2 * adj3

        if self.distance < DEFAULT_MIN_ROUTE_DISTANCE:
            if not self.t1:
                self.f1 = 0
                self.f2 = 0
                self.f3 = 0
                self.ep = 0
                self.sp = 0
                self.ap = 0
                self.fx = 0
                self.energy = 0
            else:
                self.f1 = round((1320 - 10 * self.bl1) / adj_t1, 2)
                self.f2 = round((1320 - 10 * (self.bl2 - self.bl1)) / (adj_t2 - adj_t1), 2)
                self.f3 = round((660 * (self.distance - 4) - 10 * (self.bl3 - self.bl2)) / (adj_t3 - adj_t2), 2)
                self.ep = round((2640 - 10 * self.bl2) / adj_t2, 2)
                self.sp = round((self.ep + self.f3) / 2, 2)
                self.ap = round((self.f1 + self.f2 + self.f3) / 3, 2)
                self.fx = round((self.f1 + self.f3) / 2, 2)
                self.energy = round(self.ep / (self.ep + self.f3), 4)
        else:
            if not self.t1:
                self.f1 = 0
                self.f2 = 0
                self.f3 = 0
                self.ep = 0
                self.sp = 0
                self.ap = 0
                self.fx = 0
                self.energy = 0
            else:
                self.f1 = round((2640 - 10 * self.bl1) / adj_t1, 2)
                self.f2 = round((1320 - 10 * (self.bl2 - self.bl1)) / (adj_t2 - adj_t1), 2)
                self.f3 = round((660 * (self.distance - 6) - 10 * (self.bl3 - self.bl2)) / (adj_t3 - adj_t2), 2)
                self.ep = round((3960 - 10 * self.bl2) / adj_t2, 2)
                self.sp = round((self.ep + self.f3) / 2, 2)
                self.ap = round((self.f1 + self.f3) / 2, 2)
                self.fx = round((self.f1 + self.f3) / 2, 2)
                self.energy = round(self.ep / (self.ep + self.f3), 4)

    def __str__(self):
        ret = ''
        for k, v in vars(self).items():
            ret += f'{k}={v}, '
        return f'PaceContainerPastPerformance({ret[:-2]})'

    def __repr__(self):
        ret = ''
        for k, v in vars(self).items():
            ret += f'{k}={v}, '
        return f'PaceContainerPastPerformance({ret[:-2]})'

    def is_winner(self) -> bool:
        return self.winner == 1


class PaceContainer:
    def __init__(self, sfh: SingleFileHorse):
        self.past_performances: list[PaceContainerPastPerformance] = []
        if sfh.past_performances:
            for pp in sfh.past_performances:
                if not pp.track_code or int(pp.date[:4]) < date.today().year:
                    continue
                self.past_performances.append(PaceContainerPastPerformance(pp))
        if self.past_performances:
            fr1s = [float(pp.f1) for pp in self.past_performances]
            fr2s = [float(pp.f2) for pp in self.past_performances]
            fr3s = [float(pp.f3) for pp in self.past_performances]
            eps = [float(pp.ep) for pp in self.past_performances]
            sps = [float(pp.sp) for pp in self.past_performances]
            aps = [float(pp.ap) for pp in self.past_performances]
            es = [float(pp.energy) for pp in self.past_performances]
            self.average_fr1 = round(sum(fr1s) / len(fr1s), 2)
            self.average_fr2 = round(sum(fr2s) / len(fr2s), 2)
            self.average_fr3 = round(sum(fr3s) / len(fr3s), 2)
            self.average_ep = round(sum(eps) / len(eps), 2)
            self.average_sp = round(sum(sps) / len(sps), 2)
            self.average_ap = round(sum(aps) / len(aps), 2)
            self.average_energy = round(sum(es) / len(es), 2)
        else:
            self.average_fr1 = 0
            self.average_fr2 = 0
            self.average_fr3 = 0
            self.average_ep = 0
            self.average_sp = 0
            self.average_ap = 0
            self.average_energy = 0

    def __str__(self):
        ret = ''
        for k, v in vars(self).items():
            ret += f'{k}={v}, '
        return f'PaceContainer({ret[:-2]})'

    def __repr__(self):
        ret = ''
        for k, v in vars(self).items():
            ret += f'{k}={v}, '
        return f'PaceContainer({ret[:-2]})'
