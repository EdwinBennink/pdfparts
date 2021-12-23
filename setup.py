# For information on Python packaging, see:
# https://packaging.python.org/tutorials/packaging-projects/

import setuptools

setuptools.setup(
    name="pdfparts",
    version="0.1",
    author="Edwin Bennink",
    author_email="hebennink@gmail.com",
    description="Divides PDF pages in equal parts and prints them.",
    packages=['pdfparts'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta"
    ],
    python_requires='>=3.8',
    install_requires=[
        'click',
        'pikepdf',
        'ghostscript',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'pdfparts=pdfparts.pdfparts:app'
        ]
    }
)
