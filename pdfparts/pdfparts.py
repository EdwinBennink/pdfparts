from copy import copy
from tempfile import TemporaryDirectory

import click
from pathlib import Path

import ghostscript
import pikepdf
from PIL import Image


def get_part(page: pikepdf.Page, i: int, j: int, rows: int, columns: int) -> pikepdf.Page:
    """Copies a PDF page and sets its media box to cover row i and column j."""

    # Get the media box dimensions of the input page.
    x1, y1, x2, y2 = page.mediabox

    # Calculate the width and height for the media box of the output page.
    width = (x2 - x1) / columns
    height = (y2 - y1) / rows

    # Copy the input page and set the new media box geometry.
    x1 = x1 + j * width
    y1 = y1 + (rows - i - 1) * height  # Bottom = 0.
    part = copy(page)
    part.mediabox = x1, y1, x1 + width, y1 + height

    return part


@click.command()
@click.option('--rows', default=2, help='Number of rows.')
@click.option('--columns', default=2, help='Number of columns.')
@click.argument('filename', type=click.Path(exists=True))
def app(rows: int, columns: int, filename: str):
    """Divides PDF pages in equal parts and prints them."""

    print(f"Splitting PDF file '{filename}' into {rows} rows and {columns} columns per page and print to the default "
          "printer.")

    # Read the input file
    document = pikepdf.open(filename)

    # Iterate over all pages in the document.
    splitted = pikepdf.new()
    for p, page in enumerate(document.pages):
        # Split the page into rows × columns parts and add those parts as new pages to the output document.
        for i in range(rows):
            for j in range(columns):
                q = j + (i + p * rows) * columns
                print(f'Retrieving page {q + 1} (page {p + 1}, row {i + 1}, column {j + 1})...')
                splitted.pages.append(get_part(page, i, j, rows, columns))

    # Save the PDF file and convert it to TIFF.
    temp_dir = TemporaryDirectory()
    pdf_file = Path(temp_dir.name) / 'pdfparts.pdf'
    tiff_file = Path(temp_dir.name) / 'pdfparts.tif'
    splitted.save(pdf_file)
    ghostscript.Ghostscript(
        '-dNOPAUSE',
        '-dQUIET',
        '-sDEVICE=tiffgray',
        '-sCompression=lzw',
        '-o',
        f'{tiff_file}',
        f'{pdf_file}',
    )

    # Read the TIFF file to find out which pages have content and only print those.
    stack = Image.open(tiff_file)
    stack.load()
    for p in range(stack.n_frames):
        stack.seek(p)

        # The page is empty if there is just one unique pixel value.
        histogram = stack.getdata().histogram()
        if sum(count > 0 for count in histogram) < 2:
            print(f'Skipping empty page {p + 1}...')
            continue

        print(f'Printing page {p + 1}...')
        ghostscript.Ghostscript(
            '-dPrinted',  # Use the PDF file print settings.
            '-dNoCancel',
            '-dBATCH',  # Exit GhostScript after finishing the task.
            '-dNOPAUSE',  # Disable the prompt and pause at the end of each page.
            '-dNOSAFER',  # Allow GhostScript to write.
            '-q',  # Prevent writing to stdout.
            f'-dFirstPage={p + 1}',
            f'-dLastPage={p + 1}',
            '-dPDFFitPage',  # Fit the page to the printer's default document size.
            '-dNumCopies=1',  # Request 1 copy.
            '-dQueryUser=3',  # Don't show the printing dialog.
            '-sDEVICE=mswinpr2',
            f'{pdf_file}',
        )


if __name__ == '__main__':
    app()
