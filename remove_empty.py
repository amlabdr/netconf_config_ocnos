import re

# Regular expression to match empty elements
empty_pattern = re.compile(r"<([a-zA-Z0-9_-]+) />")

# Read the XML file
with open("xml_templates/write/openconfig-interfaces1.xml", "r") as f:
    xml_string = f.read()

# Replace the empty elements with non-empty elements
xml_string = empty_pattern.sub(r"<\1></\1>", xml_string)

# Write the modified XML string to a file
with open("output.xml", "w") as f:
    f.write(xml_string)
