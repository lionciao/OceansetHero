import datetime
import json
import re

import inflection
import numpy as np
import pandas as pd
import shapely
from geopandas import GeoDataFrame
from geoalchemy2 import Geometry
from sqlalchemy import create_engine

from app.settings import SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URI)

csv_files = [
    "2022_water_quality_data_collected_for_CIMP197.csv",
    "Athabasca_Chipewyan_First_Nation_-_Community_Based_Monitoring_Pr.csv",
    # "BC_Environmental_Monitoring_System_Data.csv",
    "CIMP167__Changes_in_dissolved_organic_carbon_quality_and_quantit.csv",
    "CIMP_161_Cumulative_Impacts_Monitoring_of_Aquatic_Ecosystem_Heal.csv",
    "CIMP_174_The_Impacts_of_Recent_Wildfires_on_Northern_Stream_Ecos.csv",
    "CIMP_177_The_influence_of_forest_fires_on_metal_deposition_to_la.csv",
    "CIMP_193_Understanding_changes_in_aquatic_ecosystem_health_and_w.csv",
    "CIMP_199_Water_quality_of_peatland_ponds_and_streams_on_a_latitu.csv",
    "CIMP_211_Impacts_of_Permafrost_Thaw_Slump_Extent_Severity_and_Pe.csv",
    "Dehcho_Region_Water_Quality_Data.csv",
    "Equipping_communities_in_data-deficient_areas.csv",
    "Fort_Nelson_First_Nation_Water_Quality_Monitoring.csv",
    "Kagee_Tu_First_Nation_KTFN_Community_Based_Monitoring_of_Kakisa_.csv",
    "LSWC_tributary_monitoring_program.csv",
    "Lac_La_Biche_County_Lake_Water_Quality_Monitoring_Program.csv",
    "LakeKeepers_Water_Quality_Data.csv",
    "LakePulse.csv",
    "LakeWatch_Water_Quality_Data.csv",
    "Living_Lakes_Canada_-_National_Lake_Blitz.csv",
    "Mackenzie_Hg_in_streamwater_survey_2018-2020.csv",
    "Mikisew_Cree_First_Nation_-_Community_Based_Monitoring_Program.csv",
    # "NWT-wide_Community-based_Monitoring_Program.csv",
    "Peace_River_Regional_District_Water_Quality_Baseline_-_Municipal.csv",
    "Seasonal_Monitoring_of_Smith_Creek_and_Scotty_Creek_2019-2021.csv",
    "Slave_River_Spring_Water_Quality_Sampling.csv",
    "Smiths_Landing_First_Nation_Community_Based_Monitoring_Program.csv",
    "Transboundary_Rivers_Water_Quality_Monitoring_Program.csv",
    "University_of_Regina_Citizen_Science_Data.csv",
    "Upper_Athabasca_Community_Based_Monitoring_UATHCBM.csv",
]


def camel_to_snake(camel_str: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


df_list = []
for csv_file in csv_files:
    print(csv_file)
    df_list.append(
        pd.read_csv(
            f'./water_data/{csv_file}'
        )
    )


df_concat = pd.concat(df_list)
df_concat = df_concat.rename(columns=lambda x: inflection.underscore(x))


df_location = df_concat[[
    'monitoring_location_id',
    'monitoring_location_name',
    'monitoring_location_latitude',
    'monitoring_location_longitude',
    'monitoring_location_horizontal_coordinate_reference_system',
    'monitoring_location_horizontal_accuracy_measure',
    'monitoring_location_horizontal_accuracy_unit',
    'monitoring_location_vertical_measure',
    'monitoring_location_vertical_unit',
    'monitoring_location_type',
]]
df_location = df_location.rename(columns=lambda x: x.replace('monitoring_location_', ''))
df_location['point'] = df_location.apply(lambda x: shapely.wkt.loads(f'POINT({x["longitude"]} {x["latitude"]})'), axis=1)
df_location = df_location.drop_duplicates()

df_concat['activity_start_time'] = df_concat['activity_start_time'].fillna('00:00:00')
df_concat['activity_start_dt'] = df_concat.apply(lambda x: datetime.datetime.strptime(f"{x['activity_start_date']} {x['activity_start_time']}", '%Y-%m-%d %H:%M:%S'), axis=1)

df_concat_latest = df_concat.sort_values('activity_start_dt', ascending=True).groupby(['characteristic_name', 'monitoring_location_name']).tail(1)

df_concat = df_concat.drop(
    columns=[
        'monitoring_location_latitude',
        'monitoring_location_longitude',
        'monitoring_location_horizontal_coordinate_reference_system',
        'monitoring_location_horizontal_accuracy_measure',
        'monitoring_location_horizontal_accuracy_unit',
        'monitoring_location_vertical_measure',
        'monitoring_location_vertical_unit',
        'monitoring_location_type',
    ],
)

df_concat_latest = df_concat.sort_values('activity_start_dt', ascending=True).groupby(['characteristic_name', 'monitoring_location_name']).tail(1)


def trans_result_value(data) -> float:
    if data['result_unit'] == 'ng/L':
        return data['result_value'] / 1000
    elif data['result_unit'] in (
        'ug/g',
        'ppm',
        'mg/kg',
        'mg/L',
    ):
        return data['result_value'] * 1000
    else:
        return data['result_value']


df_concat_latest['general_result_value'] = df_concat_latest.apply(trans_result_value, axis=1)

cannot_drink_set = set(
    df_concat_latest[
        (
            (df_concat_latest['characteristic_name'] == 'Arsenic')
            & (df_concat_latest['general_result_value'] > 10)
        )
        | (
            (df_concat_latest['characteristic_name'] == 'Copper')
            & (df_concat_latest['general_result_value'] > 2000)
        )
        | (
            (df_concat_latest['characteristic_name'] == 'Lead')
            & (df_concat_latest['general_result_value'] > 10)
        )
        | (
            (df_concat_latest['characteristic_name'] == 'Chromium')
            & (df_concat_latest['general_result_value'] > 50)
        )
        | (
            (df_concat_latest['characteristic_name'] == 'Mercury')
            & (df_concat_latest['general_result_value'] > 6)
        )
        | (
            (df_concat_latest['characteristic_name'] == 'Nitrate')
            & (df_concat_latest['general_result_value'] > 50)
        )
        | (
            (df_concat_latest['characteristic_name'] == 'Nickel')
            & (df_concat_latest['general_result_value'] > 70)
        )
        | (
            (df_concat_latest['characteristic_name'] == 'Barium')
            & (df_concat_latest['general_result_value'] > 1300)
        )
        | (
            (df_concat_latest['characteristic_name'] == 'Manganese')
            & (df_concat_latest['general_result_value'] > 80)
        )
    ]['monitoring_location_name']
)


need_characteristic_names = [
    'Arsenic',
    'Copper',
    'Lead',
    'Chromium',
    'Mercury',
    'Nitrate',
    'Nickel',
    'Barium',
    'Manganese',
]


def find_characteristic_general_result_value(row) -> str | None:
    general_result_value = df_concat_latest[
        (df_concat_latest['monitoring_location_name'] == row['name'])
        & (df_concat_latest['characteristic_name'].isin(need_characteristic_names))
    ][['general_result_value', 'characteristic_name']]

    values = general_result_value.to_dict('records')
    if values:
        return json.dumps({
            value['characteristic_name']: value['general_result_value']
            for value in values
            if not np.isnan(value['general_result_value'])
        })

    return None


df_location['drinkable'] = df_location.apply(lambda x: x['name'] not in cannot_drink_set, axis=1)
df_location['characteristic_data'] = df_location.apply(find_characteristic_general_result_value, axis=1)

gdf = GeoDataFrame(df_location, crs='EPSG:4326', geometry=df_location['point'])
gdf = gdf.set_geometry('point')
gdf = gdf.set_crs(epsg='4326')
del gdf['geometry']
'''
SELECT
    ch.id AS id,
    ml."name" AS monitoring_location_name,
    ST_DISTANCE(ch.geom, ml.geom) AS distance
FROM
    critical_habitat ch
JOIN
    monitoring_location ml ON ST_DISTANCE(ch.geom, ml.geom) < 0.2
ORDER BY
    ch.id,
    distance;
'''
with engine.connect() as conn:
    gdf.to_postgis(
        'monitoring_location',
        conn,
        if_exists="replace",
        index=False,
        dtype={'point': Geometry(geometry_type='POINT', srid=4326)},
    )
    df_concat.to_sql(
        name='water_quality',
        con=conn,
        if_exists="replace",
        index=False,
    )

    df_concat_latest.to_sql(
        name='water_quality_latest',
        con=conn,
        if_exists="replace",
        index=False,
    )

    df = pd.read_sql(
        '''
        SELECT
        critical_habitat. "id" AS habitat_id,
        monitoring_location. "name" AS monitoring_location_name,
        ST_DISTANCE("point", geom) AS distance
        FROM
        critical_habitat
        JOIN monitoring_location ON ST_DISTANCE("point", geom) < 0.2
        ORDER BY
        critical_habitat. "id",
        ST_DISTANCE("point", geom)
        ''',
        conn
    )
    df = df.sort_values(['habitat_id', 'distance'], ascending=True).groupby(['habitat_id']).tail(1)
    df.to_sql(
        name='habitat_monitoring_location',
        con=conn,
        if_exists="replace",
        index=False,
    )
