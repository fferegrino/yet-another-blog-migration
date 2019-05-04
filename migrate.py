import ntpath
import os
from glob import glob

for full_path in glob("~/Documents/GitHub/that-c-sharp-guy/en/_posts/*"):
    file_name = ntpath.basename(full_path)
    name, ext = os.path.splitext(file_name)
    properties = {}

    with open(full_path, 'r') as r:
        markdown = r.read()
        lines = markdown.split('\n')
        if lines[0] == '---':
            in_header = True
            current_prop = None
            current_values = []
            for i in range(1, len(lines)):
                line = lines[i].strip()
                if line == '---':
                    break
                parts = line.split(':', 1)
                if len(parts) == 2:
                    if current_prop:
                        if current_values:
                            properties[current_prop] = ', '.join(current_values) 
                        current_values = []
                    current_prop = parts[0].strip()
                    value_content = parts[1].strip()
                    if value_content:
                        current_values.append(value_content)
                elif len(parts) == 1:
                    list_content = parts[0].strip(' -')
                    if current_prop and list_content:
                        current_values.append(list_content)

        if current_values:
            properties[current_prop] = ', '.join(current_values) 
                

    headers = [f'{k}: {v}' for k, v in properties.items() ]
    content = '\n'.join(headers) + '\n\n' + '\n'.join(lines[i + 1:])

    with open(f'content/{name}.md', 'w') as w:
        w.write(content)
