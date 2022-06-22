import csv


def add_neighbours(step, precision, file_name):

    points = set()

    def add_point(lat, lon):
        points.add((round(lat, precision), round(lon, precision)))

    def neighbours(lat, lon):

        add_point(lat-step, lon+step)
        add_point(lat-step, lon)
        add_point(lat-step, lon-step)

        add_point(lat, lon+step)
        add_point(lat, lon)
        add_point(lat, lon-step)

        add_point(lat+step, lon+step)
        add_point(lat+step, lon)
        add_point(lat+step, lon-step)

    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            neighbours(float(row[0]), float(row[1]))

    new_file_name = file_name+"-nb.csv"
    with open(new_file_name, 'w') as out:
        writer = csv.writer(out)
        for point in sorted(points):
            writer.writerow(point)

    return new_file_name
