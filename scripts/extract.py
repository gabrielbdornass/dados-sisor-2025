import os
from dotenv import load_dotenv
from frictionless import Package
import logging
import requests
import shutil

load_dotenv()

logger = logging.getLogger(__name__)

def extract_resource(resource_name: str, descriptor: str = 'datapackage.yaml'):
    logger.info(f'Extracting resource {resource_name}')
    PROXY_USER = os.environ.get('PROXY_USER')
    PROXY_PWD = os.environ.get('PROXY_PWD')
    package = Package(descriptor)
    resource = package.get_resource(resource_name)
    proxies = {
        f'http://{PROXY_USER}:{PROXY_PWD}@proxycamg.prodemge.gov.br:8080'
    }
    res = requests.post(resource.custom['api_url'],
                        proxies=proxies,
                        headers = {'User-Agent': 'splor'},
                        data = resource.custom['payload'],
                        stream = True)
    res.raise_for_status()

    with open(resource.path, 'wb') as file:
        shutil.copyfileobj(res.raw, file)
