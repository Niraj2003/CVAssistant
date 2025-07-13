import json
from jinja2 import Template

# Load data
with open('data/info.json') as f:
    data = json.load(f)

# Load HTML template
with open('templates/site_template.html') as f:
    template = Template(f.read())

# Render HTML
rendered_html = template.render(**data)

# Save output
with open('output/index.html', 'w') as f:
    f.write(rendered_html)
