import os
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

class SimpleStaticGen:
    def __init__(self):
        # Setup directory structure
        self.content_dir = 'content'
        self.templates_dir = 'templates'
        self.output_dir = 'public'
        self.md = markdown.Markdown(extensions=['meta'])
        
        # Create Jinja environment for templates
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        
        # Ensure directories exist
        for directory in [self.content_dir, self.templates_dir, self.output_dir]:
            os.makedirs(directory, exist_ok=True)

    def create_default_template(self):
        """Create a default template if none exists"""
        default_template = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <header>
        <h1>{{ title }}</h1>
        {% if date %}
        <time>{{ date }}</time>
        {% endif %}
    </header>
    
    <main>
        {{ content | safe }}
    </main>
    
    <footer>
        <p>Generated with SimpleStaticGen</p>
    </footer>
</body>
</html>
'''
        template_path = os.path.join(self.templates_dir, 'default.html')
        if not os.path.exists(template_path):
            with open(template_path, 'w') as f:
                f.write(default_template)

    def create_default_style(self):
        """Create a default CSS file"""
        default_css = '''
body {
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
    font-family: -apple-system, system-ui, sans-serif;
    line-height: 1.6;
}

header {
    margin-bottom: 2rem;
}

time {
    color: #666;
}

footer {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
    color: #666;
}
'''
        css_path = os.path.join(self.output_dir, 'style.css')
        with open(css_path, 'w') as f:
            f.write(default_css)

    def create_example_content(self):
        """Create example markdown content"""
        example_post = '''---
title: Welcome to Gone Tomorrow
date: 2024-03-20
---

# Welcome

This is an example post created by SimpleStaticGen.

## Features

- Markdown support
- Simple templating
- Fast and lightweight
'''
        post_path = os.path.join(self.content_dir, 'welcome.md')
        if not os.path.exists(post_path):
            with open(post_path, 'w') as f:
                f.write(example_post)

    def build(self):
        """Build the static site"""
        # Clean output directory
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)

        # Create default files if they don't exist
        self.create_default_template()
        self.create_default_style()
        self.create_example_content()

        # Process all markdown files
        for filename in os.listdir(self.content_dir):
            if filename.endswith('.md'):
                self.process_file(filename)

        print(f"Site built successfully in '{self.output_dir}' directory!")

    def process_file(self, filename):
        """Process a single markdown file"""
        input_path = os.path.join(self.content_dir, filename)
        output_path = os.path.join(
            self.output_dir, 
            filename.replace('.md', '.html')
        )

        # Read and convert markdown
        with open(input_path, 'r') as f:
            content = f.read()

        # Convert markdown to HTML
        self.md.reset()
        html_content = self.md.convert(content)
        
        # Get metadata
        metadata = self.md.Meta if hasattr(self.md, 'Meta') else {}
        
        # Prepare template data
        template_data = {
            'content': html_content,
            'title': metadata.get('title', [''])[0] if metadata.get('title') else 'Untitled',
            'date': metadata.get('date', [''])[0] if metadata.get('date') else None
        }

        # Render template
        template = self.env.get_template('default.html')
        output = template.render(**template_data)

        # Write output
        with open(output_path, 'w') as f:
            f.write(output)

if __name__ == '__main__':
    generator = SimpleStaticGen()
    generator.build()
