from typing import Protocol, List, Any, runtime_checkable


@runtime_checkable
class DataSink(Protocol):
    """Output contract - anything that wants to display results must have this method"""

    def write(self, tag: str, records: List[dict]) -> None: ...
