import ncclient, yaml, logging, sys
from ncclient.operations import RPCError
import xml.etree.ElementTree as ET


from ncclient import manager


def fill_template(template_file, parameters):
    # Parse the XML template
    tree = ET.parse(template_file)
    root = tree.getroot()
    print(root.findall(".//*[@param]"))
    # Find all elements with a "param" attribute and fill in the value
    for elem in root.findall(".//***[@param]"):
        param_name = elem.attrib["param"]
        if param_name in parameters:
            elem.text = str(parameters[param_name])
        else:
            elem.text = ""
    # Return the filled-in XML object
    return ET.tostring(root, encoding="unicode")


# Open the YAML file
with open("config.yaml", "r") as f:
    # Load the YAML data
    data = yaml.safe_load(f)
# Extract the IP address and interface name
ip_address = data["interface"]["ip_address"]
interface_name = data["interface"]["name"]
prefix = data["interface"]["prefix"]


template_file = "xml_templates/write/openconfig-interfaces-copy.xml"
parameters = {"interface_name": interface_name, "ip_address": ip_address, "prefix": prefix}
xml_config = fill_template(template_file, parameters)

#print(xml_config)


# Create the XML configuration template
config = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<interfaces xmlns="http://openconfig.net/yang/interfaces">
 <interface>
 <name>{}</name>
 <config>
 <name>{}</name>
 <enabled>true</enabled>
 <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
 </config>
 <subinterfaces>
 <subinterface>
 <index>0</index>
 <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
 <addresses>
 <address>
 <ip>{}</ip>
 <config>
 <ip>{}</ip>
 <prefix-length>{}</prefix-length>
 </config>
 </address>
 </addresses>
 </ipv4>
 <config>
 <index>0</index>
 </config>
 </subinterface>
 </subinterfaces>
 </interface>
</interfaces>
</config>
""".format(interface_name,interface_name,ip_address,ip_address,prefix)

try:
    # Connect to the netconf server
    with manager.connect(
        host="10.11.200.18",
        port=830,
        username="ocnos",
        password="ocnos",
        hostkey_verify=False,
    ) as m:
        # Send the configuration to the netconf server
        # Edit the configuration on the device
        try:
            reply = m.edit_config(target="candidate", config=config)
            print(reply)
        except RPCError as e:
            logging.error(f"Error editing configuration: {e}")
            sys.exit(1)

        # Commit the changes and save them to the running configuration
        try:
            #m.discard_changes()
            m.commit()
        except RPCError as e:
            logging.error(f"Error committing and saving changes: {e}")
            sys.exit(1)
except Exception as e:
    logging.error(f"Error connecting to device: {e}")
    sys.exit(1)

logging.info("Configuration updated successfully")
