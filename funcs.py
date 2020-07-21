import win32com.client
import os
import openpyxl
import datetime


STARTING_ROW = 7
ITEM_COL = 'B'
COLS = 'DEFGHIJKLMNOPQRSTUVWXYZ'
FIN = 'money.xlsx'
FOUT = FIN
DATE_COL = 'A'
TOTALS_CELL = 'C2'

def find_open_row(sheet):
  print('finding open row...')
  row = STARTING_ROW
  while True:
    # print(row, sheet['B' + str(row)].value)
    if sheet[ITEM_COL + str(row)].value in [0, None]:
      break
    row += 1
  print(f'Found open row: {row}')
  return str(row)


def set_sheet_vals(sheet, vals, title, row):
  print("VALS:", vals)
  sheet[ITEM_COL + row].value = title
  sheet[DATE_COL + row].value = datetime.datetime.now().strftime("%m/%d/%Y")
  for column, amount in vals.items():
    # if column[0] == '_':
      # continue
    sheet[column + row].value = amount


def parse_sheet(sheet):
  print('parsing sheet data...')
  column_attributes = dict()
  for col in COLS:
    column_attributes[col] = {
      'name' : sheet[col + '1'].value,
      'max' : sheet[col + '3'].value,
      'default' : sheet[col + '4'].value,
      'increment' : sheet[col + '5'].value,
      'current' : sheet[col + '2'].value,
    }
    # print(sheet[col + '1'].value, column_attributes[col])
    if sheet[col + '1'].value == 'Cushion':
      data = {
        'column_attributes' : column_attributes,
        'cushion_col' : col,
        'total_cash' : sheet[TOTALS_CELL].value
      }
      break
  # print(f'sheet data parsed: {data}')
  return data

def fetch_sheet(workbook):
  return workbook[workbook.sheetnames[0]]

def cleanup(filename):
  print('starting cleanup cycle')
  excel = win32com.client.Dispatch('Excel.Application')
  filepath = os.getcwd() + '/' + FIN
  print(filepath)
  print('opening workbook')
  wb1 = excel.Workbooks.Open(filepath)
  ws1 = excel.ActiveSheet
  while ws1 is None:
    ws1 = excel.ActiveSheet
  ws1.EnableCalculation = True
  ws1.Calculate()
  wb1.Save()
  print('closing workbook')
  wb1.Close(True)
  print('shutting down excel')
  # os.system('taskkill /im excel.exe /t /f')
  excel.Application.quit()
  print('Cleanup Finished Successfully')

if __name__ == "__main__":
  cleanup('money.xlsx')