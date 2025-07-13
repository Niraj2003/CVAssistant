import json
import os
import re
import shutil
import subprocess

from jinja2 import Template, DebugUndefined


def escape_latex(text):
    if not isinstance(text, str):
        return text
    replacements = {'\\': r'\textbackslash{}', '&': r'\\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{',
                    '}': r'\}', '~': r'\textasciitilde{}', '^': r'\^{}'}

    # Sort keys by length descending to avoid double escaping
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)

    # Fix common mistakes like \\& from previous escapes
    text = re.sub(r'\\textbackslash{}\s*\\&', r'\\&', text)
    return text


def escape_data(data):
    """
    Recursively escapes LaTeX special characters in all string fields of the JSON data.
    """
    if isinstance(data, dict):
        return {k: escape_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [escape_data(item) for item in data]
    elif isinstance(data, str):
        return escape_latex(data)
    return data


def compile_latex():
    command = [r'C:\Users\ADITYA\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe', '-interaction=nonstopmode',
               '-output-directory', 'output', 'output/resume.tex']

    print("🛠️  Compiling LaTeX to PDF (1st pass)...")
    subprocess.run(command, capture_output=True, text=True)

    print("🔁 Compiling again (2nd pass) to fix hyperlinks/outlines...")
    result = subprocess.run(command, capture_output=True, text=True)

    return result


# Load and escape user data
with open('data/info.json', encoding='utf-8') as f:
    raw_data = json.load(f)
    data = escape_data(raw_data)

# Load LaTeX Jinja2 template
with open('templates/resume_template.tex', encoding='utf-8') as f:
    template = Template(f.read(), undefined=DebugUndefined)

# Render LaTeX with user data
rendered_tex = template.render(**data)

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# Write rendered tex to output/
with open('output/resume.tex', 'w', encoding='utf-8') as f:
    f.write(rendered_tex)

# Copy .cls file if needed
shutil.copy('templates/resume.cls', 'output/resume.cls')

result = compile_latex()

pdf_path = 'output/resume.pdf'
if result.returncode != 0:
    with open('output/error.log', 'w', encoding='utf-8') as log:
        log.write(result.stdout + "\n" + result.stderr)
    print("❌ PDF generation failed. Check 'output/error.log' for details.")
elif not os.path.exists(pdf_path):
    print("⚠️ Compilation succeeded, but PDF not found.")
else:
    print(f"✅ Resume PDF generated successfully → {pdf_path}")
