#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                        PAWS Package Marker                                    #
#                 Written by Roger Plowman (c) 2008                             #
#                                                                               #
# The C="""...""" statements scattered throughout this source code are actually #
# a work-around for Python's lack of block comments. Notepad++ can only fold    #
# block comments, not a series of comment lines. Using C="""...""" doesn't      #
# increase PAWS memory footprint, although it does have a tiny impact           #
# on loading time.                                                              #
#                                                                               #
C="""
  This file simply marks the folder as a collection of Python programs 
  intended to work together.
  
  Written By: Roger Plowman
  Written On: 08/27/98

  This folder contains a set of programs intended to work together as a 
  "single program". The files are:
  
  __init__.py      - This file.
  AboutDialog.py   - About PAWS dialog window.
  Core.py          - Core game engine.
  Terminal.py      - main() program called by LoadTerminal.pyy
  TerminalFrame.py - The bulk of the terminal program code.
  Universe.py      - The library that creates the game world.
  
  A game author never needs to change anything in this folder. If you're
  curious, the source code for Core and Universe follow PAWS style
  guidelines, but Terminal, TerminalFrame, and AboutDialog were generated
  by a GUI creation tool called Boa Constructor, so they DO NOT follow
  PAWS guidelines.
  """
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#********************************************************************************
#                                 Style Guidelines
#
C="""
  To organize PAWS all the files share the same design conventions. The 
  files have been organized into sections to make it easier to navigate 
  through them with a text editor.

  The major sections are marked by boxes with borders made of ******'s that
  stretch across the entire page. If you search for #*** you can jump from
  section to section. The sections provide an overview of the entire file.
 
  Within each section you'll find a set of related classes, objects, and
  functions. If you use the Notepad++ text editor, the Alt-0 keystroke will
  fold the file into its smallest, most easily navigated form. Clicking a +
  to the left of a folded section will allow you to unfold only that 
  section. Thus you can keep most of the file folded, seeing only the part
  you're actually interested in. This helps tremendously.

  COLOR CODES 

  This source code is best read with a color coding editor, preferably
  Notepad++ using 18 point Lucinda Console font, in 1280x1024 resolution
  (large fonts). 
 
  The following colors were used:
 
  Grey          - Comments (italics)
  Orange        - Quoted Text (bold)
  Bright Blue   - Python and PAWS keywords (bold)
  Green         - Local Variables (bold)
  Purple        - Operators, parentheses, etc.
  Red           - Numbers
  """

"""
PAWS Package marker.
"""