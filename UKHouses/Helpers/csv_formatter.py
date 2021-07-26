import csv


# INSTRUCTIONS TO COVERT A CSV INTO A DB FILE

# 1. run this file!


def prettify_no_quotes():
    reader = csv.reader(
        open("../csv_data/data-2021.csv", mode="rt"), skipinitialspace=True
    )
    writer = csv.writer(
        open("../csv_data/temp.csv", mode="wt"), quoting=csv.QUOTE_NONE, escapechar="\\"
    )
    writer.writerows(reader)


def prettify_no_parenthesis():
    with open("../csv_data/temp.csv") as file:
        data = file.read().replace("{", "").replace("}", "")
        with open("../csv_data/cleaned.csv", mode="w") as newfile:
            newfile.write(data)
        # print(data)


prettify_no_quotes()
prettify_no_parenthesis()

# 2. Terminal command to delete all rows that have more than 16 columns, since there are some:
# awk -F, 'NF==16' ./csv_data/cleaned.csv > ./csv_data/cleaned2.csv

# 3. delete elements at position: xxx that I dont need, basically:
# use terminal:
# cut -d, -f4 --complement example.csv > input.csv or in my case
# cut -d, -f1-8,10,12-14 ./csv_data/cleaned2.csv > ./csv_data/final.csv


# 4. run in terminal: awk -F, '{$1=++i FS $1;}1' OFS=, input.csv > output.csv to create a new file with an initial
# column auto incremented number in my case:
# awk -F, '{$1=++i FS $1;}1' OFS=, ./csv_data/final.csv > ./csv_data/ready_data.csv
#
#
# 5. run:
# awk '{sub(/00:00/,"00:00:00")}1' ./csv_data/ready_data.csv > ./csv_data/complete.csv
#
# Finally, run createDB.py
# 8. Delete csv in /data not needed (keep only initial and last csv )
