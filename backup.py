import os
import datetime

def backup(FNAME):
  DATETIME = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
  os.system(f'cp {FNAME} backups/{DATETIME}.xlsx')

if __name__ == "__main__":
  backup('money.xlsx')
