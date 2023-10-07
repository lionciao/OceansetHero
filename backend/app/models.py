from __future__ import annotations
import json
import geojson

import shapely
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geometry

from app import db
from app.settings import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI)


class CriticalHabitat(db.Model):
    __tablename__ = 'critical_habitat'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    common_name_en: Mapped[str] = mapped_column(db.String, nullable=False)
    population_en: Mapped[str] = mapped_column(db.String, nullable=True)
    common_name_fr: Mapped[str] = mapped_column(db.String, nullable=False)
    population_fr: Mapped[str] = mapped_column(db.String, nullable=True)
    scientific_name: Mapped[str] = mapped_column(db.String, nullable=False)
    taxon: Mapped[str] = mapped_column(db.String, nullable=False)
    eco_type: Mapped[str] = mapped_column(db.String, nullable=False)
    waterbody: Mapped[str] = mapped_column(db.String, nullable=False)
    sara_status: Mapped[str] = mapped_column(db.String, nullable=False)
    ch_status: Mapped[str] = mapped_column(db.String, nullable=False)
    comment: Mapped[str] = mapped_column(db.String, nullable=True)
    lead_region: Mapped[str] = mapped_column(db.String, nullable=False)
    support_region: Mapped[str] = mapped_column(db.String, nullable=True)
    species_id: Mapped[int] = mapped_column(ForeignKey('species.id'))
    species_link: Mapped[str] = mapped_column(db.String, nullable=False)
    area_km2: Mapped[float] = mapped_column(db.Float, nullable=False)
    shape_length: Mapped[float] = mapped_column(db.Float, nullable=False)
    shape_area: Mapped[float] = mapped_column(db.Float, nullable=False)
    geom: Mapped[Geometry] = mapped_column(Geometry(geometry_type='POLYGON', srid=4326))

    @staticmethod
    def trans_wkt_to_polygon_list(wkt_str: str) -> list:
        return geojson.Feature(geometry=shapely.wkt.loads(wkt_str), properties={})['geometry']['coordinates']


class Species(db.Model):
    __tablename__ = 'species'

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)
    taxonomic_group: Mapped[str] = mapped_column(db.String, nullable=False)
    description: Mapped[str] = mapped_column(db.String, nullable=True)
    protection: Mapped[str] = mapped_column(db.String, nullable=True)
    link: Mapped[str] = mapped_column(db.String, nullable=False)
    image_url: Mapped[str] = mapped_column(db.String, nullable=False)


class MonitoringLocation(db.Model):
    __tablename__ = 'monitoring_location'
    __mapper_args__ = {
        'primary_key': ('name',),
    }

    id: Mapped[str] = mapped_column(db.String, nullable=True)
    name: Mapped[str] = mapped_column(db.String, nullable=True)
    latitude: Mapped[float] = mapped_column(db.Float, nullable=True)
    longitude: Mapped[float] = mapped_column(db.Float, nullable=True)
    horizontal_coordinate_reference_system: Mapped[str] = mapped_column(db.String, nullable=True)
    horizontal_accuracy_measure: Mapped[float] = mapped_column(db.Float, nullable=True)
    horizontal_accuracy_unit: Mapped[float] = mapped_column(db.Float, nullable=True)
    vertical_measure: Mapped[float] = mapped_column(db.Float, nullable=True)
    vertical_unit: Mapped[float] = mapped_column(db.Float, nullable=True)
    type: Mapped[str] = mapped_column(db.String, nullable=True)
    point: Mapped[Geometry] = mapped_column(Geometry(geometry_type='POINT', srid=4326))
    drinkable: Mapped[bool] = mapped_column(db.Boolean, nullable=True)
    characteristic_data: Mapped[str] = mapped_column(db.String, nullable=True)

    @staticmethod
    def query_by_habitat_id(habitat_id: int) -> MonitoringLocation | None:
        return (
            db.session.query(
                MonitoringLocation
            )
            .filter(HabitatMonitorLocation.habitat_id == habitat_id)
            .filter(MonitoringLocation.name == HabitatMonitorLocation.monitoring_location_name)
            .first()
        )

    def get_characteristic_value(self: MonitoringLocation, characteristic_name: str) -> float:
        characteristic_data = json.loads(self.characteristic_data)
        return characteristic_data.get(characteristic_name)

    def get_characteristic_status(self: MonitoringLocation, characteristic_name: str) -> str:
        characteristic_data = json.loads(self.characteristic_data)

        # @Arsenic    砷         10 ug/L
        # @Copper     銅       2000 ug/L
        # @Lead       鉛         10 ug/L
        # @Chromium   鉻         50 ug/L
        # @Mercury    汞          6 ug/L
        # @Nitrate    硝酸根      50 ug/L
        # @Nickel     鎳         70 ug/L
        # @Barium     鋇       1300 ug/L
        # @Manganese  錳         80 ug/L

        characteristic_threshold_config = {
            'Arsenic': 10,
            'Copper': 2000,
            'Lead': 10,
            'Chromium': 50,
            'Mercury': 6,
            'Nitrate': 50,
            'Nickel': 70,
            'Barium': 1300,
            'Manganese': 80,
        }

        value = characteristic_data.get(characteristic_name)
        if value is None or value < characteristic_threshold_config[characteristic_name]:
            return 'PASS'
        else:
            return 'INVALID'


class HabitatMonitorLocation(db.Model):
    __tablename__ = 'habitat_monitoring_location'
    __mapper_args__ = {
        'primary_key': ('monitoring_location_name', 'habitat_id'),
    }

    monitoring_location_name: Mapped[str] = mapped_column(db.String)
    habitat_id: Mapped[int] = mapped_column(db.Integer)
    distance: Mapped[float] = mapped_column(db.Float)


def create_table() -> None:
    from app import app

    with app.app_context():
        db.create_all()
