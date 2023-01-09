import ncclient, yaml, logging, sys
from ncclient.operations import RPCError
import re, traceback
from ncclient import manager

def fill_xml_template(template_file, values):
    # Read the XML template from the file
    with open(template_file, "r") as f:
        xml_template = f.read()

    # Replace all parameters in the template with their values
    #for param, value in values.items():
        #xml_template = re.sub(f"{{{param}}}", str(value), xml_template)

    # Return the filled-in XML template
    return xml_template

# Open the YAML file
with open("config.yaml", "r") as f:
    # Load the YAML data
    data = yaml.safe_load(f)
# Extract the IP address and interface name
ip_address = data["interface"]["ip_address"]
interface_name = data["interface"]["name"]
prefix = data["interface"]["prefix"]
old_ip_address = ip_address = data["interface"]["old_ip_address"]
interface2_name = data["interface2"]["name"]
ip2_address = data["interface2"]["ip_address"]
template_file = "xml_templates/write/openconfig-interfaces1.xml"

template_file = "interfaces_ip_addr_primary.xml"

values = {"interface_name": interface_name, "ip_address": ip_address, "prefix": prefix,"old_ip_address":old_ip_address, "interface2_name": interface2_name, "ip2_address": ip2_address}

xml_obj = fill_xml_template(template_file, values)
#print(xml_obj)




try:
    # Connect to the netconf server
    with manager.connect(
        host="10.11.200.19",
        port=830,
        username="ocnos",
        password="ocnos",
        hostkey_verify=False,
    ) as m:
        # Send the configuration to the netconf server
        # Edit the configuration on the device
        try:
            reply = m.edit_config(target="candidate", config=xml_obj, default_operation="merge")
            print(reply)
        except Exception as e:
            print(traceback.format_exc())
            print(e)

            logging.error(f"Error editing configuration: {e}")
            sys.exit(1)

        # Commit the changes and save them to the running configuration
        try:
            #m.discard_changes()
            m.commit()
            
        except RPCError as e:
            logging.error(f"Error committing and saving changes: {e}")
            m.discard_changes()
            sys.exit(1)
except Exception as e:
    logging.error(f"Error connecting to device: {e}")
    sys.exit(1)

logging.info("Configuration updated successfully")
