
ExprValue = str | int | float | None


class BaseValue:
    def __init__(self, type_name: str):
        self.type_name = type_name
        self.value = 0


class IntValue(BaseValue):
    def __init__(self, value: int):
        super().__init__('i')
        self.value = value


class StringValue(BaseValue):
    def __init__(self, value: str):
        super().__init__('s')
        self.value = value


class FloatValue(BaseValue):
    def __init__(self, value: float):
        super().__init__('f')
        self.value = value


class BoolValue(BaseValue):
    def __init__(self, value: bool):
        super().__init__('b')
        self.value = value


class FunctionValue(BaseValue):
    def __init__(self, name: str, block_start: int, params=None):
        super().__init__('fn')
        self.name = name
        self.block_start: int = block_start
        self.params = params or []
        self.return_value: int = 0
        self.variables = {}  # function-local variables
