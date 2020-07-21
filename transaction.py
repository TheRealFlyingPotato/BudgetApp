import funcs
import sys
import openpyxl
import get

def parseArgs(args):
  print(args)
  d = {}
  while len(args) > 1:
    amt = float(args.pop(0))
    item = args.pop(0).lower().strip()
    d[amt] = item

  if len(args) == 0:
    return -1
  d["_name"] = args[0]
  return d
  
def getColumns(transaction_data, sheet_data):
  columns = {}
  for amount, item_name in transaction_data.items():
    if amount == "_name":
      continue
    found = False
    for att in sheet_data['column_attributes']:
      print(att)
      i_n = item_name
      col_n = sheet_data['column_attributes'][att]['name'].lower()
      print(f'i_n:{i_n}, col_n:{col_n}')
      # print(sheet_data['column_attributes'][att]['name'])
      if i_n == col_n:
        found = True
        columns[att] = amount
        break
    if not found:
      return -1
  return columns


def main(l, outputHandle = None):
  l = l.split(',')
  data = parseArgs(l)
  if data == -1:
    outputHandle.output("Transaction Failure: Invalid Arguments")
    return
  print(data)
  workbook = openpyxl.load_workbook(filename = funcs.FOUT, data_only=False)
  sheet = funcs.fetch_sheet(workbook)
  sheet_data = funcs.parse_sheet(sheet)
  col_data = getColumns(data, sheet_data)
  if col_data == -1:
    outputHandle.output('Transaction Failure: Column not found')
    return
  open_row = funcs.find_open_row(sheet)
  print("DEBUG: ", data)
  funcs.set_sheet_vals(sheet, col_data, data['_name'], open_row)
  workbook.save(funcs.FOUT)
  funcs.cleanup(funcs.FOUT)
  s = 'Columns updated:\n' + '\n'.join([f'{name}: {amt}' for amt,name in data.items() if amt != '_name'])
  if outputHandle == None:
    print(s)
    get.main()
  else:
    outputHandle.output(s)
    get.main(outputHandle)



if __name__ == "__main__":
  main(' '.join(sys.argv[1:]))