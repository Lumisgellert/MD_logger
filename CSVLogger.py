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
        if not par.time_start:
            raise ValueError("time_start wurde noch nicht gesetzt!")

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
                    "time", "lat", "lon", "alt_GND[m]", "v[kmh]",
                    "v[knts]", "cours[deg]",
                    "Acc_x0[g]", "Acc_y0[g]", "Acc_z0[g]", "Gyro_x0[deg_s]", "Gyro_y0[deg_s]", "Gyro_z0[deg_s]",
                    "Acc_x1[g]", "Acc_y1[g]", "Acc_z1[g]", "Gyro_x1[deg_s]", "Gyro_y1[deg_s]", "Gyro_z1[deg_s]",
                    "Acc_x2[g]", "Acc_y2[g]", "Acc_z2[g]", "Gyro_x2[deg_s]", "Gyro_y2[deg_s]", "Gyro_z2[deg_s]",
                    "Acc_x3[g]", "Acc_y3[g]", "Acc_z3[g]", "Gyro_x3[deg_s]", "Gyro_y3[deg_s]", "Gyro_z3[deg_s]",
                    "Acc_x4[g]", "Acc_y4[g]", "Acc_z4[g]", "Gyro_x4[deg_s]", "Gyro_y4[deg_s]", "Gyro_z4[deg_s]",
                    "temp0[°C]", "temp1[°C]", "temp2[°C]", "temp3[°C]", "temp4[°C]",
                    "sat[n]"
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