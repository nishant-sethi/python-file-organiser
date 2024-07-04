# Python File Organiser

This project is a Python script that helps you organise your files in a specified directory. It allows you to sort files based on their extension and move them to designated folders based on how similar 2 files are.
Note: Please ensure that the 'images' key is present in the config.json file when running this script. This limitation is currently being addressed.


## Features

- Sorts files based on their extension
- Moves files to designated folders
- Customizable folder structure. (it only works for images at this time)

## Installation

1. Clone the repository: `git clone https://github.com/your-username/python-file-organiser.git`
2. Navigate to the project directory: `cd python-file-organiser`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage

1. Open the `config.json` file and specify the folder structure you want to create.
2. Run the script: `python file_organiser.py`
3. Enter the path of the directory you want to organise when prompted.
4. Sit back and let the script do its magic!

**Note for Windows users:** If you are using Windows, make sure you have Python installed and added to your system's PATH environment variable. You can download Python from the official website: [Python Downloads](https://www.python.org/downloads/)

## Configuration

The `config.json` file allows you to customize the folder structure. Each key represents a folder name, and the corresponding value is a list of file extensions that should be moved to that folder.

Example:
```json
{
    "Documents": ["pdf", "docx", "txt"],
    "Images": ["jpg", "png", "gif"],
    "Videos": ["mp4", "avi", "mkv"]
}
```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

-+-+-+-+-+

```markdown
## Limitations

- The 'images' key must be present in the `config.json` file for the script to work properly. This limitation is currently being addressed and will be resolved in future updates.

- The current functionality of the script only supports reordering and arranging files within folders for images.
```

This section highlights the limitation of the script and informs the user about the requirement of the 'images' key in the `config.json` file. It also assures the user that this limitation is being addressed and will be resolved in future updates.

-+-+-+-+-+

## Next Step

Future plans for this project include:
- Give appropriate names to the generated folders based on the files inside it.
- Adding support for organizing files based on file size or creation date
- Implementing a user-friendly command-line interface
- Enhancing the folder structure customization options
- Adding support for organizing files in subdirectories

Stay tuned for updates and new features!


