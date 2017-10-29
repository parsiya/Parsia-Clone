#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                      Python Adventure Writing System                          #
#                                Core Engine                                    #
#                      Written by Roger Plowman (c) 1998-2008                   #
#                                                                               #
# The C="""...""" statements scattered throughout this source code are actually #
# a work-around for Python's lack of block comments. Notepad++ can only fold    #
# block comments, not a series of comment lines. Using C="""...""" doesn't      #
# increase PAWS memory footprint, although it does have a tiny impact           #
# on loading time.                                                              #
#                                                                               #
C="""
  This module contains the constants and classes required to create the Core
  of the PAWS runtime system. This includes the game engine, parser, global
  variables, and *very* basic "thing" object and verb object.

  It assumes some sort of library will be layered on top of it before games
  are developed. By default this library is Universe.

  Written By: Roger Plowman
  Written On: 07/30/98
  """
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#********************************************************************************
#                                 Style Guidelines                              #
#                                                                               #
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

#********************************************************************************
#                                PAWS Contants
#
C="""
  The following contants may be considered "global", that is, they are
  usable anywhere in your game. A constant is simply a name given to a 
  number. For example you COULD say "return 1" to indicate success, but 
  "return SUCCESS" is much clearer.
  """
#------------------
# Boolean Constants
#------------------

TRUE = 1                # Test or condition is true
SUCCESS = TRUE          # Function was successful
TURN_ENDS = TRUE        # Verb Action causes turn to end

FALSE = 0               # Test or condition is not true (it's false)
FAILURE = FALSE         # Function was NOT successful, it failed
TURN_CONTINUES = FALSE  # Verb Action doesn't end current turn

TEXT_PICKLE = FALSE     # Argument for pickle.dump(), file is stored as text
BINARY_PICKLE = TRUE    # Argument for pickle.dump(), file is stored as binary

SHALLOW = TRUE          # Shallow refers to displaying only the first layer of
                        # a container's contents, regardless if nested containers
                        # are transparent or open.

#-----------------
# Daemon Constants
#-----------------

C="""
  These are used to identify which kind of automatically running program
  (daemon, fuse, or recurring fuse) is being examined. Used mainly by the 
  RunDaemon() function.

  Daemons run every turn once activated, fuses delay for a given number of
  turns, run once, then don't run again. Recurring fuses happen every X
  turns.
  """
  
DAEMON = 0
FUSE = 1
RECURRING_FUSE = -1

#---------------------
# Game State Constants
#---------------------

C="""
  These constants define the various states the game can enter. STARTING
  means the game is either starting for the first time or restarting to the
  very beginning (because the player typed "restart").

  RUNNING means the game is running normally, accepting input from the
  player and processing commands.

  FINISHED means the player is quitting the game. Any command that sets the
  game status to FINISHED should cause the TurnHandler to fail, which will
  immediately terminate the game loop and cause the PostGameWrapUp() method
  to execute, just prior to ending the game and shutting down Python.
  """
  
STARTING = 1
RUNNING = 2
FINISHED = 3

#------------------
# Pronoun Constants
#------------------

# These constants are used as keys into the PronounDict dictionary. They make
# it easy to remember the numeric keys and make the code clearer.

IT = 0
THEM = 1
HIM = 2
HER = 3

#-------------------------
# Verb Allowance Constants
#-------------------------

C="""
  These constants are used to tell the verb object which "style" of
  direct/indirect objects to expect. By default the verb is in state 3 which
  expects no direct or indirect objects. This is part of the disambiguation
  process.
  """

ALLOW_NO_DOBJS = 1          # Allow No Direct Objects
ALLOW_NO_IOBJS = 2          # Allow No Indirect Objects
ALLOW_ONE_DOBJ = 4          # Allow 1 Direct Object
ALLOW_ONE_IOBJ = 8          # Allow 1 Indirect Object
ALLOW_MULTIPLE_DOBJS = 16   # Allow Multiple Direct Objects
ALLOW_MULTIPLE_IOBJS = 32   # Allow Multiple Indirect Objects
ALLOW_OPTIONAL_DOBJS = 64   # Allow Optional Direct Objects

#---------------------------------
# All asIF visual editor constants
#---------------------------------

C="""
  asIF is a visual editor for PAWS programs.

  We also define a constant, AsIf_TrueFalseType.  AsIF needs to distinguish
  between true/false values (which are presented with a checkbox) and
  numbers (which are presented with an entry field) -- but this is a
  distinction Python doesn't make on its own.  So we define the constant
  TrueFalseType with an arbitrary value, whose sole purpose is to tell
  AsIF to use a checkbox rather than an entry field.
  """
  
AsIF_TrueFalseType = 1

#********************************************************************************
#                                 Library Imports
#
C="""
  We need some standard Python libraries. These aren't part of PAWS, rather
  they're supplied as part of Python. It's good programming practice not to
  "re-invent the wheel" when you don't have to, so always look for a pre-written
  library to do your work for you!
  """

import os               # Operating System Related Functions
import pickle           # picking functions (for save/restore)
import re               # Regular Expressions
import string           # String handling functions
import random           # Random # generator & functions
import sys              # System related functions
import types            # variable type identifiers
import wx               # wxPython GUI
 
#********************************************************************************
#                            Bootstrap Classes/Functions
#
C="""
  To avoid some chicken-and-egg problems with terminal handling we define a 
  few non-terminal classes now, such as ClassFundamental and ClassActiveIO.
  These classes are the "Adam and Eve" classes from which all other classes
  and objects in PAWS, Universe, and your game descend.
 
  The functions are truly fundamental, so we define them now because Python
  likes things defined in a file before they're used. 
  """

def Union(List1,List2):
    """Returns union of two lists"""

    #-----------------------------
    # Copy List 1 Into Return List
    #-----------------------------

    # Put a copy of List 1 into ReturnList. This gives us the base list to
    # compare against.

    ReturnList = List1[:]
    
    #---------------------------
    # For Each Element In List 2    
    #---------------------------
                                                
    for Element in List2:        
        
        #-----------------------------------------
        # Append Element To Return List If Missing
        #-----------------------------------------

        # If Element isn't in the return list, append it.
        
        if not Element in ReturnList: ReturnList.append(Element)
        
    
    #-----------------
    # Return To Caller
    #-----------------

    # The return list now contains a union of list 1 and list 2. 

    return ReturnList

def BaseClasses(Class):
    """
    This function takes a class and recursively returns a list of the
    class's base classes, starting with the object's immediate parent(s)
    and stepping upward through all the object's ancestors.
    """

    #-------------------------
    # Create Empty Return List
    #-------------------------

    C="""
      This creates an empty list as a starting point. Since this function
      returns a list of ancestor classes for a passed class, the default 
      assumption (for error checking) is that an erroneous object has no base
      classes.
      """
      
    ReturnList = []
    
    #----------------------------
    # Exit if Class isn't a class
    #----------------------------

    C="""
      If the argument we were passed (Class) isn't actually a class object
      we exit the function immediately, returning ReturnList (which we set
      to [] in the statement above). 
      """
      
    if type(Class) <> types.ClassType: return ReturnList
    
    #-----------------------------
    # Append Class to return list.
    #-----------------------------

    C="""
      The first element of the return list MUST be the class we were passed.
      As an example, assume we were passed ClassFundamental as the argument.
      This class has no ancestors (it's created from the basic Python
      object).
    
      However BaseClasses(ClassFundamental) must return [ClassFundamental]
      to work properly with the ObjectBaseClasses() function.
      """

    ReturnList.append(Class)
    
    #---------------------------
    # Find Class's Base Class(s)
    #---------------------------

    C="""
      A classes base classes are stored in a tuple in the __bases__
      property. A tuple is kind of awkward for us since we want to return a
      list, but the FOR loop below handles the conversion gracefully.
      """
      
    ClassTuple = Class.__bases__
    
    #-----------------------
    # For Each Base Class...
    #-----------------------

    # Remember that Python supports multiple inheritance. This means that any
    # given class can contain multiple base classes, and when that's the case
    # we have to follow the chain of ancestors for each class.
    #
    # By convention to make multiple inheritance more useful and less confusing
    # in PAWS a class may have only one base class, along with service classes.
    # A service class by definition has no ancestors (Python's base object
    # isn't counted). Thus we really only follow one chain down. For instance,
    # in Thief's Quest the ClassTQRoom class is composed of
    # ServiceDictDescription (a service class) and ClassRoom (a base class).
    #
    # Thus in theory ClassTuple contains two classes, ServiceDictDescription
    # and ClassRoom. The FOR loop thus executes twice. BaseClass will be 
    # ServiceDictDescription the first time through the loop and ClassRoom the
    # second time through.
    
    for BaseClass in ClassTuple:
        
        #-------------------------------
        # Call BaseClasses() Recursively
        #-------------------------------
        
        # We want to add any base classes to ReturnList THAT IT DOES NOT
        # ALREADY HAVE. To accomplish this we use the Union() function and
        # pass it the existing return list (as the base list for comparison)
        # and the list resulting from the base classs of BaseClass (our FOR
        # loop variable).
        #
        # Sharp eyed readers will note we're calling THIS FUNCTION to get a 
        # list of base classes. While somewhat mind-bending, this is perfectly
        # legal and logical.
        #
        # Having a function call itself within itself is called RECURSION. 
        # Recursion works because we're not really calling the function itself,
        # we're calling an identical copy of the function with a new argument.
        # As far as the computer is concerned they are two seperate functions,
        # and are "named" differently. The computer sees nothing special since
        # the recursive call creates a new function.
        #
        # As you could guess there has to be a stopping point, or recursion 
        # would go on forever. In Python you must define a class in terms of
        # an ancestor class--and so on and so on...
        #
        # So eventually you get to the Python base object, which isn't defined
        # as a class. An empty list is returned and the recursive calls are
        # completed.
        #
        # Recursion can go 20 or more levels deep, but it will end eventually. 
        
        ReturnList = Union(ReturnList,BaseClasses(BaseClass))
        
    
    #-----------------
    # Return To Caller
    #-----------------

    # Now the return list will contain every base class a class is composed of,
    # all the way back to the Python object (which isn't included). The first
    # class in the list will always be the one passed to us.

    return ReturnList
  
def ObjectBaseClasses(Object):
    """
    This funcion takes an object and returns a list of the object's base
    classes, starting with the object's immediate parent(s) and stepping
    upward through all the object's ancestors.
    """
    
    #-------------------------
    # Create Empty Return List
    #-------------------------

    # An empty return list gives us a starting point to return base classes 
    # with.

    ReturnList = []
        
    #------------------------------------
    # Return [] if Object not an Instance
    #------------------------------------ 

    # If the passed Object isn't an instance (object) then we return the empty
    # Return List that we defined above. This is an error check to prevent
    # a class from being passed. This function will fail if a class were passed
    # to it.

    if type(Object)<>types.InstanceType: return ReturnList
    
    #--------------------------
    # Get Object's Base Classes
    #--------------------------
    
    # We use the BaseClasses() function to find the object's classes. This is 
    # why we had to check to make sure Object was really an object and not a 
    # class, because a class doesn't have a __class__ property.

    ReturnList = BaseClasses(Object.__class__)
    
    
    #-----------------
    # Return To Caller
    #-----------------
    
    # We return to caller with a list of the Object's base classes.

    return ReturnList
    


class ClassFundamental:
    """
    The Fundamental Class is intended to supply all classes defined in PAWS
    as well as "plumbing" methods that allow us certain liberties with the
    Python programming language.

    Certain constraints are built-in Python assumptions. Properties and
    methods have differing syntax, making them impossible to interchange
    freely. This has unfortunate implications, especially for game authors
    coming from TADS.

    This class helps alleviate some of the more annoying problems.
    """

    def MakeCurrent(self):
        """
        Because "self" isn't really a variable in the global sense we use
        this method to explicitly mark which object is "current".
        Global.CurrentObject will always equal "self" and can safely be
        used in place of self when creating services that need to refer to
        self with {} expressions.
        """
        
        Global.CurrentObject = self
    
    def Get(self,Attribute):
        """
        Python has different syntax for returning the value of properties
        versus the value of methods. Because we want to allow Location and
        other attributes to be either a property OR a method we had to
        develop this method.

        Note, only methods without arguments can be returned by this
        function. "self" doesn't count as an argument.
        """
        
        #------------------------------------
        # Return None If self lacks Attribute
        #------------------------------------

        # self refers to this object (for example, a rock). So the code 
        # rock.Get("Location") would be the same as rock.Location, except this
        # method returns None instead of raising an exception if rock lacks the
        # Location property/method. 

        if not hasattr(self,Attribute): return None
        
        #-----------------------
        # Return Attribute Value
        #-----------------------
        
        # If the attribute isn't a method use getattr() to return the property
        # value. If the attribute is a method use getattr() to return the 
        # ADDRESS of the attribute, which we then use an indirect reference
        # to execute the method.
        #
        # Therefore if Location was a property rock.Get("Location") is
        # identical to rock.Location.
        #
        # If Location is a method then rock.Get("Location") is identical to
        # rock.Location(). 
        #
        # This is advanced programming, you can ignore it if you don't
        # understand it, since you're unlikely to do this type of thing
        # yourself.
        
        if type(getattr(self,Attribute)) <> types.MethodType:
            return getattr(self,Attribute)
        else:
            return getattr(self,Attribute)()
                 
    def InheritProperties(self):
        """
        To make object __init__() functions more generic (because they're
        involved and somewahat difficult to extend) we created this method
        to actually define an object's properties when it is instantiated.
        All you have to do is add the class and instance properties you
        want to set. This method will automatically run SetMyProperties()
        for each ancestor class, starting with the descendant of
        ClassFundamental and progressing through the generations until it
        has run all of them.

        For example, when this code is run for an object created with
        ClassRoom it runs the following code automatically:
        
            ClassBaseObject.SetMyProperties()
            ClassBasicThing.SetMyProperties()
            ClassRoom.SetMyProperties()
        """

        #----------------
        # Get Family Tree
        #----------------

        # The family tree is ordered by most RECENT ancestor first, so we need
        # to reverse the order to make the OLDEST ancestor first. This insures
        # that properties are overridden by descendant classes as they should
        # be.

        Ancestors = ObjectBaseClasses(self)
        Ancestors.reverse()
        
        #------------------------------------
        # Remove Class Fundamental If Present
        #------------------------------------

        # ClassFundamental is the root class of all classes--but not services!
        # That's why we need to check to see if it's present. If so, we remove
        # it so a recursive infinite loop won't occur when this method tried 
        # to call itself...

        if ClassFundamental in Ancestors: Ancestors.remove(ClassFundamental)
        
        #------------------
        # For Each Class...
        #------------------

        # For each ancestor we try to call SetMyProperties(). If an exception
        # occurs because the ancestor doesn't have SetMyProperties() defined we
        # simply ignore the exception.

        for Ancestor in Ancestors:
            try:
                Ancestor.SetMyProperties(self)
            except:
                pass


#********************************************************************************
#                           Terminal Classes                
#
# In this section we define the code that runs the wxPython terminal.

class ClassActiveIO(ClassFundamental):
    """Holds the Active Terminal reference."""
        
    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Active I/O"
        ClassFundamental.InheritProperties(self)
    
    def SetMyProperties(self):
        """Set Terminal's Properties"""
       
        #----------
        # Active IO
        #----------

        # This variable (actually a property, but who's counting?) holds the
        # current IO object, the object used to input and output to the hardware. 
        # This allows for device independence, we can use the default text IO 
        # supplied by Python's raw_input() and print functions, or we can take
        # advantage of GLK or other GUI interfaces. We put this here so that
        # the chosen IO device can attach itself and the save/restore functions
        # will save the parser object properties (particularly vocabulary).

        self.ActiveIO = None

        #----------------
        # Frame Reference
        #----------------

        # This is a reference to the Frame class that imports the Core
        # and Universe, it also holds the display and input field that
        # interact with the player.
        
        self.Frame = None

    def ActiveTerminal(self):
        """Returns ActiveIO.ActiveIO"""
        return self.ActiveIO

class ClassTerminal(ClassFundamental):
    """
    wxPython Terminal
    
    This is a wxPython based GUI terminal capable of lights, colors, bells
    and whistles...at least, once those features are implemented.

    wxPython terminals have the following abilities:

    Querying Screen dimensions (NO)
    Query cursor position (NO)
    Move cursor to beginning of next line (YES)
    Homing cursor (YES)
    Full cursor control (NO)
    Screen Erase (Yes)
    Screen attributes (bold, inverse video, etc. NO BLINKING!) (YES)
    Screen Color (16 color foreground/16 color background) (YES)
    Independent status line at bottom of the screen (YES)
    Word Wrap (YES)
    Query IO Capabilities (NO)
    Font style and size changes (YES)
    """    
    
    def __init__(self):
        """Sets default instance properties and initializes terminal."""
        self.NamePhrase = "PAWS Terminal"
        ClassFundamental.InheritProperties(self)
        self.SetMyProperties()    
    
    def SetMyProperties(self):
        """Set I/O Properties"""
        
        #------------------
        # Screen Management
        #------------------

        self.CurrentFontPitch = 12
        self.CurrentFont = None
        
        #--------------------------
        # I/O Capability Properties
        #--------------------------
        
        self.BackColor = TRUE
        self.Bold = TRUE
        self.CrLf = TRUE
        self.CursorControl = FALSE
        self.Erase = TRUE
        self.Home = TRUE
        self.FontColor = TRUE
        self.FontPitch = TRUE
        self.FontFace = TRUE
        self.Italic = TRUE
        self.Underline = TRUE
        
        #---------------------
        # Attribute Properties
        #---------------------

        self.BLACK        = 'black'
        self.BLUE         = 'blue'
        self.GREEN        = 'green'
        self.CYAN         = 'cyan'
        self.RED          = 'red'
        self.MAGENTA      = 'magenta'
        self.BROWN        = 'brown'
        self.GRAY         = 'grey'
        self.LIGHTBLACK   = 'dark grey'
        self.LIGHTBLUE    = 'light blue'
        self.LIGHTGREEN   = 'lime green'
        self.LIGHTCYAN    = 'aquamarine'
        self.LIGHTRED     = 'coral'
        self.LIGHTMAGENTA = 'orchid'
        self.YELLOW       = 'yellow'
        self.WHITE        = 'white'

    def ClearScreen(self):
        """Clear Screen"""
        Terminal.Frame.TDisplay.Clear()
    
    def Configure(self):
        """Configure terminal colors"""
        Say("Use the View Fonts... menu item instead.")            
    
    def DisplayStatusLine(self,DisplayString):
        """Display Status Line"""
        Terminal.Frame.TStatusBar.SetStatusText(DisplayString)

    def Feed(self,Command):
        """
        Feeds a command to the terminal, just as if the player had typed
        it.
        """
        Terminal.Frame.TInput.Clear()
        Terminal.Frame.TInput.AppendText(Command)
        Terminal.Frame.ProcessPlayerInput()
    def GetXY(self):
        TD = Terminal.Frame.TDisplay
        x,y = TD.PositionToXY(TD.GetInsertionPoint())
        return x,y

    def HomeCursor(self):
        """Return Cursor To Home Position"""        
        pass
        
    def Input(self,PromptString):
        """Get player input."""
        
        #-------------------
        # Get Player's Input
        #-------------------

        InputValue = Terminal.Frame.TInput.GetValue()
        if InputValue is None: InputValue = ""

        #---------------------------------------------
        # Echo the player's command in the Output pane
        #---------------------------------------------

        self.RawOutput(" " + InputValue + "\n")

        if Global.Transcribe:
            Global.LogFile.write("\n\n"+PromptString+InputValue+"\n")
            if Global.Debug: Global.DebugFile.write("\n\n"+PromptString+InputValue+"\n")
       
        #------------------------------
        # Return Player's Typed Command
        #------------------------------
       
        return InputValue
    
    def MoreMessage(self):
        """
        Insert a 'more' message, wait for '<Return>', then erase the 'more'
        message. MORE doesn't work in this terminal yet.
        """
        pass
                
    def MoveCursor(self,Row,Column):
        """Move Cursor"""
        pass
    
    def NewLine(self):
        """Print a CR/LF to the screen."""
        self.Output("\n")
        self.CurrentScreenColumn, self.CurrentScreenLine = self.GetXY()
            
    def NewParagraph(self):
        """
        Prints a pair of CR/LF's to the screen, making a blank line between
        paragraphs.
        """
           
        self.NewLine()
        self.NewLine()
        
    def Output(self,OutputString):
        """
        Display Output string to the terminal.
        
        The color and style settings must be set BEFORE calling output,
        using the SetStyle() method.
        """

        self.RawOutput(OutputString)
        if OutputString <> "\n": self.RawOutput(" ")
        self.CurrentScreenColumn,self.CurrentScreenLine = self.GetXY()
    
    def RawOutput(self,Text):
        """
        Output directly to terminal. The last line moves the view back 500
        characters, which helps eliminate the lack of scrolling in the text
        control on Windows.
        """
        TD = Terminal.Frame.TDisplay
        TD.SetEditable(True) 
        TD.AppendText(Text)
        TD.SetEditable(False) 
        TD.ScrollLines(-1)
        #TD.ShowPosition(TD.GetLastPosition() - 200)

    def SetStyle(self,
                 Foreground = None,
                 Background = None,
                 Font = None,
                 FontPitch = None,
                 IsNormal = True,
                 IsBold = False,
                 IsItalic = False,
                 IsUnderlined = False):
        """
        Set terminal's default style, color, font, and style.
        """

        TF = Terminal.CurrentFont
        TA = wx.TextAttr(wx.NullColor,wx.NullColor)
        TD = Terminal.Frame.TDisplay

        if FontPitch: TF.SetPointSize(FontPitch)
        #if Font: TF.SetFontFace(Font)

        if Foreground: TA.SetTextColour(Foreground)
        if Background: TA.SetBackgroundColour(Background)

        if IsNormal:
             TF.SetStyle(wx.FONTSTYLE_NORMAL)
             TF.SetWeight(wx.FONTWEIGHT_NORMAL)
    
        if IsBold: TF.SetWeight(wx.FONTWEIGHT_BOLD)
        if IsItalic: TF.SetStyle(wx.FONTSTYLE_ITALIC)
        TF.SetUnderlined(IsUnderlined)
        
        TA.SetFont(TF)
        TD.SetDefaultStyle(TA)
        
    def Terminate(self):
        """Close up the Tkinter widgets."""
        self.RawOutput("\n")
        self.MoreMessage()
        Terminal.Frame.TDisplay.SetFocus()
        Terminal.Frame.TInput.Enable(False)
        Terminal.Frame.TInput.Clear()
        Terminal.Frame.TInput.AppendText("Please click File / Exit to close terminal")
        
    #----------------------
    # Background Dim Colors
    #----------------------
    
    def A_BBLACK(self):
        Terminal.SetStyle(Background=self.BLACK)

    def A_BBLUE(self):
        Terminal.SetStyle(Background=self.BLUE)

    def A_BBROWN(self):
        Terminal.SetStyle(Background=self.BROWN)

    def A_BCYAN(self):
        Terminal.SetStyle(Background=self.CYAN)

    def A_BGRAY(self):
        Terminal.SetStyle(Background=self.GRAY)
        
    def A_BGREEN(self):
        Terminal.SetStyle(Background=self.GREEN)

    def A_BMAGENTA(self):
        Terminal.SetStyle(Background=self.MAGENTA)

    def A_BRED(self):
        Terminal.SetStyle(Background=self.RED)
        
    #-------------------------
    # Background Bright Colors
    #-------------------------

    def A_BLBLACK(self):
        Terminal.SetStyle(Background=self.LIGHTBLACK)

    def A_BLBLUE(self):
        Terminal.SetStyle(Background=self.LIGHTBLUE)

    def A_BLCYAN(self):
        Terminal.SetStyle(Background=self.LIGHTCYAN)

    def A_BLGREEN(self):
        Terminal.SetStyle(Background=self.LIGHTGREEN)

    def A_BLMAGENTA(self):
        Terminal.SetStyle(Background=self.LIGHTMAGENTA)

    def A_BLRED(self):
        Terminal.SetStyle(Background=self.LIGHTRED)

    def A_BWHITE(self):
        Terminal.SetStyle(Background=self.WHITE)

    def A_BYELLOW(self):
        Terminal.SetStyle(Background=self.YELLOW)

    #----------------------
    # Foreground Dim Colors
    #----------------------

    def A_BLACK(self):
        Terminal.SetStyle(Foreground=self.BLACK)

    def A_BLUE(self):
        Terminal.SetStyle(Foreground=self.BLUE)

    def A_BROWN(self):
        Terminal.SetStyle(Foreground=self.BROWN)

    def A_CYAN(self):
        Terminal.SetStyle(Foreground=self.CYAN)

    def A_GRAY(self):
        Terminal.SetStyle(Foreground=self.GRAY)
        
    def A_GREEN(self):
        Terminal.SetStyle(Foreground=self.GREEN)

    def A_MAGENTA(self):
        Terminal.SetStyle(Foreground=self.MAGENTA)

    def A_RED(self):
        Terminal.SetStyle(Foreground=self.RED)
        
    #-------------------------
    # Foreground Bright Colors
    #-------------------------

    def A_LBLACK(self):
        Terminal.SetStyle(Foreground=self.BLACK)

    def A_LBLUE(self):
        Terminal.SetStyle(Foreground=self.BLUE)

    def A_LCYAN(self):
        Terminal.SetStyle(Foreground=self.CYAN)

    def A_LGREEN(self):
        Terminal.SetStyle(Foreground=self.GREEN)

    def A_LMAGENTA(self):
        Terminal.SetStyle(Foreground=self.MAGENTA)

    def A_LRED(self):
        Terminal.SetStyle(Foreground=self.RED)

    def A_WHITE(self):
        Terminal.SetStyle(Foreground=self.WHITE)

    def A_YELLOW(self):
        Terminal.SetStyle(Foreground=self.YELLOW)

    

    #-------------------
    # Styles (bold, etc)
    #-------------------
    
    def A_BLINK(self):
        Terminal.SetStyle(IsBold=True,IsItalic=True)

    def A_BOLD(self):
        Terminal.SetStyle(IsBold=True)
    
    def A_DIM(self):
        Terminal.SetStyle(IsBold=False)

    def A_INPUT(self):
        Terminal.SetStyle(IsBold=False,IsItalic=False,IsUnderlined=False)

    def A_ITALIC(self):
        Terminal.SetStyle(IsItalic=True)
    
    def A_MORE(self):
        Terminal.A_GRAY()
        Terminal.A_DIM()

    def A_NORMAL(self):
        Terminal.A_BWHITE()
        Terminal.A_BLACK()
        Terminal.A_INPUT()
        Terminal.SetStyle(FontPitch=self.CurrentFontPitch,
                          Font=self.CurrentFont)
        
    def A_REVERSE(self):
        Terminal.A_BBLACK
        Terminal.A_WHITE()
        Terminal.A_INPUT()

    def A_STANDOUT(self):
        Terminal.A_BLUE()
        Terminal.A_BOLD()

    def A_TITLE(self):
        Terminal.SetStyle(Foreground=self.BLACK,
                          FontPitch=self.CurrentFontPitch+4,
                          Font=self.CurrentFont,
                          IsBold=True)

    def A_UNDERLINED(self):
        Terminal.SetStyle(IsUnderlined=True)
        
#********************************************************************************
#                                 Utility Functions
#
# These functions are of general use for PAWS, Universe, and the game author
# themselves. Note the functions are arranged in alphabetical order to make them
# easy to find.

def AppendDictList(Dict,Key,Value):
    """
    Appends value to a list dictionary

    This routine doesn't return a value, it appends a value to a dictionary
    of lists. A Dictionary List is just a dictionary who's values are
    actually lists. For example, the VerbsDict is a list dictionary, it
    might look like this:

    {'look': [LookVerb, LookIntoVerb, LookThroughVerb],
     'quit': [QuitVerb],
     'exit': [QuitVeb]}

    You supply the dictionary name, the key, and the value you want to
    append. The key must be a string, either a single value (without any
    commas) or multiple values seperated by commas. For instance:

    AppendDictList(NounsDict,"rock,stone",SmallRock)

    This would place SmallRock in the dictionary under two keys,
    "rock", and "stone".
    """
    
    #------------
    # Massage Key
    #------------

    # We have to massage the key to make it easier to work with. The
    # first thing we do is force the key strings to lower case
    # (string.lower), then split the comma delimited string into a
    # list of strings (string.split).
    #
    # Since this function is mainly used to add words to the verb, noun,
    # preposition and adjective dictionaries. We want to make sure
    # the developer doesn't have to worry about case sensitivity when
    # defining verbs and objects.

    WordList = string.split(string.lower(Key),",")

    #-----------------------------
    # For each word in the list...
    #-----------------------------

    # For each word in the wordlist (dictionary key) do the following...

    for word in WordList:

        #----------------------------
        # Word in dictionary already?
        #----------------------------
        
        # If the word is already in the dictionary we append the value
        # to the entry. This has the effect of adding Value to the
        # list of values already filed under the key.
        #
        # If the word ISN'T in the dictionary, we add the LIST of Value
        # to the dictionary. Notice how the Value is surrounded by
        # square brackets?
        #
        # This is a 'casting' trick. It forces value (which is generally
        # one item) to become a list of one item. This is important
        # because append only works with a list. If we didn't convert
        # Value to a list the second object added to the same key value
        # would cause the game to blow up with an error message.

        if Dict.has_key(word):
            Dict[word] = Union(Dict[word],[Value])
        else:
            Dict[word] = [Value]

def Choose(Decision,TrueChoice,FalseChoice):
    """
    Ternary IIF operator, returns TrueChoice or FalseChoice based on
    Decision.
    
    This function is handy for use inside Curly Brace Expressions (CBE's).
    Decision must evaluate to true or false (0 or 1, empty or full, etc).
    If TRUE then TrueChoice will be returned, else FalseChoice will be
    returned.
    """

    if Decision:
        return TrueChoice
    else:
        return FalseChoice

def ClearScreen():
    """Clears the screen. This is the function game authors should use."""
    Terminal.ClearScreen()


def Complain(Text=""):
    """Call Say(Text) and return TURN_CONTINUES.

    Because the action of printing a message and going back for a more 
    player input is so common (it's called "complaining") there's a simple
    way to do both steps at once. Usually a compaint is part of a return
    statement, like this:
    
    return Complain("I don't understand.")
    """

    Say(Text)
    return TURN_CONTINUES
def DebugTrace(Text):
    """
    This function lets you put debug tracing into the system and turn it on
    or off with Global.Debug. TRUE is on, FALSE if off.
    
    The output of the trace is written to the stdout window, if
    Global.Transcribe is TRUE it is also written to the debug file named
    <game name>.DBG.
    """
    
    if not Global.Debug: return
    print Text
    if Global.Transcribe: Global.DebugFile.write(Text+"\n")

def DebugDObjList():
    """
    This function is used to list the contents of the (parsed) list of
    direct objects associated with the current command. It's intended
    to help debug the parser and verbs that use direct objects.
    
    Note it calls DebugTrace() for each direct object name.
    """
    
    for Object in P.DOL():
        DebugTrace("-->" + Object.Get(SDesc))


def DebugIObjList():
    """
    This function is used to list the contents of the (parsed) list of
    indirect objects associated with the current command. It's intended
    to help debug the parser and verbs that use indirect objects.
    
    Note it calls DebugTrace() for each indirect object name.
    """

    for Object in P.IOL():
        DebugTrace("Debug-->" + Object.Get(SDesc))


def DebugPassedObjList(Msg,ObjList):
    """
    This function is used to list the contents of the (passed) list of
    objects. The output is titled by Msg. It's intended to help debug the
    parser and verbs that use objects.
    """

    DebugTrace(Msg)
    for Object in ObjList:
        DebugTrace("-->" + Object.SDesc())
    return ""
    

def DeleteDictList(Dictionary,Object=None):
    """
    This function deletes an object from a dictionary list (a dictionary who's
    values are lists) and replaces it.
    """
    
    #-------------------------
    # Return if no real object
    #-------------------------

    # If Object is None then there's nothing to do.

    if Object == None: return
    
    #---------------------------
    # Return If Dictionary Empty
    #---------------------------

    # If the dictionary is empty there's nothing to do either.

    if len(Dictionary) == 0: return
    
    #------------------------------
    # For each key in dictionary...
    #------------------------------

    # For each key in the dictionary we retrieve the value, which should be
    # a list. If it isn't we skip this key.

    for key in Dictionary.keys():
        
        #------------------------------
        # Retrieve List From Dictionary
        #------------------------------

        # List is the value of the dictionary key. For example:
        # [LookVerb, LookIntoVerb, LookUnderVerb].

        List = Dictionary[key]
        
        #---------------------
        # Continue If Not List
        #---------------------

        # If this dictionary key isn't a list, we skip this key and continue
        # the for loop, getting the next key.

        if type(List) <> type([]): continue

        
        #-------------------------
        # Remove Object If In List
        #-------------------------

        # If object is in list, remove it. If the resulting list is 0 length the 
        # entire dictionary entry should be deleted, otherwise the current
        # dictionary entry will be replaced with the new List.

        if Object in List:
            List.remove(Object)
            if len(List) == 0:
                del Dictionary[key]
            else:
                Dictionary[key] = List




def DeleteObjectFromVocabulary(Object):
    """
    PAWS requries the use of a pre-written library. This library (normally
    Universe) creates lots of objects, usually verbs, that sometimes need to
    be overridden. To do this you need to remove all references from the
    vocabulary dictionaries of the old objects (so Python can "garbage
    collect" them) before replacing them with your new definition.

    This function deletes the object from the Verb, Preposition, Noun and
    Adjective parser dictionaries so you can either disable the verb or
    replace it with your own. It also works for objects.
    """

    DeleteDictList(P.AP().VerbsDict,Object)
    DeleteDictList(P.AP().PrepsDict,Object)
    DeleteDictList(P.AP().NounsDict,Object)
    DeleteDictList(P.AP().AdjsDict,Object)

def DisambiguateList(List,TestMethod,ErrorMethod,Actor=None):
    """
    This function actually figures out which object the player meant.
    It does so by testing the object with the passed TestMethod. If the
    result is true the object is kept, if false it's discarded.

    When all objects in the list have been discarded (because none of them
    return true) the function prints the ErrorMethod.

    This function returns either a single object (if it can be
    disambiguated), an empty list (if no objects pass the test), or a list
    of objects that do pass the test.
    """

    #-------------------------
    # Return List Starts Empty
    #-------------------------

    # Our return list starts empty because we're going to be appending
    # to it.

    ReturnList = []
    
    #-----------------------
    # Set Last Tested Object
    #-----------------------

    # If ALL of the objects in List fail the test we need to use the last
    # object tested as error method argument. Unfortunately the Object
    # variable set in the FOR loop disappears when the loop is completed.
    #
    # LastTestedObject saves the last object tested by the loop. Under certain
    # circumstances, that object may be None, which would cause the ErrorMethod
    # to crash if used as an argument, which is why we have to test for it.
    #
    # Setting LastTestedObject to None now is good programming practice, it 
    # gives the variable existance now and sets it to a known value.

    LastTestedObject = None
    
    #---------------------------
    # For Each Object in List...
    #---------------------------

    # We're guaranteed that List will always be a list, since this function
    # is only called for ambiguous object lists.

    for Object in List[:]:

        #-----------------------
        # Set Last Tested Object
        #-----------------------

        LastTestedObject = Object

        #----------------
        # Actor involved?
        #----------------

        
        # Some test methods require an actor AND an object, while some dont.
        # IsReachable(), for example needs to calculate the path between two
        # objects. If an actor is needed for the test method, it will be
        # passed to DisambiguateListOfLists which in turn passes it to this
        # function.

        if Actor == None:
            TestResult = TestMethod(Object)
        else:
            TestResult = TestMethod(Object,Actor)

        #--------------------
        # Object passes test?
        #--------------------

        
        # If the object passes the test we append it to the ReturnList. If
        # it doesn't...
        #
        # In that case we delete it from the List. If the List loses EVERY
        # member we've eliminated all objects, so we say the error method
        # of the object we just eliminated.

        if TestResult == TRUE:
            ReturnList.append(Object)
            DebugTrace("    "+Object.SDesc() + " passed")
        else:
            List.remove(Object)
            DebugTrace("    "+Object.SDesc() + " failed")

    
    #------------------------
    # No Items in ReturnList?
    #------------------------

    # If there are no items in the return list we need to use the last object
    # tested and print the error condition, since every object failed! We then
    # return an empty list.

    if len(ReturnList) == 0:
        Say(ErrorMethod(LastTestedObject))
        return []

    
    #--------------------------------
    # Exactly One item in ReturnList?
    #--------------------------------

    # If there is exactly one item on the return list we're finished!
    # Instead of returning ReturnList we return just the 0'th (first) element
    # of ReturnList. This returns a single object instead of a list.
    #
    # If there are no objects in ReturnList or more than 1 we return the
    # entire list.

    if len(ReturnList) == 1:
        return ReturnList[0]
    else:
        return ReturnList[:]




def DisambiguateListOfLists(ListOfLists,TestMethod,ErrorMethod,Actor=None):
    """
    Break list of lists into multiple lists for DisambiguateList() function
    
    This function performs "disambiguation" of the kinds of object lists
    created by the parser. In other words, it intelligently chooses which
    objects are intended when there's a choice.

    For instance, if the game contains three keys, a bone key, a brass key,
    and a silver key but only one rock and the player says "get key and
    rock" the resulting direct object list looks like:

    [ [BoneKey,BrassKey,SilverKey], [Rock] ]

    Notice the direct object list contains two other lists! Key could refer
    to any of the keys, at the time of parsing there's no way to know which
    is intended. Thus we say the key is ambiguous.

    Rock isn't of course, since there's only one rock in the game.

    The theory of disambiguation is complex and messy, so pay close
    attention. There are three major problems we have to deal with.

    First, we're starting off with  a list of lists. It's messy, but the
    only way we can handle ambiguous objects.

    The second problem is that of delegation. Since the PAWS engine is
    intended to be library independent we have to build an engine that can
    work with anyone's library. This means both the test method(s) and the
    error method(s) are supplied by the library, along with the specific
    disambiguation method itself.

    Which leads to our third problem. We have no way of predicting ahead of
    time which tests the library author will want to perform, or how many of
    them there will be. The implication is we have to be able to handle
    multiple disambiguation passes.

    There's another implication. If we handle multiple passes, then at some
    point part of the list will be single objects and part of the list will
    be lists!

    For example, let's say that there are two passes. The first tests to see
    if the objects are known. (Assume the player doesn't know a silver key
    exists in the game).

    The first pass yields: [ Rock, [BoneKey,BrassKey] ]

    Notice Rock is no longer a list, it's a single object. That's because
    the aim of disambiguation is to reduce our list of lists to a simple
    list of objects, if possible. Since the [Rock] list contains only one
    item we convert it to an object. We've eliminated the silver key, but
    key is still ambiguous.

    Second pass, are the items reachable? The bone key is in the basement,
    but both the rock and the brass key are in the kitchen with the player.

    Thus our second pass yeilds: [ Rock, BrassKey ] and our disambiguation
    is done.

    BUT there's a third pass, are all objects visible? Our third pass
    doesn't eliminate anything and yields: [ Rock, BrassKey ].

    And depending on the library you use there might be more passes yet. So
    we have to be able to handle all three states of the list.
    """

    #------------------------------------
    # Empty list automatically successful
    #------------------------------------

    if len(ListOfLists) == 0:
        return SUCCESS

    
    #-------------------------
    # Return List Starts Empty
    #-------------------------

    # Our return list starts empty because we're going to be appending to it.

    ReturnList = []
    
    #--------------------------------
    # For Each item in ListOfLists...
    #--------------------------------

        # Each item in the list of lists might be a single object (unambiguous)
    # or it might be a list of objects (ambiguous). The purpose of this loop
    # is to either directly append an unambiguous object to the return list
    # or pass an ambigous object list to the DisambiguateList function to see
    # if it can be disambiguated and append the result.

    for List in ListOfLists:
        
        #---------------------
        # Is Object ambiguous?
        #---------------------

        
        # Remember, "List" will either be a single object (unambigous) or
        # a list of objects with the same noun (ambiguous). If it is an
        # ambiguous list we pass it to the disambiguate function, which
        # will either return a single object if it was able to narrow it
        # down to one or it will return a (hopefully smaller) list of
        # objects. In either case we simply append the result to the
        # ReturnList.
        #
        # If the object isn't ambiguous we just append the object to the
        # return list.

        if type(List) == type([]):
            WorkList = DisambiguateList(List,TestMethod,ErrorMethod,Actor)
            ReturnList.append(WorkList)
            continue

        
        #-----------------------
        # Not Ambiguous, test it
        #-----------------------

        if Actor == None:
            TestResult = TestMethod(List)
        else:
            TestResult = TestMethod(List,Actor)

        #--------------------
        # Object fails test?
        #--------------------

        
        # If the object passes the test we append it to the ReturnList. If
        # it doesn't...
        #
        # In that case we delete it from the List. If the List loses EVERY
        # member we've eliminated all objects, so we say the error method
        # of the object we just eliminated.

        if not TestResult:
            DebugTrace("    "+List.SDesc() + " Failed")
            ListOfLists.remove(List)
            Say(ErrorMethod(List))
            DebugTrace("    "+List.SDesc() + " unambiguous failure")
            continue

        DebugTrace("    "+List.SDesc() + " passed")
        ReturnList.append(List)


    #-------------------
    # Remove empty lists
    #-------------------

    # From time to time the DisambiguateList() function will eliminate EVERY
    # object in the list. For example, the player says "get rock" but the
    # rock isn't here. In that case the DisambiguateList function returns
    # an empty list -- []. You may have (depending on the situation) many
    # empty lists in your ListOfLists.
    #
    # The line below eliminates empty lists, leaving single items and
    # object lists untouched. How it does it is something of a Python
    # mystery, but rest assured it works.

    ReturnList = filter(None,ReturnList)

    #---------------------------
    # Return New "List Of Lists"
    #---------------------------

    # The result of this function is either a partially disambiguated list
    # or a completely disambiguated one. The list of lists may be run
    # through this function again with a different test method to further
    # disambiguate the list.

    # Notice the peculiar syntax we use to assign ListOfLists. The reason
    # we do this is extremely involved, but the short form is that Python
    # doesn't support "pass by reference".
    #
    # Instead it passes a copy of an object reference. ListOfLists isn't
    # a copy of Global.CurrenDIObjList, for instance, it *points* to it.
    #
    # But the statement "ListOfLists = ReturnList" means that instead of
    # assigning ReturnList to Global.DObjList as you might expect, it
    # actually changes where ListOfLists is *pointing* to!
    #
    # By putting [:] on the end, we change this from pointer assignment to
    # object reference. Since ListOfLists is still pointing to Global.DObjList
    # it does what we want it to (replace Global.DObjList with a copy of
    # ReturnList).

    ListOfLists[:] = ReturnList[:]

    if len(ReturnList) > 0:
        return SUCCESS
    else:
        return FAILURE



def DoIt(CodeString,ReturnMessage=""):
    """
    This function takes a string and tries to turn it into valid Python
    code, then execute it. Its main purpose is for use in debugging, to set
    variables and the like, but you can execute any valid Python code
    fragment with it. Be careful!
    """
    try:
        eval(compile(CodeString,"<string>","exec"))
    except:
        Say("Syntax Error In CodeString")

    return ReturnMessage

def Fence(Token,Fence1='\"',Fence2='\"'):
    """
    This function takes token and returns it with Fence1 leading and Fence2
    trailing it. By default the function fences with quotations, but it
    doesn't have to.

    For example:

    A = Fence("hi there")
    B = Fence("hi there","'","'")
    C = Fence("hi there","(",")")
    D = Fence("hi there","[","]")

    yields the following:

    A -> "hi there"
    B -> 'hi there'
    C -> (hi there)
    D -> [hi there]
    """

    return Fence1+Token+Fence2

def GameDaemon():
    """
    This function is a DAEMON, a function that will be run automatically
    every turn by the game engine. All it does is increment the turn
    counter, but it demonstrates how to write a daemon.
    """

    Global.CurrentTurn = Global.CurrentTurn + 1
    Terminal.DisplayStatusLine(Global.StatusLine)

def Indent(Level):
    """
    This function merely creates a string of " ~t " (tab) characters for
    each indent level passed in the argument. It's intended to be used with
    Say(). For example, Indent(3) returns 3 tab characters. NOTE: TAB
    CHARACTERS TRANSLATE TO 3 SPACES, NOT ASCII CODE 9!
    """

    RV = ""
    for x in range(0,Level): RV = RV + " ~t "
    return RV

def Intersect(list1,list2):
    """
    This function takes two lists and returns a list of items common to both
    lists.
    """

    ReturnList = []

    for x in list1:
        if x in list2: ReturnList.append(x)

    return ReturnList

def InVocabulary(Word):
    """
    This function returns TRUE if the passed word is in the game's
    vocabulary, FALSE if it isn't.
    """

    if P.AP().NounsDict.has_key(Word): return TRUE
    if P.AP().VerbsDict.has_key(Word): return TRUE
    if P.AP().AdverbsDict.has_key(Word): return TRUE
    if P.AP().AdjsDict.has_key(Word): return TRUE
    if P.AP().PrepsDict.has_key(Word): return TRUE
    if P.AP().PronounsListDict.has_key(Word): return TRUE
    if Word in P.AP().ArticlesList: return TRUE
    if Word in P.AP().ConjunctionsList: return TRUE
    if Word in P.AP().DisjunctionsList: return TRUE
    if Word in P.AP().CommandBreaksList: return TRUE

    return FALSE

def NZ(PassedValue,ValueIfNone=""):
    """
    This function replaces the first argument with the second if the first
    argument is None. By default the second argument is an empty string.
    """

    if PassedValue:
        return PassedValue
    else:
        return ValueIfNone

def RunDaemons():
    """
    This function runs all daemons and fuses in Global.DaemonDict. It does
    all the scheduling for fuses and recurring fuses.
    """
    
    #---------------------
    # For Each Daemon/Fuse
    #---------------------
    
    # Global.DaemonDict.keys() returns a list of the keys in the dictionary. Each
    # key is a function reference so DaemonFuse, in addition to being the
    # dictionary key for this particular entry in Global.DaemonDict is also an
    # indirect reference to a function. That means the expression DaemonFuse()
    # will actually run the appropriate function!


    for DaemonFuse in Global.DaemonDict.keys():

        #-------------------------
        # Get Original Fuse Length
        #-------------------------

        # Remember, the original fuse length will be a negative, 0, or positive
        # number. If negative the remaining turns will be reset to the absolute
        # value of this number.

        FuseLength = Global.DaemonDict[DaemonFuse][1]
        
        #-------------------
        # Get Remaining Time
        #-------------------

        # Get the remaining time. Note this is the time *before* the fuse is
        # reduced for the current turn. For example, if the value was 1, then
        # the fuse will execute THIS turn, since 1 minus 1 is 0. However, if the
        # value were 2 it would execute NEXT turn, since 2 - 1 is 1, not 0.

        RemainingTime = Global.DaemonDict[DaemonFuse][0]
        
        #---------------------
        # Identify Daemon Type
        #---------------------

        # Any function in Global.DaemonDict can be either a daemon, a fuse, or a
        # recurring fuse. A daemon runs every turn, a fuse runs after X turns
        # delay and is then removed from DaemonDict, a recurring fuse runs after
        # a delay of X turns but is then reset to run in another X turns.

        if FuseLength < 0:  DaemonType = RECURRING_FUSE
        if FuseLength == 0: DaemonType = DAEMON
        if FuseLength > 0:  DaemonType = FUSE
        
        #-----------------
        # Handle If Daemon
        #-----------------

        # If the function we're examining is a daemon (has an original fuse
        # length of 0) then it's supposed to run every turn. So we run it and
        # continue, which skips the rest of the FOR loop. Note we DO NOT return!
        # If we returned then only the first daemon/fuse in the dictionary would
        # execute.

        if DaemonType == DAEMON:
            DaemonFuse()
            continue
        
        #----------------------
        # Reduce Remaining Time
        #----------------------

        # By reaching this point we know the function being examined is either a
        # fuse or a recurring fuse, so we shorten the remaining time by 1. We
        # know we aren't dealing with a daemon because daemons are handled above,
        # we'd never have gotten here if it was a daemon.
        #
        # Notice we reduce RemainingTime, then assign it back to the dictionary.
        # We use RemainingTime because it makes the code easier to read and
        # nderstand.

        RemainingTime -= 1
        Global.DaemonDict[DaemonFuse][0] = RemainingTime
        
        #-------------------------
        # Continue If Time Remains
        #-------------------------

        # If there's still remaining time (RemainingTime is more than 0) then we
        # need do nothing further for either fuses or recurring fuses, since
        # they haven't "gone off" yet.

        if RemainingTime > 0: continue
        
        #----------------------
        # Execute Fuse Function
        #----------------------

        # If we've gotten this far it means the Remaining Time has been
        # exhausted, it has reached 0. Remember that DaemonFuse contains an
        # indirect function reference. All we have to do to execute the function
        # is put parentheses after it, as we do in the code below. If DaemonFuse
        # contains a reference to the ClearScreen function, for instance, then:
        #
        # DaemonFuse()
        #
        # would be identical to:
        #
        # ClearScreen()

        DaemonFuse()
        
        #----------------------
        # Handle If Normal Fuse
        #----------------------

        # If we're dealing with a regular fuse we simply call StopDaemon and
        # pass it DaemonFuse, which is the indirect reference to the function we
        # just executed. This removes it from Global.DaemonDict. Then we
        # continue, to skip the rest of the FOR loop.

        if DaemonType == FUSE:
            StopDaemon(DaemonFuse)
            continue
        
        #-------------------------
        # Handle If Recurring Fuse
        #-------------------------

        # If dealing with a recurring fuse (one that resets itself after the
        # function is executed) then we reset RemainingTime to the absolute
        # value of FuseLength. This turns the negative FuseLength into a
        # positive value for Remaining time.
        #
        # Then we set the 0'th (first) element of the dictionary to
        # the remaining time. Doing it this way makes the code easier
        # to understand than the equivalent single line:
        #
        # Global.DaemonDict[DaemonFuse][0] = abs(FuseLength)

        if DaemonType == RECURRING_FUSE:
            RemainingTime = abs(FuseLength)
            Global.DaemonDict[DaemonFuse][0] = RemainingTime
            continue

    #-----------------
    # Return To Caller
    #-----------------

    # Notice we're returning, but we aren't returning a value to the caller. This
    # is reasonable, since this function just runs daemons, and really can't say
    # much about their statuses.

    return

def SayOriginal(Text=""):
    """
    Because the print statement isn't particularly intelligent when it comes
    to printing we'll have to create our own. This function makes sure that
    when a word is printed it doesn't "wrap" from the right edge of the
    screen to the left edge.

    In addition, if a single piece of text is printed that exceeds the
    number of screen lines available, a [--more--] capability allows all
    text to be read before it scrolls of the end of the screen.

    Note this function interprets no "\" characters (\n, \t, etc) but it
    does recognize three commands, ~n, ~p and ~m. These must be space
    separated from the words around them.

    ~n causes a \n line break. ~p is just ~n ~n (two line breaks, in other
    words a paragraph break). ~m forces a "[-- more --]" message and the
    screen to pause. ~n and ~p let you format text and ~m lets you pause the
    printing exactly where you want to.
    """
    
    #------------------
    # Ignore Empty Text
    #------------------

    # If Text is empty (nothing) then return without doing anything.

    if Text == "": return
    
    #--------------------------------
    # Translate {} Expressions and ~p
    #--------------------------------

    # Any text inside {} will be replaced with the value of the Python
    # expression. ~p is replaced with a pair of ~n's.
    
    Text = Engine.XlateCBEFunction(Text)
    Text = string.replace(Text,"~p","~n ~n")

    #-----------------
    # Create Word List
    #-----------------

    # This will break the text into a list of words which we can then use a FOR
    # loop on.

    WordList = string.split(Text)
    
    #---------------------------
    # For each word in Word List
    #---------------------------

    for Word in WordList:
        
        #----------------------
        # Terminal Mode Changes
        #----------------------

        # Various special characters to control the terminal. The series of IF
        # tests below changes the current style of the terminal. Note that we
        # have connected the Word="" statement on the same physical line, this
        # is just to make the code easier on the eyes.

        if Word[0] == "~":
            if Word == "~title": Terminal.A_TITLE();Word = ""
            if len(Word) == 2:
                if Word == "~b": Terminal.A_BOLD();Word = ""
                if Word == "~d": Terminal.A_DIM();Word = ""
                if Word == "~e": Terminal.A_MORE();Word = ""
                if Word == "~i": Terminal.A_ITALIC();Word = ""
                if Word == "~l": Terminal.A_NORMAL();Word = ""
                if Word == "~r": Terminal.A_REVERSE();Word = ""
                if Word == "~s": Terminal.A_STANDOUT();Word = ""
                if Word == "~u": Terminal.A_UNDERLINED();Word = ""
            if len(Word) == 3:
                if Word == "~bk": Terminal.A_BLACK();Word = ""
                if Word == "~bl": Terminal.A_BLUE();Word = ""
                if Word == "~gr": Terminal.A_GREEN();Word = ""
                if Word == "~cy": Terminal.A_CYAN();Word = ""
                if Word == "~rd": Terminal.A_RED();Word = ""
                if Word == "~mg": Terminal.A_MAGENTA();Word = ""
                if Word == "~br": Terminal.A_BROWN();Word = ""
                if Word == "~gy": Terminal.A_GRAY();Word = ""
            if len(Word) == 4:
                if Word == "~lbk": Terminal.A_LBLACK();Word = ""
                if Word == "~lbl": Terminal.A_LBLUE();Word = ""
                if Word == "~lgr": Terminal.A_LGREEN();Word = ""
                if Word == "~lcy": Terminal.A_LCYAN();Word = ""
                if Word == "~lrd": Terminal.A_LRED();Word = ""
                if Word == "~lmg": Terminal.A_LMAGENTA();Word = ""
                if Word == "~lbr": Terminal.A_YELLOW();Word = ""
                if Word == "~lgy": Terminal.A_WHITE();Word = ""
                if Word == "~bbk": Terminal.A_BBLACK();Word = ""
                if Word == "~bbl": Terminal.A_BBLUE();Word = ""
                if Word == "~bgr": Terminal.A_BGREEN();Word = ""
                if Word == "~bcy": Terminal.A_BCYAN();Word = ""
                if Word == "~brd": Terminal.A_BRED();Word = ""
                if Word == "~bmg": Terminal.A_BMAGENTA();Word = ""
                if Word == "~bbr": Terminal.A_BBROWN();Word = ""
                if Word == "~bgy": Terminal.A_BGRAY();Word = ""
            if len(Word) == 5:
                if Word == "~blbk": Terminal.A_BLBLACK();Word = ""
                if Word == "~blbl": Terminal.A_BLBLUE();Word = ""
                if Word == "~blgr": Terminal.A_BLGREEN();Word = ""
                if Word == "~blcy": Terminal.A_BLCYAN();Word = ""
                if Word == "~blrd": Terminal.A_BLRED();Word = ""
                if Word == "~blmg": Terminal.A_BLMAGENTA();Word = ""
                if Word == "~blbr": Terminal.A_BYELLOW();Word = ""
                if Word == "~blgy": Terminal.A_BWHITE();Word = ""
        
        
        #----------------------------------
        # Replace Format Control Characters
        #----------------------------------

        # Replace ~n and ~t with their print() statement equivalents.
        
        Word = string.replace(Word,"~n","\n")
        Word = string.replace(Word,"~t","  ")
        
        #-------------------------------
        # If it starts with a line break
        #-------------------------------

        # If the first two characters of Word are \n this means a newline
        # character will be printed, followed by the word.
        # Send a newline to the terminal, increment the number of lines printed
        # and clear the word.

        if Word == "\n":
            Terminal.NewLine()

            if Global.Transcribe:
                Global.LogFile.write("\n")
                if Global.Debug: Global.DebugFile.write("\n")

            Word = ""
        
        #-------------------------
        # Will Word Fit on line?
        #-------------------------

        # If the word fits on the current line output it to the terminal, if not
        # the send a newline, THEN output it. In that case also increment the
        # lines printed.

        if len(Word) > 0:
            Terminal.Output(Word)

            if Global.Transcribe:
                Global.LogFile.write(Word+" ")
                if Global.Debug: Global.DebugFile.write(Word+" ")

def Say(Text=""):
    """
    Because the print statement isn't particularly intelligent when it comes
    to printing we'll have to create our own. This function makes sure that
    when a word is printed it doesn't "wrap" from the right edge of the
    screen to the left edge.

    In addition, if a single piece of text is printed that exceeds the
    number of screen lines available, a [--more--] capability allows all
    text to be read before it scrolls of the end of the screen.

    Note this function interprets no "\" characters (\n, \t, etc) but it
    does recognize three commands, ~n, ~p and ~m. These must be space
    separated from the words around them.

    ~n causes a \n line break. ~p is just ~n ~n (two line breaks, in other
    words a paragraph break). ~m forces a "[-- more --]" message and the
    screen to pause. ~n and ~p let you format text and ~m lets you pause the
    printing exactly where you want to.
    """
    
    #------------------
    # Ignore Empty Text
    #------------------

    # If Text is empty (nothing) then return without doing anything.

    if Text == "": return
    
    #--------------------------------
    # Translate {} Expressions and ~p
    #--------------------------------

    # Any text inside {} will be replaced with the value of the Python
    # expression. ~p is replaced with a pair of ~n's.
    
    Text = Engine.XlateCBEFunction(Text)

    #-----------------
    # Create Word List
    #-----------------

    # This will break the text into a list of words which we can then use a FOR
    # loop on.
    
    # We want to get rid of any extraneous whitespace.
    Text = " ".join(Text.split())
    
    # We'll display chunks separated by style changes, so split the text up by
    # space ~. We need to account for the possibility that the ~ is at the
    # beginning of the line.
    if Text[0] == "~": Text = " " + Text
    WordsList = Text.split(" ~")

    #---------------------------
    # For each word in Word List
    #---------------------------
    
    for Index, Words in enumerate(WordsList):
        # If a style change is the very first portion of a piece of text, the
        # first chunk will be an empy string. We need to avoid this. (If the
        # first chunk doesn't begin with a style change, we can ignore it, so
        # we lose nothing by skipping it.)
        if Index > 0:
            
            # The style marker will be the first 'word'. Get the first space
            # to be able to extract it.
            FirstSpace = Words.find(" ")
            
            # The index will be -1 if there is no actual space. If there are
            # no spaces, the chunk itself is a style marker.
            if FirstSpace != -1:
                StyleMarker = Words[:FirstSpace]
            else:
                StyleMarker = Words
            
            Words = Words[FirstSpace + 1:] if FirstSpace != -1 else ""
            
            if StyleMarker == "title": Terminal.A_TITLE()
            elif StyleMarker == "b": Terminal.A_BOLD()
            elif StyleMarker == "d": Terminal.A_DIM()
            elif StyleMarker == "e": Terminal.A_MORE()
            elif StyleMarker == "i": Terminal.A_ITALIC()
            elif StyleMarker == "l": Terminal.A_NORMAL()
            elif StyleMarker == "r": Terminal.A_REVERSE()
            elif StyleMarker == "s": Terminal.A_STANDOUT()
            elif StyleMarker == "u": Terminal.A_UNDERLINED()
            elif StyleMarker == "bk": Terminal.A_BLACK()
            elif StyleMarker == "bl": Terminal.A_BLUE()
            elif StyleMarker == "gr": Terminal.A_GREEN()
            elif StyleMarker == "cy": Terminal.A_CYAN()
            elif StyleMarker == "rd": Terminal.A_RED()
            elif StyleMarker == "mg": Terminal.A_MAGENTA()
            elif StyleMarker == "br": Terminal.A_BROWN()
            elif StyleMarker == "gy": Terminal.A_GRAY()
            elif StyleMarker == "lbk": Terminal.A_LBLACK()
            elif StyleMarker == "lbl": Terminal.A_LBLUE()
            elif StyleMarker == "lgr": Terminal.A_LGREEN()
            elif StyleMarker == "lcy": Terminal.A_LCYAN()
            elif StyleMarker == "lrd": Terminal.A_LRED()
            elif StyleMarker == "lmg": Terminal.A_LMAGENTA()
            elif StyleMarker == "lbr": Terminal.A_YELLOW()
            elif StyleMarker == "lgy": Terminal.A_WHITE()
            elif StyleMarker == "bbk": Terminal.A_BBLACK()
            elif StyleMarker == "bbl": Terminal.A_BBLUE()
            elif StyleMarker == "bgr": Terminal.A_BGREEN()
            elif StyleMarker == "bcy": Terminal.A_BCYAN()
            elif StyleMarker == "brd": Terminal.A_BRED()
            elif StyleMarker == "bmg": Terminal.A_BMAGENTA()
            elif StyleMarker == "bbr": Terminal.A_BBROWN()
            elif StyleMarker == "bgy": Terminal.A_BGRAY()
            elif StyleMarker == "blbk": Terminal.A_BLBLACK()
            elif StyleMarker == "blbl": Terminal.A_BLBLUE()
            elif StyleMarker == "blgr": Terminal.A_BLGREEN()
            elif StyleMarker == "blcy": Terminal.A_BLCYAN()
            elif StyleMarker == "blrd": Terminal.A_BLRED()
            elif StyleMarker == "blmg": Terminal.A_BLMAGENTA()
            elif StyleMarker == "blbr": Terminal.A_BYELLOW()
            elif StyleMarker == "blgy": Terminal.A_BWHITE()
            elif StyleMarker == "n": Words = "\n" + Words
            elif StyleMarker == "p": Words = "\n\n" + Words
            elif StyleMarker == "t": Words = "  " + Words
            
            # If none of the above, it wasn't a style marker.
            else: Words = "~" + StyleMarker + " " + Words
                
        if len(Words) > 0:
            # We may have an extra space at the end. Oops. Get rid of that.
            if Words[-1] == " ": 
                Words = Words[:-1]
                
            Terminal.Output(Words)

            if Global.Transcribe:
                Global.LogFile.write(Words)
                if Global.Debug: Global.DebugFile.write(Words)


def SCase(Sentence):
    """
    This function acts like lower except it capitalizes the first letter of
    the passed argument.Note it ALSO strips leading whitespace before
    capitalizing the string!
    """

    #--------------
    # Not A String?
    #--------------
    
    # If the passed sentence isn't actually a string (it's None or a non-string),
    # exit immediately, returning Sentence unchanged.
    
    if Sentence == None: return Sentence
    if type(Sentence) <> type(""): return Sentence

    #-------------------------
    # Strip Leading Whitespace
    #-------------------------
    
    # Just in case there are leading spaces, we strip them away so the function
    # will work correctly.
    
    NewSentence = string.lstrip(Sentence)

    #--------------------------------
    # Return the Capitalized Sentence
    #--------------------------------
    
    # In English the string below reads "Return the first letter of NewSentence
    # capitalized, along with the rest of new sentence from the second character
    # onward. (Remember the first character of a string is 0, not 1.)
    
    return string.capitalize(NewSentence[0]) + NewSentence[1:]

def Self():
    """
    Because "self" is actually only a method argument defined by classes it
    can't be used in curly-brace expressions (which are evaluated by a
    function). Therefore we store the "current object" (self, in other
    words) in Global.CurrentObject. Because that's such a long string, we
    define this function to make it easier to use.

    Therefore instead of saying something like:

    {Global.CurrentObject.TheDesc()}

    we can use the shorter:

    {Self().TheDesc()}

    They mean exactly the same thing, but Self() is a lot easier to read AND
    type!

    The complement to this function is the MakeCurrent() method which is
    called as part of the parsing process.
    """
    return Global.CurrentObject

def SetRemove(list1,list2):
    """
    Returns a list containing list1 with items in list2 removed.
    """

    #----------------------
    # Make A Copy Of List 1
    #----------------------

    ReturnList = list1[:]

    #---------------------------
    # For Each Item In List 2...
    #---------------------------
    
    # Check each item in list 2. If it's in the return list, remove it.
    
    for Item in list2:
        if Item in ReturnList: ReturnList.remove(Item)

    #----------------------
    # Return List To Caller
    #----------------------
    
    # ReturnList has had all the items in List 2 removed from it. We're all done!
    
    return ReturnList

def StartDaemon(DaemonFuse,FuseLength = 0):
    """
    This function takes the function reference in DaemonFuse and adds it to
    Global.DaemonDict. It sets the Remaining Turns appropriately as well.
    
    Note FuseLength is optional, if not supplied it will default to 0, which
    means the "fuse" is actually a daemon (runs every turn).

    This function returns SUCCESS unless DaemonFuse isn't a funciton, in 
    which case it returns FAILURE.
    """

    #------------------------------------
    # Fail If DaemonFuse isn't a function
    #------------------------------------

    # Daemons *must* be functions, they can't be methods, strings, or anything
    # else. Oh, and though we can't check for it, daemons/fuses can't have 
    # arguments either.

    if type(DaemonFuse) <> type(StartDaemon): return FAILURE
    
    #-------------------------
    # Append/Update DaemonDict
    #-------------------------

    # If DaemonFuse is already in Global.DaemonDict then the remaining turns and
    # fuse length will be *updated*. This lets you change a daemon into a fuse or
    # vice versa, or reset a fuse's activation time.
    #
    # If DaemonFuse isn't in DaemonDict it will be added. Since both cases are
    # handled by a single simple line of code, you can appreciate just how
    # powerful dictionaries are!

    Global.DaemonDict[DaemonFuse] = [abs(FuseLength), FuseLength]
    
    #---------------
    # Return SUCCESS
    #---------------

    return SUCCESS

def StopDaemon(DaemonFuse):
    """
    This function takes the function reference in DaemonFuse and removes it
    from Global.DaemonDict. Obviously, this will stop the daemon/fuse from
    running.

    This function returns SUCCESS unless DaemonFuse isn't a function, in
    which case it returns FAILURE. It will also return FAILURE if DaemonFuse
    isn't currently in the dictionary.
    """

    #------------------------------------
    # Fail If DaemonFuse isn't a function
    #------------------------------------

    # Daemons *must* be functions, they can't be methods, strings, or anything
    # else.

    if type(DaemonFuse) <> type(StartDaemon): return FAILURE

    #---------------------------------------
    # Fail If DaemonFuse Isn't In DaemonDict
    #---------------------------------------

    # Return FAILURE if DaemonFuse isn't in the dictionary. This allows us a
    # silent but testable way to see if the daemon was removed, or wasn't
    # in the dictionary to start with.

    if not Global.DaemonDict.has_key(DaemonFuse): return FAILURE
    
    #-----------------------------------------
    # Remove DaemonFuse From Global.DaemonDict
    #-----------------------------------------

    del Global.DaemonDict[DaemonFuse]
    
    #---------------
    # Return SUCCESS
    #---------------

    return SUCCESS

def TupleToList(Tuple):
    """Converts the passed tuple to a list."""
    
    return Union([],Tuple)
    

#********************************************************************************
#                      Default Handler Functions For Engine
#
# The game author will probably hook new functions to the engine in place of
# these.

def default_AfterTurnHandler():
    """
    This routine is intended for actions (like daemons) that should occur
    after a given amount of time has elapsed, or after a successful player's
    turn, which is assumed to take a few minutes. Note this routine is only
    called when the Turn handler routine returns TURN_ENDS.
    """
    #--------------------
    # Refresh Status Line
    #--------------------

    # We pass the short description of the player's current location to the
    # BuildStatusLine() method of the game engine. This refreshes the status 
    # line on terminals that support it, putting the room name on the left side
    # and the score and turn count on the right.
    #
    # All current terminals except the Glass TTY support a status line. If using
    # a Glass TTY nothing happens when you call BuildStatusLine().
    
    Engine.BuildStatusLine(NZ(Global.Player.Location.SDesc()))

    #---------------------------
    # Run Daemons and Burn Fuses
    #---------------------------
    
    # This function runs all the daemons and burns fuses. By default the only
    # daemon running is GameDaemon, and all that does is increment the turn 
    # counter.
    
    RunDaemons()

def default_BuildStatusLine():
    """
    This method is just a place holder for the one written in the Universe
    library. You may also replace the library method with a more elaborate
    one if your game needs it.
    """
    pass

def default_GameSkeleton():
    """
    This is the heart of the game. It calls your game and stays active until
    the game ends.
    """
    
    #==========
    # Game Loop
    #==========

    # The basic logic in IF games is simple. Get a command from the player, 
    # figure it out, do it, then tell the player what happened. Repeat until
    # the player quits the game.

    while Global.GameState != FINISHED:

        #-----------------------
        # While Game is STARTING
        #-----------------------

        # The first time this loop executes GameState will be STARTING so we set
        # up the Game and set GameState to RUNNING.

        if Global.GameState == STARTING:
            Engine.SetUpGame()
            Global.GameState = RUNNING

        #----------------------
        # While Game is RUNNING
        #----------------------
        
        # While the game is running (which it will do until something sets the
        # GameState to FINISHED) we call the pre-turn handler then the parser.
        #
        # If the parser executes successfully we then execute the turn hanlder,
        # and if *that* succeeds then we execute the after turn handler.
        #
        # The implication is that if the parser returns FAILURE (which it might 
        # do if the command wasn't understood), the pre-turn handler will 
        # *still* execute. Another implication is you can deliberately cause the
        # turn-handler to return TURN_CONTINUES, and avoid running the after
        # turn handler. This gives you total control of when events outside the
        # player's control happen.

        if Global.GameState == RUNNING:
            Engine.PreTurnHandler()
            if P.AP().Parser() == SUCCESS:
                if Engine.TurnHandler() == TURN_ENDS:
                    Engine.AfterTurnHandler()
    
    #=============
    # Wrap Up Game
    #=============

    # Once the game is over (the loop ended because Global.GameState was set to
    # FINISHED) we call the PostGameWrapUp method to print a closing message, or
    # whatever's appropriate to your game.

    Engine.PostGameWrapUp()
    
    #===============
    # Shut down game
    #===============

    # Finally, we shut down the terminal (especially important on Unix/Linux 
    # systems) and quit the Python interpreter, which shuts down the game and
    # returns us to the operating system.

    Terminal.Terminate()

def default_PostGameWrapUp():
    """
    The post game wrap up lets the developer print a message after the game
    is over, if they want. The default version below does absolutely 
    nothing.
    """

    pass

def default_PreTurnHandler():
    """
    Although the default pre-turn handler does nothing, the developer can
    replace it with one that handles "quick" actions, actions which should
    happen just before the player is allowed to type their command WHETHER
    OR NOT THE LAST COMMAND WAS SUCCESSFUL, OR EVEN UNDERSTOOD!

    Pre-turn handlers aren't normally required.
    """

    pass

def default_SetUpGame():
    """
    This method sets up the starting parameters for the game. It places
    objects, initialzies daemons, and all the rest. Note if the developer
    wants they can create their own.
    
    This particular method is a placeholder, it will be replaced by the 
    one in Universe.
    """

    pass

def default_TurnHandler():
    """
    The default turn handler doesn't actually do much, it simply returns
    the TURN_ENDS or TURN_CONTINUES value returned by the current verb's
    Execute method.

    In other words, if the player typed "look at rose" then all the 
    turnhandler does is call LookAtVerb.Execute(), which returns either
    TURN_ENDS or TURN_CONTINUES, which 
    this method returns to the gaming loop.
    """

    return P.AP().CurrentVerb.Execute()

def default_UserSetUpGame():
    """
    This method is just a place holder for the user written User set up
    game method. It does absolutely nothing.
    """

    pass

#********************************************************************************
#                                PAWS Classes
#
# These are the core parts of PAWS (and thus Universe and any games written with
# them).

class ClassGlobal(ClassFundamental):
    """
    This class defines the Global variables object. The global variables
    object is used to hold all the variables that you want to get to from
    every part of the program (such as the Game State).
    """

    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Global Object"
        ClassFundamental.InheritProperties(self)
        
    
    def SetMyProperties(self):
        """Set Global Properties"""
        
        #--------------
        # Active Parser
        #--------------

        # This property holds the current parser object, the object used to
        # translate the player's input into terms the engine can understand. We
        # put this here so that the parser can attach itself and the
        # save/restore functions will save the parser object properties
        # (particularly vocabulary).

        self.ActiveParser = None
        
        #-----------------------------
        # Dictionary Of Active Daemons
        #-----------------------------
        
        # This "dictionary of lists" contains all the daemons and fuses which
        # are currently active (use StartDaemon() to add daemons/fuses to the
        # list and StopDaemon() to remove them.).
        #
        # Use RunDaemon() to actually execute daemons in the list.
        #
        # The dictionary key is the indirect reference to the function you want
        # to run. It MUST be a function reference, an object method won't work.
        # In addition, you can't pass any arguments to a daemon/fuse.
        #
        # Each entry in the dictionary is a list. The elements of the entry list
        # is:
        #
        # 0 - Remaining Turns. How many turns remain before the daemon activates.
        # For a daemon that runs every turn this value will be 0. For a fuse
        # (function that runs once) this value will be the number of turns
        # before the function is executed. Each turn this number is reduced by 1.
        #
        # 1 - Initial Fuse Length. When the daemon or fuse is added to
        #     Global.DaemonList by RunDaemon() the Remaining Turns value above is
        #     set to the ABSOLUTE VALUE of this number.
        #
        #     0  - If this number is 0 the function will be executed every turn.
        #          In other words, it's a daemon just like in TADS.
        #
        #     >0 - If this number is positive (5, say) then the remaining turns
        #          above will be set to 5 and the function will be run 5 turns
        #          later. It will run once and be removed from Global.DaemonList.
        #          In other words, this is like a fuse in TADS.
        #
        #     <0 - If this number is NEGATIVE (-5, say) then the remaining turns
        #          above will be set to 5 and the function will be run 5 turns
        #          later. However, once run instead of being removed the
        #          remaining turns count is RESET. Using a negative number is
        #          like running a daemon every X turns instead of every turn.

        self.DaemonDict = {}

        #---------------
        # Debug Property
        #---------------
        
        # The debug property is an easy way to embed (and leave) debugging trace
        # code in your program. In production it should be set to FALSE

        self.Debug = FALSE
       
        #-----------
        # Game State
        #-----------

        # This property holds the current state of the game, which starts off as
        # STARTING. This is how the game logic loop knows when the game is
        # starting or running or finished.

        self.GameState = STARTING
        
        #----------------
        # Player "Object"
        #----------------

        # The player object is the one the player controls, it's usually refered
        # to as "me". When a player types a command it's usually assumed the
        # player object is the one that will do the command.
        #
        # Global.Player is set in the object library (Universe), but can be
        # easily be overridden in your game library.

        self.Player = None
        
        #----------------------
        # Game is in Production
        #----------------------

        # This variable allows you to enable/disable the Debug verb. All you
        # need to do to disable the Debug verb is set Production to TRUE instead
        # of FALSE.
        #
        # The default TQ.py file comes with Production set to FALSE, so that the
        # Debug verb works.
        #
        # When your game is finished and completely tested, change the line in
        # your specially created UserSetUpGame() function replacement to TRUE.
        #
        # IMPORTANT NOTE: Do *NOT* change the value here! Do it in your game 
        # library's UserSetUpGame() function! For example, in Thief's Quest the
        # library is called TQLib.py and the function is called TQUserSetUpGame(). THAT's where you
        # should change it, NOT HERE.

        self.Production = TRUE
       
        #------------
        # Status Line
        #------------

        # The status line is maintained even if the terminal can't support it.
        
        self.StatusLine = " "

        #--------------
        # Logging Flags
        #--------------
        
        # The Transcribe property turns the transcription log on and off. The log
        # records every bit of text produced by Say() and player input to one log,
        # (<gamename>.log) and debugging output to a second file (<gamename>.dbg).
                
        self.Transcribe = FALSE
        self.LogFile = 0
        self.DebugFile = 0
        
class ClassParser(ClassFundamental):
    """Defines all parser functionality"""

    def __init__(self):
        """
        Create Instance Variables

        ClassFundamental.InheritProperties() will automatically call
        SetMyProperties() for every ancestor class of self that defined it,
        in the proper sequence.
        """

        self.NamePhrase = "Parser Object"
        ClassFundamental.InheritProperties(self)
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        
        #--------------------------
        # Active Command Words List
        #--------------------------

        # The active command words list contains a list of words for the
        # command currently being processed.

        self.ActiveCommandList = []
        
        #----------------------
        # Adjectives Dictionary
        #----------------------

        # The AdjsDict dictionary holds all objects associated with a given
        # adjective, just like the NounsDict dictionary, for example:
        #
        # 'small': [SmallRock, Kitten, Phial, House]
        # 'glass': [CrystalBall, Window]
        # 'large': [Troll, Cliff, Diamond]

        self.AdjsDict = {}
        
        #-----------------------
        # The Adverbs Dictionary 
        #-----------------------
        
        # 'Carefully': [CarefullyAdverb]

        self.AdverbsDict = {}
        
        #--------------
        # Articles List
        #--------------
        
        # Articles aren't used, they're discarded at the present time. It is
        # possible future enhancements of the parser will make use of these.

        self.ArticlesList = ["a","an","the"]
        
        #--------------------
        # Command Breaks List
        #--------------------
        
        # Items in this list seperate multiple commands entered on a single line.

        self.CommandBreaksList = ["then", ".", "?", "!"]
        
        #--------------
        # Commands List
        #--------------

        # This list holds the list of seperate commands that the player typed
        # on the same line, for instance "Go west then open door" is two
        # commands, not just one. The Commands List for this would look like
        # this:
        #
        #   [['go','west'],['open','door']]
        #
        # In other words CommandsList[0] is ['Go','west'].

        self.CommandsList = []
        
        #------------------
        # Conjunctions List
        #------------------
        
        # Conjunctions are currently ignored, but future enhancements to the
        # parser may make of them.

        self.ConjunctionsList = ["and",","]
        
        #----------------
        # Decoded Objects
        #----------------

        # Once the parser figures out which objects the player's command
        # indicated it puts them in these variables.
        #
        # CurrentActor and CurrentVerb are both single objects.
        #
        # CurrentPrepList is a list of strings, the preposition(s) used with the
        # verb. For instance, 'get book from under the bed' would have 2
        # prepositions, 'from' and 'under.' You generally won't need these but
        # if you ever do you'll have them.
        #
        # CurrentDObjList is a list of the direct object(s) the player meant,
        # and CurrentIObjList is a list of indirect object(s) the player
        # meant.
        #
        # SaidText is literally the text the player typed in for the
        # ActiveCommandList. As in "Say "Hello". SaidText would be "Hello" 
        # inside quotes.

        self.CurrentActor = None        # Object
        self.CurrentVerb = None         # Object
        self.PreviousVerb = None        # Object
        self.Again = None               # Object (again verb)
        self.CurrentObject = None       # Object (within CurrentDObjList)

        self.CurrentDObjList = []       # Objects
        self.CurrentIObjList = []       # Objects
        self.CurrentAdverbList = []     # Adverb objects

        self.CurrentVerbNoun = None     # Word
        self.CurrentPrepList = []       # WORDS
        self.SaidText = ""              # string
        
        #------------------
        # Disjunctions List
        #------------------
        
        # Disjunctions are currently ignored, but may be used in future enhancements to the
        # parser.

        self.DisjunctionsList = ["but","except"]
        
        #-----------------------
        # Noun/Verb Dictionaries
        #-----------------------

        # The actual heart of the parsing algorhythmn is based on these two
        # dictionaries, so understanding them is vital to understanding the
        # parser.
        #
        # Every discete 'thing' in the game (like a sword or a rock) has 1 (or
        # more!) names associated with it. For example, let's say we created an
        # object we named SmallRock in the program. The player can refer to
        # SmallRock either with 'rock' or 'stone' or 'pebble'.
        #
        # Ok, fine. NounsDict will have 3 entries, 'rock', 'stone', and 'pebble'.
        # These are called the KEYS. But what value does each key hold?
        #
        # You guessed it.
        #
        # 'rock': [SmallRock]
        # 'stone': [SmallRock]
        # 'pebble': [SmallRock]

        # Now, let's say we created a second object called Boulder, that the
        # player can refer to as 'boulder', or 'rock', or 'stone'. Now our
        # dictionary looks like:
        #
        # 'rock': [SmallRock, Boulder]
        # 'stone': [SmallRock, Boulder]
        # 'pebble': [SmallRock]
        # 'boulder': [Boulder]
        #
        # Ok, now we know that 'rock; can be either SmallRock or Boulder. How
        # do we tell which one the player meant?
        #
        # If there's any doubt (for example both SmallRock and Boulder are
        # in the same room as the player) the parser will compare the
        # adjectives used. No two objects with the same name should ever
        # have exactly the same list of adjectives, otherwise the parser
        # will go off and sulk.

        self.NounsDict = {}
        
        #--------------
        # Parser Errors
        #--------------

        self.NoVerb = "There's no verb in that sentence."
        self.NoPreposition = "'%s' needs a preposition."
        self.NoPreviousCommand = "You haven't done anything yet!"
        self.NoSuchVerbPreposition = "I don't recognize that verb/preposition(s) combination"
        self.MultipleVerbPrepositions = "PROGRAMMING ERROR: Two or more verbs share this verb and preposition combination."
        self.MultipleActors = "You can only tell one thing at a time to do something."
        self.DObjsNotAllowed = "'%s' can't have any direct objects."
        self.IObjsNotAllowed = "'%s' can't have any indirect objects."
        self.NotInVocabulary = "I don't know the word '%s'."
       
        #---------------------------
        # Parts Of Speech Dictionary
        #---------------------------
        
        # Like the noun, verb, adjective and preposition dictionaries this
        # dictionary contains lists. Also like those dictionaries POSDict is
        # keyed on the vocabulary word.
        #
        # This dictionary identifies which of the 8 parts of speech the word
        # belongs to:
        #
        #   Noun (sword, ring, rock)
        #   Verb (take, run, hide)
        #   Adjective (blue, big, small, heavy)
        #   Limiting adjective (a, an, the, some, first)
        #   aDverb (quickly, slowly, carefully)
        #   pRonoun (him, her, them)
        #   Preposition (in, behind, of, about)
        #   Conjuctions (and, but, or, nor, after, if)
        #
        # The capitalized letter is what's put in the dictionary. For example,
        # here are two entries:
        #
        #   "take": ["V"]
        #   "gold": ["A", "N"]
        #
        # These entries tell us that "take" is a verb, and that "gold" is both
        # an adjective and a noun.
        #
        # A "Limiting" adjective is one used to identify a sub-group or one
        # particular item from a group of similar items "That rock", "a rock",
        # "some rocks", "the fifth rock", etc. We distinguish them from regular
        # adjectives to make the parser's job easier.

        self.POSDict = {}
        
        #------------------------
        # Prepositions Dictionary
        #------------------------
        
        # The PrepsDict dictionary works like the AdjsDict dictionary but holds
        # lists of VERBS, not THINGS. For example:
        #
        # 'with': [DigWithVerb, AttackWithVerb]
        # 'from': [TakeFromVerb]
        # 'under': [LookUnderVerb, DigUnderVerb, SearchUnderVerb]
                
        self.PrepsDict = {}

        #-------------------------
        # Pronouns Dictionary/List
        #-------------------------

        # Pronouns work a little differently. There are 4 kinds, gender neutral
        # singular, gender neutral plural, male and female singular.
        #
        # The parser uses the PronounsList to search for words in the command
        # which it replaces with the objects from the program dictionary.
        #
        # For instance, let's say the player said "Get Book". The parser
        # (once it knows the player means BlueBook) assigns BlueBook to the
        # PronounsDict entry 'it' (since the book is gender neutral and
        # singular). If the player later says 'Read it', the parser knows
        # "it" refers to BlueBook.

        self.PronounsListDict = {"it": IT,
                                 "them": THEM,
                                 "all": THEM,
                                 "everything":THEM,
                                 "him":HIM,
                                 "her":HER}

        self.PronounsDict = {IT: None,
                             THEM: [],
                             HIM: None,
                             HER: None}


        

        #-----------------
        # Verbs Dictionary
        #-----------------
        
        # The VerbsDict works the same way, except we distinguish verbs by the
        # prepositions used with them. For example, 'Look', 'look into mirror',
        # and 'look under bed' are actually three distinct verbs,just as Boulder
        # and SmallRock were two distinct objects. So our VerbDicts dictionary
        # would contain:
        #
        # 'Look': [LookVerb, LookIntoVerb, LookUnderVerb]

        self.VerbsDict = {}
    
        #----------
        # SAY Verb
        #---------
        
        # This is used for the Say verb, because the Say verb is special, it's
        # used in debugging, so the parser needs to know which verb will be used
        # for Say.
        
        self.SayVerb = None
        

    def GetPlayerInput(self):
        """
        Get Player's command.
        
        This routine takes the player's typed line and turns it into a list
        of commands which are placed in Global.CommandsList.
        """
        
        #-------------------
        # Get Player Command
        #-------------------

        # InputString holds the string the player typed. Notice the use of
        # the Prompt function inside the Input function.

        InputString = Terminal.Input(self.Prompt())
        
        #----------------------
        # Preserve Exact String
        #----------------------
        
        # We need to preserve the exact string that the player typed so we can
        # use it in special case situations--like debugging, quoted strings, 
        # and so on. Far too much detail is lost during the parsing process
        # so we have to do this.

        self.SaidText = InputString

        #----------------------------
        # Is Player using "Say" Verb?
        #----------------------------
        
        # Because the Say verb is used in debugging it can't go through the 
        # normal parsing process. Instead we use the mini-parse below, which
        # first makes sure the Say verb exists at all...
        
        if not self.SayVerb is None:

            #-----------------------------
            # Get First Word Player Typed
            #----------------------------
            
            # Whenever the player uses the "say" verb, it's always the first
            # word on the line. It's also the name phrase of the Say verb, so
            # we make sure it's in lower case.
            
            FirstWord = string.lower(self.SayVerb.NamePhrase)

            #---------------------
            # Is First Word "Say"?
            #---------------------
            
            # The weird test below is looking at SaidText, from the beginning to
            # the length - 1'th character. So if First Word is "say" it's length
            # is 3. We compare First Word against Said Text, from the beginning
            # to the 3'rd letter.

            if string.lower(self.SaidText[:len(FirstWord)]) == FirstWord:

                #-------------------------
                # Return Say Verb's Action
                #-------------------------
                
                # This returns the results of the action method of the Say verb
                # (which is always TURN_CONTINUES), which is what the parser
                # does when it successfully interprets a command. Because we've
                # never filled the Commands List the parser will turn around
                # and immediately call this routine again--which is EXACTLY what
                # we want to happen...
                
                return self.SayVerb.Action()
                
        #------------------
        # Fence Punctuation
        #------------------
        
        # Because punctuation is basically a "word" to the parser we need to
        # fence each punctuation character with spaces. So instead of:
        #
        # Get the sword, then kill the troll.
        #
        # we have:
        # 
        # Get the sword , then kill the troll .
        #
        # We're doing this to make splitting the typed string into a list of 
        # words MUCH easier.
        #
        # Basically we're building the output string by adding each character
        # to the string one at a time. But if the character is punctuation
        # however, we add *3* characters, a space, the puncutation and another
        # space.
        
        OutputString = ""
        
        for Character in InputString:
        
            if Character in string.punctuation: 
                Character = Fence(Character," ", " ")
        
            OutputString = OutputString + Character
        
        #--------------------------------------                
        # Split Typed String Into List Of Words
        #--------------------------------------

        # string.split takes a string and creates a list by dividing the string
        # by a given character. By default that character is a space.
        
        TempWordList = string.split(OutputString)
        
        #---------------------------------------
        # Break Word list into separate commands
        #---------------------------------------

        # Since the player can type muliple commands on a single line
        # (such as "go west then open door" or just "go west. open door")
        # we have to make sure we get all commands.

        #--------------------------------
        # For each word in Temp Word List
        #--------------------------------

        # The FOR loop says in English: "for each word in a COPY of
        # TempWordList do the following...
        #
        # We use a copy because in the course of the FOR loop we're going
        # to completely destroy the real TempWordList.

        for word in TempWordList[:]:
            
            #----------------------
            # Is Word a terminator?
            #----------------------

            # Is the current word in the Global.CommandBreaksList? This
            # list includes all valid ways to end a command. By default
            # this includes all the valid ending sentence punctuation and
            # the word "then" (as in "Go west then open door"). Ending
            # sentence punctuation is assumed to a period, exclamation
            # point, or question mark.

            if word in self.CommandBreaksList:
                
                #-----------------------------
                # Find word's current position
                #-----------------------------

                # We're constantly deleting words from TempWordList, so we
                # need to find the current position of word within the word
                # list. Position will contain the position of word.

                Position = TempWordList.index(word)
                
                #-------------------------------
                # Append Command To CommandsList
                #-------------------------------

                # The command to append to the commands list starts at the
                # beginning of TempWordList and runs up to position Item.
                # The line below will NOT include the actual terminating
                # word in the appended command. So "go west. Open door" will
                # append the command ["go","west"] to the command list, but
                # not include the period.

                self.CommandsList.append(TempWordList[:Position])
                
                #------------------------------
                # Delete command from word list
                #------------------------------

                # Since we no longer need the command we discard everything
                # from the beginning of TempWordList through (and including)
                # the terminating word.
                #
                # In English the code below reads: "Set TempWordList to
                # the remainder of TempWordList from the word after the
                # terminating word till the end of the temp word list.
                #
                # For instance: ["go","west",".","open","door"] becomes
                # ["open","door"].

                TempWordList = TempWordList[Position+1:]

        else:
            
            #-----------------------------------------
            # Remaining TempWordList has no terminator
            #-----------------------------------------

            # This code is part of the FOR/ELSE loop. If we actually
            # have reached this point it means the FOR loop has reached
            # the end of the COPY of TempWordList, but there may still be
            # an extra command in process. Let's examine our example "go
            # west. open door"
            #
            # The copy of TempWordList being processed by the FOR loop
            # ended without a terminator. Therefore the REAL TempWordList
            # still contains ["Open" "Door"]
            #
            # To handle this situation we just append the entire remaining
            # TempWordList (in this case ["open","door"] to the commands
            # list.

            self.CommandsList.append(TempWordList)
        
        #--------------------------------
        # Make Sure last command is valid
        #--------------------------------
        
        # Consider what self.CommandList will look like if the player
        # types "go west." (ie ends with a period). This yields ["go",
        # "west"],[]] In other words, a bogus last command is introduced
        # into the list.
        #
        # self.CommandList[-1] means "the last command in the list". If
        # the last command is [] (ie, nothing) then we want to get rid of
        # it. We do that by setting the command list to the command list
        # [:-1].
        #
        # In English, [:-1] means "from the beginning to the end -1. If
        # the list contained 5 commands, then :-1 would give us the first 4
        # commands.
            
        if not self.CommandsList[-1]:
            self.CommandsList = self.CommandsList[:-1]
        
        #-------------------------
        # Tell caller we succeeded
        #-------------------------

        # We don't really need to indicate success or failure, since the
        # existing code doesn't check, but it's good programming practice
        # because a game author might rewrite the parser and need to know
        # if this routine succeeded or failed.

        return SUCCESS
  
    def Parser(self):
        """
        Parsing routine. Almost never overridden.
        
        This is the big cheese as far as most developers are concerned. It
        handles translating the command the player typed into recognizable
        objects so the parser can then hand off execution to the objects in
        question.

        It's reasonably intelligent, it handles multiple commands on a 
        single line, has the ability to handle multiple direct and indirect
        objects, can handle preparsing and a fair degree of disambiguation,
        ala TADS.

        The parser can return SUCCESS or FAILURE. If it returns FAILURE it
        means the command wasn't understood, SUCCESS means the command was
        understood and parsed into objects that TurnHandler() can deal with.
        """
        
        #--------------
        # Get a command
        #--------------
    
        # The first thing we have to do is get a command to parse. That isn't as
        # easy as it sounds, for two reasons. First, the player can type
        # multiple commands on a single line, such as"East, then open door" This
        # is two commands "East" and "Open door".
        #
        # Second, if the player does type multiple commands on a single line
        # then the *game loop* has no way to tell if the player typed the
        # commands on one line or several, so the parser has to deal with it.
        #
        # Once the player types a string it is broken down into one or more
        # commands which are put in self.CommandsList. If the command list
        # is empty that means we need to go back to the player for more 
        # commands.
        #
        # In English: "While the command list is empty, get player input."

        if not self.CommandsList: return TURN_CONTINUES
       
        #--------------------------
        # Get Active (next) command
        #--------------------------

        # The parser places the words from the first command in the list the
        # player typed (self.CommandsList[0]) into the list the parser actually
        # uses to do the parsing (self.ActiveCommandList).

        self.ActiveCommandList = self.CommandsList[0]
        
        #-----------------------------
        # Delete it from commands list
        #-----------------------------

        # Now that we've saved the command we're interested in, we delete it
        # from the CommandsList. Doing this does two things. First, it lets us
        # write simpler code (ALWAYS desirable) and it also allows the parser to
        # know when the CommandsList is empty so the parser can ask the player
        # to type in more.

        del self.CommandsList[0]
        
        #----------------------------
        # Delete Trailing Conjuctions
        #----------------------------

        # Because of the nature of English, it's very possible for the player to
        # type in "go west and then open door". This makes our active command
        # list ['go','west','and'], which doesn't make much sense. So we need to
        # make sure the last word isn't a conjunction.
        #
        # To gracefully handle parser abuse (like "go west and and then open
        # door" we use a while loop which will whittle off as many trailing
        # conjunctions as might prove necessary.
        #
        # Translated, the while loop says "While the last word is a conjunction,
        # set the ActiveCommandList to the ActiveCommandList
        # up to but not including the last word."

        while self.ActiveCommandList[-1] in self.ConjunctionsList:
            self.ActiveCommandList = self.ActiveCommandList[:-1]
        
        #-----------------------------
        # Pre-parse the active command
        #-----------------------------

        # Now that we have winnowed a single command from the command list
        # we're ready to apply any pre-parsing rules to the command.

        if not self.PreParse(): return FAILURE
        
        #-------------------
        # Debug Parser Trace
        #-------------------

        # If debug is active then for each word in the active command list print it's
        # part of speech. If it's unrecognized, print "Not In Vocabulary".

        if Global.Debug:
            for Word in self.ActiveCommandList:
                if P.AP().POSDict.has_key(Word):
                    DebugTrace(Word + ": " + repr(P.AP().POSDict[Word]))
                else:
                    DebugTrace(Word+": Not In Vocabulary")

        
        #===================
        # Break Down Command
        #===================

        # English is a difficult language to parse. Fortunately, all we have
        # to parse are commands, which, while difficult, always follow a
        # consistant format.
        #
        # The format is:
        #
        # [Actor] VERB [direct object(s)] [preposition] [indirect object(s)]
        #
        # (We're going to ignore the inconvenient form "VERB [direct objects]
        # [Actor]" since it's too difficult to handle cleanly and most
        # people use the first form anyway...)
        #
        # All items in square brackets are optional, which means the only
        # item required in the command is a verb!
        #
        # This suggests the strategy the parser uses to break down the
        # command. First it scans the command for a verb. If it doesn't find
        # a verb, there's nothing more to be done, we complain and return
        # a FAILURE.
        #
        # Assuming we find a verb we save its location. The next thing we do
        # is try and find one or more prepositions, saving the location of
        # the first one we find.
        #
        # The locations of the verb and first preposition are landmarks in
        # the command.
        #
        # Consider the command: "John, dig the hole with the shovel." Since
        # "John" preceeds the verb, we know that John must be the actor,
        # you can't put anything else in front of a verb.
        #
        # Likewise we know "with" is a preposition. Therefore "the hole" is
        # a direct object.
        #
        # And "the shovel" is the indirect object. Translate those
        # (see below) and the parser's job is finished.
        #
        # There's one special case we need to look at. That's a command
        # where the preposition immediately follows the verb, which makes
        # the command's indirect object into the direct object.
        #
        # For example: "Look into chest"
        #
        # Left to itself, chest would become the command's indirect object.
        # However, all we have to do when the first preposition immediately
        # follows the verb is copy the indirect object list into the
        # direct object list and then zap the indirect object list. 
        
        #----------
        # Find Verb
        #----------
        
        # A command can only have one verb in it, so break out of the FOR
        # loop when we find it. If we don't find it complain and return
        # FAILURE.
        #
        # Now to translate the following code into English. First line:
        # "Set PotentialVerbList to an empty list (there aren't any).
        #
        # "For each word in Global.ActiveCommandList, do the following"
        #
        # "If the current word is a verb, then set VerbLocation to the
        # current word's position and then append the VERB'S OBJECT (NOT
        # the word!) to the PotentialVerbList. (We now have one verb
        # object). Since a command may only have one verb we break the
        # FOR loop immediately, stopping our scan.
        #
        # If none of the words in the ActiveCommandList are verbs then
        # we print a complaint ("That sentence doesn't contain a verb!")
        # and immediately return a FAILURE code. This causes the game loop
        # to call the parser again, so the next command can be processed.
        

        PotentialVerbList = []

        for word in self.ActiveCommandList:
            if self.VerbsDict.has_key(word):
                self.CurrentVerbNoun = word
                VerbLocation = self.ActiveCommandList.index(word)
                PotentialVerbList = Union(PotentialVerbList,self.VerbsDict[word])
                break
        else:
            #return Complain(self.NoVerb)
            if self.PreviousVerb is None: return Complain(self.NoVerb)
            self.CurrentVerbNoun = self.PreviousVerb.NamePhrase
            VerbLocation = 0
            PotentialVerbList.append(self.PreviousVerb)
            self.ActiveCommandList = [self.CurrentVerbNoun] + self.ActiveCommandList

        DebugPassedObjList("Potential Verbs",PotentialVerbList)
        
        
        #-----------------
        # Find Preposition
        #-----------------

        # If we get this far we found a verb, now we have to find its
        # prepositions (if any). We start at the verb's location and
        # move to the end of the active command list. If we don't find
        #
        # one the preposition location remains the verb's location.
        #
        # This code is similar to the verb code above, except as noted
        # below.
        #
        # In English: "Set PrepositionList to an empty list (there aren't
        # any). Set FirstPrepositionLocation to VerbLocation".
        #
        # "For each word in Global.ActiveCommandList (starting at the
        # Verb's location and continuing to the end of the list), do the
        # following:"
        #
        # "If the current word is a preposition, append it to
        # Global.CurrentPrepList, append all objects with this preposition
        # to the PrepositionList, then (if this is the first preposition),
        # reset the FirstPrepLocation to the current word's position."
        #
        # Unlike a verb, there can be multiple prepositions in the command,
        # so the FOR loop continues even after we find the first preposition.
        

        self.CurrentPrepList = []
        PrepositionList = []
        FirstPrepLocation = VerbLocation

        if len(self.ActiveCommandList) > 1:
            for word in self.ActiveCommandList[VerbLocation + 1:]:
                if self.PrepsDict.has_key(word):
                    self.CurrentPrepList.append(word)
                    PrepositionList = Union(PrepositionList,self.PrepsDict[word])
                    if FirstPrepLocation == VerbLocation:
                        FirstPrepLocation = self.ActiveCommandList.index(word)
        
        
        #--------------------------------------------
        # Player didn't use a preposition in command?
        #--------------------------------------------
        
        # If the player did NOT use a preposition in the command (like
        # "Take" or "look", then we have a problem. This is because if
        # you intersect any list with an empty list you get an empty
        # list.
        #
        # To solve the problem PAWS requires ALL verbs to have at least one
        # preposition. Verbs that don't normally have a preposition are
        # given the preposition "nopreposition".
        #
        # Let's use "look" as an example. Let's say we have 3 verbs named
        # look, "look", "look into", and "look under". Therefore our
        # potential verb list would be [LookVerb,LookIntoVerb,LookUnderVerb].
        #
        # Let's further assume the player typed "look". The preposition list
        # is empty ([]), but we can't intersect with an empty list, or we'll
        # just get an empty list.
        #
        # So if PrepositionList is empty, we append all the verbs in
        # the preposition dictionary with the name "nopreposition". This
        # makes the preposition list (for instance) [LookVerb, TakeVerb,
        # QuitVerb]. Intersection with our verb list yields exactly one
        # verb! (unless we screwed up and gave two different verbs the
        # same name and preposition(s)!)
       

        if len(PrepositionList) == 0:
            PrepositionList = Union(PrepositionList,self.PrepsDict["nopreposition"])

        DebugPassedObjList("Prepositions",PrepositionList)
       
        
        #============================
        # Positively Identify the Verb
        #=============================

        # It's time to narrow the verb to exactly one candidate. Be aware
        # it's a rule of PAWS that each verb must have a unique name and
        # set of prepositions. For example, you can only have one QuitVerb,
        # since Quit has no prepositions. You can have a look, look into,
        # and look under verb since each "look" verb has a different
        # preposition.
        #
        # There are 3 possible outcomes:
        #
        # 1) We eliminate everything. This means the player either used a
        #verb that doesn't have prepositions with prepositions
        #("quit from here") or used a verb that needed prepositions
        #without any (such as "dig"). We complain and fail.
        #
        # 2) We still have more than one possible verb. This generally
        #means a programming error (two verbs with the same verb
        #name and the same set of prepositions). We complain with a
        #bug report. Make one of the verbs use a different preposition
        #or give it a new name.
        #
        # 3) We only have one verb left. This is only way we continue.
 
        PotentialVerbList = Intersect(PotentialVerbList,PrepositionList)

        DebugPassedObjList("Winnowed Verb List",PotentialVerbList)
        
        #-------------------------------
        # No Verbs, no prepositions used
        #-------------------------------

        # Remember our VerbPosition and FirstPrepPosition variables?
        # If the player used no prepositions the two values will be
        # equal. If PotentialVerbList is empty and the two values are
        # equal, the player typed a verb that needed one but didn't
        # give us one (like typing "dig" and not saying "with".)

        if len(PotentialVerbList) == 0 and VerbLocation == FirstPrepLocation:
            return Complain(SCase(self.NoPreposition % P.CVN()))

        
        #----------------------------
        # No verbs, prepositions used
        #----------------------------

        # On the other hand, say the player used a preposition with a verb
        # that doesn't have one (like "Quit to DOS". In that case we don't
        # have any intersecting verbs, but since we did have a preposition
        # FirstPrepPosition will be at least one greater than the
        # VerbPosition. (In our example "Quit To DOS" VerbPosition is 0, and
        # FirstPrepPosition is 1.)

        if len(PotentialVerbList) == 0 and VerbLocation < FirstPrepLocation:
            return Complain(self.NoSuchVerbPreposition)

        
        #-------------------------
        # More than one verb left?
        #-------------------------

        # This only happens when the game developer (you) gives two different
        # verbs the same name and preposition. For instance you might have
        # LookInVerb and LookIntoVerb and mistakenly given them both "in"
        # when you really wanted one to have "in" and one to have "into".

        if len(PotentialVerbList) > 1:
            return Complain(self.MultipleVerbPrepositions)

        
        #====================
        # VERB IDENTIFIED!!!!
        #====================

        # By reaching this point we have successfully identified one and
        # only one verb. We also know where the verb is, and where the
        # first preposition is. Given this information we can now set
        # the self.CurrentVerb variable to the first element in
        # PotentialVerbList.

        self.CurrentVerb = PotentialVerbList[0]
        DebugTrace("Current Verb-->"+PotentialVerbList[0].SDesc())
        
        
        #---------------------------
        # Check to see if Again verb
        #---------------------------

        # If the player typed a verb meaning AGAIN, then (assuming they typed
        # a previous command) set the current verb to the previous verb. At this
        # point the direct and indirect object lists haven't been disturbed, so
        # the previous command should execute normally.

        if self.CurrentVerb == self.Again and self.Again <> None:
            DebugTrace("Verb is 'Again' ("+self.Again.SDesc()+")")
            if self.PreviousVerb == None: return Complain(self.NoPreviousCommand)
            self.CurrentVerb = self.PreviousVerb
            return SUCCESS

        
        #---------------------
        # Set Previous Command
        #---------------------

        # This will allow the above command to work when the *NEXT* command is
        # "again".

        self.PreviousVerb = self.CurrentVerb

        
        #===============
        # Identify Actor
        #===============

        
        # The current actor will always be the player's character unless
        # the player puts something in front of the verb. So we play a
        # small programming trick.
        #
        # We deliberately set the current actor to the player. Then we test
        # to see if the verb's position in the command was greater than 0.
        #
        # If not then the player didn't give us an actor. We don't have to
        # do anything else, because the current actor is already the
        # player's object! This is called "defaulting", it's a very useful
        # trick to keep code short and simple.
        #
        # If the verb's position is greater than 0 that means the player
        # typed the name of an actor in front of the verb.
        #
        # We have a special function called ParserIdentifyNoun() that will
        # identify objects in a command. You pass it the starting and
        # ending position within Global.ActiveCommandList and it returns
        # a list of corresponding objects.
        #
        # So we pass it 0 (the start of the command) and VerbPosition.
        #
        # In the command "John, Take the book" this means John is the
        # only word scanned. Thus the function returns [JohnActor] as
        # a single item list of lists.
        #
        # Unfortunately, everything that uses CurrentActor expects it to
        # be a single item, not a list. So we employ a trick called
        # "type conversion" to convert it from a list to a single item.
        # To do that we simply assign the first element of the first list
        # to CurrentActor, this converts it from a list to a single item.
        #
        # The IF test below tests the type of P.CA() against
        # the type of an empty list. If the currentActor is a list, the
        # parser gives up (rather than trying to weed out which object
        # is the actor), complains, and returns FALSE.

        self.CurrentActor = Global.Player

        if VerbLocation > 0:
            self.CurrentActor = self.ParserIdentifyNoun(0,VerbLocation)
            self.CurrentActor = self.CurrentActor[0]
            self.CurrentActor = self.CurrentActor[0]

            if type(self.CurrentActor) == type([]):
                self.CurrentActor = Global.Player
                return Complain(self.MultipleActors)
        
        #---------------------------
        # Clear Current Adverbs List
        #---------------------------

        # The current adverb list consists of objects that the parser identifies
        # as adverbs. By their nature adverbs will never be anything else, the 
        # word can't also be any other part of speech. 
        
        self.CurrentAdverbList = []
        
        #-------------------
        # Get Direct objects
        #-------------------

        # Direct objects are the objects the verb acts on. For example,
        # in the command "Take book", "book" is the direct object. The
        # parser uses a simple rule to identify direct objects, they're
        # everything that lie between the verb and the first preposition.
        #
        # There's a special case we need to handle, but that's actually a
        # special case of indirect objects (stay tuned). Notice we use our
        # defaulting trick again.

        self.CurrentDObjList = []

        if len(self.ActiveCommandList) > 1:
            self.CurrentDObjList = self.ParserIdentifyNoun(VerbLocation,FirstPrepLocation)
   
        
        #-----------------
        # Indirect Objects
        #-----------------

        # Indirect objects are those that follow a preposition. In the
        # command "dig hole with shovel", shovel is the indirect object.

        self.CurrentIObjList = []

        if len(self.ActiveCommandList) > FirstPrepLocation + 1:
            self.CurrentIObjList = self.ParserIdentifyNoun(FirstPrepLocation + 1,len(self.ActiveCommandList) + 1)
        
        #---------------------------
        # DIRECT OBJECT SPECIAL CASE
        #---------------------------

        # There is one special case for direct objects. This occurs when
        # the preposition immediately follows the verb. For instance,
        # in the command "Look into chest", "chest" is actually a direct
        # object, although the parser considers it an indirect object.
        #
        # The solution is simple. When the preposition immediately follows
        # a verb, copy the indirect object list to the direct object list,
        # then clear the indirect list.

        if (FirstPrepLocation - VerbLocation) <= 1:
            self.CurrentDObjList = self.CurrentIObjList[:]
            self.CurrentIObjList = []
        
        #------------------
        # That's All, Folks
        #------------------

        # The parser is finished. Notice it doesn't handle disambiguation of
        # objects, that's left to the verbs. You'll notice the BasicVerb
        # object is quite sophisticated, it handles default disambiguation
        # for most cases, you can override specific verbs on a case by case
        # basis.

        DebugTrace("Parsed Verb Is "+self.CurrentVerb.SDesc())
        return SUCCESS
    
    def ParserIdentifyNoun(self,StartPos,EndPos):
        """
        Returns a list of objects identified by nouns in
        Global.ActiveCommandList.
   
        This function returns a list of objects identified by the word range
        in Global.ActiveCommandList. Objects are identified by zero or more
        adjectives preceeding a noun. Other parts of speech are ignored by
        this search.

        It is very possible for this routine to return a list within a list.

        For example, let's say the phrase was "stone". This is a noun, and
        could apply to any of three objects, a small grey stone, a boulder,
        or a large blue rock. In this case our list is only 1 item long--but
        that item is a list of 3 objects!

        Normally the player types something like "Get stone, lamp, and 
        knife". This would return (assuming there's only one knife and lamp
        object):

        [Knife,Lamp,[SmallRock,Boulder,BlueRock]]

        This is a list of 3 items, Knife, Lamp, and the list [SmallRock,
        Boulder,BlueRock]. The fact we have a list means the verb itself may
        have to disambiguate further. For example, it makes little sense to
        try and dig a hole with a lamp, right?
        """
        
        #-------------------
        # Create Empty Lists
        #-------------------

        # We have to create lists for one object's adjectives and nouns. We
        # use a list for nouns (even though an object only has one) because
        # it's possible for more than one object to have the same noun.
        #
        # The Return list returns all objects found (the command list might
        # have listed multiple objects).

        AdjectiveList = []
        NounList = []
        ReturnList = []
        
        
        #----------------------------------
        # Loop through each word in command
        #----------------------------------

        # In English: "For each word in the Active command list from the
        # starting postion up to (but not including) the ending position,
        # do the following..."
        #
        # We take advantage of the fact that all non-verb/preposition words
        # in the command pass through this function eventually. The 
        
        for word in self.ActiveCommandList[StartPos:EndPos]:
            
            #-------------------
            # Word is adjective?
            #-------------------

            # If the word is an adjective, look up all objects that have
            # that adjective and append them to the adjective's list.

            if self.AdjsDict.has_key(word):
                AdjectiveList = Union(AdjectiveList,self.AdjsDict[word])
                DebugTrace(word + " is Adjective")

             
            #--------------
            # Is word noun?
            #--------------

            # When the word is a noun we basically append all objects that
            # have that noun, then (if there were adjectives) intersect the
            # noun and adjective list. Then we append all the objects in
            # the trimmed down NounList to the ReturnList (the list of
            # objects returned by this function).

            if self.NounsDict.has_key(word):
                DebugTrace(word + " is Noun")
                NounList = Union(NounList,self.NounsDict[word])

                if len(AdjectiveList) > 0:
                    NounList = Intersect(NounList,AdjectiveList)

                ReturnList.append(NounList)
                AdjectiveList = []
                NounList = []

            
            #----------------
            # Is Word Adverb?
            #----------------

            # If the word is in the adverbs dictionary append the entry(s) to the 
            # current adverb list. Normally an adverb will be only one object, but
            # it doesn't hurt to have more than one adverb object use the same
            # word.
            
            if self.AdverbsDict.has_key(word):
                self.CurrentAdverbList = Union(self.CurrentAdverbList,self.AdverbsDict[word])
                DebugTrace(word + " is Adverb")


        
        #--------------------------
        # Return Found Objects List
        #--------------------------

        # Now it's time to return the list of objects we parsed from the
        # section of the active command list. Note it's very possible for
        # this function to return an empty list.

        return ReturnList
    
    def PreParse(self):
        """
        Default routine for pre-parsing a command. This function translates
        pronouns into the actual objects.
        """
                
        #---------------------------------------
        # Determine Word Count In Active Command
        #---------------------------------------
        
        # WordCount is the # of words in the command list.

        WordCount = len(self.ActiveCommandList)
        
        #-----------------------------------
        # For Each Word In Active Command...
        #-----------------------------------

        # If there are 5 words in the active command then:
        #
        # WordCount = 5 
        # range(WordCount) = [0,1,2,3,4]
        #
        # Thus Position will range from 0 to 4, which as it happens is exactly
        # the range of numbers we need to loop through the active command.
        
        for Position in range(WordCount):
            
            #--------------------
            # Get Lower Case Word
            #--------------------

            # Word is a synonym for everything on the right side of the equal
            # sign--as you can see it's MUCH easier to work with Word than 
            # the complex expression it stands for!

            Word = self.ActiveCommandList[Position].lower()
            Word = Word.encode()
            
            #-----------------------------------------------
            # Complain If Neither Vocabulary nor Punctuation
            #-----------------------------------------------

            # Generally, when we say "Complain" about something, it means that
            # A) we're going to print text for the player to read AND B) that
            # we're going to abort whatever function we're running and return
            # FALSE to the caller.
            #
            # In this case if Word is neither punctuation nor a word in our 
            # vocabulary we complain with the appropriate parser message 
            # (telling the player which word we didn't understand) and we
            # return FALSE to the parser, indicating the pre-parsing process
            # failed.

            if not InVocabulary(Word) and Word not in string.punctuation:
                Text = self.NotInVocabulary % Word
                return Complain(Text)
                
            #-------------------------    
            # Force Word To Lower Case
            #-------------------------
            
            self.ActiveCommandList[Position] = Word
        
        #------------------
        # Create Empty List
        #------------------

        # ReturnList will hold the new command, with it, him, her, or
        # them/all/everything translated to the appropriate object names.

        ReturnList = []
        
        #-------------------------
        # For Each Word In Command
        #-------------------------
        
        # The return list is the new command resulting from the translation of
        # pronouns.
        #
        # We look at each word in the active command list, and if it is NOT a
        # pronoun we simply append it to the return list unchanged. If it's a
        # singular pronoun (it/him/her) we get the object's short description
        # and save it.
        #
        # If it's a plural pronoun (them/all/everything) we loop through the
        # resulting list of objects, appending each object's short description
        # to a variable.
        #
        # In either case we then create a list from the resulting set of words
        # and append them to the return list.
        #
        # In the case of "Take it" (where it refers to a rock) the resulting
        # new command would be "take small gray rock". If the command was "Look at
        # them (and them referred to a ring and a sword) then the command would
        # be translated to "look at gold ring sharp sword" (this command will
        # parse correctly, for all it's horrible English).

        for word in self.ActiveCommandList:
            
            #-------------------
            # Empty Object Names
            #-------------------

            # This string variable holds one or more pronoun short descriptions.
            # For example if the command was "take it" where it was a ring, then
            # ObjectNames would eventually hold "gold ring".
            #
            # If the command was "take them" where them was a ring and sword then
            # ObjectNames would eventually hold "gold ring sharp sword".

            ObjectNames = ""
            
            #-------------------
            # Is Word A Pronoun?
            #-------------------

            # If the word is a pronoun it will be in the Global.PronounsListDict.
            # has_keys returns true if word is in the dictionary, false if it
            # isn't.

            if P.AP().PronounsListDict.has_key(word):

                #------------------
                # Word IS A Pronoun
                #------------------

                # By getting to this point we're convinced the word IS a pronoun
                # that needs to be translated.

                #-------------------
                # Get Pronoun Number
                #-------------------

                # There are 4 kinds of pronouns. They're numbered 0 to 3. The 
                # pronouns are listed below:
                #
                # 0 - it
                # 1 - them/all/everything
                # 2 - him
                # 3 - her
                #
                # Everything but pronoun #1 is singular--it can refer only to a
                # single object. Pronoun #1 is PLURAL, it can refer to more than
                # one object. We have to treat singular and plural pronouns very
                # differently, which is why we need to know the pronoun number.
                #
                # The PronounsListDict contains a list of pronouns and their 
                # corresponding numbers, keyed by word.

                PronounNumber = self.PronounsListDict[word]
                
                #-------------------------------
                # Is Pronoun Singular Or Plural?
                #-------------------------------

                # Any pronoun that isn't THEM is singular. Because pronoun numbers
                # are important, each has been given a constant. IT = 0, THEM = 1,
                # HIM = 2, and HER = 3.
                #
                # Thus the IF test below could have been written:
                #
                # if PronounNumber <> 1:
                #
                # We think this way is easier to understand!

                if PronounNumber <> THEM:
                    
                    #--------------------
                    # Pronoun Is SINGULAR
                    #--------------------
                    
                    # If the pronoun is singular we need to get it from the
                    # PronounsDict dictionary, using the Pronoun Number we looked
                    # up above as the key.
                    #
                    # Each time objects are described to the player the parser
                    # automatically sets the values in PronounsDict for you. The
                    # line below sets Object to whatever object the parser last
                    # described to the player for the pronoun in question (the
                    # parser can store 3 objects, one for it, one for him, and one
                    # for her.

                    Object = self.PronounsDict[PronounNumber]

                    #----------------------------
                    # Get words to add to command
                    #----------------------------
 
                    # ObjectNames will contain the words we're going to add to the
                    # command, in this case the object's short description (which,
                    # conveniently is made up of one or two adjectives and a single
                    # noun). Notice if there is no object stored in the pronoun
                    # dictionary we don't replace the pronouns with ANY words.

                    if Object <> None:
                        ObjectNames = Object.SDesc()

                else:
                    
                    #------------------
                    # Pronoun is PLURAL
                    #------------------

                    # If the pronoun used was them, all, or everything then we take
                    # the short description of EACH OBJECT and add it to
                    # ObjectNames. The next step will be to add the words in 
                    # ObjectNames to the command, replacing the plural pronoun.
                    # 
                    # Notice we do NOT add the current actor to the list!

                    ObjectList = self.PronounsDict[PronounNumber]

                    for Object in ObjectList:
                        if Object <> None and Object<> self.CurrentActor and not Object.IsScenery:
                            ObjectNames = ObjectNames + " " + Object.SDesc()
                
                #================================
                # Add Object Words To Return List
                #================================

                # ObjectNames contains all the words we want to add to the
                # command regardless of whether the pronoun was singular or
                # plural.
                
                #-------------------------
                # Strip leading whitespace
                #-------------------------

                # Strip off any leading spaces to make the conversion easier.

                ObjectNames = string.lstrip(ObjectNames)

                #-------------------------
                # Add Words To Return List
                #-------------------------

                # If ObjectNames has any words in it go ahead and convert the
                # string to a list, then append each word in the list to the
                # return list. Remember, the return list contains the translated
                # command.

                if len(ObjectNames)>0:
                    WordList = string.split(ObjectNames)
                    for word in WordList: ReturnList.append(word)

            else:
                
                #----------------------
                # Word Is NOT A Pronoun
                #----------------------

                # If the word isn't a pronoun we don't need to translate it, so
                # just append it to the ReturnList untouched.

                ReturnList.append(word)
        
        #--------------------------
        # Record Translated Command
        #--------------------------
        
        self.ActiveCommandList = ReturnList

        return SUCCESS

    
    def Prompt(self,PromptArg=">"):
        """
        Default function to return player prompt

        This function provides the player's prompting character. We define
        it first because the parser needs it.
        """

        return PromptArg

class ClassParserAlias:
    """
    This object provides short aliases for some of the monster-length
    properties otherwise required. If you swap out the parser you should
    create your own aliasing class and recreate the P instance with your
    class.

    Note this alias class is NOT based on ClassFundamental(), it's a
    "lightweight" class based directly on the Python's own base object.
    """

    def AP(self):
        """
        The active parser, the current parser. Allows you access to all
        kinds of parser information.
        """
        return Global.ActiveParser
        
    def AVL(self):
        """
        Synonym for Global.ActiveParser.CurrentAdverbList.
        """
        return Global.ActiveParser.CurrentAdverbList

    def CA(self):
        """
        Synonym for Global.ActiveParser.CurrentActor.
        """
        return Global.ActiveParser.CurrentActor
    def CV(self): return Global.ActiveParser.CurrentVerb
    def CVN(self): return Global.ActiveParser.CurrentVerbNoun
    def DOL(self): return Global.ActiveParser.CurrentDObjList
    def IOL(self): return Global.ActiveParser.CurrentIObjList
    
class ClassEngine(ClassFundamental):
    """
    The class ClassEngine lays out the majority of the runtime system. Along
    with the Global object and the parser it makes up about 95% of the
    runtime system.
    """
    
    #--------------------
    # Initialize function
    #--------------------

    def __init__(self):
        """Sets default instance properties"""
        self.NamePhrase = "Engine Object"
        ClassFundamental.InheritProperties(self)

        
    
    def SetMyProperties(self):

        #----------------------
        # Assign method Aliases
        #----------------------

        
        # We want to set up aliases for the default game engine routines.
        # These aliases are the "functions" called by you the developer, not
        # the default function itself.

        # For example, Prompt is the alias to default_Prompt. Note we're not
        # instantiating an object here, we're assigning an alias. At this
        # point in the code Prompt() and default_Prompt() do exactly the
        # same thing.
        #
        # Why bother, you ask? Because the developer (the game author--you)
        # can replace the default prompt with your own function. Let's say
        # you create a really neat function called MyPrompt().
        #
        # At the end of your function all you have to say is:
        #
        #   Engine.Prompt = MyPrompt
        #
        # and the game engine will start using your prompt instead of the
        # default one! Pretty neat, eh? Notice you don't follow MyPrompt
        # with parentheses, you want to assign the address of your function
        # to Prompt, not the return value!

        self.AfterTurnHandler = default_AfterTurnHandler
        self.BuildStatusLine = default_BuildStatusLine
        self.GameSkeleton = default_GameSkeleton
        self.PreTurnHandler = default_PreTurnHandler
        self.PostGameWrapUp = default_PostGameWrapUp
        self.RestoreFunction = None
        self.SaveFunction = None
        self.SetUpGame = default_SetUpGame
        self.TurnHandler = default_TurnHandler
        self.UserSetUpGame = default_UserSetUpGame
        self.Version = "2.03"
        self.XlateCBEFunction = None

class ClassBaseObject(ClassFundamental):
    """
    This class is used to extend all "thing" classes. It basically adds the
    current object's name(s) and adjectives to the parser dictionaries. It
    also provides minimal functionality to support the parser.
    """

    def __init__(self,Name = "",Adjs = "", PluralName = ""):
        """
        This method is called ONLY when an object is instantiated. For
        instance if "rock" were being defined the instantiation would look
        like:

        SmallRock = ClassBaseObject("rock,stone","small,grey")
    
        This is the equivalent of saying:
    
        SmallRock = ClassBaseObject.__init__("rock,stone","small,grey")
    
        In other words, you're actually calling the __init__() method when
        you instantiate a class.
        """

        #-------------------------------------------------
        # Append Object to Noun and Adjective Dictionaries
        #-------------------------------------------------

        AppendDictList(P.AP().NounsDict,Name,self)
        AppendDictList(P.AP().NounsDict,PluralName,self)
        AppendDictList(P.AP().AdjsDict,Adjs,self)
        
        #--------------------------------------------------
        # Append Vocabulary To Part Of Speech To Dictionary
        #--------------------------------------------------

        AppendDictList(P.AP().POSDict,Name,"N")
        AppendDictList(P.AP().POSDict,PluralName,"N")
        AppendDictList(P.AP().POSDict,Adjs,"A")
        
        #---------------------------
        # Set KeyNoun And NamePhrase
        #---------------------------

        # The KeyNoun lets us find this object in the NounDict for disambiguation
        # purposes. Notice we also set the NamePhrase to the KeyNoun, this
        # allows us to avoid having to set it explicitly.

        NounList = string.split(Name,",")

        if len(NounList) > 0:
            self.KeyNoun = NounList[0]
        else:
            self.KeyNoun = ""

        self.NamePhrase = self.KeyNoun
        
        #--------------------
        # Set AdjectivePhrase
        #--------------------

        AdjectiveList = string.split(Adjs,",")

        if len(AdjectiveList) > 0:
            self.AdjectivePhrase = AdjectiveList[0]
        else:
            self.AdjectivePhrase = ""

        #--------------------
        # Set self properties
        #--------------------

        ClassFundamental.InheritProperties(self)

class ClassBaseVerbObject(ClassFundamental):
    """
    This class is used to extend all verb classes. It basically adds the
    current verb's name(s) ("go","walk", etc) to the dictionary, along with
    the appropriate prepositions.
    """

    def __init__(self,Name = "",Preps = "nopreposition"):
        """
        This method is called ONLY when an object is instantiated. For
        instance if "quit" were being defined the instantiation would look
        like:

        QuitVerb = ClassBaseVerb("quit")
    
        This is the equivalent of saying:
    
        QuitVerb = ClassBaseVerb.__init__("quit")
    
        In other words, you're actually calling the __init__() method when
        you instantiate a class.
    
        Notice how we default the Preps argument? This way, a developer can
        easily create verbs that have no prepositions ("quit", "save", etc).
        """
        
        #-----------------------------------------
        # Append all verb names to verb dictionary
        #-----------------------------------------

        AppendDictList(P.AP().VerbsDict,Name,self)
        AppendDictList(P.AP().PrepsDict,Preps,self)
        
        
        #-----------------------------------------------
        # Append All Verbs To Parts Of Speech Dictionary
        #-----------------------------------------------

        AppendDictList(P.AP().POSDict,Name,"V")
        AppendDictList(P.AP().POSDict,Preps,"P")
        
        
        #---------------------------
        # Set KeyNoun And NamePhrase
        #---------------------------

        # The KeyNoun lets us find this object in the NounDict for
        # disambiguation purposes. Notice we also set the NamePhrase
        # to the KeyNoun, this allows us to avoid having to set it
        # explicitly.

        VerbList = string.split(Name,",")

        if len(VerbList) > 0:
            self.KeyNoun = VerbList[0]
        else:
            self.KeyNoun = ""

        self.NamePhrase = self.KeyNoun

        
        #--------------------
        # Set Self Properties
        #--------------------

        ClassFundamental.InheritProperties(self)
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        
        #----------------------------
        # Only Allowed Direct Objects
        #----------------------------

        # This is a "placeholder" list. If any objects are put in this list,
        # they become the only direct objects that can be used with this verb, 
        # any other direct objects will cause the verb to fail.
        #
        # This allows a simple way to restrict verbs to certain direct objects.

        self.OnlyAllowedDObjList = []
        
        #------------------------------
        # Only Allowed Indirect Objects
        #------------------------------

        # This is a "placeholder" list. If any objects are put in this list, they
        # become the only indirect objects that can be used with this verb, any
        # other indirect objects will cause the verb to fail.
        #
        # This allows a simple way to restrict verbs to certain objects.

        self.OnlyAllowedIObjList = []
        
        #-----------------
        # Object Allowance
        #-----------------

        # The object allowance property determines what the verb expects in the
        # way of direct and indirect objects. As you can see we set the property
        # by adding two of the object allowance constants together, one for the
        # direct and one for the indirect objects.

        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_ONE_IOBJ
        
        #-----------
        # OK In Dark
        #-----------

        # Set this value to TRUE if the verb can be used in the dark. The default
        # is FALSE.

        self.OkInDark = FALSE
    
    def Action(self):
        """
        Although this method is a simple "placeholder" intended to be
        replaced in every descendent class, the replacement methods are the
        ones that actually "do" something.
    
        The Action() method must always return either TURN_ENDS or 
        TURN_CONTINUES. Return TURN_ENDS if you want the AfterTurnHandler to
        run, TURN_CONTINUES if you don't.
        """

        return TURN_CONTINUES

    def Execute(self):
        """
        The execute method is small, but very flexible. The first thing it
        does is call the GenericDisambiguate method. The GenericDisambiguate
        method elminates direct and indirect objects that don't make sense
        for the verb. In addition, it verifies that verbs that don't allow
        direct and indirect objects don't have any. If it should fail it
        returns FAILURE immediately.
    
        Then if the SanityCheck() fails we return FAILURE immediately. The
        SanityCheck allows us a way to test each verb, we replace it the
        same way we do Action().
    
        Finally, if both the GenericDisambiguate() and SanityCheck() methods
        are successful we return the value of Action() (which will be either
        TURN_ENDS or TURN_CONTINUES).
        """

        if not self.GenericDisambiguate(): return TURN_CONTINUES
        if not self.SanityCheck(): return TURN_CONTINUES
        return self.Action()
    
    def GenericDisambiguate(self):
        """
        Disambiguate means to remove ambiguity (uncertainty) from something.
        In this case it means remove the direct and indirect objects that
        don't make sense in the current context.
    
        For instance, this would include objects the current actor (usually
        the player) hasn't yet encountered, or couldn't know about. In this
        "generic" disambiguation, we handle situations that are common to
        ANY game you might write.
    
        We also call a specific disambiguate routine at the end of our
        generic one. This "layered" approach allows us to create a default
        behavior (aborting disambiguation immediately if there are no
        objects, and removing unknown objects) as well as library or game
        specific disambiguation (object isn't here, isn't reachable,
        is invisible, is locked, etc).
        """

        DebugTrace("Chosen Verb --> "+self.__class__.__name__)
        
        #-----------------------------------
        # Check for forbidden direct objects
        #-----------------------------------

        # If the verb doesn't allow direct objects, and direct objects were used
        # we complain and return TURN_CONTINUES. This insures the Execute()
        # method won't call the verb's action.

        if len(P.DOL()) <> 0 and (self.ObjectAllowance & ALLOW_NO_DOBJS):
            return Complain(SCase(P.AP().DObjsNotAllowed % P.CVN()))
       
        #-------------------------------------
        # Check for forbidden indirect objects
        #-------------------------------------

        # If the verb doesn't allow indirect objects, and indirect objects were
        # used we complain and return TURN_CONTINUES. This insures the Execute()
        # method won't call the verb's action.

        if len(P.IOL()) <> 0 and (self.ObjectAllowance & ALLOW_NO_IOBJS):
            return Complain(SCase(P.AP().IObjsNotAllowed % P.CVN()))

         
        #-----------------------------
        # Call Specific Disambiguation
        #-----------------------------

        # Verbs defined in the library must have a more specific
        # disambiguation routine defined. The library will override our
        # definition of the method with its own. If the disambiguation
        # fails for some reason we will abort the GenericDisambiguation
        # routine, and thus abort the command.

        if not self.SpecificDisambiguate(): return FAILURE

        return SUCCESS
    
    def SanityCheck(self):
        """
        This function is (optionally) implemented on a verb by verb basis
        (maybe). It's a last ditch effort to make the action fail before
        it's executed. Return SUCCESS if you want the action to execute,
        FAILURE if you don't.
        """
        
        return SUCCESS

    def SDesc(self):
        """Verb short description"""
        return self.NamePhrase
        
    def SpecificDisambiguate(self):
        """
        Specific disambiguation handles removing objects specific to the
        game. This routine will be overridden by the game library, or even
        specific verbs within the game itself.
        """

        return SUCCESS

class ClassAdverb(ClassFundamental):
    """
    This class is used to create adverb objects. An adverb object is 
    basically just the name of the adverb and a method to determine if the
    adverb was used in the current command.
    """

    def __init__(self,Name = ""):
        """Adds adverb to appropriate Global dicts"""

        #---------------------------------------------
        # Append all adverb names to adverb dictionary
        #---------------------------------------------

        AppendDictList(P.AP().AdverbsDict,Name,self)
        
        #-----------------------------------------------
        # Append All Verbs To Parts Of Speech Dictionary
        #-----------------------------------------------

        AppendDictList(P.AP().POSDict,Name,"D")
        
        #---------------
        # Set NamePhrase
        #---------------

        # The KeyNoun lets us find this object in the NounDict for
        # disambiguation purposes. Notice we also set the NamePhrase
        # to the KeyNoun, this allows us to avoid having to set it
        # explicitly.

        AdverbList = string.split(Name,",")
        self.NamePhrase = AdverbList[0]
        
        #--------------------
        # Set Self Properties
        #--------------------

        ClassFundamental.InheritProperties(self)

    def SetMyProperties(self):
        """Sets default instance properties"""
        pass
         


    def Applies(self):
        """
        This method returns TRUE if this adverb was used in the current
        command, FALSE if it wasn't.
        """        

        return (self in P.AVL())
                              


#********************************************************************************
#                                     Create Terminal
#
# Up until now, we've just been defining things. This is the part of the program
# that actually starts DOING something!

#-----------------------
# Set Up ActiveIO Object
#-----------------------

ActiveIO = ClassActiveIO()

#-------------------------
# Set Up And Save Terminal
#-------------------------

ActiveIO.ActiveIO = ClassTerminal()
Terminal = ActiveIO.ActiveTerminal()

#********************************************************************************
#                               Create Core Objects
#
C="""
  Here's where the file gets down to some serious work. We're creating the
  objects Universe and your game file need to call on: Global information, 
  the parser and parser alias obects, and finally the game engine itself.
  
  After these objects are created Universe will have a solid foundation to 
  rest on.
  """

Global = ClassGlobal()
Global.ActiveParser = ClassParser()
ParserObject = Global.ActiveParser
P = ClassParserAlias()
Engine = ClassEngine()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                            End of Core Module                                 #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%