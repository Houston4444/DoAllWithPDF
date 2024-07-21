# ---  INSTALL for Do All With PDF Service Menu  ---

To install Do All With PDF Service Menu, simply run as usual: <br/>
`$ make` <br/>
`$ [sudo] make install`

IN FUTURE You can run Do All With PDF Service Menu without installing them, by using instead: <br/>
`$ make` <br/>
`$ python3 src/doallwithpdf_service_menu`

Packagers can make use of the 'PREFIX' and 'DESTDIR' variable during install, like this: <br/>
`$ make install PREFIX=/usr DESTDIR=./test-dir`

<br/>

===== BUILD DEPENDENCIES =====
--------------------------------
The required build dependencies are: <i>(devel packages of these)</i>

 - PyQt5 (Py3 version)
 - qtchooser

On Debian and Ubuntu, use these commands to install all build dependencies: <br/>
`$ sudo apt-get install python3-pyqt5 pyqt5-dev-tools qtchooser`

To run it, you'll additionally need:

 - python3-pypdf2
 - pdftk
 - poppler-utils
 - qpdf
 - pdfjam (texlive-extra-utils)
 - #TODO

for a full dependencies install on Debian bookworm: <br/>
`$ apt install python3-pyqt5 pyqt5-dev-tools qtchooser python3-pypdf2 pdftk poppler-utils qpdf texlive-extra-utils tesseract-ocr`
