import ncclient, yaml, logging, sys
from ncclient.operations import RPCError
import re, traceback
from ncclient import manager

def fill_xml_config(config):
    # Read the XML template from the file
    with open("xml_templates/config.xml", "r") as f:
        xml_template = f.read()
    xml_template = re.sub("{configuration}", config, xml_template)
    return xml_template

def fill_xml_template(template_file, configuration):
    # Read the XML template from the file
    with open(template_file, "r") as f:
        xml_template = f.read()
    xml_template = re.sub("{operation}", configuration["operation"], xml_template)
    for param, value in configuration["content"].items():
        xml_template = re.sub(f"{{{param}}}", str(value), xml_template)
    return xml_template

configuration_list = []
configuration = {"resource": "vlan", "operation": "merge", "content": {"bridge":"1","vlan-id":"212","name":"vlan212"}}
configuration_list.append(configuration)
configuration = {"resource": "vlan", "operation": "delete", "content": {"bridge":"1","vlan-id":"2","name":"vlan2"}}
#configuration_list.append(configuration)
xml_obj = ""
for configuration in configuration_list:
    template_file = "xml_templates/"+configuration["resource"]+"/"+configuration["resource"]+".xml"
    xml_obj += fill_xml_template(template_file, configuration)
xml_configuration=fill_xml_config(xml_obj)
print(xml_configuration)



if __name__ == '__main__':
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
                reply = m.edit_config(target="candidate", config=xml_configuration)
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
