import sys
from statistics import mean

class Driver:
    """Represents a driver and their lap times."""
    def __init__(self, code):
        self.code = code
        self.lap_times = []
    
    def add_lap_time(self, time):
        """Adds a lap time to the driver."""
        self.lap_times.append(time)
    
    def get_fastest_lap(self):
        """Returns the fastest lap time of the driver."""
        return min(self.lap_times) if self.lap_times else float('inf')
    
    def get_average_lap(self):
        """Returns the average lap time of the driver."""
        return mean(self.lap_times) if self.lap_times else 0

def read_file(filename):
    """
    Reads the input file and extracts race location and driver lap times.
    """
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")  # Handle missing file
        sys.exit(1)

    if not lines or len(lines) < 2:
        print("Error: File is empty or does not contain enough data.")
        sys.exit(1)

    # Extract race location (first line)
    race_location = lines[0].strip()
    drivers = {}

    # Process each subsequent line
    for line in lines[1:]:
        line = line.strip()
        if len(line) < 4 or not line[:3].isalpha() or not line[3:].replace('.', '', 1).isdigit():
            print(f"Error: Invalid format in line '{line}'. Skipping.")
            continue

        driver_code = line[:3]
        lap_time = float(line[3:])
        if driver_code not in drivers:
            drivers[driver_code] = Driver(driver_code)
        drivers[driver_code].add_lap_time(lap_time)

    return race_location, drivers

def display_race_info(race_location, drivers):
    """
    Displays the race location and the fastest driver.
    """
    print(f"Race Location: {race_location}")
    fastest_driver = min(drivers.values(), key=lambda d: d.get_fastest_lap())
    print(f"Fastest Driver: {fastest_driver.code} with a time of {fastest_driver.get_fastest_lap():.3f} seconds")

def display_driver_stats(drivers):
    """
    Displays each driver's fastest and average lap times.
    """
    total_times, total_laps = 0, 0
    print("\nDriver Statistics:")
    for driver in drivers.values():
        total_times += sum(driver.lap_times)
        total_laps += len(driver.lap_times)
        print(f"Driver {driver.code} - Fastest Lap: {driver.get_fastest_lap():.3f} seconds, "
              f"Average Lap: {driver.get_average_lap():.3f} seconds, Total Laps: {len(driver.lap_times)}")
    
    overall_avg_time = total_times / total_laps if total_laps else 0
    print(f"\nOverall Average Lap Time: {overall_avg_time:.3f} seconds")
    print(f"Total Drivers: {len(drivers)}")

def display_sorted_times(drivers):
    """
    Displays the fastest lap times of all drivers in descending order.
    """
    sorted_drivers = sorted(drivers.values(), key=lambda d: d.get_fastest_lap(), reverse=True)
    print("\nFastest Times in Descending Order:")
    for driver in sorted_drivers:
        print(f"Driver {driver.code} - Fastest Lap: {driver.get_fastest_lap():.3f} seconds")

def export_results(filename, race_location, drivers):
    """
    Exports the results to a file.
    """
    with open(filename, 'w') as file:
        file.write(f"Race Location: {race_location}\n")
        fastest_driver = min(drivers.values(), key=lambda d: d.get_fastest_lap())
        file.write(f"Fastest Driver: {fastest_driver.code} with a time of {fastest_driver.get_fastest_lap():.3f} seconds\n")

        file.write("\nDriver Statistics:\n")
        total_times, total_laps = 0, 0
        for driver in drivers.values():
            total_times += sum(driver.lap_times)
            total_laps += len(driver.lap_times)
            file.write(f"Driver {driver.code} - Fastest Lap: {driver.get_fastest_lap():.3f} seconds, "
                       f"Average Lap: {driver.get_average_lap():.3f} seconds, Total Laps: {len(driver.lap_times)}\n")

        overall_avg_time = total_times / total_laps if total_laps else 0
        file.write(f"\nOverall Average Lap Time: {overall_avg_time:.3f} seconds\n")
        file.write(f"Total Drivers: {len(drivers)}\n")

        file.write("\nFastest Times in Descending Order:\n")
        sorted_drivers = sorted(drivers.values(), key=lambda d: d.get_fastest_lap(), reverse=True)
        for driver in sorted_drivers:
            file.write(f"Driver {driver.code} - Fastest Lap: {driver.get_fastest_lap():.3f} seconds\n")
    print(f"Results exported to '{filename}'.")

def main():
    """
    Main function to orchestrate the program flow.
    """
    if len(sys.argv) != 2:
        print("Usage: python timing_board.py <input_filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    race_location, drivers = read_file(input_filename)

    # Display data
    display_race_info(race_location, drivers)
    display_driver_stats(drivers)
    display_sorted_times(drivers)

    # Ask user if they want to export results
    export_choice = input("\nWould you like to export the results to a file? (y/n): ").strip().lower()
    if export_choice == 'y':
        output_filename = input("Enter the output filename: ").strip()
        export_results(output_filename, race_location, drivers)

if __name__ == "__main__":
    main()
