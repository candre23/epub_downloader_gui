# GUI

I have added a simple GUI to make this application a little easier to use.  Simply paste the URL for the book and select a directory for it to end up in.


# Original EPUB Downloader Info

This script downloads an ebook from an online reader and creates an EPUB file for offline viewing.

Though this script can be used if you know the URL to a remote EPUB archive, it is specifically designed to handle finding EPUB URLs for the following sites:
- [epub.pub](https://www.epub.pub/)
- [readanybook.com](https://www.readanybook.com)
 
Please open an issue to request support for other domains, or submit a PR!


## Description

Given a URL to a remote EPUB file, this script parses its content list and downloads all the necessary files to recreate the EPUB archive locally.

If a URL to an www.epub.pub or a www.readanybook.com book page is supplied, it can automatically resolve the EPUB's remote storage URL.

This script supports verbose output to help track the progress and identify issues during the download and creation process.

Works on Linux, MacOS and Windows.

## Prerequisites

- Python 3.6 or higher (Python 3.13 is known to have issues with a dependancy, libxml, so a prior version is recommended instead)
- Dependencies:
    - `bs4`
    - `lxml`
    - `tqdm`
    - `urllib3`

## Installation

1. Clone the repository or download the script file.

2. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

To run the script, use the following command:

```bash
Copy code
python epub_downloader.py [book_url] [-v]
```

- `book_url`: The URL of the EPUB archive or to the book page on epub.pub or readanybook.com
- `-v`, `--verbose`: Enable verbose output (optional)

### Example

The script handles downloading directly from the book page for the www.epub.pub and www.readanybook.com domains:
```bash
python epub_downloader.py https://www.epub.pub/book/it-by-stephen-king
```
```bash
python epub_downloader.py https://www.readanybook.com/ebook/it-book-565296
```

Or you can download from the epub.pub spread or continuous page (after clicking on one of the Read Online buttons):
```bash
python epub_downloader.py https://spread.epub.pub/epub/5a5827247412f4000781f18e
python epub_downloader.py https://continuous.epub.pub/epub/5a5827247412f4000781f18e
```

Or if you're into digging for the EPUB URL manually:
```bash
python epub_downloader.py https://asset.epub.pub/epub/it-by-stephen-king-1.epub
```

## Notes

- The script will create a temporary directory to store downloaded files, which will be cleaned up after the EPUB is created.
- **Support Authors: If you enjoy an ebook you downloaded using this script, please consider supporting the author by purchasing the book from a legitimate retailer.**
