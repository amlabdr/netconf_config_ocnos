import xmltodict

def json_to_xml(json_data):
    xml_data = None
    if "operation" in json_data:
        operation = json_data["operation"]
        if operation == "delete":
            xml_data = "<delete>"
        elif operation == "add":
            xml_data = "<add>"
        elif operation == "replace":
            xml_data = "<replace>"
        if "resource" in json_data:
            resource = json_data["resource"]
            xml_data += "<{0}>".format(resource)
            if "content" in json_data:
                content = json_data["content"]
                xml_data += "<content>{0}</content>".format(content)
            xml_data += "</{0}>".format(resource)
        xml_data += "</{0}>".format(operation)
    return xmltodict.unparse({"root": xml_data}, pretty=True)

json_data = {"operation": "delete", "resource": "vlan", "content": "ip_address:10.22.2.2"}
print(json_to_xml(json_data))
