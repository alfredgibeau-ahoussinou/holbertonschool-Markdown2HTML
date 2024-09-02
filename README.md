# holbertonschool-Markdown2HTML
# Markdown2HTML

**Markdown2HTML** is a simple tool for converting Markdown files into HTML. This tool is designed to make it easy to transform Markdown content into well-formatted HTML pages.

## Features

- Converts Markdown to HTML with customizable options
- Supports standard Markdown syntax
- Easy to integrate into build processes or workflows
- Command-line interface for easy use

## Installation

To install Markdown2HTML, you need to have Node.js and npm installed. You can then install the tool globally using npm:

```bash
npm install -g markdown2html 
```
## Usage
To convert a Markdown file to HTML, use the following command
```bash
markdown2html input.md -o output.html
```
## Options
 - o, --output Specify the output file (e.g., output.html)
 - t, --template Use a custom HTML template
 - h, --help Display help information
## Examples
Convert a Markdown file to HTML:
```bash
markdown2html README.md -o README.html
```
Convert a Markdown file with a custom template:
```bash
markdown2html input.md -t custom-template.html -o output.html
```
## API
For programmatic use, you can require markdown2html in your Node.js scripts:
```javascript
const markdown2html = require('markdown2html');

markdown2html.renderFile('input.md', 'output.html', (err) => {
  if (err) {
    console.error('Error converting Markdown to HTML:', err);
  } else {
    console.log('Markdown converted to HTML successfully!');
  }
});
```
