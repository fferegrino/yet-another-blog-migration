import ntpath
import os
import re
from glob import glob

POST_IMAGE_REGEX = re.compile(r'\{%\s+post_image\s+([a-zA-Z0-9-\.]+)\s+([\w\.\"\s]+)\s+%\}')

for full_path in glob("/Users/antonioferegrino/Documents/GitHub/that-c-sharp-guy/en/_posts/*"):
    file_name = ntpath.basename(full_path)
    name, ext = os.path.splitext(file_name)
    properties = {}

    body = []

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
                    value_content = parts[1].strip("\" ")
                    if value_content:
                        current_values.append(value_content)
                elif len(parts) == 1:
                    list_content = parts[0].strip(' -')
                    if current_prop and list_content:
                        current_values.append(list_content)

            if current_values:
                properties[current_prop] = ', '.join(current_values)

            for line in lines[i + 1:]:
                clean_line = line.strip()
                if clean_line.startswith('{% highlight'):
                    language = clean_line[len('{% highlight'):-2].strip()
                    body.append(f'```{language}  ')
                elif clean_line == '{% endhighlight %}':
                    body.append('```  ')
                else:
                    if re.search(POST_IMAGE_REGEX, clean_line):
                        images_path = properties.get('images_folder', name[11:])

                        parts = '__'.join([part for part in images_path.split('/') if part.strip()])

                        l = re.sub(POST_IMAGE_REGEX, f'<img src="/images/{parts}__' + r'\1" title="\2" />', clean_line)
                        body.append(l)
                    else:
                        body.append(line)

    headers = [f'{k}: {v}' for k, v in properties.items()]

    content = '\n'.join(headers) + '\n\n' + '\n'.join(body)

    with open(f'content/{name}.md', 'w') as w:
        w.write(content)
