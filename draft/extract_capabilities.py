import ncclient
import os, re
import xml.etree.ElementTree as ET
from ncclient import manager
# Connect to the netconf server
with manager.connect(
    host="10.11.200.18",
    port=830,
    username="ocnos",
    password="ocnos",
    hostkey_verify=False,
) as conn:

    # Retrieve the YANG models from the server
    models = conn.server_capabilities
    print(models)

    # Iterate over the models
    for model in models:
        print(model)
        # Use a regular expression to extract the identifier
        match_name_space = re.search(r'http://openconfig.net/yang/(.+?)(/|\?)', model)
        match_identifier = re.search(r'module=(.+?)&', model)
        match_revision = re.search(r'revision=(.+?)(&|$)', model)
        if match_name_space and match_identifier and match_revision:
            namespace = 'yang/'+ match_name_space.group(1)
            identifier = match_identifier.group(1)
            revision = match_revision.group(1)

            # Retrieve the schema of the model as an XML string
            schema = conn.get_schema(identifier = identifier).xml
            root = ET.fromstring(schema)
            # Extract the 'data' element
            schema = root.find('./{urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring}data')

            # Generate the file name and path
            file_name = f'{identifier}.yang'
            file_path = os.path.join(namespace)

            # Create the directories and subdirectories if they do not exist
            if not os.path.exists(file_path):
                os.makedirs(file_path)

            # Write the schema to a file
            with open(os.path.join(file_path, file_name), 'w') as f:
                f.write(schema.text)