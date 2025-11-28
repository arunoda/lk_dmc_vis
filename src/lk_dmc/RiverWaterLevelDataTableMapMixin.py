import os

import matplotlib.pyplot as plt
from gig import Ent, EntType
from utils import Log

from lk_dmc.GaugingStation import GaugingStation
from lk_dmc.Location import Location
from lk_dmc.River import River

log = Log("RiverWaterLevelDataTableMapMixin")


class RiverWaterLevelDataTableMapMixin:

    def __draw_map__(self, ax):
        district_ents = Ent.list_from_type(EntType.DISTRICT)
        for ent in district_ents:
            geo = ent.geo()
            geo.plot(
                ax=ax,
                color=(0.9, 0.9, 0.9),
                edgecolor=(0.75, 0.75, 0.75),
                linewidth=0.5,
            )

    def __draw_rivers__(self, ax):
        rivers = River.list_all()
        for river in rivers:
            locations = [
                GaugingStation.from_name_safe(name)
                or Location.from_name(name)
                for name in river.location_names
            ]
            n_locations = len(locations)
            for i in range(n_locations - 1):
                loc1 = locations[i]
                loc2 = locations[i + 1]
                y1, x1 = loc1.lat_lng
                y2, x2 = loc2.lat_lng

                dx = x2 - x1
                dy = y2 - y1

                dmin = min(abs(dx), abs(dy))
                xmid = x1 + dmin * dx / abs(dx)
                ymid = y1 + dmin * dy / abs(dy)

                ax.plot(
                    [x1, xmid, x2],
                    [y1, ymid, y2],
                    color=(0.6, 0.6, 0.9),
                    linewidth=2,
                    alpha=0.7,
                )

    def __draw_locations__(self, ax):
        locations = Location.list_all()
        for location in locations:
            lat, lng = location.lat_lng
            ax.plot(
                lng,
                lat,
                marker="o",
                markersize=5,
                color="grey",
            )

    def __draw_station__(self, ax, rwld):
        station = rwld.gauging_station
        lat, lng = station.lat_lng
        color = "green"

        if rwld.current_water_level >= station.major_flood_level:
            color = "red"

        elif rwld.current_water_level >= station.minor_flood_level:
            color = "orange"

        elif rwld.current_water_level >= station.alert_level:
            color = "yellow"

        ax.plot(
            lng,
            lat,
            marker="o",
            markersize=10,
            color=color,
        )
        ax.text(
            lng + 0.03,
            lat,
            station.name,
            fontsize=5,
            color="black",
        )

    def __draw_stations__(self, ax):
        for rwld in self.d_list:
            self.__draw_station__(ax, rwld)

    def draw(self):
        fig, ax = plt.subplots(figsize=(9, 16))

        self.__draw_map__(ax)
        self.__draw_rivers__(ax)
        self.__draw_locations__(ax)
        self.__draw_stations__(ax)
        ax.set_axis_off()
        for spine in ax.spines.values():
            spine.set_visible(False)

        image_path = os.path.join("images", "map.png")
        fig.savefig(image_path, dpi=300, bbox_inches="tight", pad_inches=0)
        log.info(f"Wrote {image_path}")
