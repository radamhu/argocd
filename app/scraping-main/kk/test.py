# https://www.guru99.com/python-csv.html

#import necessary modules
import csv
import pandas

# reader = csv.DictReader(open("test.csv"))
# for raw in reader:
#     print(raw)

# with open("test.csv", "r") as fh:
#     lines = csv.reader(fh)
#     for line in lines:
#         address = line[0]
#         print(line[0])
        # driver.find_element_by_name('emailAddress').send_keys(address)

result = pandas.read_csv('test.csv')
#details_lst = []
#for column in result.columns:
#    details_lst.append(result[column][0])
for d in result.values:
    if d[3] != 'FALSE':
        print(d[0])

# print(details_lst)