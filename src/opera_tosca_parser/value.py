import copy

from typing import Optional, Any

from opera_tosca_parser.error import DataError


class Value:
    def __init__(self, typ: Optional, present: bool, data: Optional[Any] = None):
        """
        Construct Value object
        :param typ: Value type (not implemented)
        :param present: Value present
        :param data: Value data
        """
        self.type = typ
        self.present = present
        self._data = data

    @property
    def data(self) -> Any:
        """
        Get data from Value object
        :return: Data
        """
        if not self.present:
            raise AssertionError("Accessing an unset value. Bug-fixing ahead ;)")
        return self._data

    def set(self, data: Any):
        """
        Set data for Value object
        :return: Data
        """
        self._data = data
        self.present = True

    def __str__(self) -> str:
        """Overridden string representation"""
        return f"Value({self.present})[{self._data}]"

    def dump(self):
        return dict(is_set=self.present, data=self._data)

    def load(self, data):
        self.present = data["is_set"]
        self._data = data["data"]

    @property
    def data(self):
        if not self.present:
            raise AssertionError("Accessing an unset value. Bug-fixing ahead ;)")
        return self._data

    def copy(self):
        return type(self)(self.type, self.present, copy.deepcopy(self._data))

    def unset(self):
        self._data = None
        self.present = False

    def eval(self, instance, key):
        if not self.present:
            raise DataError(f"Cannot use an unset value: {key}")

        if self.is_function:
            return Value.eval_function(self.data, instance)

        if isinstance(self.data, dict):
            result_map = {}
            for map_key, value in self.data.items():
                result_map[map_key] = Value.check_eval_function(value, instance)
            return result_map

        if isinstance(self.data, list):
            result_list = []
            for value in self.data:
                result_list.append(Value.check_eval_function(value, instance))
            return result_list

        return self.data

    @property
    def is_function(self):
        return Value.check_function(self.data)

    @staticmethod
    def check_function(data):
        return isinstance(data, dict) and len(data) == 1 and tuple(data.keys())[0] in Value.FUNCTIONS

    @staticmethod
    def eval_function(data, instance):
        (function_name, params), = data.items()
        return getattr(instance, function_name)(params)

    @staticmethod
    def check_eval_function(data, instance):
        if Value.check_function(data):
            return Value.eval_function(data, instance)
        return data

