import json
import random
from flask import jsonify, request
from geoalchemy2 import functions
from sqlalchemy.sql import text

from app import db
from app.models import CriticalHabitat, HabitatMonitorLocation, MonitoringLocation, Species
from app.utils import km_to_degree

import app.ai as ai
from . import app


@app.route('/api/', methods=['GET'])
def home():
    return jsonify(message='Hello, API')


@app.route('/api/search', methods=['GET'])
def search():
    q = request.args.get('q')

    rs: list[tuple[dict, CriticalHabitat]] = (
        db.session.query(
            functions.ST_AsText(functions.ST_Centroid(CriticalHabitat.geom)).label('center'),
            CriticalHabitat,
        )
        .filter(text('waterbody ~* :q OR lead_region ~* :q'))
        .order_by(
            text('similarity(waterbody, :q) + similarity(lead_region, :q) DESC')
        )
        .params(q=q)
        .limit(10)
        .all()
    )

    return jsonify(
        [
            {
                'id': critical_habitat.id,
                'region': critical_habitat.lead_region,
                'name': f'{critical_habitat.waterbody} - {critical_habitat.common_name_en}',
                'centre': CriticalHabitat.trans_wkt_to_polygon_list(center),
            }
            for center, critical_habitat in rs
        ]
    )


@app.route('/api/list', methods=['GET'])
def list_():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))

    # unit: km
    distance = float(request.args.get('distance', 100))

    # 1 degree = 111.32km
    distance_degree = km_to_degree(distance)

    critical_habitats = (
        db.session.query(
            CriticalHabitat.id,
            functions.ST_AsText(CriticalHabitat.geom)
        )
        .filter(
            functions.ST_Distance(
                functions.ST_GeomFromText(
                    f'POINT({longitude} {latitude})',
                    4326
                ),
                CriticalHabitat.geom
            ) < distance_degree
        )
        .order_by(
            functions.ST_Distance(
                functions.ST_GeomFromText(
                    f'POINT({longitude} {latitude})',
                    4326
                ),
                CriticalHabitat.geom
            )
        )
        .limit(17)
        .all()
    )

    return jsonify(
        [
            {
                'id': id_,
                'polygon': CriticalHabitat.trans_wkt_to_polygon_list(polygon),
            }
            for id_, polygon in critical_habitats
        ]
    )


@app.route('/api/describe/<int:habitat_id>', methods=['GET'])
def describe(habitat_id: int):

    rs: list[CriticalHabitat, Species, dict] = (
        db.session.query(
            CriticalHabitat,
            Species,
            functions.ST_AsText(functions.ST_Centroid(CriticalHabitat.geom)).label('center'),
        )
        .filter(CriticalHabitat.id == habitat_id)
        .filter(CriticalHabitat.species_id == Species.id)
        .all()
    )

    monitoring_location = MonitoringLocation.query_by_habitat_id(habitat_id)

    return jsonify(
        {
            'name': rs[0][0].waterbody,
            'centre': CriticalHabitat.trans_wkt_to_polygon_list(rs[0][2]),
            'species': [
                {
                    'name': species.name,
                    'toxo': species.taxonomic_group,
                    'description': species.description,
                    'url': species.image_url,
                    'link': species.link,
                }
                for _, species, _ in rs
            ],
            'actions': [
                {
                    'name': 'swimming',
                    'status': 'NOT_RECOMMENDED',
                },
                {
                    'name': 'eating',
                    'status': 'NOT_RECOMMENDED',
                },
                {
                    'name': 'drinking',
                    'status': 'PERFORM_WELL' if monitoring_location and monitoring_location.drinkable else 'NOT_RECOMMENDED',
                },
            ],
            'quality': [
                {
                    'name': 'arsenic',
                    'value': monitoring_location.get_characteristic_value('Arsenic') if monitoring_location else None,
                    'status': monitoring_location.get_characteristic_status('Arsenic') if monitoring_location else 'PASS',
                },
                {
                    'name': 'copper',
                    'value': monitoring_location.get_characteristic_value('Copper') if monitoring_location else None,
                    'status': monitoring_location.get_characteristic_status('Copper') if monitoring_location else 'PASS',
                },
                {
                    'name': 'lead',
                    'value': monitoring_location.get_characteristic_value('Lead') if monitoring_location else None,
                    'status': monitoring_location.get_characteristic_status('Lead') if monitoring_location else 'PASS',
                },
            ],
        }
    )


@app.route('/api/analyze/<int:habitat_id>', methods=['GET'])
def analyze(habitat_id: int):

    monitoring_location = MonitoringLocation.query_by_habitat_id(habitat_id)

    data_is_empty = False
    if monitoring_location is None or monitoring_location.characteristic_data is None:
        data_is_empty = True
    else:
        characteristic_data = json.loads(monitoring_location.characteristic_data)
        characteristic_data_str_list = [
            f'{name} {value} µg/L'
            for name, value in characteristic_data.items()
        ]

    if data_is_empty:
        message = random.choice([
            'Try to explain some standard rules to someone who is trying to go to an open water.',
            'Is there any common sense one should follow when he is trying to go to an open water.',
            'Try to explain the standard rules when somebody want to go to the open water.',
            'Give some suggestions to someone who plans to go to open water and have some outdoor activities',
        ])
        message += ' And do not using positive words in the begin.'

    else:
        message = "There is an open water's monitor data, please help me to analyze if the person near this water, what should he/she notice?"
        message += ', '.join(characteristic_data_str_list)

    message += '\n Give me a summation of the above within five sentences.'

    analyze_result = ai.analyze(message)

    return jsonify(
        {
            'content': analyze_result
        }
    )
