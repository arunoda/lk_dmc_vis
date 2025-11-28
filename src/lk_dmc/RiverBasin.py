from dataclasses import dataclass


@dataclass
class RiverBasin:
    code: str
    name: str

    @staticmethod
    def from_df_row(row) -> "RiverBasin | None":
        river_basin_str = row[0].strip()
        if not river_basin_str:
            return None
        parts = river_basin_str.split("\n")
        basin_name = parts[0].strip()
        basin_code = parts[1].strip("()") if len(parts) > 1 else ""
        return RiverBasin(code=basin_code, name=basin_name)
