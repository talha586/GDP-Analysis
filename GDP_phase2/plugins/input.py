import json
import re
from core.contracts import PipelineService


class ExcelReader:

    def __init__(self, service: PipelineService, filepath: str):
        self._service  = service
        self._filepath = filepath

    def run(self):
        import openpyxl

        wb   = openpyxl.load_workbook(self._filepath, data_only=True)
        ws   = wb.active
        rows = list(ws.iter_rows(values_only=True))

        if not rows:
            print("Warning: file is empty.")
            return

        headers  = [str(h) if h is not None else "" for h in rows[0]]
        raw_data = list(map(lambda row: dict(zip(headers, row)), rows[1:]))

        print(f"Loaded {len(raw_data)} records from '{self._filepath}'")
        self._service.execute(raw_data)
