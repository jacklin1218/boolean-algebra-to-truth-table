import csv
import sys
import truth_table as tt

path = "table.csv"
input = []
x = ""
for i in range(1,len(sys.argv)):
    input.append(sys.argv[i])
table = tt.make_table(input)
tt.print_table(table)
tt.table_to_csv(path,table)
