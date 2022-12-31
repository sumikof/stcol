import re
import operator

import db.model


class Connector:
    def __init__(self, model):
        self._model = model

    @property
    def model(self):
        return self._model

    def get_daily_data(self, symbols=None, date=None, count=None):
        pass

    def setup(self):
        pass


class DateCondition:
    operator_map = {
        "<": operator.lt,
        "<=": operator.le,
        ">": operator.gt,
        ">=": operator.ge,
        "==": operator.eq,
        "": operator.eq,
    }

    def __init__(self, date):
        if (match := re.compile(r"([<>=]*)([0-9]{8})").match(date)) and (match.group(1) not in self.operator_map):
            self.date_op = self.operator_map[match.group(1)]
            self.dateymd = match.group(2)
        else:
            raise RuntimeError(f"Not Dateformat => {date}")

    def check(self, date):
        self.date_op(date, self.dateymd)


class Condition:

    def __init__(self, date):
        self._date = DateCondition(date)

    def chack_date(self, date):
        return self._date.check(date)

    @property
    def date(self):
        return self.chack_date

