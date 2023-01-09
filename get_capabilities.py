
from ncclient import manager
from rich import print
import re

if __name__ == "__main__":

    device = {
        "host": "10.11.200.19",
        "port": 830,
        "username": "ocnos",
        "password": "ocnos",
        "hostkey_verify": False,
    }
    

    with manager.connect(**device) as nconf:
        models = list(nconf.server_capabilities)
        print(models)

        for model in models:
            # Use a regular expression to extract the identifier
            print(model)
            '''match_name_space = re.search(r'(.+?)\?module', model)
            match_identifier = re.search(r'module=(.+?)&', model)
            match_revision = re.search(r'revision=(.+?)(&|$)', model)
            if match_name_space and match_identifier and match_revision:
                name_space = match_name_space.group(1)
                identifier = match_identifier.group(1)
                revision = match_revision.group(1)
                print(name_space, identifier, revision)
            else:
                print( "no parameters for ", model)

        #schema = nconf.get_schema('zebm-cli')
        #print(schema)'''