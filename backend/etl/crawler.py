import requests
import json
from sqlalchemy import create_engine, distinct, insert, select, update
from sqlalchemy.orm import Session

from app.models import CriticalHabitat, Species
from app.settings import SQLALCHEMY_DATABASE_URI


CONFIG_API_BASE_URL = 'https://species-registry.canada.ca/sar-config.json'
API_BASE_URL = 'https://ecprccsarsrch.search.windows.net/indexes/speblobidxen/docs/search?api-version=2017-11-11'
IMAGE_BASE_URL = 'https://wildlife-species.az.ec.gc.ca/species-risk-registry/images/photos/'

engine = create_engine(SQLALCHEMY_DATABASE_URI)


def get_species_links() -> list[str]:
    with Session(engine) as session:
        return list(session.execute(select(distinct(CriticalHabitat.species_link))).scalars().all())


def extract_config_data_from_api() -> dict:
    resp = requests.get(CONFIG_API_BASE_URL, timeout=10)
    return resp.json()


def trans_config_data_to_api_key_and_taxonomic_group_config(config_data: dict) -> tuple[str, dict]:
    api_key = config_data['documents']['apiKey']

    species_columns = config_data['species']['en']['columns']
    for species_column in species_columns:
        if species_column['name'] == 'taxonomyId':
            taxonomic_group_config = species_column['options']

    return api_key, taxonomic_group_config


def extract_species_info_response_from_api(link: str, api_key: str) -> dict:

    species_id = link.split('/')[-1]

    headers = {'api-key': api_key}
    body = {
        'filter': f"id eq '{species_id}'",
        'select': 'id,profiles,cosewicCommonName,imageFileName,taxonomyId',
    }

    resp = requests.post(API_BASE_URL, headers=headers, json=body, timeout=10)
    print(link)
    return resp.json()


def trans_response_to_species_info(link: str, response: dict, taxonomic_group_config: dict) -> dict:

    response_value = response['value'][0]

    name = response_value['cosewicCommonName']
    profiles = json.loads(response_value['profiles'][0])
    description = profiles['description']
    protection = profiles['otherProtection']
    image_name = response_value['imageFileName']
    taxonomy_id = response_value['taxonomyId']

    taxonomic_group = ''
    for taxonomic in taxonomic_group_config:
        if taxonomic['id'] == taxonomy_id:
            taxonomic_group = taxonomic['label']

    print(name)
    return {
        'link': link,
        'name': name,
        'description': description,
        'protection': protection,
        'image_url': f'{IMAGE_BASE_URL}{image_name}',
        'taxonomic_group': taxonomic_group
    }


def load_species_info_list_to_db(species_info_list: list[dict]) -> None:
    with Session(engine) as session:
        session.execute(
            insert(Species),
            species_info_list,
        )
        session.commit()


def create_relation_between_critical_habitat_and_species() -> None:
    with Session(engine) as session:
        session.execute(
            update(CriticalHabitat).values(species_id=Species.id).where(CriticalHabitat.species_link == Species.link)

        )
        session.commit()


if __name__ == '__main__':

    species_links = get_species_links()

    config_data = extract_config_data_from_api()

    api_key, taxonomic_group_config = trans_config_data_to_api_key_and_taxonomic_group_config(config_data)

    species_info_list = []
    for link in species_links:
        response = extract_species_info_response_from_api(link, api_key)
        species_info_list.append(trans_response_to_species_info(link, response, taxonomic_group_config))

    load_species_info_list_to_db(species_info_list)
    create_relation_between_critical_habitat_and_species()
