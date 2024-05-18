#! python
''' **rivt** is a lightweight markup language for writing, organizing and
sharing engineering documents and reports. It is designed to be legible,
flexible and efficient. **rivt** is also the name of an open source framework
used for producing rivt documents.

**rivtlib** is a Python library that processes rivt files and is distributed
under the open source MIT license. It runs on platforms that support Python
3.11 or later and works within a framework of five established, open souce
technologies:

- Language: Python with open source libraries including **rivtlib**
- IDE: VSCode and extensions
- Typesetting: Latex TexLive Distribution
- Diagrams: QCAD
- Version control: GitHub

The **rivt** framework can be downloaded as a portable Windows zip file or
installed through OS specific shell scripts (https://rivtcode.net). It is also
available as an online service at https://rivtonline.net.

A rivt document (doc) is a text, HTML or PDF ouput file from a processed rivt
file. A rivt report (report) is an organized collection of rivt docs.
**rivtlib** organizes and generates both large reports and single file docs.

A rivt file is a Python file that imports **rivtlib** and its 6 API
functions:

*import rivtlib.rivtapi as rv*

rv.R(rS) - (Run) Execute shell scripts 
rv.I(rS) - (Insert) Insert static text, images, tables and math equations 
rv.V(rS) - (Values) Evaluate values and equations 
rv.T(rS) - (Tools) Execute Python functions and scripts 
rv.X(rS) - (eXclude) Skip rivt-string processing 
rv.W(rS) - (Write) Write formatted rivt documents 

where rS is a triple quoted Python string. These 6 API functions implement

    - input indents for clarity and code folding

    - a wrapper for the reStructuredText markup language (see
    https://quickrestructuredtext.com)


    - two dozen commands and tags for processing files and
    formatting output.

**rivt** commands and tags are summarized below. Further details are provided
in the user manual (https://rivt.net).


Commands - file processing
--------------------------

Commands process files (image, equations, tables etc. ) and start with | or ||
in the first indented column (for code folding, all rivt strings start in the
fourth column following the API function call.) A command has the form

    | label or title | /relative/path/file.typ(:s-e) | parameters

where s and e are optional start and end line numbers, and the parameters
depend on the file type. If the command starts with a double bar the referenced
lines are also inserted into the input for faster checking.

================ ===============================================================
 API (snippet)                     Command Overview
================ ===============================================================

Run (run)           rv.R("""function label | pass;redact | color;none

                        The Run function processes shell commands.

                        """)

Insert (ins)       rv.I(""" function label | pass;redact | color;none
                        
                        The Insert function formats static objects.                     
                        
                        | file.png, .jpg, .svg -- formats images
                        | file.txt -- formats plain, sympy, rivt
                        | file.tex -- formats latex
                        | file.csv -- formats tables
                        | file.pdf -- appends pdf files to document 

                        """)

Values (val)        rv.V("""function label | pass;redact | color;none
                
                        The Values function 

                        | file.png, .jpg, .svg -- formats images
                        | file.txt -- formats equations, displays data  
                        | file.csv -- formats values, displays data
                        | file.xls -- displays data

                        """)

Tools (too)          rv.T("""function label | pass;redact | color;none
                

                         """)

Exclude              rv.X(""" xxx | yyy | zzz

                         When a function name is changed to X it is not
                         evaluated. This function may be used for testing,
                         debugging and comments.

                         """)

Write (wri)          rv.W("""function label | doc; report | sync;async

                         | output
                         | files
            
                          """)

The rv.W() function generates formatted docs (single files) as text (.txt),
HTML (.html) and PDF (.pdf), and formatted reports as reStructuredText
(used for GitHub README.rst), HTML (.html) and PDF (.pdf).

In VSCode each API function or sequence of functions may be run interactively
using the standard cell decorator *# %%*. Interactive output, and output to
stdout when a rivt file is run from a terminal, is formatted as utf-8 text.


Tags - text formatting
----------------------

A rivt tag evaluates and/or formats text. Line tags are added at the end of a
line. Block tags are inserted at the beginning and end of a text block.
reStructuredText markup may also be used for formatting
(see https://quickrestructuredtext.com).

===================== ========= ========================== ==================
 tags                   scope       description               API scope  
===================== ========= ========================== ==================
text _[u]               line        underline                   I                             
text _[r]               line        right justify               I                        
text _[c]               line        center                      I                 
text _[bc]              line        bold center                 I     
text _[bi]              line        bold italic                 I
text _[s]               line        sympy math equation         I
text _[x]               line        latex math equation         I                           
text _[t]               line        table title                 I
text _[bs]              line        bold numbered sympy         I     
text _[bl]              line        bold numbered latex         I    
label _[o]              line        values lookup               V             
title _[v]              line        value table title           V                                
label _[e]              line        equation label              V                                
var :=, a               line        declare value               V
var = a + b             line        assign value                V
text _[f]               line        numbered figure             V,I
text _[#]               line        footnote (autonumber)       V,I
text _[d]               line        footnote description        V,I   
_[page]                 line        new page                    V,I
_[[p]]                  block       start monospace             I 
_[[l]]                  block       start LaTeX                 I
_[[e]]                  block       end block                   I



Folders 
------- 

**rivt** implements a file and folder structure to simplify file access. rivt
docs are idenfiifed by a unique rivt file number used for organizing reports.
Each rivt file starts with rivddss- where dd is a two digit division number and
ss is a two digit subdivision number e.g., riv0203-loads.py is the third
subdivision of division two.

To facilitate file sharing, specified document inputs and outputs may be
directed to public folders during processing. The privacy level may be set at
for each API function in a doc or at the rivt file level.

Report and document headings are taken from folder and file names unless
overridden in the config file. An example folder structure is shown below.
Required file names or prefixes are shown in [ ].

Source files for rivt docs and reports are stored in 6 folders

- append
- images
- scripts
- tables
- text
- values

Output files are stored in the *write* folder. Source files may be stored in
separate sub-folders for simplicity and to allow separation of public and
private date.

[rivt]-Project-Name/               
    ├── [append]/            
        ├── app01/  
        └── app02/  
            ├── attach3.pdf                   
            └── attach4.pdf
    ├── [images]/            
        ├── img01/  
        └── img02/  
            ├── image3.jpg                   
            └── image4.jpg
    ├── [scripts]/
        ├── py01/                 
        └── py02/  
            ├── function3.py
            └── function4.py               
        ├── run01/  
        └── run02/  
            ├── script3.bat
            └── script4.sh  
    ├── [tables]/            
        ├── tbl01/  
        └── tbl02/  
            ├── table3.csv                   
            └── table4.csv
    ├── [text]/            
        ├── tex01/  
        ├── tex02/  
            ├── latex3.tex
            └── latex4.tex
        ├── txt01/  
        └── txt02/  
            ├── text3.txt                   
            └── text4.txt
    ├── [values]/                 
        ├── dat01/  
        ├── dat02/  
            ├── table3.csv                   
            └── table4.csv
        ├── equ01/                      
        ├── equ02/                    
            ├── equation1.txt      
            └── equation2.txt       
        ├── val01/                    
        └── val02/                    
            ├── values3.csv      
            └── values4.csv       
    ├── [write]/                        (rivt output)
        ├── [html]/                  
            └── riv0101-codes.html
                riv0102-loads.html
                riv0201-walls.html
                riv0201-frames.html
                Project-Name.html        
        ├── [pdf]/                          
            └── riv0101-codes.pdf
                riv0102-loads.pdf
                riv0201-walls.pdf
                riv0201-frames.pdf
                Project-Name.pdf                
        ├── [rivt-redacted]/            
            └── README.rst              (redacted GitHub searchable report)
                riv0000x-report.py      (redacted input files)
                riv0101x-codes.py
                riv0102x-loads.py
                riv0201x-walls.py
                riv0201x-frames.py   
        ├── [temp]/                          
            └── temp-files.txt
        └── [text]/  
            └── riv0000-report.txt
                riv0101-codes.txt
                riv0102-loads.txt
                riv0201-walls.txt
                riv0201-frames.txt
    └── config.ini                      (rivt config file)
        README.rst                      (GitHub searchable rivt report)
        riv0000-report.py               (rivt input files)
        riv0101-codes.py
        riv0102-loads.py
        riv0201-walls.py
        riv0201-frames.py


Example rivt file
-----------------

import rivtlib.rivtapi as rv

rv.R("""Introduction | pass; redact | nocolor; color code

    The Run function processes shell commands.

    Each API function defines a new document section. The first line is a heading
    line which includes the section heading, a parameter for redacting sections
    for sharing on GitHub and a parameter for a background color for the
    section. If the section heading is preceded by two dashes (--) it becomes a
    location reference without starting a new section. 
    
    File formatting follows pep8 and ruff. API functions
    start in column one. All other lines are indented 4 spaces to
    facilitate section folding, bookmarks and legibility.

    
    """)

rv.I("""The Insert method | pass; redact | nocolor 

    The Insert function formats static objects including images, tables,
    equations and text.

    ||text | data01/describe.txt | rivt     

    The table command inserts and formats tabular data from csv or xls files.
    The _[t] tag formats and autonumbers table titles.

    A table title  _[t]
    || table | data/file.csv | 60,r

    The image command inserts and formats image data from png or jpg files. The
    _[f] tag formats and autonumbers figures.
        
    A figure caption _[f]
    || image | data/f1.png | 50

    Two images may be placed side by side as follows:

    The first figure caption  _[f]
    The second figure caption  _[f]
    || image | private/image/f2.png, private/image/f3.png | 45,35
    
    The tags _[x] and _[s] format LaTeX and sympy equations:

    \gamma = \frac{5}{x+y} + 3  _[x] 

    x = 32 + (y/2)  _[s]

    """)

rv.V("""The Values method |  pass; redact | nocolor 

    The Values fucntion evaluates variables and equations. 
    
    The equal tag declares a value. A sequence of declared values terminated
    with a blank line is formatted as a table.
    
    Example of assignment list _[t]
    f1 = 10.1 * LBF |LBF, N| a force value
    d1 = 12.1 * IN  |IN, CM| a length value

    An equation tag provides an equation description and number. A colon-equal
    tag assigns a value and specifies the result units and the output decimal
    places printed in the result and equation.

    Example equation - Area of circle  _[e]
    a1 := 3.14(d1/2)^2 | IN^2, CM^2 | 1,2

    || declare | data01/values02.csv
    
    The declare command imports values from the csv file written by rivt when
    processing values in other documents. 

    """)

rv.T("""The Tools method | pass; redact | nocolor

    The Tools function processes Python code.
        
    """)

rv.X("""Any text 

    Changing a function to X skips evaluation of that function. Its purposes
    include review commenting and debugging.

    """) 

rv.W("""Doc labels | pass; redact | nocolor

    The Write function generates docs and reports.

    | docs |
 
    | report |

    """)



rivt profile for VSCode
-----------------------

============= ==============================================================
Keystrokes            description
============= ==============================================================

alt+q                rewrap paragraph with hard line feeds (80 default)
alt+p                open file under cursor
alt+.                select correct spelling under cursor
alt+8                insert date
alt+9                insert time

ctl+1                focus on first editor
ctl+2                focus on next editor
ctl+3                focus on previous editor
ctl+8                focus on explorer pane
ctl+9                focus on github pane    

ctl+alt+x            reload window
ctl+alt+[            reload window
ctl+alt+]            unfold all code
ctl+alt+u            unfold all code
ctl+alt+f            fold code level 2 (rivt sections visible)
ctl+alt+a            fold code - all levels
ctl+alt+t            toggle local fold
ctl+alt+e            toggle explorer sort order
ctl+alt+s            toggle spell check
ctl+alt+g            next editor group

ctl+shift+u          open URL under cursor in browser
ctl+shift+s          open GitHub README search for rivt
ctl+shift+a          commit all 
ctl+shift+z          commit the current editor
ctl+shift+x          post to remote   
rivt file example


============================================== ===============================
Extensions                                       description
============================================== ===============================

BUTTONS
tombonnike.vscode-status-bar-format-toggle          format button
gsppvo.vscode-commandbar                            command buttons
AdamAnand.adamstool                                 command buttons
nanlei.save-all                                     save all button
Ho-Wan.setting-toggle                               toggle settings
yasukotelin.toggle-panel                            toggle panel
fabiospampinato.vscode-commands                     user command buttons
jerrygoyal.shortcut-menu-bar                        menu bar

EDITING 
henryclayton.context-menu-toggle-comments           toggle comments
TroelsDamgaard.reflow-paragraph                     wrap paragraph
streetsidesoftware.code-spell-checker               spell check
jmviz.quote-list                                    quote elements in a list
njpwerner.autodocstring                             insert doc string
oijaz.unicode-latex                                 unicode symbols from latex
jsynowiec.vscode-insertdatestring                   insert date string
janisdd.vscode-edit-csv                             csv editor

VIEWER
GrapeCity.gc-excelviewer                            excel viewer
SimonSiefke.svg-preview                             svg viewer
tomoki1207.pdf                                      pdf viewer
RandomFractalsInc.vscode-data-preview               data viewing tools
Fr43nk.seito-openfile                               open file from path
vikyd.vscode-fold-level                             line folding tool
file-icons.file-icons                               icon library
tintinweb.vscode-inline-bookmarks                   inline bookmarks

MANAGEMENT
alefragnani.project-manager                         folder, project management
Anjali.clipboard-history                            clipboard history
dionmunk.vscode-notes                               notepad
hbenl.vscode-test-explorer                          test explorer
mightycoco.fsdeploy                                 save file to second location
lyzerk.linecounter                                  count lines in files
sandcastle.vscode-open                              open files in default app
zjffun.snippetsmanager                              snippet manager
spmeesseman.vscode-taskexplorer                     task explorer

GITHUB
GitHub.codespaces                                   run files in codespaces
GitHub.remotehub                                    run remote files
ettoreciprian.vscode-websearch                      search github within VSCode
donjayamanne.githistory                             git history
MichaelCurrin.auto-commit-msg                       git auto commit message     
github.vscode-github-actions                        github actions
GitHub.vscode-pull-request-github                   github pull request
k9982874.github-gist-explorer                       gist explorer
vsls-contrib.gistfs                                 gist tools

PYTHON
ms-python.autopep8                                  python pep8 formatting
ms-python.isort                                     python sort imports
donjayamanne.python-environment-manager             python library list
ms-python.python                                    python tools
ms-python.vscode-pylance                            python language server
ms-toolsai.jupyter                                  jupyter tools
ms-toolsai.jupyter-keymap                           jupyter tools
ms-toolsai.jupyter-renderers                        jupyter tools
ms-toolsai.vscode-jupyter-cell-tags                 jupyter tools
ms-toolsai.vscode-jupyter-slideshow                 jupyter tools

LANGUAGES 
qwtel.sqlite-viewer                                 sqlite tools
RDebugger.r-debugger                                R tools
REditorSupport.r                                    R tools
ms-vscode-remote.remote-wsl                         windows linux tools
James-Yu.latex-workshop                             latex tools
lextudio.restructuredtext                           restructured text tools
trond-snekvik.simple-rst                            restructured syntax
yzane.markdown-pdf                                  markdown to pdf
yzhang.markdown-all-in-one                          markdown tools
'''
