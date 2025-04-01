# Auto Podcast

An automated tool to interact with Google's NotebookLM for processing documents and generating audio overviews.

## Features

- Automated browser interaction with NotebookLM
- Automatic file upload handling with multiple fallback methods
- Support for various file formats (PDF, TXT, CSV)
- Automated audio overview generation
- Robust error handling and retry mechanisms

## Prerequisites

- Python 3.12 or higher
- Google Chrome browser installed
- Access to NotebookLM (Google account required)
- OpenAI API key for LLM interactions

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd auto_podcast
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Run the main script:
```bash
python upload_browseruse.py
```

2. The script will:
   - Open Google Chrome
   - Navigate to NotebookLM
   - Create a new notebook
   - Upload specified files
   - Generate audio overview
   - Wait for processing
   - Handle file downloads

## Configuration

The script uses several configuration options that can be modified in `upload_browseruse.py`:

- `chrome_instance_path`: Path to Chrome executable
- `headless`: Boolean to run Chrome in headless mode
- File types: Modify `create_file()` function to support different file types

## Error Handling

The script implements multiple file upload methods with fallbacks:
1. Direct file input using `set_input_files`
2. File chooser dialog handling
3. Generic file input detection

Each method has proper error handling and logging for debugging purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Troubleshooting

If you encounter issues:

1. Ensure Chrome is installed and the path is correct
2. Check your internet connection
3. Verify your Google account has access to NotebookLM
4. Check the console output for detailed error messages
5. Ensure your OpenAI API key is properly set

## Support

For support, please [create an issue](link-to-issues) in the repository.
