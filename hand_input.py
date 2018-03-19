import csv
import sys
import truth_table as tt

path = "table.csv"
input1 = []
x = ""
while True:
    x = input()
    if x == "":
        break
    input1.append(x)
table = tt.make_table(input1)
tt.print_table(table)
tt.table_to_csv(path,table)
