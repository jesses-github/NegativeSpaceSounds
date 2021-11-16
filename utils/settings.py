import os
import json
from requests.structures import CaseInsensitiveDict

BOUNCES_FOLDER = '1DivoBumUG6G6qJebYiU7b5Ylmj01vmsf'
clients_file = os.path.join(os.getcwd(), 'resources', 'clients.json')
with open(clients_file) as f:
    CLIENTS = CaseInsensitiveDict(json.load(f))
# CLIENTS = CaseInsensitiveDict(CLIENTS)
user_name = "Jesse Williams"
user_email = "jesse@negativespacesounds.com"