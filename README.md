# pdfparts
```
Usage: pdfparts [OPTIONS] FILENAME

  Divides PDF pages in equal parts and prints them.

Options:
  --rows INTEGER     Number of rows.
  --columns INTEGER  Number of columns.
  --help             Show this message and exit.
```

This application was made to easily print DHL packaging labels to a DYMO LabelWriter printer. Those packaging label PDF files have 2x2 labels per page and poster-printing will make the LabelWriter spit out empty labels if a page contains less than 4 labels.

The application will always print to the default printer. After installing this Python package, the input PDF file can just be dragged and dropped onto the pdfparts executable.

## Installation
1. Install GhostScript from https://www.ghostscript.com/releases/gsdnld.html
2. Run `python -m pip install ./` from the repository root.
