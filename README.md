# HTML to Markdown Converter

This project converts HTML files to Markdown format using the OpenAI API. It can process individual files or entire directories, with an option for recursive processing.

## Features

- Convert HTML files to Markdown
- Process individual files or entire directories
- Optional recursive directory processing
- Uses OpenAI's GPT model for intelligent conversion
- Preserves important content structure while ignoring non-essential elements

## Requirements

- Python 3.6+

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/et0x/ai-html-to-markdown.git
   cd ai-html-to-markdown
   ```

2. Install the required packages:

   ```
   # Create a virtual environment if you want to
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

Run the script from the command line:

```
python main.py path/to/html/files -r -o path/to/output
```

## How it works

1. The script reads HTML content from the input file(s).
2. It sends the HTML content to the OpenAI API, requesting a conversion to Markdown.
3. The API returns the converted Markdown content.
4. The script writes the Markdown content to the specified output directory.
