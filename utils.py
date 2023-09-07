def check_batch_time(trips, actual_datetime):
    trips_initiated = []
    for trip in trips:
        if trip['second_batch_datetime'] == actual_datetime:
            trips_initiated.append(trip)
    return trips_initiated


def check_trip_ended(started_trips, actual_datetime):
    for trip in started_trips:
        if trip['finish_time'] == actual_datetime:
            print(f"trip con id: {trip['id']} eliminado...")
            started_trips.remove(trip)