import json
import os
import sys
import re
import requests
from bs4 import BeautifulSoup

def get_description_from_docs(api_name):
    doc_urls = {
        "card": "https://dev.blues.io/api-reference/notecard-api/card-requests/latest/",
        "dfu": "https://dev.blues.io/api-reference/notecard-api/dfu-requests/latest/",
        "env": "https://dev.blues.io/api-reference/notecard-api/env-requests/latest/",
        "file": "https://dev.blues.io/api-reference/notecard-api/file-requests/latest/",
        "hub": "https://dev.blues.io/api-reference/notecard-api/hub-requests/latest/",
        "note": "https://dev.blues.io/api-reference/notecard-api/note-requests/latest/",
        "ntn": "https://dev.blues.io/api-reference/notecard-api/ntn-requests/latest/",
        "var": "https://dev.blues.io/api-reference/notecard-api/var-requests/latest/",
        "web": "https://dev.blues.io/api-reference/notecard-api/web-requests/latest/"
    }
    
    base_type = api_name.split('.')[0]
    
    if base_type not in doc_urls:
        print(f"Warning: No documentation URL found for {base_type} requests")
        return None
    
    url = doc_urls[base_type]
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        section_id = api_name.replace('.', '')
        section = soup.find(id=section_id)
        
        if not section:
            section = soup.find(string=re.compile(api_name))
            if not section:
                print(f"Warning: Could not find documentation for {api_name}")
                return None
        
        parent = section.parent
        description_section = None
        
        for sibling in parent.next_siblings:
            if sibling.name == 'p':
                description_section = sibling
                break
        
        if description_section:
            description = description_section.text.strip()
            return description
        
        print(f"Warning: Could not extract description for {api_name}")
        return None
    except Exception as e:
        print(f"Error fetching documentation for {api_name}: {e}")
        return None

for filename in os.listdir('.'):
    if not filename.endswith('.notecard.api.json'):
        continue
    
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing {filename}: {e}")
            continue
    
    if data.get('title') != "Notecard Application Programming Interface (API) Schema":
        continue
    
    match = re.match(r'(.+)\.(req|rsp)\.notecard\.api\.json', filename)
    if not match:
        print(f"Warning: filename {filename} doesn't match expected pattern")
        continue
    
    api_name, req_type = match.groups()
    
    req_or_resp = "Request" if req_type == "req" else "Response"
    data['title'] = f"{api_name} {req_or_resp} Application Programming Interface (API) Schema"
    
    if req_type == "req" and 'description' not in data:
        description = get_description_from_docs(api_name)
        if description:
            data['description'] = description
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        f.write('\n')
    
    print(f"Updated {filename}")

print("Done updating schema files")
