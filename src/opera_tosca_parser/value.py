from typing import Optional, Any


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
