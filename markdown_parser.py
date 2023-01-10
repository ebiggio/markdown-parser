# Markdown parser
# Simple Python script that reads a Markdown file and creates a dictionary based on the contents of the file, using
# the headings of the document as the keys
from collections import defaultdict

main_headers = []
# Counter for the main headers of the document (headers that starts with only one '#' char). We start at -1 to get 0 for the first header, and use its
# index to later get the associated info from the 'document_content' list
main_heading_counter = -1
document_content = defaultdict(list)

markdown_file = 'resume.markdown'


def process_heading(heading):
    global main_heading_counter
    main_headers.append(heading.replace('#', '').strip())
    main_heading_counter += 1


def process_content(content, attr_dict, attr_list):
    if ':' in content:
        split = content.split(':')
        attr_dict[split[0].strip()] = split[1].strip()
    else:
        attr_list.append(content)


try:
    with open(markdown_file, encoding='utf8') as fo:
        file_lines = fo.readlines()
except FileNotFoundError:
    print(f'File {markdown_file} not found in script directory')
    raise SystemExit

if not file_lines:
    print('The markdown file is empty')
    raise SystemExit

attribute_list = []
attribute_dict = {}

for lines in file_lines:
    line = lines.strip()
    if line:
        if line.startswith('# '):
            if attribute_dict:
                document_content[main_heading_counter].append(attribute_dict)
            elif attribute_list:
                document_content[main_heading_counter].append(attribute_list)
            process_heading(line)
            attribute_list = []
            attribute_dict = {}
        elif line.startswith('* '):
            process_content(line.replace('* ', ''), attribute_dict, attribute_list)
        else:
            document_content[main_heading_counter].append(line.strip())

print(main_headers)
print(document_content)
