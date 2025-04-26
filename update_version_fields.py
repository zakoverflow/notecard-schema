import json
import os
import sys

updated_files = 0
skipped_files = 0

for filename in os.listdir('.'):
    if not filename.endswith('.notecard.api.json'):
        continue

    print(f"Processing {filename}...", end='')
    
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing {filename}: {e}")
            continue
    
    updated = False
    
    if "version" in data and "apiVersion" in data:
        print(" already updated, skipping.")
        skipped_files += 1
        continue
    
    if "properties" in data and "manifestVersion" in data["properties"]:
        manifest_version = data["properties"]["manifestVersion"]["const"]
        data["version"] = manifest_version
        del data["properties"]["manifestVersion"]
        updated = True
    
    if "properties" in data and "apiVersion" in data["properties"]:
        api_version = data["properties"]["apiVersion"]["const"]
        data["apiVersion"] = api_version
        del data["properties"]["apiVersion"]
        updated = True
    
    if updated:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            f.write('\n')  # Add newline at end of file
        print(" updated.")
        updated_files += 1
    else:
        print(" no changes needed.")
        skipped_files += 1

print(f"\nDone: Updated {updated_files} files, skipped {skipped_files} files.")
