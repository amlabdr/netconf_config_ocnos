import requests
import re

# URL of the OpenConfig YANG models repository
repository_url = "https://github.com/openconfig/public/tree/master/release/models"

# Regular expression to match the YANG model file names
model_pattern = re.compile(r"^.*\.yang$")

# HTTP headers to send with the requests
headers = {
    "Accept": "application/vnd.github+json"
}

# Fetch the list of files in the repository
response = requests.get(repository_url, headers=headers)
response.raise_for_status()

# Extract the list of YANG model files from the response
models = [f for f in response.json()["tree"] if model_pattern.match(f["path"])]

# Fetch the contents of each YANG model file
for model in models:
    # URL of the YANG model file
    model_url = model["url"]

    # Fetch the contents of the YANG model file
    response = requests.get(model_url, headers=headers)
    response.raise_for_status()

    # Extract the YANG model text from the response
    yang_model = response.json()["content"]

    # Convert the YANG model to an XML template
    xml_template = yang_model_to_xml_template(yang_model)

    # Save the XML template to a file
    with open(f"{model['path']}.xml", "w") as f:
        f.write(xml_template)
