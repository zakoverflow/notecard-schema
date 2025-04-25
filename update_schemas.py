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
        heading = soup.find(id=section_id)
        
        if not heading:
            for tag in ['h2', 'h3']:
                headings = soup.find_all(tag)
                for h in headings:
                    if api_name in h.text:
                        heading = h
                        break
                if heading:
                    break
        
        if not heading:
            print(f"Warning: Could not find documentation heading for {api_name}")
            return None
        
        description_section = None
        current = heading.next_sibling
        
        while current and not description_section:
            if current.name == 'p':
                description_section = current
            elif hasattr(current, 'text') and current.text.strip() and current.name not in ['h2', 'h3', 'h4', 'header']:
                description_section = current
            current = current.next_sibling
        
        if description_section:
            description = description_section.text.strip()
            return description
        
        print(f"Warning: Could not extract description for {api_name}")
        return None
    except Exception as e:
        print(f"Error fetching documentation for {api_name}: {e}")
        return None

updated_count = 0
for filename in os.listdir('.'):
    if not filename.endswith('.notecard.api.json'):
        continue
    
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing {filename}: {e}")
            continue
    
    match = re.match(r'(.+)\.(req|rsp)\.notecard\.api\.json', filename)
    if not match:
        print(f"Warning: filename {filename} doesn't match expected pattern")
        continue
    
    api_name, req_type = match.groups()
    
    if "Notecard Application Programming Interface (API) Schema" in data.get('title', ''):
        req_or_resp = "Request" if req_type == "req" else "Response"
        data['title'] = f"{api_name} {req_or_resp} Application Programming Interface (API) Schema"
        updated_count += 1
    
    if req_type == "req":
        description = get_description_from_docs(api_name)
        if description:
            data['description'] = description
            updated_count += 1
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        f.write(' ')
    
    print(f"Updated {filename}")

print(f"Done updating schema files. Updated {updated_count} fields.")
