import sys
from statistics import mean

class Driver:
    """Class representing a driver with their code and lap times."""
    def __init__(self, code):
        self.code = code
        self.lap_times = []
    
    def add_lap_time(self, time):
        self.lap_times.append(time)
    
    def get_fastest_lap(self):
        return min(self.lap_times) if self.lap_times else float('inf')
    
    def get_average_lap(self):
        return mean(self.lap_times) if self.lap_times else 0

def read_file(filename):
    """Reads the file and extracts the race location and driver lap times."""
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)

    race_location = lines[0].strip()
    drivers = {}
    for line in lines[1:]:
        driver_code = line[:3]
        lap_time = float(line[3:])
        if driver_code not in drivers:
            drivers[driver_code] = Driver(driver_code)
        drivers[driver_code].add_lap_time(lap_time)
    return race_location, drivers

def display_race_info(race_location, drivers):
    """Displays the race location and fastest driver."""
    print(f"Race Location: {race_location}")
    fastest_driver = min(drivers.values(), key=lambda d: d.get_fastest_lap())
    print(f"Fastest Driver: {fastest_driver.code} with a time of {fastest_driver.get_fastest_lap():.3f} seconds")

def display_driver_stats(drivers):
    """Displays each driver's fastest and average lap times."""
    total_times, total_laps = 0, 0
    for driver in drivers.values():
        total_times += sum(driver.lap_times)
        total_laps += len(driver.lap_times)
        print(f"Driver {driver.code} - Fastest Lap: {driver.get_fastest_lap():.3f} seconds, Average Lap: {driver.get_average_lap():.3f} seconds")
    overall_avg_time = total_times / total_laps if total_laps else 0
    print(f"Overall Average Lap Time: {overall_avg_time:.3f} seconds")

def display_sorted_times(drivers):
    """Displays the fastest lap times in descending order."""
    sorted_drivers = sorted(drivers.values(), key=lambda d: d.get_fastest_lap(), reverse=True)
    print("\nFastest Times in Descending Order:")
    for driver in sorted_drivers:
        print(f"Driver {driver.code} - Fastest Lap: {driver.get_fastest_lap():.3f} seconds")

def main():
    if len(sys.argv) != 2:
        print("Usage: python timing_board.py <filename>")
    sys.exit(1)

    filename = sys.argv[1]
    race_location, drivers = read_file(filename)
    display_race_info(race_location, drivers)
    display_driver_stats(drivers)
    display_sorted_times(drivers)

if __name__ == "__main__":
    main()
