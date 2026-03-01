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


class JSONReader:

    def __init__(self, service: PipelineService, filepath: str):
        self._service  = service
        self._filepath = filepath

    @staticmethod
    def _sanitize_json(text: str) -> str:
        text = re.sub(r'\bNaN\b', 'null', text)
        text = re.sub(r'\bInfinity\b', '1e308', text)
        text = re.sub(r'\b-Infinity\b', '-1e308', text)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        text = re.sub(r'(?<=: )([#@\$!\\][^,\n\]]*)', 'null', text)
        return text

    def run(self):
        with open(self._filepath, 'r', encoding='utf-8', errors='replace') as fh:
            raw_text  = fh.read()
            sanitized = self._sanitize_json(raw_text)
            raw_data  = json.loads(sanitized)

        if not isinstance(raw_data, list):
            raise ValueError("Expected a JSON array at the top level.")

        raw_data = list(map(lambda row: {str(k): v for k, v in row.items()}, raw_data))

        print(f"Loaded {len(raw_data)} records from '{self._filepath}'")
        self._service.execute(raw_data)