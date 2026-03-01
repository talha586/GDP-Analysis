from typing import Protocol, List, Any, runtime_checkable


@runtime_checkable
class DataSink(Protocol):
    """Output contract - anything that wants to display results must have this method"""

    def write(self, tag: str, records: List[dict]) -> None: ...


@runtime_checkable
class PipelineService(Protocol):
    """Input contract - the engine must have this method so readers can send data to it"""

    def execute(self, raw_data: List[Any]) -> None: ...
