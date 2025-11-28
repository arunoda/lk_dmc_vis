from dataclasses import dataclass


@dataclass
class GaugingStation:
    name: str
    alert_level_m: float
    minor_flood_level_m: float
    major_flood_level_m: float

    @staticmethod
    def convert_to_meters(value: float, unit: str) -> float:
        return value * 0.3048 if unit.lower() == "ft" else value

    @classmethod
    def from_df_row(cls, row) -> "GaugingStation":
        name = row[2].strip()
        unit = row[3].strip()
        alert_level = row[4].strip()
        minor_flood_level = row[5].strip()
        major_flood_level = row[6].strip()

        alert_m = float(alert_level) if alert_level else 0.0
        minor_m = float(minor_flood_level) if minor_flood_level else 0.0
        major_m = float(major_flood_level) if major_flood_level else 0.0

        return cls(
            name=name,
            alert_level_m=cls.convert_to_meters(alert_m, unit),
            minor_flood_level_m=cls.convert_to_meters(minor_m, unit),
            major_flood_level_m=cls.convert_to_meters(major_m, unit),
        )
