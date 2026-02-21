# from app.models.csv_data import CSVData, CSVDataType


# class CSVDataParser:
#     """`CSVData` を総括表フォーマットに従ってヘッダーごとに分割するクラス"""

#     def __init__(self, csv_data: CSVData):
#         self._csv_data = csv_data
#         self._csv_tables = self._parse_tables()

#     def _parse_tables(self) -> list[CSVData]:
#         """`CSVData` をヘッダーごとに分割してテーブルのリストを生成"""
#         csv_tables: list[CSVData] = []
#         csv_rows: CSVDataType = []
#         for row in self._csv_data:
#             if row[0].startswith("#") and row[0].endswith("レベル名"):
#                 if len(csv_rows) > 0:
#                     csv_table = CSVData(csv_rows)
#                     csv_tables.append(csv_table)
#                 csv_rows = [row]
#                 continue
#             csv_rows.append(row)
#         csv_table = CSVData(csv_rows)
#         csv_tables.append(csv_table)
#         return csv_tables

#     @property
#     def csv_data(self) -> CSVData:
#         """分割前の `CSVData`"""
#         return self._csv_data

#     @property
#     def csv_tables(self) -> list[CSVData]:
#         """分割された `CSVData` のリスト"""
#         return self._csv_tables
