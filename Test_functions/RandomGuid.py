import re
import uuid

def replace_guid(match):
    return f'"id":"{str(uuid.uuid4())}"'

your_clob_data = '{"resourceType":"AuditEvent","id":"64c30c45-b1ed-4f77-b117-636ba162e31b".....' # Import your clob here

# Define the regular expression pattern
pattern = r'"id":"[0-9a-fA-F\-]+"'

# replace the matched pattern with a random GUID
modified_data = re.sub(pattern, replace_guid, your_clob_data)

print(modified_data)