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
    # http://10.100.127.232:8080
    # proxies = {
    #     'http': f'http://{PROXY_USER}:{PROXY_PWD}@http://proxy.prodemge.gov.br:8080',
    #     'https': f'http://{PROXY_USER}:{PROXY_PWD}@http://proxy.prodemge.gov.br:8080',
    # }
    res = requests.post(resource.custom['api_url'],
                        # proxies=proxies,
                        headers = {'User-Agent': 'splor',
                                   'X-Forwarded-For': '187.113.201.87',
                                   },
                        data = resource.custom['payload'],
                        stream = True)
    # breakpoint()
    res.raise_for_status()

    with open(resource.path, 'wb') as file:
        shutil.copyfileobj(res.raw, file)

extract_resource('base_orcam_despesa_item_fiscal')
