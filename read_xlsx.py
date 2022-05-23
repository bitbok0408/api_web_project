import requests
import openpyxl



wb_obj = openpyxl.load_workbook('test.xlsx')


sheet = wb_obj.active

count = 0
for i in sheet.values:
    if i.count(None) < len(i):
        print(i)
        count += 1
print(count)

