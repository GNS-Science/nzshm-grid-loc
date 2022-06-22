import csv

# exec(open('scripts/round-csv.py').read())

precision = 2
file_in = 'test-0.05.csv'
file_out = 'test-0.05-rounded.csv'

with open(file_in, 'r') as csvfile:
    reader = csv.reader(csvfile)
    with open(file_out, 'w') as out_file:
        writer = csv.writer(out_file)
        for row in reader:
            new_row = [
                round(float(row[0]), precision),
                round(float(row[1]), precision)]
            writer.writerow(new_row)
