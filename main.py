import os
import argparse
from pathlib import Path
import json
from openai import OpenAI
from pydantic import BaseModel


class MarkdownResponse(BaseModel):
    markdown_content: str


def convert_html_to_markdown(html_content: str, openai_client: OpenAI) -> str:
    """
    Convert HTML content to Markdown using the OpenAI API with structured output.

    Args:
        html_content (str): The HTML content to convert.
        openai_client (OpenAI): The OpenAI client instance.

    Returns:
        str: The converted Markdown content.
    """
    response = openai_client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=MarkdownResponse,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that converts HTML to Markdown.",
            },
            {
                "role": "user",
                "content": f"Convert the following HTML to Markdown, focusing only on the main content. Ignore navigation items, headers, footers, and other non-essential elements. Preserve the important content structure:\n\n{html_content}",
            },
        ],
        max_tokens=16384,
    )

    try:
        return response.choices[0].message.parsed.markdown_content
    except (json.JSONDecodeError, KeyError):
        raise ValueError("Failed to get structured output from OpenAI API")


def process_file(input_path: Path, output_path: Path, openai_client: OpenAI) -> None:
    """
    Process a single HTML file and convert it to Markdown.

    Args:
        input_path (Path): The path to the input HTML file.
        output_path (Path): The path to the output Markdown file.
        openai_client (OpenAI): The OpenAI client instance.
    """
    with open(input_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    try:
        markdown_content = convert_html_to_markdown(html_content, openai_client)
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(markdown_content)


def process_input(
    input_path: Path, output_path: Path, openai_client: OpenAI, recursive: bool
) -> None:
    """
    Process the input path, which can be a file or directory.

    Args:
        input_path (Path): The input file or directory path.
        output_path (Path): The output directory path.
        openai_client (OpenAI): The OpenAI client instance.
        recursive (bool): Whether to process directories recursively.
    """
    if input_path.is_file():
        output_file = output_path / f"{input_path.stem}.md"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        process_file(input_path, output_file, openai_client)
        print(f"Converted {input_path} to {output_file}")
    elif input_path.is_dir():
        for html_file in sorted(
            input_path.glob("**/*.html" if recursive else "*.html")
        ):
            relative_path = html_file.relative_to(input_path)
            output_file = output_path / relative_path.with_suffix(".md")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            process_file(html_file, output_file, openai_client)
            print(f"Converted {html_file} to {output_file}")
    else:
        print(f"Error: {input_path} is not a valid file or directory")


def main():
    """
    Main function to handle command-line arguments and initiate the conversion process.
    """
    parser = argparse.ArgumentParser(
        description="Convert HTML files to Markdown using OpenAI API"
    )
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Process directories recursively"
    )
    parser.add_argument("-o", "--output", help="Output directory", default="output")
    args = parser.parse_args()

    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    input_path = Path(args.input)
    output_path = Path(args.output)

    process_input(input_path, output_path, openai_client, args.recursive)


if __name__ == "__main__":
    main()
