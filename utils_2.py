import csv
from datetime import datetime, timedelta
from classes.trip import Trip

def calculate_speed(datetime_1,coor_1,datetime_2,coor_2):
    duration = datetime_2 - datetime_1
    duration = duration.total_seconds() // 60
    speed = (coor_2 - coor_1) / duration
    return speed

def read_data(filename):
    data = []
    with open(filename, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            filtered_data = {
                'lift': row['lift'],
                'equipment': row['equipment'],
                'truck': row['truck'],
                'cmdb': row['cmdb'],
                'vol': float(row['vol']),
                'batch_time_1':datetime.strptime(row['first_batch_time'],'%m/%d/%Y %H:%M'),
                'batch_time_2': datetime.strptime(row['last_batch_time'],'%m/%d/%Y %H:%M'),
                'arrive_datetime': datetime.strptime(row['arrive_date_time'],'%m/%d/%Y %H:%M'),
                'start_datetime': datetime.strptime(row['start_date_time'],'%m/%d/%Y %H:%M'),
                'end_datetime': datetime.strptime(row['finish_date_time'],'%m/%d/%Y %H:%M'),
            }
            data.append(filtered_data)
        return data
    
def get_unique(data, key):
    unique_list = []
    for x in data:
        if x[key] not in unique_list:
            unique_list.append(x[key])

    return unique_list

def find_object(property, object, objects):
    result = [x for x in objects if getattr(x, property) == object]
    if result:
        return result[0]
    return None

def get_start_datetime(data):
    return data[0]['batch_time_1']

def get_finish_datetime(data):
    return data[len(data)-1]['end_datetime']

def create_trip_list(data, truck_objects,equipment_objects):
    counter = 1
    trips_info = []
    for x in data:
        trips_info.append(Trip(
            counter,
            find_object("name",x['equipment'],equipment_objects),
            find_object("id",x['truck'],truck_objects),
            x['vol'],
            x['batch_time_1'],
            x['batch_time_2'],
            x['arrive_datetime'],
            x['start_datetime'],
            x['end_datetime'],

        ))
        counter += 1
    return trips_info
        

    