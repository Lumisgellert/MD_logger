import csv
import os
import Parameter as par


class CSVLogger:
    def __init__(self, folder="CSV-Datein"):
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)
        self._initialized = False
        self.filename = None

    def save(self, row):
        if not isinstance(row, (list, tuple)):
            raise ValueError("Row must be a list or tuple.")

        # Ordner sicherstellen
        os.makedirs(self.folder, exist_ok=True)

        self.filename = f"Messdaten_{par.time_start}.csv"

        filepath = os.path.join(self.folder, self.filename)

        write_header = not os.path.exists(filepath) or os.stat(filepath).st_size == 0

        with open(filepath, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow([
                    "time", "lat", "lon", "alt_GND[m]", "temp[°C]", "v[kmh]", "v[knts]",
                    "cours[deg]", "Acc_x[g]", "Acc_y[g]", "Acc_z[g]", "Gyro_x[deg_s]",
                    "Gyro_y[deg_s]", "Gyro_z[deg_s]", "sat[n]"
                ])
            writer.writerow(row)

        self._initialized = True

    def get_filepath(self):
        if self.filename is None:
            filename = f"Messdaten_{par.time_start}.csv"
        else:
            filename = self.filename
        return os.path.join(self.folder, filename)


# Beispielhafte Nutzung:
if __name__ == "__main__":
    logger = CSVLogger()
    logger.save(["Apfel", 3, 1.49, 6, 8, 9, 5, 4, 3, 6, 8, 9, 9, 7])
    logger.save(["Birne", 5, 2.10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])