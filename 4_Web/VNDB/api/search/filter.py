from api.utils.utils import check_date


class VN_Filter:
    def __init__(self, query: list) -> None:
        self.query = query
    def get_filters(self):
        return self.query

class VN_Operactor:
    def __init__(self, operator: str, filters: list | None) -> None:
        self.operator = operator
        self.filters = filters if filters else []
    def __add__(self, other):
        if isinstance(other, VN_Operactor) or isinstance(other, VN_Filter):
            self.filters.append(other)
            return self
        raise TypeError("unsupported operand type(s) for +: 'VN_Operactor' and '{}'".format(type(other)))
    def get_filters(self):
        return [self.operator] + [sub_filters.get_filters() for sub_filters in self.filters]


class VN_Operactor_And(VN_Operactor):
    def __init__(self, filters: list | None = None) -> None:
        super().__init__("and", filters)

class VN_Operactor_Or(VN_Operactor):
    def __init__(self, filters: list | None = None) -> None:
        super().__init__("or", filters)

class VN_Filter_ID(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["id", "=", query]
        super().__init__(query)

class VN_Filter_Staff(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["staff", "=", ["search", "=", query]]
        super().__init__(query)

class VN_Filter_Character(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["character", "=", ["search", "=", query]]
        super().__init__(query)

class VN_Filter_Developer(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["developer", "=", ["search", "=", query]]
        super().__init__(query)

class VN_Filter_Length(VN_Filter):
    def __init__(self, query: int = 1) -> None:
        if query < 1 or query > 5:
            raise ValueError("Invalid length")
        query = [] if not query else ["length", "=", query]
        super().__init__(query)

class VN_Filter_Language(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["lang", "=", query]
        super().__init__(query)

class VN_Filter_OriginalLanguage(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["olang", "=", query]
        super().__init__(query)

class VN_Filter_Platform(VN_Filter):
    def __init__(self, query: str = "") -> None:
        query = [] if not query else ["platform", "=", query]
        super().__init__(query)

class VN_Filter_DevStatus(VN_Filter):
    def __init__(self, query: int = 0) -> None:
        if query < 0 or query > 2:
            raise ValueError("Invalid devstatus")
        query = [] if not query else ["devstatus", "=", query]
        super().__init__(query)

class VN_Filter_HasDescription(VN_Filter):
    def __init__(self, query: bool = False) -> None:
        query = [] if not query else ["has_description", "=", 1]
        super().__init__(query)

class VN_Filter_HasAnime(VN_Filter):
    def __init__(self, query: bool = False) -> None:
        query = [] if not query else ["has_anime", "=", 1]
        super().__init__(query)

class VN_Filter_HasScreenshot(VN_Filter):
    def __init__(self, query: bool = False) -> None:
        query = [] if not query else ["has_screenshot", "=", 1]
        super().__init__(query)

class VN_Filter_HasReview(VN_Filter):
    def __init__(self, query: bool = False) -> None:
        query = [] if not query else ["has_review", "=", 1]
        super().__init__(query)

class VN_Filter_ReleasedDate(VN_Filter):
    def __init__(self, operator: str, date: str) -> None:
        if operator not in ["<", ">", "=", ">=", "<=", "!="]:
            raise ValueError("Invalid operator")
        if not check_date(date):
            raise ValueError("Invalid date format")
        query = (
        ["release", "=", 
            ["and",
                ["released", operator, date],
                ["platform", "=", "win"],
                ["or",
                    ["lang", "=", "ja"],
                    ["lang", "=", "zh-Hans"]
                ]
            ]
        ])
        super().__init__(query)