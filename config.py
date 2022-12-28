import ncclient, yaml
from ncclient import manager

# Open the YAML file
with open("config.yaml", "r") as f:
    # Load the YAML data
    data = yaml.safe_load(f)
# Extract the IP address and interface name
ip_address = data["interface"]["ip_address"]
interface_name = data["interface"]["name"]


# Create the XML configuration template
config = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<interfaces xmlns="http://openconfig.net/yang/interfaces">
 <interface>
 <name>xe10</name>
 <config>
 <name>xe10</name>
 <enabled>true</enabled>
 <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
 </config>
 <subinterfaces>
 <subinterface>
 <index>0</index>
 <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
 <addresses>
 <address>
 <ip>30.1.1.1</ip>
 <config>
 <ip>30.1.1.1</ip>
 <prefix-length>24</prefix-length>
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
"""


# Connect to the netconf server
with manager.connect(
    host="10.11.200.18",
    port=830,
    username="ocnos",
    password="ocnos",
    hostkey_verify=False,
) as m:
    # Send the configuration to the netconf server
    m.edit_config(target="candidate", config=config)
    m.commit()
    
