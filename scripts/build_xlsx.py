"""data/*.csv -> stock.xlsx (4 sheets). Run by GitHub Actions on every data change."""
import csv
import datetime as dt
import pathlib

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHEETS = [("celline", "celline.csv"), ("bacteria", "bacteria.csv"),
          ("reagent", "reagent.csv"), ("siRNA", "siRNA.csv")]
NUMERIC_COLS = {"concentration (ng/µl)"}  # pure numbers; other concentrations keep their unit text
HEADER_FILL = PatternFill("solid", fgColor="DAE6F0")


def convert(col, value):
    if value == "":
        return None
    if col == "date":
        try:
            return dt.datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return value
    if col in NUMERIC_COLS:
        try:
            return float(value) if "." in value else int(value)
        except ValueError:
            return value
    return value


def main():
    wb = Workbook()
    wb.remove(wb.active)
    for name, fname in SHEETS:
        ws = wb.create_sheet(name)
        with open(ROOT / "data" / fname, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        header = rows[0]
        ws.append(header)
        for r in rows[1:]:
            r = r + [""] * (len(header) - len(r))
            ws.append([convert(c, v) for c, v in zip(header, r)])
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.fill = HEADER_FILL
        for ci, col in enumerate(header, start=1):
            letter = ws.cell(row=1, column=ci).column_letter
            for (cell,) in ws.iter_rows(min_row=2, min_col=ci, max_col=ci):
                if col == "date" and isinstance(cell.value, dt.date):
                    cell.number_format = "yyyy-mm-dd"
                elif col not in NUMERIC_COLS:
                    cell.number_format = "@"
            width = max([len(str(col))] + [len(str(r[ci - 1])) for r in rows[1:] if len(r) >= ci])
            ws.column_dimensions[letter].width = min(max(width + 2, 8), 60)
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
    wb.save(ROOT / "stock.xlsx")
    print("stock.xlsx written")


if __name__ == "__main__":
    main()
