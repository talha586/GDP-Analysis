from typing import Protocol, runtime_checkable


# Contract for any class that wants to receive and process raw data packets
@runtime_checkable
class PacketProcessor(Protocol):
    def process(self, packet: dict) -> dict | None: ...


# Contract for any class that wants to receive processed results
@runtime_checkable
class ResultSink(Protocol):
    def write(self, packet: dict) -> None: ...


# Contract for any class that acts as a telemetry subject (Observable)
@runtime_checkable
class TelemetrySubject(Protocol):
    def subscribe(self, observer) -> None: ...
    def notify(self) -> None: ...
