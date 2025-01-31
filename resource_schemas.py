"""
Resource schemas generator for qrm2.
---
Copyright (C) 2021 Abigail Gold, 0x5c

This file is part of qrm2 and is released under the terms of
the GNU General Public License, version 2.
"""


import utils.resources_models as models


print("Generating schema for index.json")
with open("./dev-notes/rs_index_schema.json", "w") as file:
    file.write(models.Index.schema_json(indent=4))

print("Done!")
