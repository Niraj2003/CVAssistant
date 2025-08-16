import json
import os
import shutil
import subprocess

from jinja2 import Template, DebugUndefined


def escape_latex(text):
    if not isinstance(text, str):
        return text
    text = text.replace('%', r'\%')
    text = text.replace('&', r'\&')
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
               '-output-directory', 'resume', 'resume/resume.tex']

    print("Compiling LaTeX to PDF (1st pass)...")
    subprocess.run(command, capture_output=True, text=True)

    print("Compiling again (2nd pass) to fix hyperlinks/outlines...")
    result = subprocess.run(command, capture_output=True, text=True)

    return result


if __name__ == '__main__':
    # Load and escape user data
    with open('data/info.json', encoding='utf-8') as f:
        raw_data = json.load(f)
        data = escape_data(raw_data)

    # Load LaTeX Jinja2 template
    with open('templates/resume_template.tex', encoding='utf-8') as f:
        template = Template(f.read(), undefined=DebugUndefined)

    # Render LaTeX with user data
    rendered_tex = template.render(**data)

    # Ensure directory exists
    os.makedirs('resume', exist_ok=True)

    # Write rendered tex to resume/
    with open('resume/resume.tex', 'w', encoding='utf-8') as f:
        f.write(rendered_tex)

    # Copy .cls file
    shutil.copy('templates/resume.cls', 'resume/resume.cls')

    result = compile_latex()

    pdf_path = 'resume/resume.pdf'
    if result.returncode != 0:
        with open('resume/error.log', 'w', encoding='utf-8') as log:
            log.write(result.stdout + "\n" + result.stderr)
        print("PDF generation failed. Check 'resume/error.log' for details.")
    elif not os.path.exists(pdf_path):
        print("Compilation succeeded, but PDF not found.")
    else:
        print(f"Resume PDF generated successfully → {pdf_path}")
