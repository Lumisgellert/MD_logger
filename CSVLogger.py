import csv
import os
from datetime import datetime


class CSVLogger:
    def __init__(self, base_filename="Messdaten", folder="CSV-Datein"):
        self.base_filename = base_filename
        self.folder = folder
        os.makedirs(self.folder, exist_ok=True)
        self.filename = self._generate_unique_filename()
        self.filepath = os.path.join(self.folder, self.filename)
        self._initialized = False

    def _generate_unique_filename(self):
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"{self.base_filename}_{timestamp}.csv"
        counter = 1

        while os.path.exists(os.path.join(self.folder, filename)):
            filename = f"{self.base_filename}_{timestamp}_{counter}.csv"
            counter += 1

        return filename

    def save(self, row):
        if not isinstance(row, (list, tuple)):
            raise ValueError("Row must be a list or tuple.")

        write_header = not self._initialized and not os.path.exists(self.filepath)

        with open(self.filepath, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if write_header:
                writer.writerow(["time", "lat", "lon", "alt_GND[m]", "temp[°C]", "v[kmh]", "v[knts]", "cours[deg]", "Acc_x[g]", "Acc_y[g]", "Acc_z[g]", "Gyro_x[deg_s]", "Gyro_y[deg_s]", "Gyro_z[deg_s]", "sat[n]"])
            writer.writerow(row)

        self._initialized = True
        #print(f"Zeile gespeichert in {self.filename}: {row}")

    def get_filepath(self):
        return self.filepath


# Beispielhafte Nutzung:
if __name__ == "__main__":
    logger = CSVLogger()
    logger.save(["Apfel", 3, 1.49,6,8,9,5,4,3,6,8,9,9])
    logger.save(["Birne", 5, 2.10])
