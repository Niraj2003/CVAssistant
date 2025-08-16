import json
import os

from jinja2 import Template


def site_generator():
    # Load data
    with open('data/info.json') as f:
        data = json.load(f)

    # Load HTML template
    with open('templates/site_template.html') as f:
        template = Template(f.read())

    # Render HTML
    rendered_html = template.render(**data)

    # Save output
    os.makedirs('portfolio', exist_ok=True)
    with open('portfolio/index.html', 'w') as f:
        f.write(rendered_html)

    print("Portfolio site generated successfully at portfolio/index.html")
