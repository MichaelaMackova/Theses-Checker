# Theses-Checker

### Autor: Michaela Macková ([michaela.mackovaa@gmail.com](mailto:michaela.mackovaa@gmail.com))
---

The developed applications implement a tool that checks for typographical errors that often occur in theses. Two applications were created: one web-based and the other command-line executable. Both applications were developed in Python and use the [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) library to process PDF documents.

***This program is a part of a bachelor's thesis.***

---

### Web tool

The developed web application is freely available at <https://theseschecker.eu.pythonanywhere.com/>.

The input of this application is a PDF file containing the technical report that will be checked.  The output is the same file with graphical indications of any identified mistakes. The edited PDF is displayed directly on the web page, with errors marked using PDF annotations.

### Command-line executable

The input to this application is one or more PDF files, each containing a technical report that will be checked. Using the available arguments, you can set which checks are performed and whether embedded PDF files (located inside the PDF documents) are treated as images during the checks. The output consists of the provided PDF files, each accompanied by a graphical indication of any identified mistakes, with errors marked using PDF annotations.



---
## Bachelor's thesis
If you want to learn more and know Czech you can read my thesis at
[https://www.vut.cz/studenti/zav-prace/detail/144733](https://www.vut.cz/studenti/zav-prace/detail/144733).

> **Abstract:** </br>
> The main goal of this work is to create an application that checks technical reports and
marks all the found errors with PDF annotations. The technical documentation of this thesis
breaks down the structure of a PDF file, commonly found mistakes in graduate theses, web
development using the Django framework and discusses existing libraries for editing PDF
documents. The resulting application is implemented in Python and is accessible as a web
tool with the help of the Django framework. The developed solution recognizes six mostly
typographical errors frequently found in graduate theses. The mistakes found are visually
marked and the edited PDF file is then displayed directly on the web page. The resulting
tool is freely available and helps students and supervisors to correct the technical reports
the students create.



---
# Development

## 1. Installation of dependencies

Before running the program, you must install all the packages on which the application depends. For easier installation, files have been created containing the packages and their versions that can be used with the `pip install` command. These files are stored in the root folder. Both versions of Theses Checker (the web tool and the command line program) were developed in the **Python programming language version 3.10**.
Other versions have not been tested.

### Web tool

To install dependencies for the *web tool*, use the following command:

```
> pip install -r requirements_web.txt
```

### Command-line executable

To install dependencies for the *command-line executable*, use the following command:

```
> pip install -r requirements.txt
```



---
## 2. Before first use

After installing the dependencies, you’ll need to make a few adjustments before using either application for the first time.

### Web tool

+ For the web application to work properly, the `theses_checker.py` file must be located in the `src\web\theses_checker\bl\` folder (its original location).
+ The next step is creating a `.env` file in `src\web\` folder. This file will contain the secret key that should be set before this application is published. The file must contain a line starting with `SECRET_KEY=` followed by the newly generated secret key. The example below contains the base value of the secret key, but this value must be manually changed to maintain security. This secret key can be generated, for example, at [Djecrety](https://djecrety.ir/).
+ Next, the `DEBUG` variable in the `settings.py` file (located in `src\web\web\` folder), must be set. This variable can be used to specify whether the application will run in development mode or production mode. (Static files such as `style.css` and `script.js` may not function correctly in production mode on the local server.)

**`.env` file example:**
```
SECRET_KEY=django-insecure-8%7#%6m22)=2**4c50n1h-&_!z_&3os6r+0g3_0eofna9mlkx*
```

### Command-line executable

In order for the command line program to work properly, the `theses_checker.py` file must be located in the same folder as the `check.py` file. The original folder of this `check.py` file is `src\` and the `theses_checker.py` file is originally located in the `src\web\theses_checker\bl\` folder.



---
## 3. Usage

### Web tool

To start the server locally for the web tool, use this command (used primarily for debugging purposes):
```
> python manage.py runserver
```

### Command-line executable

To execute this program, use the following command:

```
> python check.py [ARG]… in_file [in_file]…
```

**Command description:** Makes a new pdf file called '*_annotated.pdf' in the folder, where this program is saved. If no check flag is given, everything will be checked.

Available arguments are:

+ `-h` or `--help`
+ `--embedded_PDF` - if used, embedded PDF files will be treated as part of the PDF; otherwise, they will be considered as images
+ `-o` or `--overflow` - performs overflow check
+ `-i` or `--image_width` - performs image width check
+ `-H` or `--Hyphen` - performs hyphen check
+ `-t` or `--TOC` - performs table of content section check
+ `-s` or `--space_bracket` - performs space before left bracket check
+ `-e` or `--empty_chapter` - performs text between titles check
+ `-b` or `--bad_reference` - performs bad reference check (finding '??' in text - usually found in PDFs exported from LaTeX)

The application can be used as follows:

```
> python check.py -h
```

```
> python check.py file.pdf
```

```
> python check.py file1.pdf file2.pdf file3.pdf
```

```
> python check.py -o -t file.pdf file2.pdf
```

```
> python check.py file.pdf -H -s -b
```



# Known Issues

+ overflow check doesn't work for two-sided papers (padding on odd pages is different than padding on even pages)
+ when user leaves mid request, files stay in `static` folder
+ when error is thrown during file processing, files stay in `files` folder
