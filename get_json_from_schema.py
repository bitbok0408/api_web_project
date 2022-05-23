import os
import re
from definition import SCHEMAS_DIR


product_name = 'scm'

schema_name = 'post_dictionaries.json'

product_file_path = os.path.join(SCHEMAS_DIR, product_name)
with open(os.path.join(product_file_path, schema_name), "r") as f:
    all_file = f.readlines()

result = re.findall(r"\$[a-zA-Z_]*", "".join(all_file))


a = {key: "" for key in result}

print("{")
for key, val in a.items():
    print(f'"{key}": "{val}",')
print("}")

