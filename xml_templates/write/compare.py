import xml.etree.ElementTree as ET

def compare_xml(xml1, xml2):
    # Parse the XML files into Element objects
    root1 = ET.fromstring(xml1)
    root2 = ET.fromstring(xml2)

    # Compare the Element objects recursively
    compare_elements(root1, root2)

def compare_elements(elem1, elem2):
    # Compare the tag and attributes of the elements
    if elem1.tag != elem2.tag:
        print(f'Different tags: {elem1.tag} and {elem2.tag}')
    if elem1.attrib != elem2.attrib:
        print(f'Different attributes: {elem1.attrib} and {elem2.attrib}')

    # Compare the text content of the elements
    if elem1.text != elem2.text:
        print(f'Different text content: {elem1.text} and {elem2.text}')

    # Compare the children of the elements recursively
    if len(elem1) != len(elem2):
        print(f'Different number of children: {len(elem1)} and {len(elem2)}')
    else:
        for i in range(len(elem1)):
            compare_elements(elem1[i], elem2[i])

# Compare two XML files
with open('xml_templates/write/openconfig-interfaces1.xml', 'r', encoding='utf-8') as f:
    xml1 = f.read()
with open('xml_templates/write/xml2.xml', 'r', encoding='utf-8') as f:
    xml2 = f.read()
compare_xml(xml1, xml2)
