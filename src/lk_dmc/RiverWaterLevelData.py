from dataclasses import dataclass
from datetime import datetime

from utils import Log

from lk_dmc.GaugingStation import GaugingStation
from lk_dmc.River import River
from lk_dmc.RiverBasin import RiverBasin
from lk_dmc.WaterLevel import WaterLevel

log = Log("RiverWaterLevelData")


@dataclass
class RiverWaterLevelData:
    gauging_station_name: str
    time_str: str
    time_ut: int
    previous_water_level: float
    current_water_level: float
    remarks: str
    rising_or_falling: str
    rainfall_mm: float

    @property
    def gauging_station(self) -> GaugingStation:
        return GaugingStation.from_name(self.gauging_station_name)

    @classmethod
    def from_df_row(
        cls, row, current_river_basin: RiverBasin
    ) -> tuple["RiverWaterLevelData", str]:
        river_basin = RiverBasin.from_df_row(row) or current_river_basin
        river = River.from_df_row(row, river_basin)
        assert river, "River could not be created from row"

        unit = row[3].strip()
        assert unit in ("m", "ft"), f"Unknown unit: {unit}"
        remarks = row[9].strip()
        rising_falling = row[10].strip()
        rainfall = row[11].strip()

        gauging_station = GaugingStation.from_df_row(row, river, river_basin)
        previous_water_level = WaterLevel.from_str(row[7].strip(), unit)
        current_water_level = WaterLevel.from_str(row[8].strip(), unit)
        rainfall_mm = (
            float(rainfall)
            if rainfall and rainfall not in ("-", "N.A.")
            else 0.0
        )

        now = datetime.now()
        time_6am = now.replace(hour=6, minute=0, second=0, microsecond=0)

        rwld = cls(
            gauging_station_name=gauging_station.name,
            time_str=now.strftime("%Y-%m-%d 06:00:00"),
            time_ut=int(time_6am.timestamp()),
            previous_water_level=previous_water_level,
            current_water_level=current_water_level,
            remarks=remarks,
            rising_or_falling=rising_falling,
            rainfall_mm=rainfall_mm,
        )

        return rwld, river_basin

    @classmethod
    def from_dict(cls, d):
        return cls(**d)
