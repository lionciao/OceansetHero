import fiona
import geopandas as gpd
from geoalchemy2 import Geometry
from geopandas.geodataframe import GeoDataFrame
from sqlalchemy import create_engine

from app.settings import SQLALCHEMY_DATABASE_URI


GDB_FILE_PATH = ''


def extract_gdf_from_file(file_path: str) -> GeoDataFrame:

    # Get all the layers from the .gdb file
    layers = fiona.listlayers(file_path)

    for layer in layers:
        return gpd.read_file(file_path, layer=layer)


def trans_gdf_to_critical_habitat_df(gdf: GeoDataFrame) -> GeoDataFrame:

    t_gdf = gdf.to_crs(epsg='4326')

    t_gdf['largest_polygon'] = t_gdf['geometry'].apply(lambda multipolygon: max(multipolygon.geoms, key=lambda polygon: polygon.area))
    f_t_gdf = t_gdf[[
        'Nom_commun_ANG',
        'Population_ANG',
        'Nom_commun_FR',
        'Population_FR',
        'Scientifique',
        'Taxon',
        'Type_eco',
        'Plan_d_eau',
        'Statut_LEP',
        'Statut_HE',
        'Commentaire',
        'Région_responsable',
        'Région_de_soutien',
        'Lien_d_espèce',
        'Zone_Km2',
        'Shape_Length',
        'Shape_Area',
        'largest_polygon',
    ]]

    critical_habitat_df = f_t_gdf.rename(columns={
        'Nom_commun_ANG': 'common_name_en',
        'Population_ANG': 'population_en',
        'Nom_commun_FR': 'common_name_fr',
        'Population_FR': 'population_fr',
        'Scientifique': 'scientific_name',
        'Taxon': 'taxon',
        'Type_eco': 'eco_type',
        'Plan_d_eau': 'waterbody',
        'Statut_LEP': 'sara_status',
        'Statut_HE': 'ch_status',
        'Commentaire': 'comment',
        'Région_responsable': 'lead_region',
        'Région_de_soutien': 'support_region',
        'Lien_d_espèce': 'species_link',
        'Zone_Km2': 'area_km2',
        'Shape_Length': 'shape_length',
        'Shape_Area': 'shape_area',
        'largest_polygon': 'geom',
    })

    return critical_habitat_df.set_geometry('geom')


def load_critical_habitat_df_to_db(critical_habitat_df: GeoDataFrame) -> None:

    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    with engine.connect() as conn:
        critical_habitat_df.to_postgis(
            name='critical_habitat',
            con=conn,
            if_exists='append',
            index=False,
            dtype={'geom': Geometry(geometry_type='POLYGON', srid=4326)},
        )


if __name__ == '__main__':
    gdf = extract_gdf_from_file(GDB_FILE_PATH)
    critical_habitat_df = trans_gdf_to_critical_habitat_df(gdf)
    load_critical_habitat_df_to_db(critical_habitat_df)
