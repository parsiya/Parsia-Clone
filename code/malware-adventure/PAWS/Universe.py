#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                 Universe Object Library For PAWS Engine                       #
#          Written by Roger Plowman & Kevin Russell (c) 1998-2008               #
#                                                                               #
# The C="""...""" statements scattered throughout this source code are actually #
# a work-around for Python's lack of block comments. Notepad++ can only fold    #
# block comments, not a series of comment lines. Using C="""...""" doesn't      #
# increase PAWS memory footprint, although it does have a tiny impact           #
# on loading time.                                                              #
#                                                                               #
C="""
  This library supplies the basic "laws of nature" for the PAWS engine. It
  provides the basic functionality a game author expects. This is the layer
  most people will think of when they think of PAWS.

  Written By: Roger Plowman
  Written On: 08/27/98

  Portions By: Kevin Russell
  Written On:  09/14/99
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

#********************************************************************************
#                                    Contributors
#
C="""
  Although I created Universe and wrote most of it, others have contributed 
  significant portions to the whole. Here's a list of who contributed what:
 
  Contributor      Contribution
  -----------      ------------
 
  Kevin Russel     ServiceActivation, ServiceOpenable, 
                   ServiceContain In/On/Under/Behind, ServiceFollow, 
                   ServiceOpenable, ServiceLockable, ServiceRevealWhenTaken,
                   ClassDoor, ClassLockableDoor, ClassUnder/BehindHiderItem,
                   Insert() method, all verbs to make the above work,
                   Functions: Agree(), Be(), Have(), Do(), Go(),
                   FollowerDaemon()
 
  Atholbrose       Verbose/Tense Verbs

  James Cunningham Fixes to TerminalFrame that allowed it to work in OS X
                   and Linux as well. Speed enhancements to Say() that work
                   in all 3 OSs but are particulary helpful in OS X. Also 
                   solved the scrolling issue on all 3 OSs.
                   
  Greg @ R.A.I.F   Suggestion that allowed binary pickling to work, enabling
                   the Save Game file to be somewhat obfuscated, reducing
                   player cheating.                   
  """

#********************************************************************************
#                            Import needed Modules
#
C="""
  By importing (a reference) to everything in PAWS.py we gain two benefits. 
  First, we can refer to *anything* in the PAWS module without putting
  "PAWS." in front of it. For example instead of saying PAWS.Engine we can
  just say Engine.
 
  Second, we don't have to perform any imports for the standard modules PAWS
  already imported, which is convenient. Keep in mind, when it comes to
  programming *LAZY IS GOOD*. In this case we save memory by not having 2
  copies of the same thing, and we also save on typing!
"""

from Core import *

#********************************************************************************
#                        U N I V E R S E   F U N C T I O N S
#
# This section contains functions that can be referenced by your game. These are
# similar in nature to the functions in the PAWS file, your game can use both.

def Agree(Verb, Subject=None, Contract=FALSE):
    """
    Returns proper verb to agree with subject, allows contraction.
    
    The arguments of the Agree() function are:
    
    Verb:     This is the verb whose format is to be decided.

    Subject:  This is the Actor whose "you/he/she/they" status the verb
              should agree with.  If none is given, the verb will agree
              with the status of the current player.

    Contract: if true, Agree() will return a contracted form of the verbs
              "be" or "have".  Contract has no effect on other verbs. 

    Some examples of use:

    "{You()} {Agree('put')} the coin into the slot."

    "{Fred.FormatYou} {Agree('be',Fred)}n't going anywhere without {Fred.FormatYour} security blanket."

    "Surprise, {You()}{Agree('be',contract=TRUE)} dead."
    """

    #----------------------------
    # Setting the default subject
    #----------------------------

    # If Agree() wasn't called with a specific subject (in which case the Subject
    # parameter will contain the special None value given to it above in the
    # function header), then we want to set the subject to the current actor.

    if not Subject: Subject = P.CA()
    
    #----------------------------------
    # Strip Leading/Trailing Whitespace
    #----------------------------------

    # Get rid of any leading or trailing whitespace (not that there should be
    # any, of course). This is just adding robustness to the function, 99 times
    # out of 100 it won't make any difference, but that 100'th time...

    Verb = string.strip(Verb)
    
    #---------------------
    # Use Contracted Form?
    #---------------------

    # If the author wants a contraction we have to physically add the word
    # "contracted" for "be" and "have", so we can find it in the
    # VerbAgreementDict. VerbAgreementDict holds exceptions to the general rules
    # of verb agreement (which both "be" and "have" are).

    if Contract and Verb in ["be","have"]: Verb = "contracted" + Verb
    
    #-------------------
    # Is Verb Irregular?
    #-------------------

    # If the verb has irregular forms of subject agreement it will be in
    # VerbAgreementDict. VerbAgreementDict stores a LIST of entries, the first is
    # the plural/you form, the second is the singular form.
    #
    # Note if this IF test is true, the function returns a value and
    # doesn't continue.

    if Global.VerbAgreementDict.has_key(Verb):
        if Subject.FormatYou == "you" or Subject.IsPlural:
            return Global.VerbAgreementDict[Verb][0]
        else:
            return Global.VerbAgreementDict[Verb][1]
    
    #------------------------------------
    # Verb Is Regular. Is Subject Plural?
    #------------------------------------

    # Getting this far means the verb wasn't in VerbAgreementDict so it wasn't an
    # irregular verb.
    #
    # If the subject is "you" or the subject is plural (like "they") then just
    # return the verb you were sent and the function stops here.

    if Subject.FormatYou == "you" or Subject.IsPlural: return Verb
    
    #-------------------------------------
    # Verb Is Regular, Subject is Singular
    #-------------------------------------

    # We"re dealing with a third person singular. First handle the case where the
    # Verb ends in "y": if the second last letter is not a vowel, the "y" should
    # be replaced with "ies", otherwise just add "s"

    if Verb[-1] == "y" and Verb[-2] not in "aeiou":
        return Verb[:-1]+"ies"
    else:
        return Verb+"s"

def Be(Subject = P.CA(), Contract=FALSE):
    """Synonym for Agree("be")."""
    return Agree("be", Subject, Contract)

def Do(Subject = P.CA(), Contract=FALSE):
    """Synonym for Agree("do")."""
    return Agree("do", Subject, Contract)

def FollowerDaemon():
    """
    This function is a DAEMON, a function that will be run automatically
    every turn by the game engine (when started with the StartDaemon
    function).
    
    It makes an actor follow the player around.
    """

    for actor in Global.ActorList:
        if actor.Get("Follow"): actor.FollowPlayer()

def Go(Subject = P.CA(), Contract=FALSE):
    """Synonym for Agree("go")."""
    return Agree("go", Subject, Contract)

def Have(Subject = P.CA(), Contract=FALSE):
    """Synonym for Agree("have")."""
    return Agree("have", Subject, Contract)

def IncrementScore(Amount,Silent=FALSE):
    """
    This function increments the player's score, and lets the player know
    when it happens. Use this function with a negative Amount to reduce the
    player's score.
    """

    #-----------------------
    # Adjust Score By Amount
    #-----------------------

    Global.CurrentScore = Global.CurrentScore + Amount
    
    #---------------------------------
    # Determine proper word for Change
    #---------------------------------

    # We want to say decreased for a negative amount, increased for a positive
    # one, and nothing at all for a 0 amount.

    ChangeWord = ""
    if Amount < 0: ChangeWord = "decreased"
    if Amount > 0: ChangeWord = "increased"
    
    #--------
    # Plural?
    #--------

    # It's 1 point, but otherwise 0 points, 2 points, etc...

    PluralWord = "points"
    if abs(Amount) == 1: PluralWord = "point"
    
    #--------------
    # Build Comment
    #--------------

    Comment = "[Your score just %s by %d %s.] ~p" % \
              (ChangeWord,Amount,PluralWord)
    
    #------------------------
    # Say it if score changed
    #------------------------

    # If the score changed and Silent is false (not TRUE is FALSE) then
    # say comment, otherwise don't. Silent score changes can be handy
    # if you don't want the player to know when their score changes.

    if Amount <> 0 and not Silent:
        Say(Comment)
        Terminal.DisplayStatusLine(Global.StatusLine)

def Me():
    """Synonym for current actor's FormatMe property."""
    return P.CA().FormatMe
def UniverseBanner():
    """
    Don't touch this, it must appear in all games (Universe is free, but I
    want people to know who wrote it! <grin> Having this said in all your 
    games is the "price" you pay for using Universe.
    """

    Text = """
           ~n This game uses Universe version %s, a PAWS class library. ~n %s. ~n Displayed on 
           terminal ~i {Terminal.NamePhrase}. ~l
           ~p
           """

    Text = Text % (UniverseVersion,UniverseCopyright)

    return Text


def Universe_BuildStatusLine(LeftSideText=None):
    """
    This function replaces the Engine method that builds the status line to
    display on the terminal. It puts the score and turn count on the right
    side of the status line and the passed text (usually the room's short
    description) on the left. If no text is passed the game's name will 
    be used instead.
    """

    if not LeftSideText: LeftSideText = Game.Name

    RightSide = " Score: " + repr(Global.CurrentScore) + \
                " Turn: " + repr(Global.CurrentTurn) + "  " 

    SLL = 80 # Terminal.MaxScreenColumns
    RSL = len(RightSide)   
    LeftSide = string.ljust(" " + LeftSideText[:SLL], SLL)
    Global.StatusLine = LeftSide[:-RSL] + RightSide
    
def Universe_SetUpGame():
    """
    This function replaces the Engine method called at the start of your
    game. It sets up fuses, daemons, and other game mechanics required
    before the game can begin. It also calls UserGameSetup() as the first
    thing it does.
    """
    
    #--------------------
    # Clear Contents List
    #--------------------

    # Clear contents lists. This is part of initial set up AND it happens during
    # a restart as well.

    for Object in Global.AllObjectsList: Object.Contents=[]
    Global.MaxScore = 0
    
    #--------------
    # Object Set Up
    #--------------

    # In English: For all objects in the AllObjectsList (all "things"), do the
    # following...

    for Object in Global.AllObjectsList:
        
        #--------------------
        # Set Object Location
        #--------------------

        # If the object's starting location is not None (meaning it has no 
        # location) then call the object's MoveInto method to move it into the
        # starting location. Notice we don't set the object's location directly!
        #
        # The location of an object is actually stored in two places. First, it's
        # stored in the object's Location property, second it's stored in the
        # contents list of Object's Location.
        #
        # The Location property holds either None or the object that contains the
        # object. (In this case a room is considered a "container", although a
        # special kind of one).
        #
        # Floating objects are special, but the Where() method will tell you the
        # location of any object, floating or not.

        if Object.StartingLocation <> None:
            Object.MoveInto(Object.StartingLocation)
        
        #------------------------
        # Increment Maximum Score
        #------------------------

        # Since the loop we're in runs through all objects, all we need to do is
        # add the object's value (if it has one) to the maximum score.

        if hasattr(Object,"Value"):
            Global.MaxScore = Global.MaxScore + Object.Value
        
        #---------------------------
        # Append Actor To Actor List
        #---------------------------

        # If this object is an actor then we append it to the Actor list.
        # This lets us find it very quickly later if we want to look just
        # for an actor...

        if Object.IsActor: Global.ActorList.append(Object)
        
        #---------------------------------
        # Append to Floating Location List
        #---------------------------------

        # If this object has a floating location, then we append it to the
        # floating location object list. This allows us to easily deal with
        # floating objects in the future as a group.

        if Object.HasFloatingLocation:
            Global.FloatingLocationList.append(Object)

        #----------------------------
        # Append To Light Source List
        #----------------------------

        # If this object is a potential light source, append it to the light
        # source list.

        if Object.IsLightSource: Global.LightSourceList.append(Object) 
        
        #-------------------------
        # Append Item To Item List
        #-------------------------

        # If this object is not scenery, then it's takable. then we append it to
        # the Item list. This lets us find it very quickly later if we want to
        # look just for an item...

        if ServiceTakeableItem in ObjectBaseClasses(Object):
            Global.ItemList.append(Object)

        #-------------------------
        # Append Item To Item List
        #-------------------------

        # If this object is scenery, then it's not takable. We append it to the
        # Scenery list. This lets us find it very quickly later if we want to
        # look just through scenery items...

        if Object.IsScenery: Global.SceneryList.append(Object)
    
    #---------------------------
    # Add "Everything" and "All"
    #---------------------------

    # We want to be able to say "Get all" or "Drop everything". In order to do
    # that we simply add two nouns to the NounsDict with values of
    # Global.ItemList. Remember, the item list contains only takable items.

    P.AP().NounsDict["everything"] = Global.ItemList
    P.AP().NounsDict["all"]        = Global.ItemList
    
    #----------------------
    # Call User Set Up Game
    #----------------------

    # The UserSetUpGame method lets us set information specific to our game, such
    # as some of the Game object properties like Game.Name, Game.Version, etc.

    Engine.UserSetUpGame()
    
    #----------------
    # Call Game Intro
    #----------------

    # Note the game introduction is printed AFTER the author-written game 
    # setup is complete.
    
    Game.PrintGameIntroduction()
    
    #------------------
    # Start Game Daemon
    #------------------

    # The statement below starts the GameDaemon function running. At the end of
    # each turn the function GameDaemon() will run automatically.

    StartDaemon(GameDaemon)
    
    #----------------------
    # Memorize Ground & Sky
    #----------------------

    # By this time we've already run the UserSetUpGame routine, meaning we know
    # who the current actor is. We need to memorize ground and sky so the
    # player's character knows what they are.

    P.CA().Memorize(Sky)
    P.CA().Memorize(Ground)
    P.CA().Memorize(Wall)
    P.CA().Memorize(NoWall)
    
    #-------------------
    # Memorize Inventory
    #-------------------

    # The player already knows about anything he's carrying, so we need to have
    # the player's character memorize it.
    
    for Object in Global.Player.Contents:
        Global.Player.Memorize(Object)


def You():
    """Synonym for current actor's FormatYou property."""
    return P.CA().FormatYou
def Your():
    """Synonym for current actor's FormatYour property."""
    return P.CA().FormatYour
def Youm():
    """Synonym for current actor's FormatYoum property."""
    return P.CA().FormatYoum


#********************************************************************************
#                    U N I V E R S E     S E R V I C E S
#
C="""
  A SERVICE is just a "mini" class used to add abilities to the base 
  classes. For example, an actor by themselves isn't much use. But add a
  combat service and you have a monster. Add a Patrol service and you have
  a wandering monster.
 
  Take a room and add a Patrol service and you have a moving room! Services
  are carefully designed so any service can be used with any class.
 
  Note services never inherit from a base class, they *are* base classes.
  """

class ServiceActivation:
    """
    This service allows devices to be activated and deactivated. This is
    generally used for light sources but can be used for any device that
    is switched on or off, with or without a tool.
    """

    def SetMyProperties(self):
        """
        This service is particularly involved, having lots of possible
        complaints and options. Therefore each property below gets its own
        lengthy explanation. Note this service is designed primarily for 
        lightsources (like flashlights, torches, candles, etc) but can
        easily accomodate any device with a simple on/off function just by
        changing the wording of the various properties.
        """
        
        #------------------------------------
        # Activate Spontaneous/Passive Phrase
        #------------------------------------
        
        # These two properties are used by the ActivateDesc() method to describe
        # the activation to the player. The word "spontaneous" in this context
        # means "active", as in "active voice" and Passive means "passive voice".
        # By default Spontaneous is false, so passive voice will be used.
        #
        # Spontaneous would be "You light the lamp." while passive would be 
        # "The lamp lights up." Notice we use curly brace expressions so the
        # strings will always reflect the object in question.
        #
        # You'll also notice the use of the function "Self()." instead of the
        # more familiar "self.". This is due to a design issue in Python. "self"
        # is actually a variable that only exists inside the class definition of
        # the object. Self(), on the other hand can safely be used in place of
        # "self" in curly brace expressions.

        self.ActivatePassivePhrase = """
                                     {SCase(You())} light
                                     {Self().TheDesc()}.
                                     """

        self.ActivateSpontaneousPhrase = """
                                         {SCase(Self().TheDesc())}
                                         lights up.
                                         """
        
        #--------------------
        # Activation Property
        #--------------------

        # This is the TRUE/FALSE property that is manipulated by the Activate()
        # and Deactivate() methods. You'll note it's a string, by default it's
        # the IsLit property.
        #
        # So activating a light source device makes self.IsLit TRUE and
        # deactivating it makes self.IsLit FALSE.
        #
        # Of course if self isn't a light source you could use a different
        # property, including those of your own creation, perhaps IsOn, or
        # IsRunning.

        self.ActivationProperty = "IsLit"
        
        #-------------------------------------
        # Already Activated/Deactivated Phrase
        #-------------------------------------

        # This pair of properties is returned by the AlreadyActivatedDesc() and
        # DeactivatedDesc() methods. They say "The lamp is already lit" and 
        # "The lamp is already out."
        #
        # Obviously the wording is skewed toward light source devices and can
        # easily be changed for other things. For instance change "lit" to
        # "running" and "already out" to "isn't running" if you're dealing with
        # an electric water pump.

        self.AlreadyActivatedPhrase = """
                                      {Self().TheDesc()} {Be(Self())}
                                      already lit.
                                      """

        self.AlreadyDeactivatedPhrase = """
                                      {Self().TheDesc()} {Be(Self())}
                                      already out.
                                      """

        
        #--------------------------------------
        # Deactivate Spontaneous/Passive Phrase
        #--------------------------------------
        
        # These two properties are used by the DeactivateDesc() method to
        # describe the deactivation to the player. The word "spontaneous" in
        # this context means "active", as in "active voice" and Passive means
        # "passive voice". By default Spontaneous is false, so passive voice
        # will be used.
        #
        # Spontaneous would be "You douse the lamp." while passive would be "The
        # lamp is now out." Notice we use curly brace expressions so the strings
        # will always reflect the object in question.
        #
        # You'll also notice the use of the function "Self()." instead of the
        # more familiar "self.". This is due to a design issue in Python. "self"
        # is actually a variable that only exists inside the class definition of
        # the object. Self(), on the other hand can safely be used in place of
        # "self" in curly brace expressions.

        self.DeactivatePassivePhrase = """
                                       {You()} douse
                                       {Self().TheDesc()}
                                       """

        self.DeactivateSpontaneousPhrase = "{Self().TheDesc()} goes out."
        
        #-------------------------
        # Required Activation Tool
        #-------------------------

        # Certain devices require a tool to turn them on, for example a candle
        # needs a match to light it, a bonfire might need a torch, a fire
        # hydrant might need a wrench, and so on.
        #
        # This property is set to the object needed to activate self. If set to
        # None (as it is by default) then no tool is needed to activate self.

        self.RequiredActivationTool = None
        
        #---------------------------
        # Required Deactivation Tool
        #---------------------------

        # This is the tool required to deactivate self. It can be None if no 
        # tool is required (like a flashlight), it can be the same tool used to
        # activate self (like a fire hydrant) or it can be a different tool 
        # (such as a candle snuffer).

        self.RequiredDeactivationTool = None

        #------------------
        # Maximum Life Span
        #------------------

        # The maximum number of turns this device can operate before being
        # refueled/recharged/battery replacement. This value is also used when a
        # device is recharged, to return the RemainingLifeSpan property to the 
        # value of this property.
        #
        # By default we set this value to 32,000 turns. Obviously you should
        # lower this for devices you create!

        self.MaxLifeSpan = 32000
        
        #--------------------
        # Remaining Life Span
        #--------------------

        # This is the number of turns of fuel/power the device has left to run.

        self.RemainingLifeSpan = self.MaxLifeSpan

    def Activate(self, Multiple=FALSE, Spontaneous=FALSE, Silent=FALSE):
        """
        This function activates self, if self were a flashlight for example
        this function would turn it on.
    
        The following arguments are available but may not be used in this
        default method.

        Multiple    - Not used, allows the method to detect when self is
                      part of a multiple list of objects. Defaults to
                      false. This argument can be handy to say something
                      different when self is part of a list than when it's by
                      itself.

        Spontaneous - In this context TRUE means "active voice" and FALSE
                      means "passive voice". Active voice would be "You
                      light the lamp". Passive voice would be "The lamp
                      lights up."
                    
        Silent      - If TRUE then the ActivateDesc() method is skipped, if
                      FALSE the ActivateDesc() method is called.
        """

        #------------------------------
        # Complain If No Life Span Left
        #------------------------------

        if not self.RemainingLifeSpan: return Complain("Nothing happens.")
        
        #------------------------------
        # Complain if already activated
        #------------------------------

        # Let's assume self is a flashlight. Let's further assume we didn't
        # change self.Activation property from "IsLit". Therefore the if test
        # below translates into English "if the flashlight is lit then..."

        if self.Get(self.ActivationProperty):
            return Complain(self.AlreadyActivatedDesc())
        
        #------------------------------
        # Get Tool Needed And Tool Used
        #------------------------------

        # ToolNeeded is the tool needed to activate the device, which can be
        # None (for example, a flashlight). ToolUsed is assumed to be None,
        # unless there's an indirect object in the list. This would only happen
        # where the player said "Light torch with..." or some such. If they just
        # said "light lamp" then ToolUsed remains None.

        ToolNeeded = self.RequiredActivationTool

        ToolUsed = None
        if len(P.IOL()) > 0: ToolUsed = P.IOL()[0]
        
        #----------------------------
        # If Tool Used But Not Needed
        #----------------------------

        # For example, if they tried to light the flashlight with a 
        # match...

        if ToolUsed and not ToolNeeded:
            return Complain("%s can't do that." % You())
        
        #----------------------------
        # If Tool Needed and Not Used
        #----------------------------

        # For example "light candle" instead of "light candle with match".

        if ToolNeeded and not ToolUsed:
            return Complain(self.RequiresToolDesc())
        
        #----------------------------
        # Complain If Wrong Tool Used
        #----------------------------

        # This test is a bit of elegant short-cutting. ToolNeeded will either
        # contain None or some object. If None then testing ToolNeeded returns
        # false. If ToolNeeded is any object, then testing ToolNeeded returns
        # true.
        #
        # You could also write the IF test this way:
        #
        # if ToolNeeded <> None and ToolNeeded <> ToolUsed:
        #
        # But I think this way is easier to read and understand.

        if ToolNeeded and ToolNeeded <> ToolUsed:
            return Complain(self.WrongToolDesc())
        
        #--------------------------------
        # Set Activation Property To TRUE
        #--------------------------------

        # The setattr() function lets you use a string to name the property you
        # want to set. This is exactly what we need to set any property we care
        # to put in the ActivationProperty property.

        setattr(self, self.ActivationProperty, TRUE)
        
        #----------------------------
        # Run DrainLife() As A Daemon
        #----------------------------
        
        StartDaemon(self.DrainLife, self.LifeRemaining())

        #--------------------------
        # Tell Player Unless Silent
        #--------------------------

        # If Silent is FALSE then tell the player the device activated.

        if not Silent: Say(self.ActivateDesc(Multiple, Spontaneous))
        
        #---------------
        # Return Success
        #---------------

        return SUCCESS
    
    def Deactivate(self, Multiple=FALSE, Spontaneous=FALSE, Silent=FALSE):
        """
        This function deactivates self, if self were a flashlight for
        example this function would turn it off.

        The following arguments are available but may not be used in
        this default method.
    
        Multiple    - Not used, allows the method to detect when self is
                      part of a multiple list of objects. Defaults to FALSE.
                      This argument can be handy to say something different
                      when self is part of a list than when it's by itself.
    
        Spontaneous - In this context TRUE means "active voice" and FALSE
                      means "passive voice". Active voice would be "You
                      douse the lamp". Passive voice would be"The lamp turns
                      off."

        Silent      - If TRUE then the DeactivateDesc() method is skipped,
                      if FALSE the DeactivateDesc() method is called.
        """
        
        #-----------------------------
        # Complain if already Inactive
        #-----------------------------

        # Let's assume self is a flashlight. Let's further assume we didn't
        # change self.Activation property from "IsLit". Therefore the if test
        # below translates into English "if the flashlight is not lit then..."

        if not self.Get(ActivationProperty):
            return Complain(self.AlreadyDeactivatedDesc())

        #------------------------------
        # Get Tool Needed And Tool Used
        #------------------------------

        # ToolNeeded is the tool needed to activate the device, which can be
        # None (for example, a flashlight). ToolUsed is assumed to be None,
        # unless there's an indirect object in the list. This would only happen
        # where the player said "Light torch with..." or some such. If they just
        # said "light lamp" then ToolUsed remains None.

        ToolNeeded = self.RequiredDeactivationTool
        ToolUsed = None
        
        if len(P.IOL()) > 0:
            ToolUsed = P.IOL()[0]
        
        #----------------------------
        # If Tool Used But Not Needed
        #----------------------------

        # For example, if they tried to light the flashlight with a match...

        if ToolUsed and not ToolNeeded:
            return Complain("%s can't do that." % You())
        
        #----------------------------
        # If Tool Needed and Not Used
        #----------------------------

        # For example "light candle" instead of "light candle with match".

        if ToolNeeded and not ToolUsed:
            return Complain(self.RequiresToolDesc())
        
        #----------------------------
        # Complain If Wrong Tool Used
        #----------------------------

        # This test is a bit of elegant short-cutting. ToolNeeded will either
        # contain None or some object. If None then testing ToolNeeded returns
        # false. If ToolNeeded is any object, then testing ToolNeeded returns
        # true.
        #
        # You could also write the IF test this way:
        #
        # if ToolNeeded <> None and ToolNeeded <> ToolUsed:
        #
        # But I think this way is easier to read and understand.

        if ToolNeeded and ToolNeeded <> ToolUsed:
            return Complain(self.WrongToolDesc())
        
        #---------------------------------
        # Set Activation Property To FALSE
        #---------------------------------

        # The setattr() function lets you use a string to name the property you
        # want to set. This is exactly what we need to set any property we care
        # to put in the ActivationProperty property.

        setattr(self, self.ActivationProperty, FALSE)
        
        #-------------------
        # Stop Draining Life
        #-------------------
        
        StopDaemon(self.DrainLife)
        
        #--------------------------
        # Tell Player Unless Silent
        #--------------------------

        # If Silent is FALSE then tell the player the device activated.

        if not Silent: Say(self.DeactivateDesc(Multiple, Spontaneous))
        
        #---------------
        # Return Success
        #---------------

        return SUCCESS
    
    def ActivateDesc(self, Multiple=FALSE, Spontaneous=FALSE):
        """
        This method returns the description of the device activation, in
        either active (Spontaneous=TRUE) or passive (Spontaneous=FALSE) 
        voice.
        """

        if Spontaneous:
            return self.ActivateSpontaneousPhrase
        else:
            return self.ActivatePassivePhrase

    
    def AlreadyActivatedDesc(self):
        """
        Returns the already activated complaint. (The lamp is already on).
        """
        return SCase(self.AlreadyActivatedPhrase)
        
    
    def AlreadyDeactivatedDesc(self):
        """
        This method returns the already deactivated complaint (The pump
        isn't running!)
        """
        return SCase(self.AlreadyDeactivatedPhrase)
    
    def DeactivateDesc(self, Multiple=FALSE, Spontaneous=FALSE):
        """
        Returns the description of what happens when self is turned off.
        If Spontaneous is FALSE returns "The lamp goes out." or "You put
        the lamp out" if Spontaneous is true.
        """
        if Spontaneous:
            return SCase(self.DeactivateSpontaneousPhrase)
        else:
            return SCase(self.DeactivatePassivePhrase)

    
    def DrainLife(self):
        """
        This method reduces self's remaining life span by 1. When life
        reaches 0, the device automatically deactivates. Note we manually
        set the activation property to FALSE, and say the deactivation 
        property ourselves, rather than calling Deactivate() because we
        don't want to have to use the (possible) tool, which we might not
        have when the thing runs out of gas!
        """
        self.RemainingLifeSpan -= 1

        if not self.RemainingLifeSpan:
            setattr(self, self.ActivationProperty, FALSE)
            Say(self.DeactivateDesc())
   
    def LifeRemaining(self):
        """
        Most devices have a limited lifespan (number of turns) they can
        remain active before running out of fuel or power. Flashlights are a
        perfect example. This function returns the RemainingLifeSpan
        property by default, but a more complex device (such as a battery
        powered flashlight) could override (replace) this method with one
        that returned the RemainingLifeSpan property of the *batteries*
        (for example).
        """
        return self.RemainingLifeSpan

    
    def RequiresToolDesc(self):
        """
        Returns the complaint if you try to activate a device without the
        required tool. (You'll need something to do that with.)
        """
        return SCase("%s'll need something to do that with." % You())

    def WrongToolDesc(self,ToolUsed):
        """
        Returns the Wrong Tool complaint if you try to activate self with
        the wrong tool. (You can't do that with a crowbar.)
        """

        return "%s can't do that with %s." % (You(),ToolUsed.ADesc())

class ServiceContainIn:
    """
    This service allows any class to act as a container. Note you must still
    set the container's actual MaxBulk property, these services
    automatically set the MaxWeight property to 32000 (weight isn't usually
    an issue in containment).

    Most of the containment requirements are already met by ClassBasicThing,
    so adding this service to either ClassItem, ClassScenery, or their
    descendents only needs to change a couple of properties, everything
    else is already set properly for objects that contain other objects
    "inside" themselves.
    """

    def SetMyProperties(self):
        self.CantLookInside = FALSE
        self.IsOpen = TRUE
        self.MaxBulk = 1
        self.MaxWeight = 32000

class ServiceContainOn:
    """
    This service allows any class to act as a container. Note you must still
    set the container's actual MaxBulk property, these services
    automatically set the MaxWeight property to 32000 (weight isn't usually
    an issue in containment).

    Most of the containment requirements are already met by ClassBasicThing,
    so adding this service to either ClassItem, ClassScenery, or their
    descendents only needs to change a few properties, everything else is
    already set properly for objects that contain other objects "on"
    themselves.
    """

    def SetMyProperties(self):
        self.MaxBulk = 1
        self.MaxWeight = 32000
        self.IsOpen = TRUE
        self.IsTransparent = TRUE
        self.ContainerPrepositionDynamic = "on"
        self.ContainerPrepositionStatic = "on"

class ServiceContainUnder:
    """
    This service allows any class to act as a container. Note you must still
    set the container's actual MaxBulk property, these services
    automatically set the MaxWeight property to 32000 (weight isn't usually
    an issue in containment).

    Most of the containment requirements are already met by ClassBasicThing,
    so adding this service to either ClassItem, ClassScenery, or their
    descendents only needs to change a few properties, everything else is
    already set properly for objects that contain other objects "under"
    themselves. This service is also usually combined with
    ServiceRevealWhenTaken.
    """
    
    def SetMyProperties(self):
        self.MaxBulk = 1
        self.MaxWeight = 32000
        self.IsOpen = TRUE
        self.ContainerPrepositionDynamic = "under"
        self.ContainerPrepositionStatic = "under"


class ServiceContainBehind:
    """
    This service allows any class to act as a container. Note you must still
    set the container's actual MaxBulk property, these services
    automatically set the MaxWeight property to 32000 (weight isn't usually
    an issue in containment).

    Most of the containment requirements are already met by ClassBasicThing,
    so adding this service to either ClassItem, ClassScenery, or their 
    descendents only needs to change a few properties, everything else is
    already set properly for objects that contain other objects "behind"
    themselves. This service is also usually combined with
    ServiceRevealWhenTaken.
    """
    
    def SetMyProperties(self):
        self.MaxBulk = 1
        self.MaxWeight = 32000
        self.IsOpen = TRUE
        self.ContainerPrepositionDynamic = "behind"
        self.ContainerPrepositionStatic = "behind"

class ServiceDictDescription:
    """
    This service replaces the "sensory" description methods with ones that
    read their description from the Descriptions dictionary. This service
    makes it easier to define the long, odor, sound, taste and touch
    descriptions. This service may be used by BasicThings and Rooms as
    desired.
    """

    def SetMyProperties(self):
        """Sets service properties"""
        self.Descriptions = {
                            "HereDesc": "There is {Self().ADesc()} here.",
                            "LDesc": """
                                     {SCase(Self().PronounDesc())} looks
                                     like an ordinary {Self().NamePhrase} to
                                     {Me()}.
                                     """,
                            "OdorDesc": """
                                        {SCase(Self().PronounDesc())} smells
                                        like an ordinary {Self().NamePhrase}
                                        to {Me()}.
                                        """,
                            "SoundDesc": """
                                         {SCase(Self().TheDesc())} isn't
                                         making any noise.
                                         """,
                            "ReadDesc":  "{You()} can't read {self().ADesc()}.",
                            "TasteDesc": """
                                         {SCase(Self().PronounDesc())}
                                         tastes like an ordinary
                                         {Self().NamePhrase} to {Me()}.
                                         """,
                            "FeelDesc": """
                                        {SCase(Self().PronounDesc())} feels
                                        like an ordinary {Self().NamePhrase}
                                        to {Me()}.
                                        """,
                            "GroundDesc": "The ground looks completely ordinary to {Me()}.",
                            "SkyDesc": "The sky looks completely ordinary to {Me()}.",
                            "TakeDesc": "{You()} can't take that!}",
                            "WallDesc": "The wall looks completely ordinary to {Me()}."
                            }

    def LDesc(self):
        """
        Returns long description.
        """
        return self.Descriptions["LDesc"]

    def OdorDesc(self):
        """
        Returns odor description.
        """
        return self.Descriptions["OdorDesc"]

    def ReadDesc(self):
        """
        Returns read description. (Any written text on object).
        """
        return self.Descriptions["ReadDesc"]

    def SoundDesc(self):
        """
        Returns sound description.
        """
        return self.Descriptions["SoundDesc"]

    def TasteDesc(self):
        """
        Returns taste description.
        """
        return self.Descriptions["TasteDesc"]
        
    def FeelDesc(self):
        """
        Returns touch description.
        """
        return self.Descriptions["FeelDesc"]
        
    def GroundDesc(self):
        """
        Returns ground/floor description.
        """
        return self.Descriptions["GroundDesc"]
        
    def SD(self,Key,Value):
        """SD is just a short synonym for SetDesc()."""
        self.SetDesc(Key,Value)

    def SetDesc(self,Key,Value):
        """
        This function takes the key, adds "Desc" to it, and uses that to put
        Value in the Descriptions dictionary. For example:
        
        Rock.SetDesc("L","It looks like an ordinary rock.")

        would create a key of LDesc (L + Desc) and place "It looks like an
        ordinary rock" in the descriptions dictionary. This is a shortcut
        for the longer (but functionally identical:
    
        Rock.Descriptions["LDesc"] = "It looks like an ordinary rock".
    
        Note the string.join(string.split(Value)). This reduces all white
        spaces to 1 space. For example, many triple quoted strings are 
        "formatted" in the source code using multiple spaces. The
        join/split combination changes multiple spaces into a single space,
        this *seriously* reduces memory requirements!
        """

        self.Descriptions[Key + "Desc"] = string.join(string.split(Value))

    def SkyDesc(self):
        """
        Returns sky/ceiling description.
        """
        return self.Descriptions["SkyDesc"]
        
    def WallDesc(self):
        """
        Returns Wall description.
        """

        return self.Descriptions["WallDesc"]

        
class ServiceFollow:
    """
    This service allows things to follow the player.
    """

    def SetMyProperties(self):
        """Sets service properties"""

        self.Follow = FALSE

    def FollowPlayer(self):
        """
        If the Follow property is true, set this item's location to the 
        player's location.
        """
        
        if self.Follow: self.MoveInto(Global.Player.Where())

class ServiceOpenable:
    """
    This service allows things to be opened and closed.
    """

    def SetMyProperties(self):
        """Sets service properties"""
        pass

    
    def AlreadyClosedDesc(self):
        """
        This method is called when the player tries to close an object
        that's already closed. It says something like "The door is already
        closed."
        """

        return SCase("%s %s already closed." % (self.TheDesc(), Be(self)))

    
    def AlreadyOpenDesc(self):
        """
        This method is called if the player tries to open an object that's
        already open. It says "The door is already open." or whatever.
        """
        
        return SCase("%s %s already open." % (self.TheDesc(), Be(self)))
    
    def Close(self, Multiple=FALSE, Silent=FALSE, Spontaneous=FALSE):
        """
        This method is called by the CloseVerb object when the player
        attempts to close an object.
    
        If self isn't openable the method complains, if it's already open
        the method complains, and if we don't want the closing to be silent
        we print the close description. Then we set self's IsOpen property
        to false and return SUCCESS.

        The Spontaneous argument should be FALSE when the character closes
        the door directly, and TRUE if the character pushes a button or
        something that closes the object.
        """

        if not self.IsOpenable: return Complain(self.UnopenableDesc())
        if not self.IsOpen: return Complain(self.AlreadyClosedDesc())
        if not Silent: Say(self.CloseDesc(Multiple, Spontaneous))
        self.IsOpen = FALSE

        return SUCCESS
    def CloseDesc(self, Multiple=FALSE, Spontaneous=FALSE):
        """
        The description printed when the player closes the object. Multiple
        will almost certainly be false. If Spontaneous is FALSE the
        description will be "The door closes.". This would be used in cases
        where the object isn't directly closed by the actor.

        When Spontaneous is TRUE the description is "You close the door"
        (or whatever it is the player closed).
        """

        if not Spontaneous:
            return SCase(self.TheDesc())+ " " + Agree("close", self)
        else:
            return SCase("%s %s %s." % (You(), Agree("close"), self.TheDesc()))


    
    def Open(self, Multiple=FALSE, Silent=FALSE, Spontaneous=FALSE):
        """
        This method is called when an object is opened. Silent is true if
        you don't want to say anything when the object opens, Spontaneous
        means the player didn't directly open the object.

        Only show the opening description if the Silent parameter is FALSE.
        (Setting Silent to TRUE is useful, for example, in opening a door:
        the Open command is passed to both sides of the door in both rooms,
        but you don't want to see two messages.)

        The method will complain if the object isn't openable or if it's
        already open. If Silent is FALSE then we call OpenDesc() to say
        something like "You open the door."
        """

        if not self.IsOpenable: return Complain(self.UnopenableDesc())
        if self.IsOpen: return Complain(self.AlreadyOpenDesc())
        if not Silent: Say(self.OpenDesc(Multiple, Spontaneous))

        self.IsOpen = TRUE

        return SUCCESS
    
    def OpenDesc(self, Multiple=FALSE, Spontaneous=FALSE):
        """
        This method is called to describe the object opening. If
        Spontaneous is TRUE it returns "You open the door." (or whatever).
        If Spontaneous is FALSE it says "The door opens."
        """
        
        if not Spontaneous:
            return SCase(self.TheDesc())+ " " + Agree("open", self)
        else:
            return SCase("%s %s %s." %
                         (You(), Agree("open"), self.TheDesc()))


    
    def UnopenableDesc(self):
        """
        This method is called by Open() and Close() when the object being
        opened isn't openable, say for example a rock or a tree.
        """

        return SCase("%s can't %s %s." % (You(),
                                          self.TheDesc(),
                                          P.CVN()))



class ServiceLockable(ServiceOpenable):
    """
    This service allows things to be opened and closed and locked. Note
    this is the rare exception to the rule that services never inherit, in
    this case the lockable service is merely an extension of the openable 
    service.
    """

    def SetMyProperties(self):
        """Sets service properties"""
        self.IsLocked = FALSE
        self.LocksWithoutKey = TRUE
    
    def AlreadyLockedDesc(self):
        """
        This method is called when the object being unlocked is already
        unlocked.
        """

        return SCase("%s %s already locked." % (self.TheDesc(), Be(self)))

    def AlreadyUnlockedDesc(self):
        """
        This method is called when the object being unlocked is already
        unlocked.
        """
        return SCase("%s %s already unlocked." % (self.TheDesc(), Be(self)))

    
    def Lock(self, key=None, Silent=FALSE, Spontaneous=FALSE):
        """
        This method is called to lock an object. It complains if the object
        is already locked, or if it needs a key and none was provided or the
        wrong key was provided.
    
        If Silent is FALSE a description of the object being locked is said
        and the IsLocked property is set to TRUE.
        """

        if self.IsLocked: return Complain(self.AlreadyLockedDesc())

        if not self.LocksWithoutKey and not key:
            return Complain(self.NeedAKeyDesc())

        if not self.LocksWithoutKey and key <> self.Key:
            return Complain(self.WrongKeyDesc(key))

        if not Silent: Say(self.LockDesc(Spontaneous))

        self.IsLocked = TRUE

        return TURN_CONTINUES
    
    def LockDesc(self, Spontaneous=FALSE):
        """
        This description is called when the object is locked. It says either
        "The door locks." or "You lock the door." depending on whether
         Spontaneous was FALSE or not.
        """
        if not Spontaneous:
            return SCase(self.TheDesc())+ " " + Agree("lock", self) + "."
        else:
            return SCase("%s %s %s." % (You(), Agree("lock"), self.TheDesc())) + "."

    
    def NeedAKeyDesc(self):
        """
        This method is called when the object being locked/unlocked needs
        a key and no key was given.
        """
        return SCase("%s %s some kind of key to do that." %
                     (You(), Agree("need")))

    
    def Unlock(self,key=None,Multiple=FALSE, Silent=FALSE,Spontaneous=FALSE):
        """
        This method is called to unlock an object. It complains if the
        object is already unlocked, or if it needs a key and none was
        provided or the wrong key was provided.

        If Silent is FALSE a description of the object being unlocked is 
        said and the IsLocked property is set to FALSE.
        """

        if not self.IsLocked: return Complain(self.AlreadyUnlockedDesc())

        if not key and not self.UnlocksWithoutKey:
            return Complain(self.NeedAKeyDesc())

        if key <> self.Key and not self.UnlocksWithoutKey:
            return Complain(self.WrongKeyDesc(key))

        if not Silent:
            Say(self.UnlockDesc(Spontaneous))

        self.IsLocked = FALSE

        return TURN_CONTINUES
    
    def UnlockDesc(self, Multiple=FALSE, Spontaneous=FALSE):
        """
        This description is called when the object is locked. It says
        either "The door unlocks." or "You unlock the door." depending on
        whether Spontaneous was True or not.
        """
        if not Spontaneous:
            return SCase(self.TheDesc())+ " " + Agree("unlock", self) + "."
        else:
            return SCase("%s %s %s." %
                         (You(), Agree("unlock"), self.TheDesc()))
    
    def WrongKeyDesc(self, key):
        """
        Called when the wrong key is used to lock/unlock objects that needs
        a specific key. It returns "This key doesn't work with the door."
        """

        return SCase("This %s doesn't work with %s." %
                     (key.NamePhrase, self.TheDesc())) + "."



class ServiceRevealWhenTaken:
    """
    If you take a rock, the things that are hiding under/behind the rock
    should normally be left behind.  This service overrides the usual Take
    method of ServiceTakeableThing so that the contents of the hider will
    be moved to the hider's old location.

    Note this service only makes sense when used with objects that store
    their contents behind or under, rather than in or on top. After all,
    it would defeat the purpose of a box to have it dump its contents on
    the ground when taken!
    """

    def Take(self):
        """
        Reveal items when self is taken.
        """

        #------------------
        # Save Old Location
        #------------------

        # self's current location is where we want to return any items hidden by
        # self.

        OldLocation = self.Location
        
        #------------------------------
        # Fail If Actor Can't Take Self
        #------------------------------

        if not P.CA().Enter(self): return FAILURE
        
        #----------------------------
        # Succeed If No Hidden Things
        #----------------------------
        
        # Desc contains self's normal take description (usually "Taken").
        # HiddenThings contains self.Contents, a list of all objects contained
        # by self.
        #
        # If there are no hidden things we say Desc and return SUCCESS, which of
        # course ends the method immediately.
        #
        # A note about the IF test. The syntax "if not HiddenThings:" is exactly
        # the same as saying if len(HiddenThings) == 0:" but it's a lot more
        # like English!

        Desc = self.TakeDesc()
        HiddenThings = self.Contents

        if not HiddenThings:
            Say(Desc)
            return SUCCESS

        #------------------------
        # Describe Revealed Items
        #------------------------

        Desc += " " + self.LookDeepDesc()
        Say(Desc)

        #-----------------------------------------
        # Move Hidden Items to Self's Old Location
        #-----------------------------------------

        for Thing in HiddenThings: Thing.MoveInto(OldLocation)

        #---------------
        # Return Success
        #---------------

        return SUCCESS

class ServiceTakeableItem:
    """
    This service allows an item to be taken. Notice it uses the ENTER
    method, so the BasicThing ENTER method has to be satisfied as well.
    """

    def SetMyProperties(self):
        """Sets service properties"""
        pass

    def Drop(self,Multiple=FALSE):
        """
        Drop self into current actor's location. This is the method called
        by the Drop verb.
        """

        #---------------------
        # Actor Carrying Self?
        #---------------------

        # If the actor isn't carrying Self, then complain. Remember Complain
        # returns FAILURE, so when you return a Complain() function, you are
        # returning FAILURE.

        if not self in P.CA().Contents:
            return Complain(self.NotCarryingDesc())

        #-----------------------
        # Will Room accept item?
        #-----------------------
        
        # Notice we're letting the room decide whether the object can enter or
        # not, which means (in a normal room) it will check to see if there's
        # enough bulk and weight left. If so, we say the DropDesc property, if
        # not we let the room do the complaining.

        if P.CA().Where().Enter(self):
            Say(self.DropDesc(Multiple) + " ~n")

    def DropDesc(self,Multiple=FALSE):
        """
        This function returns either "Dropped" (if the object is the only 
        one currently being dropped) or "Rock: Dropped" if this object is
        one of many objects being dropped at the same time.
        """

        ReturnValue = ""

        #----------------------------
        # Part of multiple item drop?
        #----------------------------

        # If Mutiple is true the actor is dropping multiple objects so we have
        # to prepend the Short Description the object uses when part of a
        # multiple object description.

        if Multiple: ReturnValue = self.MultiSDesc()+": "

        #---------------
        # Return Message
        #---------------

        return ReturnValue + "Dropped."
    
    def NotCarryingDesc(self):
        """
        This is the message returned when the player tries to drop something
        they aren't carrying. It says "You aren't carrying that." or "Fred
        isn't carrying that."
        """

        #--------------
        # Set Complaint
        #--------------

        # The code below says Complaint is going to be equal to the string with
        # the two %s's replaced by You() and Be(). You() is the word that's
        # appropriate for the "you" part of "You aren't carrying that". Be() is 
        # the word for "is" or "are".

        Complaint = "%s %sn't carrying that." % (You(), Be())

        return SCase(Complaint)
    
    def Take(self,Multiple=FALSE):
        """
        This is the method invoked by the Take command. It basically says if
        self can enter the current actor then say the take description. If
        it can't, the Enter() method of the actor takes care of any
        complaints.
        """

        if self in P.CA().Contents:
            Say("{SCase(You())}{Be(Contract=TRUE)} already carrying it.")
            return

        if P.CA().Enter(self):
            Say(self.TakeDesc(Multiple))

    
    def TakeDesc(self,Multiple=FALSE):
        """
        Like the DropDesc method, the TakeDesc method returns either "Taken"
        or "Rock: Taken".
        """

        ReturnValue = ""

        if hasattr(self,"Descriptions"):
            ReturnValue = self.Descriptions["TakeDesc"]
        else:
            ReturnValue = "Taken."

        if Multiple: ReturnValue = self.MultiSDesc()+": "

        return ReturnValue

class ServiceFixedItem:
    """
    This service prevents an item from being taken. It complains
    appropriately if the player tries to take or drop self.
    """

    def SetMyProperties(self):
        """Sets service properties"""
        pass

    
    def Drop(self,Multiple=FALSE):
        """
        Complain with drop description. This is the method called by the
        Drop verb.
        """

        return Complain(self.DropDesc())
    
    def DropDesc(self):
        """Drop complaint"""

        Complaint = "%s %sn't carrying that!" % (You(), Be())

        if hasattr(self,"Descriptions"):
            Complaint = self.Descriptions["DropDesc"]

        return Complaint

    def Take(self,Multiple=FALSE):
        """Take self by complaining you can't."""

        Complain(self.TakeDesc())

    def TakeDesc(self,Multiple=FALSE):
        """Take complaint"""

        Complaint = "%s can't take that!" % You()

        if hasattr(self,"Descriptions"):
            Complaint = self.Descriptions["TakeDesc"]

        return SCase(Complaint)

#********************************************************************************
#                    U N I V E R S E   B A S I C  C L A S S E S
#
C="""
  There are only a handful of major classes, all objects are made from
  these. Where additional functionality is required we use SERVICES to
  augment the basic classes. This is a deliberate design decision, to 
  leverage the maximum utility from the minimum of code.
  """

class ClassGameObject(ClassFundamental):
    """
    This object lets us set all the properties for the game itself (author,
    version, copyright, etc).
    """
    
    def __init__(self):
        """ Initialize game specific info"""
        self.SetMyProperties()
    
    def SetMyProperties(self):
        """Set Object Properties"""
        
        #------------
        # Game Author
        #------------

        # This property holds your name. It's usually set in your replacement
        # Engine.UserInit() or Engine.UserPreInit() function. By default this
        # property is said as part of the game banner.

        self.Author = "Put your name here"
        
        #----------
        # Copyright
        #----------

        # This property hold your copyright, for instance: "1998-2001"

        self.Copyright = "Your copyright here"
        
        #------------------
        # Game Introduction
        #------------------

        # The game introduction text can be quite long, just look at Thief's
        # Quest (the sample game that comes with Universe). It says after the
        # banner and gives the player an introduction to the game. Who they are,
        # what they're doing in the game, etc.

        self.IntroText = "Your Game's Introductory Text Goes Here"
        
        #----------
        # Game Name
        #----------

        # This is the name of your game, as it will appear to the player. By
        # default it appears as the first text said on the screen once
        # your game is run.

        self.Name = "Your Game's Name Goes Here"
        
        #-------------
        # Game Version
        #-------------

        # The version of your name, you should include only the number, such
        # as "1.0" since the game banner automatically says the word
        # Version.

        self.Version = "1.0"
    
        #---------------
        # Game Help Text
        #---------------
        
        self.HelpText = "Sorry, you're on your own for this one!"
        
    def Banner(self):
        """
        By default this text is said at the beginning of your game. Don't
        alter this property unless you make sure you include the 
        UniverseBanner property in it, that's a copyright requirement!
    
        It's unlikly you'll need to alter the game banner anyway.
        """

        Text = "~title %s ~l version %s ~n Copyright (c) %s by %s ~n "

        Text = Text % (self.Name,self.Version,self.Copyright,self.Author)
        Text = Text + UniverseBanner()

        return Text
    
    def PrintGameIntroduction(self):
        """
        This function says the game introduction, including the banners for
        the game and Universe.
        """
       
        #--------------------------
        # Abort Intro If Restarting
        #--------------------------

        # If the global restarting flag isn't nil then we simply return from the
        # function immediately, doing nothing.

        if Global.Restarting: return
        
        #---------------------
        # Say Introductory Text
        #----------------------

        # Notice that all the introductory text is being said by the two lines
        # below. The game banner contains all the information about your name
        # that normally says at the start of a game, such as it's name, your
        # name and copyright, the Universe banner, and so forth.

        # The Game Intro contains all the other text you want to say just
        # before the first room's description. For example, in Thief's Quest
        # the game intro is a full screen of text!

        ClearScreen()
        Say(Game.Banner() + Game.IntroText)

        Global.Player.StartingLocation.Enter(Global.Player)

class ClassBasicThing(ClassBaseObject):
    """
    ClassBasicThing is the root for all "real" objects (like a rock), or
    rooms. It is descended from ClassBaseObject. Basic Things have some
    fundamental attributes such as weight and bulk, the ability to provide
    basic descriptions of themselves (such as an ldesc, sdesc, adesc, etc.)

    In addition, certain fundamental functions (like checking for light) are
    also supplied here. In short, if an ability is required by *ALL* objects
    you'll likely find it here.
    In the examples we're going to use two objects, a rock for physical
    objects, and a forest for room objects. (It's much easier to talk about
    "a rock" than "an object", right?)
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        
        #---------------------------
        # Append To All Objects list
        #---------------------------

        # Now we've done everything our ancestor did, it's time to ALSO append
        # this object to a list of all Thing objects. The AllObjectsList must
        # contain all "thing" objects, but it doesn't contain verb objects.

        Global.AllObjectsList.append(self)
        
        #--------
        # Article
        #--------

        # This is the indefinite article used with the object. In English there
        # are two articles, "a", or "an", depending on the word the article is
        # describing. You have to be careful when choosing the correct article,
        # make sure it agrees with the object's short description. Adjectives
        # are a problem here.
        #
        # For example, it's "AN umbrella", but also "A red umbrella". By default
        # basic things use 'a' as their article. To decide which article to use
        # try saying "a", followed by the short description. If it sounds ok,
        # then use "a", otherwise use "an".

        self.Article = "a"
        
        #-----
        # Bulk
        #-----

        # Bulk is measured in completely arbitrary units--there is no equivalent
        # unit of measurement in the real world. The closest concept comes from 
        # the world of RPG's--"encumberance".
        #
        # The idea of bulk is how hard something is to carry. A pound of
        # feathers only weighs a pound but it's awkwardness makes up for that.
        # So we measure an item's weight AND it's bulk.

        self.Bulk = 0
        
        #-------------------------------
        # Can't Look Behind/Inside/Under
        #-------------------------------

        # These defaults assume a solid object that can be moved (like a rock)
        # that isn't openable. Change them appropriately if you need to.

        self.CantLookBehind = FALSE
        self.CantLookInside = TRUE
        self.CantLookUnder  = FALSE
        self.CantLookOn     = FALSE
        
        #---------
        # Contents
        #---------

        # This list contains every object the room (or container) contains.

        self.Contents = []
        
        #--------------------------------
        # Container Preposition (dynamic)
        #--------------------------------

        # Preposition used when putting object in/under/behind/on another object.
        # The "active" preposition.

        self.ContainerPrepositionDynamic = "inside"

        #-------------------------------
        # Container Preposition (static)
        #--------------------------------

        # Preposition used when describing how an object holds its contents.

        self.ContainerPrepositionStatic  = "inside"
        
        #--------------------
        # Format Descriptions
        #--------------------

        # These are the parts of speech that say "is/are" or "do/does" when
        # dealing with objects generically. FormatYou being blank makes the
        # Agree() function (and its siblings) consider this
        # object singular by default (which is generally correct).

        self.FormatYou = ""
        
        #-----------
        # Has Ground
        #-----------

        # True only for rooms, used to handle commands like "Examine Ground" in
        # a fairly automatic way.

        self.HasGround = FALSE
        
        #----------------------
        # Has Floating Location
        #----------------------

        # If true then this object can change its location when another object
        # does. Currently this functionality is only implemented for the "me" 
        # object and ClassLandmark objects.

        self.HasFloatingLocation = FALSE
        
        #--------
        # Has Sky
        #--------

        # Only true for room objects, lets the room deal with the sky/ceiling
        # in a fairly automatic way.

        self.HasSky = FALSE
        
        #----------
        # Has Wall
        #----------

        # True only for rooms, used to handle commands like "Examine Wall" in
        # a fairly automatic way.

        self.HasWall = FALSE
        
        #-----------
        # Is Active?
        #-----------

        # True if device is activated, valuse if not.

        self.IsActivated = FALSE
        
        #----------
        # Is Actor?
        #----------

        # Is this object an actor? Determines whether or not this object is
        # placed in the Global.ActorList.

        self.IsActor = FALSE
        
        #-------------
        # Blatant Odor
        #-------------

        # By default this value is FALSE, set it to TRUE if the odor of the
        # object is so intrusive it should always be noticed, this is used by
        # the SmartDescribeSelf method to see if the odor should be included as
        # part of the description or not.

        self.IsBlatantOdor = FALSE
        
        #--------------
        # Blatant Sound
        #--------------

        # By default this value is nil, set it to true if the sound the object
        # makes is so intrusive it should always be noticed, this is used by the
        # SmartDescribeSelf method to see if the sound should be included as
        # part of the description or not.

        self.IsBlatantSound = FALSE
        
        #-------
        # Broken
        #-------

        # This property should return TRUE or FALSE, it's intended to handle
        # breakable objects--a mirror, for instance.

        self.IsBroken = FALSE
        
        #-----------------
        # Is Object Female
        #-----------------

        # To properly handle pronouns the parser has to know if an object is
        # male, female, or neuter. Setting IsHer lets the parser know that
        # "her" is the appropriate pronoun for this object. Note if you have
        # an androgynous object you can set both IsHer and IsHim true!

        # If neither IsHim or IsHer is set to true the parser will use "it"
        # as the object's pronoun.

        self.IsHer = FALSE
        self.IsHim = FALSE
        
        #-----------------
        # Is Light Source?
        #-----------------

        # True if this object is capable of producing light. More to the point,
        # any object with a true IsLightSource will be included in the
        # Global.LightSourceList.

        self.IsLightSource = FALSE
         
        #-----------
        # Is Liquid?
        #-----------

        # Returns true if the object is liquid, false if not.

        self.IsLiquid = FALSE
        
        #-------
        # IsLit?
        #-------

        # Returns true if the object is *ACTUALLY* producing light at the moment,
        # false if not.

        self.IsLit = FALSE
        
        #-------------------------------------
        # Is Object Referred to in the plural?
        #-------------------------------------

        self.IsPlural = FALSE
        
        #-----
        # Open
        #-----

        # Return true if the object is open, false if it is closed or open isn't
        # applicable.

        self.IsOpen = FALSE
        
        #---------
        # Openable
        #---------

        # By default most objects are not openable.

        self.IsOpenable = FALSE
        
        #----------
        # Poisonous
        #----------

        # Returns true if the object is poisonous if eaten, drunk, or (in the
        # case of actors) bitten by.

        self.IsPoisonous = FALSE
        
        #--------
        # Potable
        #--------

        # Returns true if this is a foodstuff or (if liquid) a thirst quencher.

        self.IsPotable = FALSE
        
        #------------
        # Is Scenery?
        #------------

        # Scenery isn't described unless you examine it explicitly.

        self.IsScenery = FALSE
        
        #------------
        # Transparent
        #------------

        # Returns true if the object is transparent (will pass vision), false if
        # not.

        self.IsTransparent = FALSE
        
        #---------
        # Location
        #---------

        # Location is a property. It holds self's parent. A parent is merely
        # the object that contains self. Note rooms don't ordinarily have a
        # Location, but everything else does.
        #
        # Also note you should use the Where() method to get an object's
        # location, since floating objects don't use a Location property (it's
        # always set None, Where() will return the object's "true" location.
        #
        # To set an object's location always use the MoveInto() method instead
        # of setting the location variable directly. This is required because
        # you also have to set the LOCATION'S CONTENTS property!

        self.Location = None
        
        #-------------
        # Maximum Bulk
        #-------------

        # This is the maximum number of "bulk units" the object can contain.
        # The default is 0 (it can't contain anything).

        self.MaxBulk = 0
        
        #---------------
        # Maximum Weight
        #---------------

        # The maximum amount of weight an object can "carry". Notice that we
        # make a distinction between "carry" and "contain". A container can
        # contain maxbulk units, but any amount of weight. An actor, however,
        # has both a maximum bulk AND a maximum weight they can "contain".

        self.MaxWeight = 0
        
        #--------------
        # Object Memory
        #--------------

        # This list contains all objects this object has encountered. It is
        # used with the MEMORIZE() and REMEMBERS() functions to determine what
        # objects this particular object has encountered before.
        #
        # You may have guessed this is part of an actor's "memory", to
        # determine what an actor knows or doesn't know. It's placed here so
        # that any object can be "read" for objects it has encountred or
        # knows about.

        self.Memory = []

        #--------------
        # Parser Favors
        #--------------
        
        # Mark this property TRUE only for objects that will appear in the same
        # room, when you want one object to be always used and the other 
        # eliminated. This applies mainly to ClassLandmark objects, usually
        # walls when you want your wall to override the existing wall object.

        self.ParserFavors = FALSE
        
        #------------------
        # Starting Location
        #------------------

        # The starting location lets the author indicate where objects are
        # ORIGINALLY located, this value is used when the game restarts to
        # let the object be returned to its inital location. It's also used
        # by the SetUpGame method to put the object where it belongs in the
        # first place.

        self.StartingLocation = None
       
        #------
        # Value
        #------

        # The value of an object is generally what it adds to the score. For
        # a room the value is the number of points given for discovering it.

        self.Value = 0
        
        #-------
        # Weight
        #-------

        # The weight of an object. This is measured in arbitrary units (we
        # suggest 1 unit = 1/10 of a pound) but be consistant! For example
        # don't use a weight of 10 to mean 1 pound of nails but 10 tons of
        # explosives!

        self.Weight = 0
    
    def AllowedByVerbAsDObj(self):
        """
        This method is used by the SpecificDisambiguation() method as a test
        method when disambiguating direct objects. True if verb allows this
        object to be a direct object
        """
       
        #-------------------------------------
        # Verb's allowed object list is empty?
        #-------------------------------------

        # If the verb's allowed direct object list is empty, then the verb
        # allows all objects as direct objects.

        if len(P.CV().OnlyAllowedDObjList) == 0:
            return SUCCESS

        #----------------------
        # self on allowed list?
        #----------------------

        # If self is on the allowed list return success, otherwise failure.

        if self in P.CV().OnlyAllowedDObjList:
            return SUCCESS
        else:
            return FAILURE
    
    def AllowedByVerbAsIObj(self):
        """
        This method is used by the SpecificDisambiguation() method as a test
        method when disambiguating indirect objects. True if verb allows
        this object to be an indirect object
        """
        
        #-------------------------------------
        # Verb's allowed object list is empty?
        #-------------------------------------

        # If the verb's allowed indirect object list is empty, then the verb
        # allows all objects as indirect objects.

        if len(P.CV().OnlyAllowedIObjList) == 0: return SUCCESS

        #----------------------
        # self on allowed list?
        #----------------------

        # If self is on the allowed list return success, otherwise failure.

        if self in P.CV().OnlyAllowedIObjList:
            return SUCCESS
        else:
            return FAILURE


    
    def CheckActor(self):
        """
        The parser calls this method for the object the player addressed as
        an actor as part of the specific disambiguation of the command. If
        the object is NOT an actor, say an error message and return FAILURE.
        This will abort the player's command.
    
        If the object IS an actor (something that can be commanded, like a
        person or a robot or an animal that understands commands) simply
        return SUCCESS.
    
        By default all classes EXCEPT ClassActor and its descendants use
        this method to say "You are out of your mind" and return FAILURE.
        You may want to override this method to have a variety of snide
        comments for players who command the landscape to do things...
        """
        
        #----------
        # Is Actor?
        #----------

        # If this object is an actor, return success.

        if self.IsActor: return SUCCESS

        #-----------
        # NOT ACTOR!
        #-----------

        # This object isn't an actor, or we wouldn't have gotten this far.
        # Complain (which returns FAILURE).

        return Complain(P.AP().NotAnActor)
    
    def ContentBulk(self):
        """
        This method returns the total bulk of an object's contents BUT DOES
        NOT COUNT THE OBJECT's BULK!
        """

        TotalBulk = 0
        for Obj in self.Contents: TotalBulk = TotalBulk + Obj.CurrentBulk()
        return TotalBulk
    
    def ContentWeight(self):
        """
        Returns weight of self's contents EXCLUDING self.Weight.
        """

        TotalWeight = 0
        for Obj in self.Contents: TotalWeight = TotalWeight + Obj.CurrentWeight()
        return (TotalWeight)
    
    def CurrentBulk(self):
        """
        The CURRENT bulk of an object is the bulk of the object itself PLUS
        the bulk of its contents. Since we have a method that returns the
        contents bulk it becomes trival to return an object's current bulk.
    
        Consider a sack. Folded up neatly the sack may have a bulk of 1 or
        even 0. But as you put objects in the sack its bulk increases.

        This means you'll have to change the definition of this method for a
        container with rigid sides--a box always has the same bulk (not
        weight!) no matter what goes into it--unless the box is open and
        you allow stuff to stick out, in that case it's ok to use this
        method.
        """

        return self.Bulk + self.ContentBulk()

    
    def CurrentlyIlluminated(self):
        """
        CurrentlyIlluminated is related to IsLit, but is superior to that
        property because it also looks for Self in the Global.LitParentList.

        Primarily, it's intended for checking to see if light is present in
        rooms, but like everything else in Universe we made it as generic as
        we could.
        """

        return (self.IsLit or (self in Global.LitParentList))
    
    def CurrentWeight(self):
        """
        An object's current weight is the weight of the object itself plus
        the weight of its contents. Unless you're creating an anti-gravity
        device or bag of holding this method needn't be messed with, unlike
        the CurrentBulk method, which differs for rigid and expandable
        objects (boxes and sacks, for instance).
        """

        return self.Weight + self.ContentWeight()
    
    def DescribeSelf(self,DescriptionArgument="Long"):
        """
        The describe self method takes one argument, the type of description
        desired. Unlike the various "Desc" methods, this function actually
        says something (using Say()).
        """

        #-------------------------------
        # Translate Description Argument
        #-------------------------------

        # A short cut for the many IF tests below. UCDA stands for Upper Case
        # Description Argument. We translate it to upper case so that the game
        # author (you) has a safety margin for spelling arguments in any case
        # preferred.

        UCDA=string.upper(DescriptionArgument)

        #----------------------------
        # Say Appropriate Description
        #----------------------------

        if UCDA == "SMART":  self.SmartDescribeSelf();return
        if UCDA == "SHORT":  Say(self.SDesc());return
        if UCDA == "LONG":   Say(self.LDesc());return
        if UCDA == "A":      Say(self.ADesc());return
        if UCDA == "THE":    Say(self.TheDesc());return
        if UCDA == "HELLO":  Say(self.HelloDesc());return
        if UCDA == "HERE":   Say(self.HereDesc());return
        if UCDA == "CONTENT":Say(self.ContentDesc());return
        if UCDA == "NAME":   Say(self.NamePhrase);return
        if UCDA == "ADJ":    Say(self.AdjectivePhrase);return
        if UCDA == "READ":   Say(self.ReadDesc());return
        if UCDA == "MULTISHORT": Say(self.MultiSDesc());return
        if UCDA == "PLURAL": Say(self.PluralDesc());return
        if UCDA == "SOUND":  Say(self.SoundDesc());return
        if UCDA == "ODOR":   Say(self.OdorDesc());return
        if UCDA == "TASTE":  Say(self.TasteDesc());return
        if UCDA == "FEEL":   Say(self.FeelDesc());return
        if UCDA == "TAKE":   Say(self.TakeDesc());return
        if UCDA == "DROP":   Say(self.DropDesc());return
   
    #-------------
    # Enter Object
    #-------------

     
    def Enter(self,Object):
        """
        This method implements the ability for one object to enter another.
        If entry is forbidden, then the method complains, returns false, and
        does not move the object.
    
        By default this method returns true when:

        A) Self is an actor and Obj.Bulk+self.ContentBulk<=self.MaxBulk AND
           Obj.Weight+self.ContentWeight<=self.MaxWeight.
    
        B) Self is not an actor and Obj.Bulk+self.ContentBulk<=self.MaxBulk.
    
        In other words, an actor has to be able to *LIFT* the object as well
        as have room to carry it.
        """
       
        #--------------
        # Self is Open?
        #--------------

        # If Self isn't open and not openable, then obviously you won't be able
        # to put the object into self.

        if not self.IsOpen and not self.IsOpenable:
            Complaint = You() + " can't fit " + \
                        Object.TheDesc() + " into " + self.TheDesc() + "."
            return Complain(SCase(Complaint))
        
        #--------------
        # Self is Open?
        #--------------

        # If self isn't open but can be opened, you can't put an object in it
        # either, but you should give a different complaint. Notice we're using
        # the "self.TheDesc" to replace the more cumbersome 
        # "DescribeSelf('THE')"

        if not self.IsOpen and self.IsOpenable:
            Complaint = SCase(self.TheDesc() + " is closed.")
            return Complain(Complaint)
        
        #--------------------------
        # Is Object too big to fit?
        #--------------------------

        if Object.Bulk + self.ContentBulk() > self.MaxBulk:
            Complaint = Object.TheDesc() + " won't fit."
            return Complain(Complaint)
        
        #------------
        # Move Object
        #------------

        # We've passed the tests, now it's time to actually move the object into
        # self. Note when you move an object into another ALWAYS use the
        # object's MoveInto method, it takes care of all the messy details. See
        # the MoveInto method definition to see how hard moving an object really
        # is!

        Object.MoveInto(self);

        return SUCCESS
    
    def Favored(self):
        """
        This method returns the ParserFavors property. This is used as the
        final step in the disambiguation process. It works like this. If,
        after all other disambiguation occurs, there are still multiple
        objects the parser checks to see if one or more are favored
        (self.Favored is TRUE).

        If so it keeps only favored objects, eliminating unfavored ones. If
        no objects in the final list are favored, then nothing happens and
        all unfavored objects are kept.
        """

        return self.ParserFavors


    
    def Insert(self, Object, Multiple=FALSE, Silent=FALSE, Spontaneous=FALSE):
        """
        Method called by InsertVerb objects to put self (Rock) into another
        object (Box).
        """
        
        #-------------------------
        # Get Expected Preposition
        #-------------------------

        Preposition = self.VerbPreposition()
        
        #-----------------------------------
        # Complain If Wrong Preposition Used
        #-----------------------------------

        if Preposition <> Object.ContainerPrepositionDynamic:
            return Complain(self.WrongPrepositionDesc(Object,Spontaneous))
        
        #----------------------
        # Fail if Enter() fails
        #----------------------

        if not Object.Enter(self): return FAILURE
                
        #-------------------------------------
        # Say Insert Description Unless Silent
        #-------------------------------------

        if not Silent: Say(self.InsertedDesc(Object, Spontaneous))
        
        #---------------
        # Return Success
        #---------------

        return SUCCESS
    

    def IsReachable(self,Object):
        """
        This method answers the question "Does the object passed to me have
        an unobstructed path to reach me?" To return true both objects must
        share the same ParentOpen().
    
        An unobstructed path exists for an object (either obj or self) when
        they are directly contained by the ParentRoom, or every container
        between them is open.
    
        For instance, let's take an example. The player comes upon a gem
        inside a (closed but transparent) bottle inside an (open) box in the
        forest. If we call Gem.IsReachable(Me) would it return true?
    
        No, it wouldn't. Player.ParentOpen() is Forest, but Gem.ParentOpen()
        is bottle, they do not match. If the bottle were open, 
        Gem.ParentOpen() would be Forest, and an unobstructed path would
        exist.

        Note that an unobstructed path can exist in the dark (compare
        IsVisible below).
        """

        #----------------------
        # Get Reachable Parents
        #----------------------

        # Get the REACHABLE parents of both Self and the passed objects.

        SelfParent = self.ParentReachable()
        ObjectParent  = Object.ParentReachable()

        #--------------------
        # Valid and the same?
        #--------------------
        
        # The IF test below is somewhat bizarre. You might think a simple
        # SelfParent = ObjectParent would work--and it would except for one
        # thing. The ParentReachable() method can return None.
        #
        # So? you ask. They won't match if one returns None, so what's the
        # problem?
        #
        # But what if they BOTH return None? That means NEITHER Self nor
        # Object has a reachable parent, which means they obviously can't
        # reach each other!
        #
        # It's a simple enough trick. In order to succeed all three parts
        # of the test have to be true. That means if either OR BOTH Self and
        # Object have no reachable parent (are, in effect, either a room or
        # have a nil location) the function will automatically fail.

        if SelfParent and ObjectParent and SelfParent == ObjectParent:
            return SUCCESS

        #-----
        # Fail
        #-----

        return FAILURE

    def IsVisible(self,Object):
        """
        This method answers the question "Can the object passed to me see
        me?" To return true both objects must share the same
        ParentVisible().

        A clear line of sight exists for an object (either obj or self) when
        they are directly contained by the parentroom, or every container
        between them is either open or transparent.
    
        For instance, let's take an example. The player comes upon a gem 
        inside a (closed but transparent) bottle inside an (open) box in the
        forest. If we call Gem.IsVisible(Me) would it return true?
    
        Yes it would. Player.ParentLit() is Forest, so is Gem.ParentLit().
        Forest is lit, the line of sight from gem goes through the bottle
        (it's closed but transparent) and through the box (since the box is
        open) to the Forest.
        """

        #--------------------
        # Get Visible Parents
        #--------------------

        # Get the VISIBLE parents of both Self and the passed objects.

        SelfParent = self.ParentVisible()
        ObjParent  = Object.ParentVisible()

        #--------------------
        # Valid and the same?
        #--------------------
        
        # The IF test below is somewhat bizarre. You might think a simple
        # SelfParent = ObjParent would work--and it would except for one thing.
        # The ParentVisible method can return None.
        #
        # So? you ask. They won't match if one returns None, so what's the
        # problem?
        #
        # But what if they BOTH return None? That means NEITHER Self nor Object
        # has a visible parent, which means they obviously can't see each other!
        #
        # It's a simple enough trick. In order to succeed all three parts
        # of the test have to be true. That means if either OR BOTH Self and
        # Object are in the dark the function will automatically fail.

        if SelfParent and ObjParent and SelfParent == ObjParent:
            return SUCCESS

        
        #------------------------------
        # Why Count Carried As visible?
        #------------------------------

        # You might wonder why we want to count objects the player is carrying as
        # visible. Think about it. If you were carrying something, a rock say, and
        # you wanted to drop it in a dark room you should be able to.
        #
        # If we didn't count carried objects as visible actions that would be 
        # reasonable would be forbidden because the object literally couldn't be
        # seen.

        if self in P.CA().Contents: return SUCCESS

        #-----
        # Fail
        #-----

        return FAILURE
    


    def Leave(self,Object):
        """
        Return SUCCESS if able to leave object, FAILURE if can't
        """
        
        return SUCCESS

    
    def LookDeep(self):
        """
        This function is called to print a message when a player looks
        behind, under, or inside an object. Usually it will return one of
        the following (whichever is appropriate):
    
        You don't see anything interesting under the rock.
        You don't see anything interesting behind the rock.
        It is impossible to look inside a rock.
    
        There are 3 properties which affect how the object responds either
        with disinterest or impossibility scolds). These are:

        self.CantLookInside (defaults to TRUE)
        self.CantLookUnder  (defaults to FALSE)
        self.CantLookBehind (defaults to FALSE)
        self.CantLookOn     (defaults to FALSE)
        """
        
        #----------------------------------------
        # Determine Appropriate CantLook Property
        #----------------------------------------
        
        # We need to pick which of the four CantLook properties to use
        # (CantLookInside, CantLookBehind, CantLookOn or CantLookUnder). The
        # first step is to call self.VerbPreposition() and place the result in
        # Attr. This method will either return the current verb's
        # ExpectedPreposition property or "inside" if the current verb doesn't
        # have an ExpectedPreposition property.
        #
        # self.VerbPreposition() is just a "shorthand" method. If you look at
        # the method you'll see it's really just two lines of
        # code. However, because we call it in lots of different places it's
        # easier and less confusing to make a method call rather than repeat
        # those two lines of code each time.
        #
        # Another advantage of using a method here instead of the actual code is
        # called ABSTRACTION. Abstraction allows us to put the details of
        # getting the verb's preposition in one place instead of several places.
        # If we later change our minds about how to get the verb's preposition
        # (perhaps adding additional code) we only have to do it one place
        # instead of half a dozen! This is a cornerstone of good programming
        # design. It saves you time, effort, and eliminates a particularly
        # frustrating kind of bug, caused by forgetting to change the code in
        # one place when you've changed it everywhere else.
        #
        # In other words, abstraction is all gain, and no pain!

        Attr = self.VerbPreposition()

        #-----------------------
        # Assemble property name
        #-----------------------

        # Attr contains either "inside" or "under" or "behind" (unless the
        # author screwed up the spelling when they created the verb of course!).
        #
        # This line changes "inside"/"behind"/"under" to "CantLookInside"/
        # "CantLookBehind"/"CantLookUnder"
        #
        # Notice the capitalization of the expected pronoun, it won't work
        # otherwise!

        Attr = "CantLook" + string.capitalize(Attr)
        
        #------------
        # Can't Look?
        #------------

        # Attr contains "CantLookInside", "CantLookBehind", or some other
        # appropriate CantLook property. So self.Get(Attr) is actually saying
        # something like:
        #
        # self.CantLookInside
        #
        # or whatever CantLook property is appropriate. If the CantLook
        # property is true, then we complain with the CantLookDesc()
        # method.

        if self.Get(Attr):
            return Complain(self.CantLookDesc())

        #----------------
        # Nothing to see?
        #----------------

        # If there are no items in the object, we just say there's nothing
        # interesting to see.

        if len(self.Contents) == 0:
            return Complain(self.DontSeeInterestingDesc())
        
        #-----------------------
        # Describe Deep Contents
        #-----------------------

        # If we've gotten this far there's something to see, so we
        # list it.

        Say(self.LookDeepDesc())

        return SUCCESS
   
    def MarkPronoun(self):
        """
        This method is generally called by the HereDesc() method, it records
        this object into the pronoun dictionary. There are 4 pronoun types,
        this routine only sets the singlular ones.
    
        If the object is male (IsHim) put self in the HIM slot, if IsHer put
        it in the HER slot, if neither put it in the IT slot. Notice this
        code DELIBERATELY written to handle cases where an object is BOTH
        male and female. This can be handy for actors who's gender is in
        question or not immediately known.
        """

        if self.IsHim: P.AP().PronounsDict[HIM] = self
        if self.IsHer: P.AP().PronounsDict[HER] = self
        if not self.IsHim and not self.IsHer: P.AP().PronounsDict[IT] = self
    
    def Memorize(self,Object):
        """
        This method lets Self memorize another object. It uses both the
        REMEMBER method and the MEMORY list property.
        """

        #------------------------
        # Do we already remember?
        #------------------------

        # If we already remember Object it's in MEMORY, so we do nothing except
        # return immediately.

        if self.Remembers(Object): return

        #------------
        # Memorize it
        #------------

        # Memorization is easy, we simply append OBJ to MEMORY. Notice we also
        # have the object memorize self. This allows us a reciprocal memory,
        # useful for disambiguation.

        self.Memory.append(Object)
        Object.Memorize(self)

        return
    
    def MoveInto(self,Container):
        """
        MoveInto Is used to move an object from one room (or container,
        they're very similar) into another. Note this is a "primative", it
        does nothing in the way of checking to see if the move is valid,
        that's up to the objects initiating the move.
        """

        #----------------------------
        # Is Self currently anywhere?
        #----------------------------
        
        # Ok, Self is the object we're moving into a container (could be a room,
        # could be a box, could be an actor...)
        #
        # However, self.Location (where self is currently) might be None--in
        # other words self isn't anywhere! (Don't laugh, None locations are not
        # only legal, they're handy for tucking stuff away so the player can't
        # stumble across it).
        #
        # if Self IS somewhere, it's in the Contents list of it's location--so
        # the first thing we do is remove it from its location's contents list.

        if self.Location <> None: self.Location.Contents.remove(self)

        #----------------------
        # Add Self to Container
        #----------------------

        # Next we add Self to the container's Content list--if Container isn't
        # None!

        if Container <> None: Container.Contents.append(self)

        #-----------------------------
        # Inform  Self of New Location
        #-----------------------------
        
        # Adding Self to the location's content list is only half the battle. By
        # doing so you tell the LOCATION it has a new object in it, but you
        # haven't told SELF it's in a new place!
        #
        # That's what the line of code below does.

        self.Location = Container

        return
   
    def ParentLit(self,SelfMustBeLit):
        """
        This method returns the outermost container that Self could
        illuminate if lit. If SelfMustBeLit is true this function returns
        nil if self's IsLit property is nil.
    
        In other words, if SelfMustBeLit is false we're just checking the
        last parent self COULD light if it was lit, if SelfMustBeLit is true
        we're checking to see the last parent self IS lighting...
        """

        #---------------------
        # Check If Self Is Lit
        #---------------------

        # First check to see if Self must be lit, if it isn't it obviously won't
        # illuminate it's container, much less a room!

        if SelfMustBeLit and not self.IsLit: return None

        #---------------------
        # Find Last Lit Parent
        #---------------------
        
        # This loop is the heart of the beast. Object is going to be our test
        # variable, we start by assigning self to it. We set LastObject to None
        # because we haven't examined the first object yet. (The reason we need
        # LastObject is explained in "Safety Net" below.)
        #
        # Let's use an example. We have a lit lamp in a glass bottle in an open
        # box in the forest. What is the last object it will illuminate?
        #
        # Obviously the forest, since there's an unobstructed path for the light
        # to reach the forest.
        #
        # Here's a breakdown. Obj starts off as Lamp. Lamp's location is Bottle,
        # so we test Lamp.Bottle.IsOpen, which is false (the bottle is closed).
        # Next we test Lamp.Bottle.IsTransparent, which is true. Since the And
        # connecting the tests requires both be true, the IF fails, so we make
        # LastObject = Lamp and Object = Bottle.
        #
        # The second time through the loop Bottle.Box.Open is true, so the IF
        # fails again and we make LastObject = Bottle and Object = Box.
        #
        # The third time through the loop Box.Forest.Open is false (by default
        # rooms are closed, only nested rooms are open) AND
        # Box.Forest.Transparent is false so the IF test works and we return
        # Forest.
        #
        # Had the box been CLOSED the function would have returned Box, had
        # the bottle been opaque the function would have returned Bottle.

        Object = self
        LastObject = None

        while Object.Where() <> None and Object.Where() <> SpaceTime:
            if not Object.Where().IsOpen and not Object.Where().IsTransparent:
                return Object.Where()
            LastObject = Object
            Object = Object.Where()

        #-----------
        # Safety Net
        #-----------
        
        # The above loop works fine when rooms are declared as not open and not 
        # transparent. But what happens if for some reason you defined a room as
        # either open or transparent?
        #
        # In our example above let's assume you made Forest Open for some reason.
        # In that case the IF test would have failed and Obj would have become
        # Forest. Forest.Location is None, so the loop would terminate BUT WOULD
        # NOT HAVE RETURNED ANYTHING!
        #
        # This obviously isn't what you want. To cover yourself ALWAYS assume
        # the worst. In this case we return LastObject checked (Forest), which
        # means the function will work regardless of Forest's Open and
        # transparent properties. In other words, it will tolerate mistakes on
        # your part without failing and making a bug that's probably going
        # to take you days to find!
        #
        # This "safety net" has several names in the programming community,
        # ranging from the formal "proactive debugging" or "assertion checking" 
        # to the slightly risque "CYA".

        return Object
    
    def ParentReachable(self):
        """
        This method returns the outermost container that Self could travel
        to physically
    
        For example, if we have a gem in an (open) bottle in a (closed) box
        in the forest, then this function would return box. If the box were
        open it would return forest.
        """

        #----------------------
        # Find Last Open Parent
        #----------------------
        
        # This loop is the heart of the beast. Object is going to be our test
        # variable, we start by assigning it to self. We set LastObject to None
        # because we haven't examined the first object yet. (The reason we need
        # LastObject is explained in "Safety Net" below.)
        #
        # Let's use an example. We have a gem in an (open) glass bottle in an
        # open box in the forest. Is there an unobstructed path between gem and
        # forest?
        #
        # Yes, since both box and bottle are open.
        #
        # Here's a breakdown. Object starts off as Gem. Gem's location is Bottle,
        # so we test Gem.Bottle.Open, which is true (the bottle is open). The IF
        # fails, so we make LastObj = Gem and Obj = Bottle.
        #
        # The second time through the loop Bottle.Box.Open is true, so the IF
        # fails again and we make LastObject = Bottle and Obj = Box.
        #
        # The third time through the loop Box.Forest.Open is false (by default
        # rooms are closed, only nested rooms are open) so the IF test works
        # and we return Forest.
        #
        # Had the box been CLOSED the function would have returned Box, had the
        # bottle been closed the function would have returned Bottle.

        Object = self
        LastObject = None

        while Object.Where() <> None and Object.Where() <> SpaceTime:
            if not Object.Where().IsOpen: return Object.Where()
            LastObject = Object
            Object = Object.Where()

         
        #-----------
        # Safety Net
        #-----------

        # The above loop works fine when rooms are declared as not open. But what
        # happens if for some reason you defined a room as open?
        #
        # In our example above let's assume you made Forest Open for some reason.
        # In that case the IF test would have failed and Obj would have become 
        # Forest. Forest.Location is None, so the loop would terminate BUT WOULD
        # NOT HAVE RETURNED ANYTHING!
        #
        # This obviously isn't what you want. To cover yourself ALWAYS assume the
        # worst. In this case we return LastObj (Forest), which means the
        # function will work regardless of Forest's Open property. In other 
        # words, it will tolerate mistakes on your part without failing and
        # making a bug that's probably going to take you days to find!
        #
        # This "safety net" has several names in the programming community,
        # ranging from the formal "proactive debugging" or "assertion checking"
        # to the slightly risque "CYA".

        return Object
    
    def ParentRoom(self):
        """
        This method returns the outermost room that holds this object. It
        does so by looping through each parent object until a None location
        is returned, at which point we know we've reached the outermost
        room.

        The heart of the routine is the while loop. Let's take this example.
        Suppose we have the player carrying rock in a box in a forest.
        Obviously, Me.ParentRoom(), Box.ParentRoom(), and Rock.ParentRoom()
        should all return Forest, but how?
    
        Let's take the rock as our example. We start off by setting the
        variable Object to Rock.
    
        Each time we hit the loop we have to test Object.Location to see if
        it has one. Rock does, so we set the object to the rock's location
        which is Box. Remember, the Location property holds the object that
        contains this object.
    
        The second time through the loop Object.Location is Forest, so we
        set Object to Forest.
    
        This time, however, Forest.Location is None, so we ignore the loop
        and return Object (Forest) as our parent room.
    
        Basicly, locations form a "tree" that you can follow back to the
        root. The root will always be a room for all objects that exist in
        the game's "physical" universe. You can play games by setting an
        object's location to None, which effectively removes the object
        from existance (along with all contents). You should be very careful
        doing so, however.
    
        By the way, Forest.ParentRoom() returns Forest!
        """
        Object = self
        while Object.Where()<>None and Object.Where()<>SpaceTime:
            Object = Object.Where()
        return Object
    
    def ParentVisible(self):
        """
        This method returns the outermost container that Self can "see".
        Light must be present for this function to return an object.
        Therefore if a rock were in a closed opaque box (with no light
        source) this function would return None, since no parent is visible.
    
        This function employs some programming tricks explained below.
        """
        
        #-----------------------------------------
        # Determine parent potentially illuminated
        #-----------------------------------------
        
        # The ParentLit(FALSE) method returns the outermost parent self would
        # illuminate IF self were producing light. (We don't care if self is
        # actually producing light or not, we just want a "line of sight" to the
        # last object self can "see".
        #
        # By the way, the trick is using ParentLit(None). If we tried to use
        # ParentLit(TRUE) it wouldn't work. ParentLit(TRUE) would return None
        # unless self actually were lit.
        #
        # NOTE: You might be wondering why we stored self.ParentLit(None) in
        # a variable since we turn around and use it in the very next line of
        # code.
        #
        # If you look closely you'll notice that Parent is actually used 3 times
        # in the if test. ParentLit(None) is "expensive", that means it takes a
        # significant (to the computer) amount of time to run.
        #
        # If we used it directly we'd triple the time required for this method
        # to run! ParentVisible is used a LOT, so we want to optimize the
        # performance as much as possible.
        #
        # Always pay attention to the amount of work your code does. The more
        # work, the longer it will take, and the slower your game will run.
        # Sometimes you can afford slow code, sometimes you can't.
        #
        # The more often a function or method is called, the more vital it is
        # that it run quickly.

        Parent = self.ParentLit(FALSE)
        
        #----------------
        # Is Parent None?
        #----------------

        # If Parent is None we return None, since nilspace is unlit by fiat. This
        # test prevents an interesting and subtle bug from occuring.
        #
        # I discovered that when a player sees an object and that object then
        # vanishes (location becomes None) and the player then says "look at
        # <vanished object> the next IF test below fails, and PAWS produces an
        # error message.
        #
        # It turns out that methods MUST have an object, None.IsLit (for example)
        # generates an error, since None has no properties or methods.

        if Parent == None: return None
        
        #---------------------
        # See if there's light
        #---------------------

        # Parent might be a lit room, for example if the rock were in the (lit) 
        # forest then the forest would be visible. On the other hand it might be
        # in a cavern that's illuminated by the player's lantern. In that case
        # Parent.IsLit is None, however one of the elements in the Global list
        # LitParentList will be Cavern so you're free and clear.

        if Parent.IsLit or Parent in Global.LitParentList: return Parent

        #----------
        # No Light?
        #----------

        # If there's no light then the parent isn't visible, return
        # None.

        return None
    
    def Remembers(self,Object):
        """
        This method allows an object to recall whether or not it has
        encountered the passed object before. It uses the MEMORY property to
        do this, if an object is in the MEMORY list property the object will
        remember it, if not, it won't.
        """

        #-----------------
        # Remember object?
        #-----------------
        
        # This test is very straightforward. IN is the built-in Python function
        # that returns TRUE if object is in self.Memory. If the object isn't in
        # MEMORY, then IN returns FALSE (and we fail) otherwise it returns TRUE
        # and we succeed.

        if Object in self.Memory or \
           Object.__class__ == ClassDirection or \
           self.__class__ == ClassDirection:
            return SUCCESS
        else:
            return FAILURE
    
    def SmartDescribeSelf(self):
        """   
        This is the method called by other classes and services when they
        want the object to describe itself in the most typical way. Note
        this method actually says text on the screen, unlike the DESC
        methods below.
    
        For example, self.Enter might call self.SmartDescribeSelf (in a
        room) so the room would describe itself via short and long
        descriptions, and also list the room's contents, etc. (Objects in a
        list would most likely be described by calling
        Object.SmartDescribeSelf!)
    
        By default this function says the long description of an object and
        any blatant sound or smell the object is putting off.
        """
        P.CA().Memorize(self)
        self.DescribeSelf("HERE")
        if self.IsTransparent and self.Contents: Say(self.LookDeepDesc())
        if self.IsBlatantSound: self.DescribeSelf("SOUND")
        if self.IsBlatantOdor:  self.DescribeSelf("ODOR")
    
    def VerbPreposition(self):
        """
        This method returns the preposition used with the verb. It's
        intended to make various methods easier to understand, such as
        LookDeep(), WrongPreposition(), and Insert().
    
        What it does is return the ExpectedPreposition property of the 
        current verb, the verb used in the player's command. If there is no
        ExpectedPreposition property in the verb's command then "inside" is
        assumed. Note we use the Get() method to retrieve
        ExpectedPreposition to protect ourselves from crashing the program
        if ExpectedPreposition hasn't been defined.
        """
        
        Preposition = P.CV().Get("ExpectedPreposition")
        if Preposition == None: Preposition = "inside"
        return Preposition
    
    def Where(self):
        """
        Call this function when you want to know where an object is instead
        of calling on Location. Floating objects will override this method
        with one that returns the current actor's location.
    
        See also the comments on MoveInto() and Location.
        """
        
        return self.Location


    
    #-----------------------------------------------------------------
    #                           "Descriptions"
    #-----------------------------------------------------------------

    # Descriptions are ways an object (for example, a rock) can describe
    # itself in various parts of speech. Descriptions are the building
    # blocks for the more complex DescribeSelf method.
    #
    # Every Description is a method, never a property, and it always returns
    # a string, never saying anything.

    def ADesc(self):
        """
        The ADesc by default is the object's article, a space, and the
        object's short description. For example "a small grey rock" or
        "an elephant".
    
        It's used whenever you want to use the object and the correct
        article in a sentence.
        """
        return "%s %s" % (self.ArticleDesc(),self.SDesc())
    
    def AmnesiaDesc(self):
        """
        Returns 'I don't remember ever seeing a rock around here. Used when
        the Me object doesn't remember an object.
        """

        return "I don't remember ever seeing %s %s around here." % \
               (self.ArticleDesc(),self.NamePhrase)
    
    def ArticleDesc(self):
        """
        The article description returns the article only, not the article
        and the short description like self.ADesc() does. There are cases
        where the two might not match, for example "umbrella" can use either
        "a" or "an" depending on the adjective used, or IF an adjective is
        used.
        """

        return self.Article

    def CantLookDesc(self):
        """
        This function return "It's impossible to look under/behind/inside
        the rock. The appropriate word is supplied by the current verb's
        ExpectedPreposition property. If the current verb has no
        ExpectedPreposition property then "inside" is used.
        """

        Preposition = self.VerbPreposition()
        return "It's impossible to look %s %s." % (Preposition,self.TheDesc())
   
    def CantReachDesc(self):
        """
        If the actor (generally Me) can see but not reach the object in
        question, AND the verb used doesn't have a CantReach method of its
        own, this one is used.
        """
        
        #---------------------------
        # Does self have a location?
        #---------------------------

        # If self does NOT have a location, return an empty string.

        if self.Where() == None: return ""
        
        #--------------------------------
        # Assemble first part of sentence
        #--------------------------------

        # The sentence will normally read "You can't reach the rock." Notice
        # we're using the You() function and the TheDesc method from self (the
        # rock).

        Sentence = SCase("%s can't reach %s." % (You(),self.TheDesc()))
        
        #-------------------------
        # Is Self's Location Open?
        #-------------------------

        # If the rock is in the open that's all there is to it, so we return
        # the sentence as is.

        if self.Where().IsOpen: return Sentence
        
        #-----------------
        # Add open warning
        #-----------------

        # However, if the rock is inside a closed container (say a closed
        # glass box) then we add "You'll have to open the glass box first."
        #
        # Notice we're using the TheDesc method from self.LOCATION, not
        # self! In other words, if self's location is GlassBox, we're
        # using GlassBox.TheDesc, not Rock.TheDesc.

        Sentence = Sentence + " %s'll have to open %s first." % \
            (You(),self.Where().TheDesc())
        
        #--------------------------------
        # Return fully assembled sentence
        #--------------------------------

        return Sentence
    
    def CantSeeDesc(self):
        """
        Used as an error method on the SpecialDisambiguation routine.
        """

        Sentence = "%s can't see any %s here." % (You(),self.NamePhrase)

        return SCase(Sentence)

    def ChooseArticleDesc(self):
        """
        This method will return either TheDesc() or ADesc(), as appropriate.
        If the current actor has met this object before, we use TheDesc().
        Otherwise, if the object is a new one, we use ADesc()
        """
        if self.Remembers(P.CA()):
            return self.TheDesc()
        else:
            return self.ADesc()

    
    def ContentDesc(self,Level = None,Shallow = FALSE):
        """
        This method allows an object to describe its contents. This assumes
        a standard object, special objects should override this method.
        """
        
        #-------------------
        # Find Current Level
        #-------------------

        # When the first call is made, it's always made with no arguments. This
        # test lets us make the current level 0, which allows us to add 1 to the
        # level for self's contents.

        if Level == None:
            CurrentLevel = 0
        else:
            CurrentLevel = Level
        
        #----------------
        # Properly Indent
        #----------------

        # We want all new objects to say their contents indented on a new line 
        # so we start with a line break (~n), then indent by the current level's
        # number of tabs (~t).

        Sentence = " ~n " + Indent(CurrentLevel)
        
        #-----------------------
        # Get the object's Adesc
        #-----------------------

        # The description used when the player types 'Inventory' or 'Look into 
        # <object>' is "a rock", "an elephant", etc.

        if self <> Global.Player: Sentence = Sentence + self.ADesc()
        
        #--------------------------------------
        # Check if shallow, open or transparent
        #--------------------------------------

        # If doing a shallow (non-recursive) contents description, or if the 
        # object is neither open nor transparent we want to fail silently, that
        # is, we want to do nothing. This allows us to use the ContentDesc
        # method recursively, that is, letting an object call it, then objects
        # referenced by it call their own ContentDesc, and so forth.

        if Shallow: return Sentence

        if not (self.IsOpen or self.IsTransparent or self == Global.Player):
            return Sentence
        
        #--------------
        # Has contents?
        #--------------

        # An object's contents are stored in the Contents list. If the length of
        # this list is 0 the object is empty, if not it has something in it.
        #
        # Notice we assign Prefix one of two strings based on whether there's
        # contents or not. We then indent on a new line and set the prefix. This
        # says basically either "The box is empty" or "The box contains:".

        LC = len(self.Contents)

        if LC == 0:
            Prefix = self.EmptyDesc()
        else:
            Prefix = self.ContentsPrefixDesc()

        Sentence += Choose(CurrentLevel==0,""," ~n ") + \
                    Indent(CurrentLevel) + Prefix
                
        #--------------------------------------
        # Recursive Call To Content Description
        #--------------------------------------
        
        # Recursion simply means call the same method for another object. Let's
        # take the simple example of the player carrying some keys, a rock,
        # a box, and in the box a bottle of water and a ring.
        #
        # We would like the (open) box to list its contents as well. So we
        # want to see:
        #
        # You are carrying:
        #    some keys
        #    a rock
        #    a box
        #       The box contains:
        #           a bottle
        #               The bottle contains:
        #                   some water
        #           a ring
        #
        # Here's how it works. The keys and rock are closed and opaque, so a
        # call to both keys.DescribeSelf('Content') and
        # rock.DescribeSelf('Content') produces no output. (Look at the first IF
        # test in this method).
        #
        # But Box.DescribeSelf('Content') fires the loop below for the box, which
        # obediently lists the bottle, which fires the loop below, which then
        # lists the bottle's contents. Since the water isn't open it fails
        # silently, making no more calls. That ends 
        # Bottle.DescribeSelf('Content'), returning to
        # Box.DescribeSelf('Content') which then lists the ring, which is opaque.

        for Obj in self.Contents:
            Sentence = Sentence + Obj.ContentDesc(CurrentLevel + 1)
        
        #----------------
        # Return Sentence
        #----------------

        # Now we've got a monster string, so we can return with it.

        return Sentence
    
    def ContentsPrefixDesc(self):
        """
        This method is used when a container has contents. It says "The
        box contains:"
        """
        return SCase(self.TheDesc() + " contains:")
    
    def ContentsShallowDesc(self):
        """
        Unlike ContentsDesc() which lists self's contents, and then for any
        open or transparent items lists THEIR contents as well in an
        indented outline style list, this function only does a "shallow"
        list, ie it lists self's immediate contents, but not the contents of
        open or transparent items in self.
    
        For example, assume we look in a bag. The bag contains a bell, a 
        book, a candle, and a glass box. Further since the glass box is
        transparent we can see it contains a ball.

        Here's what ContentsDesc() would display:
    
        The bag contains:
        a bell
        a book
        a candle
        a glass box
            The glass box contains:
                   a ball
    
        Here's what ContentsShallowDesc() would display, assuming the player
        had never seen any of the items before:
    
        "The bag contains a bell, a book, a candle, and a glass box."
        """
        
        #----------------------
        # Init Needed Variables
        #----------------------

        # TempList holds the intermediate results of calling ChooseArticleDesc()
        # for each object in self.Contents. ListCount tells us how many objects
        # are in self.Contents.

        TempList = []
        ListCount = len(self.Contents)
        
        #--------------------------
        # 0 or 1 Items in Contents?
        #--------------------------

        # If there are no contents, return "nothing". If there's just one return
        # it's ChooseArticleDesc(). In either case these tests simplify the
        # coding for contents of more than one object.

        if ListCount == 0: return "nothing"
        if ListCount == 1: return self.Contents[0].ChooseArticleDesc()
        
        #-----------------------------
        # 2 or more items in Contents?
        #-----------------------------
        
        # If there are two or more items in Contents then we first obtain a list
        # of strings that are the ChooseArticleDesc() results for each item. 
        # ChooseArticleDesc() returns either ADesc() ("a rock") if the player
        # hasn't seen it before or TheDesc() ("the rock") if they have.
        #
        # Then we use string.join to join all but the last item in Templist
        # together with ", " (a comma and a space), add the word "and", and
        # finally add the last item in TempList.
        #
        # So if self.Contents contained [Bell, Book, Candle], Result would become
        # (assuming he'd seen none of the three before) "a bell, a book and a 
        # candle".

        for Object in Contents:
            TempList.append(Object.ChooseArticleDesc())

        Result = string.join(TempList[:-1],", ") + " and " + TempList[-1]

        #--------------
        # Return Result
        #--------------

        return Result
   
    def DontSeeInterestingDesc(self):
        """
        This function return "It's impossible to look under/behind/inside
        the rock. The appropriate word is supplied by the current verb's
        VerbPreposition property. If there's no preposition then "inside" is
        used. So it would say: "You don't see anything interesting inside
        the box.
        """

        Preposition = self.VerbPreposition
        return SCase("%s %sn't see anything interesting %s %s." % (You(),
                                                             Do(),
                                                             Preposition,
                                                             self.TheDesc()))

    
    def EmptyDesc(self):
        """Returns 'The treasure chest is empty.'"""

        return SCase(self.TheDesc()+" is empty.")

    def FeelDesc(self):
        """
        All objects have a feel to them, silk is soft, granite is rough and
        hard, etc.
        
        Returns 'It feels like an ordinary rock to me'
        """

        Phrase = "%s feels like an ordinary %s to %s." % \
         (self.PronounDesc(),self.NamePhrase,Me())

        return SCase(Phrase)

    def GroundDesc(self):
        """Returns 'The ground looks ordinary to me.'"""

        Phrase = "The ground looks ordinary to %s." % Me()
        return SCase(Phrase)
    
    def HelloDesc(self):
        """Returns 'Did you really expect a rock to speak?'"""

        Phrase = "Did you really expect %s to speak?" % self.ADesc()

        return SCase(Phrase)
    

    def HereDesc(self):
        """
        The HereDesc contains the description of the object when being
        described by a room. By default it isn't very useful, you'll
        probably want to override it in your object definitions.
        """
        
        #------------------------
        # Record Correct Prounoun
        #------------------------

        # This records the object to the appropriate pronoun. For example: "There
        # is a rock here." Since rock is an "it" we need to record the rock as
        # "it". Then when the player says "get it" we know what "it" refers to.
        # This also works for "him" and "her". "Them", "all", and "everything"
        # are handled differently.

        self.MarkPronoun()
        
        #-----------------
        # Set Descriptions
        #-----------------

        # Here_Description is used if the object is NOT scenery, No_Description
        # is used if it is.
        #
        # Notice we override the default Here_Description if the Descriptions
        # dictionary is present and has a "Here" key. This allows the option of 
        # using the ServiceDictDescription with this function and not having to
        #  override it. Very handy for objects of ClassItem.

        Here_Description = "There's %s here." % self.ADesc()

        if hasattr(self,"Descriptions"):
            if self.Descriptions.has_key("HereDesc"):
                Here_Description = self.Descriptions["HereDesc"]

        No_Description = ""
        
        #------------
        # Is Scenery?
        #------------

        # If Self is scenery (a useless prop to add atmosphere) we return no
        # description, else we return the Here description.

        if self.IsScenery:
            return No_Description
        else:
            return Here_Description

    def InsertedDesc(self, Object, Spontaneous=FALSE):
        """
        Returns the description when one item is inserted into another, for 
        instance "The rock goes inside the bag." or "You put the rock inside
        the bag."
        """
        
        #----------------
        # Get Preposition
        #----------------

        # The preposition we want to use is self's dynamic one. 

        Preposition = P.IOL()[0].ContainerPrepositionDynamic
        
        #-------------------
        # Construct Sentence
        #-------------------

        # If Spontaneous is FALSE says "The rock goes inside the bag." Otherwise
        # it says "You put the rock inside the bag."

        if not Spontaneous:
            Sentence = "%s %s %s %s." % (self.TheDesc(),
                                          Agree("go", Object),
                                          Preposition,
                                          Object.TheDesc())
        else:
            Sentence = "%s %s %s %s %s." % (You(),
                                            Agree("put"),
                                            self.TheDesc(),
                                            Preposition,
                                            Object.TheDesc())

        
        #--------------------------------
        # Return Sentence Correctly Cased
        #--------------------------------

        # We make sure the first letter in the sentence is capitalized.

        return SCase(Sentence)

    def LDesc(self):
        """
        The LDesc is the object's long description. For an object this is
        the description provided by looking at the object, not the 
        description provided as part of a room.
    
        For instance, the rock is described as "a small grey rock" in
        general, or "There is a small rock here." when described as part of
        the room's contents. But when looked at closely it might say "The
        rock is oblong, rough, and about the right size to fit comfortably
        in your hand."

        In a room, the LDesc is the room's visual description.

        By default the long description isn't very helpful. Notice we use
        NamePhrase instead of SDesc.
        """

        BrokenDescription = ""
        if self.IsBroken: BrokenDescription = "(but broken) "

        RV = "%s looks like an ordinary %s to %s."

        RV = RV % (self.PronounDesc(),self.NamePhrase,Me())
        return SCase(RV)

    def LookDeepDesc(self):
        """
        This function returns the string for looking in/behind/on/under an
        object. It is only called when there are actually objects to be
        described.
        """
        return "%s %s %s %s %s. " % (SCase(self.ContainerPrepositionStatic),
                                     self.TheDesc(),
                                     You(),
                                     Agree("see"),
                                     self.ContentsShallowDesc())

    def MultiSDesc(self):
        """
        The MultiSDesc is used by the parser when running commands with
        multiple direct objects, for example "Take All". This lets you
        change the description of an object when it's part of a list.
        """

        return self.SDesc() + ":"

    def NoDesc(self):
        """    
        Returns an empty string. For those times when you want to say
        nothing at all.

        """

        return ""

    def NotWithVerbDesc(self):
        """
        Error condition for SpecialDisambiguation when object not allowed
        with verb.
        """

        return P.AP().Nonsense

    def OdorDesc(self):
        """Returns 'It smells like an ordinary small grey rock to me.'"""

        Phrase = "%s smells like an ordinary %s to %s." % \
                 (self.PronounDesc(),self.NamePhrase,Me())

        return SCase(Phrase)

    def PronounDesc(self):
        """
        The pronoun varies based on the IsHim/IsHer properties. If neither
        are set the pronoun is 'it', otherwise the pronoun is 'him' or 'her'
        respectively.
        """

        if self.IsHim: return "him"
        if self.IsHer: return "her"
        return "it"

    def PluralDesc(self):
        """
        Used to describe the object in plural, for example "coins". By
        default this is the SDesc followed by an S. Plural forms in English
        are lamentably unpredictable however. There's "es" (Indexes), word
        shift (Hippotomous to Hippottomi), etc.
        """

        return self.SDesc() + "s"

    def ReadDesc(self):
        """
        The description of an item when read. By default it complains you
        can't read the self.ADesc. ("You can't read a small gray rock.")
        """

        Phrase = "%s can't read %s." % (You(),self.ADesc())

        return  SCase(Phrase)
    
    def SDesc(self):
        """
        SDesc is the short description. As you can see a short description
        isn't exactly easy to come by! The basic idea is to assemble the
        description from the AdjectivePhrase and NamePhraseDesc. However,
        if the item gets broken somehow we want to put the word broken in
        front of the NamePhrase.
        """

        RV = ""
        if len(self.AdjectivePhrase) > 0: RV = self.AdjectivePhrase + " "
        if self.IsBroken: RV += "broken "
        RV += self.NamePhrase
        return RV
        
    def SkyDesc(self):
        """
        Returns 'The sky looks ordinary to me.'
        """

        Phrase = "The sky looks ordinary to %s." % Me()
        return SCase(Phrase)
    
    def SoundDesc(self):
        """
        This is the sound the object is making. By default most objects
        don't make a sound, so we say "the <whatever> isn't making any
        noise."
        """

        return SCase(self.TheDesc() + " isn't making any noise.")

    def TasteDesc(self):
        """
        Returns 'It tastes like an ordinary rock to me.'
        """

        Phrase = "%s tastes like an ordinary %s to %s." % \
                 (self.PronounDesc(),self.NamePhrase,Me())

        return SCase(Phrase)

    def TheDesc(self):
        """
        There's only one definite article in English, so the default
        TheDesc is simply the word "the" followed by a space and the 
        object's short description.
        """

        return "the " + self.SDesc()
    
    def WallDesc(self):
        """
        Returns "The wall looks normal to me."
        """

        Phrase = "The wall looks normal to %s." % Me()
        return SCase(Phrase)

    def WrongPrepositionDesc(self, Object, Spontaneous=FALSE):
        """
        Called when verb had one preposition (like "under") and the object
        had another (like "inside"). Returns "The rock can't go inside the
        table." if Spontaneous is FALSE or "You can't put the rock in the
        table." if Spontaneous is TRUE. Spontaneous defaults to FALSE.
        """
        
        #----------------------------
        # Get Preposition Player Used
        #----------------------------

        Preposition = self.VerbPreposition()
        
        #-------------------
        # Construct Sentence
        #-------------------

        # If Spontaneous is FALSE the sentence should read "The rock can't go
        # inside the table.". If Spontaneous is TRUE the  sentence should read
        # "You can't put the rock inside the table.".

        if not Spontaneous:
            Sentence = "%s can't go %s %s. " % (self.TheDesc(),
                                                Preposition,
                                                Object.TheDesc())
        else:
            Sentence = "%s can't put %s %s %s. " % (You(),
                                                    self.TheDesc(),
                                                    Preposition,
                                                    Object.TheDesc())

        #---------------------------------
        # Return Sentence In Sentence Case
        #---------------------------------

        # Make sure the first letter of the sentence is capitalized.

        return SCase(Sentence)

class ClassActor(ServiceFixedItem,ClassBasicThing):
    """
    An actor is an object capable of executing commands. Me is an actor,
    with additional capabilities. By default an actor is simply a BasicThing
    that returns true for the IsActor property. Anything declared as an
    Actor (or having Actor for an ancestor) will be placed on the actor
    list.

    In addition, many parts of speech that relate to actors are defined
    here.
    """

    def SetMyProperties(self):
        """
        Sets default instance properties.
        
        Notice we're extending ClassBasicThing's init behavior. This is
        necessary because we're adding (and changing) default valued
        instance properties.
        """
         
        self.Bulk       = 24    # 24 cubic feet (6' x 2' x 2')
        self.IsActor    = TRUE
        self.MaxBulk    = 10    # can carry 10 cubic feet
        self.MaxWeight  = 500   # can carry 50 pounds (gold piece = 1/10 pound)
        self.IsOpen     = TRUE  # actors must be open (inventory)
        self.Weight     = 1750  # 175 pounds (g.p. = 1/10 pound)
        
        #--------------------
        # Format Descriptions
        #--------------------

        # These are the parts of speech that are part of subject/verb
        # agreement.

        self.FormatMe      = "me"
        self.FormatYou     = "you"
        self.FormatYoum    = "you"
        self.FormatYour    = "your"
    
    def ADesc(self):
        """
        Actor's equivalent of "a rock", in other words "yourself".
        """
        
        return "yourself"
        
    def Enter(self,Object):
        """
        The only differences between this method and the standard
        (BasicThing) method is the wording of the complaints.
        
        Handles object entering self.
        """

        #------------------
        # Self is Openable?
        #------------------

        # If Self (the actor) isn't openable, then obviously they won't be able
        # to carry anything because they aren't openable. The PLAYER is openable
        # because of his inventory.

        if not self.IsOpenable:
            Complaint = "%s can't carry %s!" % (You(),Object.TheDesc())
            return Complain(SCase(Complaint))

        #--------------------------
        # Is Object too big to fit?
        #--------------------------

        if Object.Bulk + self.ContentBulk() > self.MaxBulk:
            Complaint = "%s can't manage to carry anything else." % You()
            return Complain(SCase(Complaint))
        
        #---------------------
        # Is object too heavy?
        #---------------------

        if Object.Weight > self.MaxWeight:
            Complaint = "%s can't even lift it, much less carry it!" % You()
            return Complain(SCase(Complaint))
            
        
        #-------------------
        # Is load too heavy?
        #-------------------

        if Object.Weight + self.ContentWeight() > self.MaxWeight:
            return Complain(SCase("%s load is too heavy." % Your()))

        
        #------------
        # OK to enter
        #------------

        Object.MoveInto(self);
        self.Memorize(Object)
        return TURN_ENDS
    
    def LDesc(self):
        Message = "%s %s about the same as always." % (You(),Agree('look'))
        return Message

    
    def TheDesc(self):
        """
        The actor's equivalent of "the rock", in other words "yourself".
        """

        return "yourself"
    
    def Travel(self,Vector):
        """
        This method allows the actor to travel along the map just like the
        player's character. Specific actors can override this method and any
        class that needs to travel should also override it (ie a vehicle).
    
        This method checks for the indicated travel direction in 3 places,
        the actor's location's Map, DefaultMap, or Global.DefaultMap, in
        that order. If direction's in none of those it complains with
        P.AP().NotADirection.
        """
        
        #-----------------------------------
        # Destination in Current Room's map?
        #-----------------------------------

        # Map is a dictionary, so the has_key method tests to see if the
        # desired Vector is in the map. Vector might be the object North, for
        # example.

        if self.Where().Map.has_key(Vector):

            #----------------------------------
            # Direction IS in map, get New Room
            #----------------------------------

            NewRoom = self.Where().Map[Vector]

            #-------------------------
            # New Room Is A Complaint?
            #------------------------
            
            # If New Room is actually a string, it MUST be a complaint, so
            # return the complaint, which has the effect of continuing the turn.

            if type(NewRoom) == type(""): return Complain(NewRoom)

            #---------------------
            # Can self Leave Here?
            #---------------------
            
            # If New Room isn't a complaint, it's a room. Check if self's 
            # current room allows self to leave. If not, the Leave() method 
            # will make the will the complaint. Then we return TURN_CONTINUES.

            if not self.Where().Leave(self): return TURN_CONTINUES

            #-----------------
            # Move to New Room
            #-----------------
            
            # By reaching here we know the current room will allow self to leave,
            # so all we have to do is call the New Room's Enter() method, 
            # passing self, and returning the result.

            return NewRoom.Enter(self)
        
        #-----------------------------------------
        # Direction in Current Room's Default Map?
        #-----------------------------------------

        # Ok, it wasn't in the room's normal map. Next we check the room's
        # default map, using the same logic.
        
        if self.Where().DefaultMap.has_key(Vector):

            #----------------------------------
            # Direction IS In Map, Get New Room
            #----------------------------------

            NewRoom = self.Where().DefaultMap[Vector]

            #-------------------------
            # New Room Is A Complaint?
            #------------------------
            
            # If New Room is actually a string, it MUST be a complaint, so
            # return the complaint, which has the effect of continuing the turn.

            if type(NewRoom) == type(""): return Complain(NewRoom)
            
            #---------------------
            # Can self Leave Here?
            #---------------------
            
            # If New Room isn't a complaint, it's a room. Check if self's 
            # current room allows self to leave. If not, the Leave() method 
            # will make the will the complaint. Then we return TURN_CONTINUES.

            if not self.Where().Leave(self): return FAILURE

            #-----------------
            # Move to New Room
            #-----------------
            
            # By reaching here we know the current room will allow self to leave,
            # so all we have to do is call the New Room's Enter() method, 
            # passing self, and returning the result.

            return NewRoom.Enter(self)
        
        #-------------------------------------
        # Direction NOT in Global default map?
        #-------------------------------------

        # If the direction isn't in the default map either, complain.
        
        if not Global.DefaultMap.has_key(Vector):
            return Complain(P.AP().NotADirection)
        
        #-----------------------------------------
        # Direction IS In Global Map, Get New Room
        #-----------------------------------------
        
        NewRoom = Global.DefaultMap[Vector]

        #-------------------------
        # New Room Is A Complaint?
        #------------------------
        
        # If New Room is actually a string, it MUST be a complaint, so return the
        # complaint, which has the effect of continuing the turn.

        if type(NewRoom) == type(""): return Complain(NewRoom)

        #---------------------
        # Can self Leave Here?
        #---------------------
        
        # If New Room isn't a complaint, it's a room. Check if self's  current
        # room allows self to leave. If not, the Leave() method will make the
        # the complaint. Then we return TURN_CONTINUES.

        if not self.Where().Leave(self): return FAILURE

        #-----------------
        # Move to New Room
        #-----------------
        
        # By reaching here we know the current room will allow self to leave, so
        # all we have to do is call the New Room's Enter() method,  passing self,
        # and returning the result.

        return NewRoom.Enter(self)

class ClassMonster(ClassActor):
    """
    A monster is just an actor with the combat service. Notice how the
    combat service preceeds the class? This is to make sure any combat
    routines take precedence over the same methods in Actor Class.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        pass


class ClassPlayer(ClassMonster):
    """
    Used to create the player's character.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.IsPlural = TRUE    # "you" words tend to the plural usage.
        self.IsScenery = TRUE   # You can't take yourself...
        self.Location = None    # Starting Location is set differently
        self.IsOpenable = TRUE  # Stuff can be put inside player (inventory)

    def ContentsPrefixDesc(self): return "You are carrying:"
    def EmptyDesc(self): return "You are empty handed."
    def HereDesc(self): return ""
    def OdorDesc(self): return "You're a bit ripe, about two months overdue for your yearly bath. . ."
    def SmartDescribeSelf(self): pass
    def SoundDesc(self): return "You aren't making any noise."
    def TasteDesc(self): return "You decide against trying to taste yourself."

class ClassDirection(ClassBasicThing):
    """
    Directions are OBJECTS in PAWS, not prepositions like in TADS. This
    takes some getting used to if you're used to TADS. All normal directions
    are instantiated here. Some, like "tree" (climb tree) are handled as
    part of the class definition for those objects.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.AdjectivePhrase = ""
        self.Location = None

    def LDesc(self):        
        """
        Return's the current actor's room long description.
        """
        return P.CA().Where().LDesc()
    def TheDesc(self):
        """
        Directions don't really have a "the" description, instead they
        use the short description.
        """

        return self.SDesc()

    def Where(self):
        """
        Return's current actor's location. This makes directions a 
        kind of floating object, even though it doesn't have the
        HasFloatingLocation property and won't appear on the floating 
        object list.
        """

        return P.CA().Location

#********************************************************************************
#                        D I R E C T I O N   O B J E C T S
#
C="""
  Because the default maps need to A) be defined in the class definition and
  B) have to be defined before the class, we make an exception to the normal
  "objects defined at the end" rule.

  Unfortunately, we have no choice, even though it makes the code slightly
  harder to follow.
  """
North = ClassDirection("north,n")
Northeast = ClassDirection("northeast,ne")
East = ClassDirection("east,e")
Southeast = ClassDirection("southeast,se")
South = ClassDirection("south,s")
Southwest = ClassDirection("southwest,sw")
West = ClassDirection("west,w")
Northwest = ClassDirection("northwest,nw")
Up = ClassDirection("up,u")
Down = ClassDirection("down,d")
Upstream = ClassDirection("upstream,us")
Downstream = ClassDirection("downstream,ds")
In = ClassDirection("in,inside")
Out = ClassDirection("out,outside")

#********************************************************************************
#                    U N I V E R S E   D E R I V E D   C L A S S E S
#
C="""
  These classes are all derived from the simpler classes given in the
  "Universe Basic Classes" section above the "Direction Objects" section.
  
  The segmentation of the classes into basic and derived is an artifact
  caused by having to have direction objects defined before the room class
  was. "Basic" classes are defined from "fundamental" classes, so there's
  no programmatic difference between basic and derived classes, those are
  just convenient section names.
  """

class ClassRoom(ClassBasicThing):
    """
    Rooms are locations where a player can go to and look around. Many of
    their methods and properties are inherited from their direct ancestor,
    BasicThing.
    """
    
    #------------
    # Default Map
    #------------

    # If no map is specified, this one is used. This particular default map
    # doesn't let you go anywhere, but at least each direction will give a
    # reasonable response.
    #
    # Note ALL ROOMS share one copy of this default map, that's why the word
    # "self" isn't in front of DefaultMap. This saves enormous amounts of memory,
    # always a Good Thing(tm).

    DefaultMap = {North:      "You can't go that way.",
                  Northeast:  "You can't go that way.",
                  East:       "You can't go that way.",
                  Southeast:  "You can't go that way.",
                  South:      "You can't go that way.",
                  Southwest:  "You can't go that way.",
                  West:       "You can't go that way.",
                  Northwest:  "You can't go that way.",
                  Up:         "There's no way up from here.",
                  Down:       "There's no way down from here.",
                  Upstream:   "There's no stream here.",
                  Downstream: "There's no stream here.",
                  In:         "There's nothing here to enter.",
                  Out:        "You're not in anything at the moment."}
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.AdjectivePhrase = ""
        self.HasGround = TRUE
        self.HasSky = TRUE
        self.HasWall = TRUE
        self.IsLit = TRUE
        self.IsOpen = TRUE
        self.IsOpenable = TRUE
        self.IsOutside = FALSE
        self.IsTransparent = FALSE
        self.Location = SpaceTime
        self.MaxBulk = 32000
        self.MaxWeight = 32000
        self.Visited = FALSE
        self.Map = {}

    def Enter(self,Visitor):
        """
        The room's Enter method overrides its immediate ancestor
        (BasicThing) because we want to do more than BasicThing's Enter()
        method provides for.
    
        Notice that ANY object can enter a room! This includes the player,
        of course, but it also includes other actors (not too surprizing)
        AND it includes literally any object!
    
        This is because we use the room's Enter method when an actor drops
        an object to perform the basic checks and (only if the object
        entering is the current actor) describe the object's location.
    
        This might seen confusing, but it's code re-use at its best. If you
        think about it, anything that enters a room (enters the room's
        Contents List) should do so with the same rules as the player,
        except that the object won't describe its new location on the
        screen. (Remote controlled objects with cameras (like a space probe)
        aren't handled by this routine very well, I'm afraid.
        """

        #---------------------
        # Use Inherited Method
        #---------------------

        # This line of code looks tricky but it really isn't. It's saying if
        # BasicThing's ENTER method returns false, then we fail. If you take the
        # time to look at BasicThing's Enter method you'll see that it handles
        # the ability for self (the room) to restrict the bulk of the object
        # entering. It also checks for open and openable properties, so those
        # have to be set to true in this class (since BasicThings by default
        # aren't openable or open). Finally, it does the actual movement of the
        # Visitor into the room. Notice the Visitor doesn't actually have to be
        # an actor, it could be any object, since this routine is also used
        # when dropping objects.

        if not ClassBasicThing.Enter(self,Visitor): return FAILURE

        #-----------------------------------
        # Make sure it's the player entering
        #-----------------------------------

        # The only time we want a description of the room is when it's the player
        # entering the room. Other objects should move but not describe their
        # surroundings.
        #
        # Notice we return success, because the object entered the room
        # successfully, whether or not it was Me.

        if id(Visitor) <>  id(Global.Player): return SUCCESS
        
        #-----------------------
        # Call SmartDescribeSelf
        #-----------------------

        # By reaching this point we know the vistor is the player, so use 
        # SmartDescribeSelf to list the room's description and contents.

        self.SmartDescribeSelf()

        #---------------
        # Return Success
        #---------------

        return SUCCESS
    
    def FeelDesc(self):
        """Feeling Description"""

        Complaint = "Scrabbling around with %s hands uncovers nothing useful."
        return Complaint % Your()

    
    def FirstView(self):
        """
        The first view of a room happens only once. By default we use this
        method to increment the player's score when a room is found that has
        a value. We also mark the room as visited.
        """
        
        IncrementScore(self.Value)
        self.Visited = TRUE
        return ""
    
    def OdorDesc(self):
        """
        If you looked at the code below you're probably scratching your head
        trying to figure it out.
    
        This function (and many other DESC functions) take advantage of
        Python's FORMAT operator -- %.

        It's really quit simple. The %s's in Complaint are there as place
        holders. They're replaced by the variables in the parentheses
        following the %. You can read the % sign as "replace with".
    
        You() = "you"
        Do()  = "do"
    
        Thus "%s %sn't smell anything." becomes: "You don't smell anything."
    
        But assume it's Fred (the player's sidekick):
    
        You() = "he"
        Do()  = "does"
    
        Making it: "HE DOESn't smell anything."
        """

        Complaint ="%s %sn't smell anything." % (You(),Do())
        return SCase(Complaint)
    
    def SmartDescribeSelf(self):
        """
        This method replaces the one inherited from BasicThing, and compared
        to that method is exceptionally "smart". Basically it describes the
        room appropriately, including visible contents, blatant sounds and
        smells, surroundings, etc. It also handles scoring, an optional
        first view, and more.
        """

        #--------------------
        # Determine Verbosity
        #--------------------

        # Verbosity is the level of detail. If Global.Verbose is true then
        # the player has selected verbosity, which means the full room
        # descriptions say all the time, otherwise they only say the
        # first time the player sees the room, or when they type look.

        Verbosity = FALSE
        if self.Visited == FALSE or Global.Verbose == TRUE: Verbosity = TRUE
        
        #-------------
        # Is Room Lit?
        #-------------

        # If the room isn't lit, there isn't a lot to describe, so fail and
        # that's that. Notice we do check for blatant noise or odor

        if self.CurrentlyIlluminated() == FALSE:
            Say("It's too dark to see anything.")

            if self.IsBlatantSound or self.IsBlatantOdor:
                Say("But darkness doesn't stop your other senses...")
                if self.IsBlatantSound == TRUE: self.DescribeSelf("SOUND")
                if self.IsBlatantOdor == TRUE:  self.DescribeSelf("ODOR")

            return TURN_CONTINUES

        
        #-------------------------------
        # Display Room Short Description
        #-------------------------------

        # Display the room's short description, followed by a blank line.

        Terminal.NewLine()
        Terminal.A_TITLE()
        Say(self.SDesc())
        Terminal.A_NORMAL()
        
        if Verbosity == TRUE: Terminal.NewLine()

        Engine.BuildStatusLine(self.SDesc())
        Terminal.DisplayStatusLine(Global.StatusLine)
        
        #--------------------
        # Describe First View
        #--------------------

        # The room must be lit since if it wasn't we wouldn't have gotten
        # this far, so if it hasn't been seen before, you can call the
        # FirstView method to do something special. FirstView can give an
        # extra comment, or do something that only happens the first time
        # the player sees the room.

        if not self.Visited == TRUE: Say(self.FirstView())
         
        #--------------------------
        # Say Long Room Description
        #--------------------------

        # Remember, Verbosity will be true if the Verbose command is in effect
        # OR if the player hasn't been in this room before. Either way they get
        # long description.
        
        if Verbosity: self.DescribeSelf("LONG")
        if self.IsBlatantSound: self.DescribeSelf("SOUND")
        if self.IsBlatantOdor:  self.DescribeSelf("ODOR")
                
        #-----------------
        # Set THEM Pronoun
        #-----------------

        # If the player refers to "them", "all", or "everything" then the
        # parser's going to assume they mean the contents of the current room.

        P.AP().PronounsDict[THEM] = self.Contents
        
        #------------------
        # Say Room Contents
        #------------------

        # Here's an illustration of a very powerful concept, encapsulation.
        # Basically, we simply tell Object to describe itself appropriately
        # and it does! All our hard work is beginning to pay off.
        #
        # This concept let us elegently express in 6 short easy to read
        # lines what would take a page of ugly code in another language.

        for Object in self.Contents:
            Global.Player.Memorize(Object)
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.SmartDescribeSelf()
            if Object.IsBlatantSound: Object.DescribeSelf("SOUND")
            if Object.IsBlatantOdor:  Object.DescribeSelf("ODOR")

    def SoundDesc(self):
        """
        Sound Description of room
        """

        # By default most rooms are silent. You're probably gagging over the
        # complex syntax. While intimidating it's very straightforward
        # (really!).
        #
        # Who is just a synonym for P.CA(), the Parser's Current Actor (the
        # actor who's been given the command). Normally Who would be the player's
        # actor).
        #
        # SCase capitalizes the result, which is:
        #
        # "You don't hear anything."
        # "You"+" "+"do"+"n't hear anything."
        
        Who = P.CA();
        Complaint = SCase("%s %sn't hear anything." % (You(), Do()))
        return SCase(Complaint)


class ClassSmartRoom(ServiceDictDescription,ClassRoom):
    """
    This room uses the ServiceDictDescription service to let you set
    descriptions using the SetDesc() method. It also replaces the FeelDesc()
    with a better method.
    """

    def SetMyProperties(self):
        self.SD("Sound","The room is silent")
        self.SD("Odor","The air is odorless.")
        
    def FeelDesc(self):
        """
        The FeelDesc() method supplied by ServiceDictDescription is 
        inappropriate for rooms, so we override it by callingClassRoom's
        FeelDesc method.
        """

        return ClassRoom.FeelDesc(self)

class ClassScenery(ServiceFixedItem,ServiceDictDescription,ClassBasicThing):
    """
    This class is used to create otherwise useless props to add atmosphere.
    For example, if you mention a hairbrush in a room's description you
    might use this class so when a player tries to take it you say "The
    hairbrush is worthless" or some such.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.IsScenery = TRUE


class ClassLandmark(ClassScenery):
    """
    This class is used to give a special Where() method to scenery objects
    that are placed with "landmarks". A landmark is a special property of
    objects created with this class. The Landmark property contains the
    suffix of the "Has" property that acts as the landmark.

    For example, you might have a series of forests with different kinds of
    trees. For each forest room you create a "Has" property, for example
    HasPineTree and set it to TRUE.

    To create an object that is only present in rooms with the HasPineTree
    property, you'd set the Landmark property of the object to "PineTree".
    Thus the Where() method will look to see if the current room possesses
    a HasPineTree property.

    This class is *extremely* useful for creating objects that must appear
    in multiple rooms. All you have to do is set the appropriate Has
    property to True in the rooms you want.

    This class is otherwise normal scenery.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.HasFloatingLocation = TRUE
        self.Landmark = ""

    def Where(self):
        if P.CA().Where().Get("Has"+self.Landmark):
            Global.Player.Memorize(self)
            return P.CA().Where()
        else:
            return None
class ClassLandmarkMissing(ClassLandmark):
    """
    This method is identical to ClassLandmark except for one crucial
    difference. This class's Where() method returns the current actor's
    location if the landmark is MISSING.

    For example, take the NoWall object, created with this class. The NoWall
    object appears in rooms where HasWall is FALSE--the exact opposite of 
    the Wall object (created with ClassLandmark) which appears in rooms
    where HasWall is TRUE.

    In fact this class was created specifically to create the NoWall
    object--but it can be used for all sorts of objects that must appear if
    a landmark is missing.
    """

    def Where(self):
        if not P.CA().Where().Get("Has"+self.Landmark):
            return P.CA().Where()
        else:
            return None

class ClassItem(ServiceTakeableItem,ServiceDictDescription,ClassBasicThing):
    """
    Items are simply objects that can be taken. This means they have the
    Takeable Item service added to the BasicThing class.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.SD("Take","Taken.")

class ClassDoor(ServiceOpenable, ClassScenery):
    """
    Doors may be opened and closed. Doors may stand in as exits for a room.
    If the player succeeds in entering a door (i.e., if it's open and
    they'll fit through), they will automatically be forwarded to the door's
    destination room.

    Note that doors that let you walk through in both directions are always
    implemented as pairs--one door object in each room. This has the
    advantage of letting doors connect ANY two rooms, thus making magical
    teleportals very easy to create.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""

        #---------------
        # Automatic Open
        #---------------

        # Setting the AutomaticOpen option to TRUE allows a player to go through
        # a closed but unlocked door with just "east" rather than "open door then
        # east". It's a courtesy to the player, not a door that opens by itself.

        self.AutomaticOpen = FALSE

        self.Destination = None
        self.IsLockable = FALSE
        self.IsLocked = FALSE
        self.IsOpen = TRUE
        self.IsOpenable = TRUE
        self.IsTransparent = FALSE
        self.Key = None
        self.Location = None
        self.MaxBulk = 32000
        self.MaxWeight = 32000
        self.NamePhrase = "door"

        #-----------
        # Other Side
        #-----------

        # All doors are really made of two door objects, one in each room the
        # door connects. For example if there's a door between the living room
        # and the kitchen you'd have to make one door object and put it in the
        # living room, and make a second door object for the kitchen. This
        # property lets you identify which door object is the twin to self.

        self.OtherSide = None

    def Close(self, IsSecondTime=FALSE):
        """Close the door. Action called by CloseVerb."""
        
        #------------------------------
        # Fail If This Door Won't Close
        #------------------------------

        # We call the ServiceOpenable Close method to actually close the door.
        # If the door won't close (for whatever reason) any complaints will
        # already have been made, so we exit the method immediately, returning
        # TURN_CONTINUES.

        if not ServiceOpenable.Close(self, Silent=IsSecondTime):
            return TURN_CONTINUES

        #---------------------------
        # Close Other Side If Needed
        #---------------------------

        # This gets a bit complex. Let's assume we have two door objects
        # (remember it takes two door objects to make a door) called 
        # LivingRoomDoor and KitchenDoor that make up the door between the 
        # living room and the kitchen.
        #
        # Let's further assume that the player closes the LivingRoomDoor. That
        # means that the following statement (eventually) gets executed.
        #
        # LivingRoomDoor.Close(FALSE)
        #
        # Then the IF test would be true and this would happen:
        #
        # KitchenDoor.Close(TRUE)
        #
        # Now, this is known as a recursive call, the method is in effect 
        # calling itself. If we'd used FALSE on the kitchen door instead of TRUE
        # then the KitchenDoor would call the LivingRoomDoor's Close which would
        # call the KitchenDoor's close...I'm sure you get the point. The IF test
        # makes sure both doors execute the Close() method exactly once.
        #
        # By the way, the IF test says "if there's another door object defined
        # and this isn't the second time we've called Close() then..."
        #
        # The IF test prevents an author's mistake from crashing the program if
        # they forget to define the other door.

        if self.OtherSide and not IsSecondTime:
            self.OtherSide.Close(TRUE)
        
        #---------------
        # Return Success
        #---------------

        return TURN_ENDS
    
    def Enter(self, Visitor):
        """
        Enter the door. This will complain if the door is closed or doesn't
        lead anywhere.  Otherwise, it passes the entry request to the
        destination room.
        """

        #-------------------------------
        # Door closed and not auto open?
        #-------------------------------

        # You can't go through if the door is closed.

        if not self.IsOpen:
            if not self.AutomaticOpen: return Complain("The door isn't open.")
            self.Open()

        #----------------
        # No Destination?
        #----------------

        # You can't go through if the Destination property isn't set.

        if not self.Destination:
            return Complain("The door doesn't lead anywhere.")

        #-----------------------
        # Too big to go through?
        #-----------------------

        # You can't go through if you're too fat :-).

        if Visitor.Bulk > self.MaxBulk:
            Complaint = Visitor.TheDesc() + " won't fit through " + self.TheDesc() + "."
            return Complain(Complaint)

        #-----------------------------------------
        # Pass Enter() request to destination room
        #-----------------------------------------

        # Pass the movement request to the destination room. You can't go
        # through if the room at the other end won't let you in.

        return self.Destination.Enter(Visitor)
    
    def Open(self, IsSecondTime=FALSE):
        """Open the door"""

        # IsSecondTime will be false if this is the side of the door the actor
        # is on.  It will be true for the Open command that is passed to the
        # other side of the door.

        # First open this side of the door
        if ServiceOpenable.Open(self, Silent=IsSecondTime):
            # Now, if the door's other side exists and still needs to
            # be opened, open it too.
            if not IsSecondTime and self.OtherSide:
                self.OtherSide.Open(IsSecondTime=TRUE)
            return SUCCESS
        else:
            return FAILURE

    def SeeThruDesc(self):
        """
        The response to "Look thru door" when the door is open.
        """

        return ""
        

class ClassLockableDoor(ServiceLockable, ClassDoor):
    """
    A combination of ClassDoor with ServiceLockable. Doors of this class can
    be locked and unlocked, as well as opened and closed. Remeber that doors
    are always defined in pairs, one door object for each side of the door!
    """
    
    def SetMyProperties(self):
        self.IsLockable = TRUE
        self.IsLocked   = TRUE
        self.IsOpen = FALSE
        self.IsOpenable = TRUE
        self.LockOnClosing = FALSE
        self.LocksWithoutKey = FALSE

        #---------------------------
        # Transmit Locking/Unlocking
        #---------------------------

        # TransmitLocking and TrasmitUnlocking control whether locking and
        # unlocking events are automatically transmitted to the other side of
        # the door.  For example, if you lock the door to my house from the
        # inside, it automatically becomes locked on the outside as well.  But
        # if you lock an emergency exit from the outside, it would still be
        # unlocked from the inside (so TransmitLocking should be FALSE).
        # TransmitUnlocking does the same thing for unlocking the door.

        self.TransmitLocking = TRUE
        self.TransmitUnlocking = TRUE

        #--------------------
        # Unlocks Without Key
        #--------------------
        
        # All interior locks work without a key, your apartment door, for 
        # instance.
        
        self.UnlocksWithoutKey = FALSE
    
    def Close(self, IsSecondTime=FALSE):
        """
        This method basically calls the ClassDoor method and (if 
        LockOnClosing is TRUE) calls the Lock() method.
        """

        # Pass the closing request on to the superclass.  If you succeed
        # in closing the door, and if the door is supposed to lock automatically,
        # then lock it too.

        if not ClassDoor.Close(self, IsSecondTime): return TURN_CONTINUES

        if self.LockOnClosing:
            self.Lock(key=self.Key, IsSecondTime=IsSecondTime)

        return TURN_ENDS

    def DoorIsLockedDesc(self):
        return self.TheDesc() + " is locked."
    def Lock(self, key=None, IsSecondTime=FALSE):
        # Try to lock this side of the door
        if ServiceLockable.Lock(self, key, Silent=IsSecondTime):
            # If appropriate, try to lock the other side of the door.
            # Cheat and use whatever key is necessary.
            if self.TransmitLocking and not IsSecondTime and \
               isinstance(self.OtherSide, ServiceLockable):
                self.OtherSide.Lock(self.OtherSide.Key, IsSecondTime=TRUE)
            return TURN_ENDS
    
    def Open(self, IsSecondTime=FALSE):
        """Open the door"""

        # IsSecondTime will be false if this is the side of the door the actor
        # is on.  It will be true for the Open command that is passed to the
        # other side of the door.

        if self.IsLocked:
            return Complain(self.DoorIsLockedDesc())
        else:
            return ClassDoor.Open(self, IsSecondTime)

    def Unlock(self, key=None, IsSecondTime=FALSE):
        
        #---------------------------------
        # Fail If This Side Doesn't Unlock
        #---------------------------------

        if not ServiceLockable.Unlock(self, key, Silent=IsSecondTime):
            return TURN_CONTINUES
            
        #----------------------------
        # Unlock Other Side If Needed
        #----------------------------

        if self.TransmitUnlocking and not IsSecondTime and isinstance(self.OtherSide, ServiceLockable):
           self.OtherSide.Unlock(self.OtherSide.Key, IsSecondTime=TRUE)

        #---------------
        # Return Success
        #---------------

        return TURN_ENDS

class ClassUnderHiderItem (ServiceRevealWhenTaken, ClassItem):
    """
    This class is used to create takeable items that reveal other items
    under them when taken. You'll note how simple the class is, we basically
    just set properties. This class is just a standard ClassItem with a
    service called ServiceRevealWhenTaken.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ContainerPrepositionStatic = "under"
        self.ContainerPrepositionDynamic = "under"

class ClassBehindHiderItem(ServiceRevealWhenTaken,ClassItem):
    """
    This class reveals objects hiden behind it when taken. Like the
    ClassUnderHiderItem it's just a standard ClassItem with the 
    ServiceRevealWhenTaken. The only difference between this class and
    the ClassUnderHiderItem is the setting of the ContainerPreposition
    properties.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ContainerPrepositionStatic = "behind"
        self.ContainerPrepositionDynamic = "behind"


class ClassActivatableItem(ServiceActivation, ClassItem):
    """
    This class is used to create items that can be activated/deactivated,
    (such as light sources, electrical devices, etc). It allows limited
    life devices and automatic deactivation of devices that run out of
    power/fuel.

    As is, the class is skewed toward light sources such as torches,
    candles, flashlights, etc, but simply rewording a couple of string
    properties allow it to be used for all sorts of devices.

    Note this class exists primarily to combine the Activation service with
    the ClassItem class, as such it has no properties or methods so to
    satisfy the needs of the Python interpreter we create a
    SetMyProperties() method that simply executes a pass command
    (which does absolutely nothing).
    """
    def SetMyProperties(self):
        """Sets default instance properties"""
        pass

class ClassOpenableItem(ServiceOpenable, ClassItem):
    """
    This class is used to create items that can be opened/closed (such as
    boxes). Although all items can potentially contain other items openable
    items are complex enough to be interesting.

    Note this class exists primarily to combine the Openable service with
    the ClassItem class, as such it has no properties or methods so to
    satisfy the needs of the Python interpreter we create a
    SetMyProperties() method that simply executes a pass command
    (which does absolutely nothing).
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        pass

class ClassShelf(ServiceContainOn,ClassScenery):
    """
    Shelves are objects on which other objects can be placed. Objects on a
    shelf are automatically visible when the shelf is described.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        pass

class ClassContainer(ServiceContainIn,ClassItem):
    """
    Containers are objects into which other objects can be placed. Objects
    in a container are NOT automatically visible when the container is
    described, only when it's looked into.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        pass

#********************************************************************************
#                U N I V E R S E   V E R B   C L A S S E S
#
C="""
  All verbs are arranged alphabetically to make them easier to find, however
  major verb classes (ClassBasicVerb, ClassSystemVerb, etc) are arranged
  first, hierarchically.
 
  Remember, these are the BLUEPRINTS for the verbs. The actual verbs
  themselves (vocabulary) are defined lower down in the file.
  """

class ClassBasicVerb(ClassBaseVerbObject):
    """
    Basic verb for Universe. All verbs descend from this class.
    
    This class extends PAWS ClassBaseVerbObject. It handles specific
    disambiguation for most verbs, although some verbs might override
    it.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ExpectedPreposition = "inside"

    def SanityCheck(self):
        """
        By default the sanity check is simply if the verb can be performed
        in the dark, or if the current actor's location has light. Otherwise
        # we complain and return FALSE.
        """
        
        #--------------------
        # Twilight Zone Check
        #--------------------

        # If, for whatever reason the current actor is in the twilight zone
        # (Location == None) return SUCCESS, since the twilight zone should have
        # light.
        #
        # P.S. Don't ask. This test is from the very early development days and
        # handles truly bizarre coding by the game author...

        if P.CA() == None: return SUCCESS
        if P.CA().Where() == None: return SUCCESS
         
        #----------------
        # Check for light
        #----------------

        LightHere = P.CA().Where().CurrentlyIlluminated()

        if LightHere or self.OkInDark:
            return SUCCESS
        else:
            return Complain(P.AP().TooDark)
            
    def SpecificDisambiguate(self):
        """
        This is where the rubber hits the road when it comes to figuring out
        what objects are acceptable to a verb and which aren't. This default
        method may be overridden or extended by different verbs.

        Basically it performs the following checks:
    
        1) Is the actor actually an actor?
        2) Is a given object allowed with the verb?
        3) Is it remembered (actor knows about it)?
        4) Is it visible?
        5) Is it reachable?
    
        If any of these checks fail for a specific object, that object is
        discarded. If all ambiguous objects for a given noun are discarded
        the ErrorMethod for those objects is said.
    
        Once the disambiguation is completed, any ambiguous objects still
        remaining are merged into the non-ambiguous object list. For
        instance, if the bone and brass keys are both present, visible, and
        reachable and the player says "get key", then BOTH keys will be
        taken. If the player wants to deal with a specific key they can
        type "get brass key" instead of just "get key".
        """
        
        #---------------------
        # Create Actor Synonym
        #---------------------

        # The actor is needed in several pieces of code, so we create a
        # synonym. P.CA() is the current actor in the parser object.

        Actor = P.CA()
        
        #--------------------
        # Perform Actor Check
        #--------------------

        # If the object being addressed as an actor (the object the player is
        # telling to do something) isn't really an actor then return a failure
        # code, which aborts the command.

        if not Actor.CheckActor():
            return FAILURE
        
        #-----------------------------------------
        # Remove Unallowed Direct/Indirect Objects
        #-----------------------------------------

        # Notice how we placed the arguments on several lines? This is legal
        # because Python ignores whitespace between the parentheses of a
        # tuple. (A tuple is any group of comma seperated things between
        # parentheses).

        DebugTrace("Testing Allowed Objects")

        if not DisambiguateListOfLists(P.DOL(),
                                       ClassBasicThing.AllowedByVerbAsDObj,
                                       ClassBasicThing.NotWithVerbDesc):
            return FAILURE

        if not DisambiguateListOfLists(P.IOL(),
                                       ClassBasicThing.AllowedByVerbAsIObj,
                                       ClassBasicThing.NotWithVerbDesc):
            return FAILURE

        
        #-----------------------------------------
        # Remove Invisible Direct/Indirect Objects
        #-----------------------------------------

        DebugTrace("Testing Visible Objects")

        if not DisambiguateListOfLists(P.DOL(),
                                       ClassBasicThing.IsVisible,
                                       ClassBasicThing.CantSeeDesc,
                                       Actor):
            return FAILURE

        if not DisambiguateListOfLists(P.IOL(),
                                       ClassBasicThing.IsVisible,
                                       ClassBasicThing.CantSeeDesc,
                                       Actor):
           return FAILURE
        
        #-------------------------------------------
        # Remove Unreachable Direct/Indirect Objects
        #-------------------------------------------

        DebugTrace("Testing Reachable Objects")

        if not DisambiguateListOfLists(P.DOL(),
                                       ClassBasicThing.IsReachable,
                                       ClassBasicThing.CantReachDesc,
                                       Actor):
           return FAILURE

        if not DisambiguateListOfLists(P.IOL(),
                                       ClassBasicThing.IsReachable,
                                       ClassBasicThing.CantReachDesc,
                                       Actor):
           return FAILURE

        
        #---------------------------------------
        # Remove Unknown Direct/Indirect Objects
        #---------------------------------------

        DebugTrace("Testing Known Objects")

        if not DisambiguateListOfLists(P.DOL(),
                                       ClassBasicThing.Remembers,
                                       ClassBasicThing.AmnesiaDesc,
                                       Actor):
            return FAILURE

        if not DisambiguateListOfLists(P.IOL(),
                                       ClassBasicThing.Remembers,
                                       ClassBasicThing.AmnesiaDesc,
                                       Actor):
            return FAILURE

        
        #-------------------------------------
        # Gather Parser Favored Objects If Any
        #-------------------------------------

        DebugTrace("Testing Favored Objects")
        List = P.DOL()[:]

        if DisambiguateListOfLists(List,
                                   ClassBasicThing.Favored,
                                   ClassBasicThing.NoDesc):
            P.AP().CurrentDObjList = List[:]


        List = P.IOL()[:]

        if DisambiguateListOfLists(List,
                                   ClassBasicThing.Favored,
                                   ClassBasicThing.NoDesc):
           P.AP().CurrentIObjList = List[:]
        
        #----------------------------------
        # Merge remaining ambiguous objects
        #----------------------------------

        # If any objects are still ambiguous, give it up. Merge them into the
        # unambiguous list. Basically we create a list, using Union if the list
        # item is a list, or append if it's a single object. We then copy our
        # resulting list back to the original list.

        #---------------------
        # Merge Direct Objects
        #---------------------

        List = []
        for Object in P.DOL():
            if type(Object) == type([]):
                List = Union(List,Object)
            else:
                List.append(Object)

        Global.CurrentDObjList = List

        #-----------------------
        # Merge Indirect Objects
        #-----------------------

        List = []
        for Object in P.IOL():
            if type(Object) == type([]):
                List = Union(List,Object)
            else:
                List.append(Object)

        Global.CurrentIObjList = List
        
        #----------------------------
        # Check for ONE direct object
        #----------------------------

        # If the verb allows one direct object, and either no direct direct 
        # objects were used or more than 1 direct object is left we complain and
        # return failure. This insures the Execute() method won't call the verb's
        # action.

        if len(P.DOL()) > 1 and (self.ObjectAllowance & ALLOW_ONE_DOBJ):
            return Complain(P.AP().OnlyOneDObj)
        
        #------------------------------
        # Check for ONE indirect object
        #------------------------------

        # If the verb allows one indirect object, and either no indirect objects
        # were used we complain and return failure. This insures the Execute()
        # method won't call the verb's action.

        if len(P.IOL()) > 1 and (self.ObjectAllowance & ALLOW_ONE_IOBJ):
            return Complain(P.AP().OnlyOneIObj)
        
        #----------------------------
        # Check for NO direct object
        #----------------------------

        # If no direct objects are left but one or more was expected, say
        # a complaint (Dig what? Take what?) and return FAILURE.

        if len(P.DOL())==0 and not \
           (self.ObjectAllowance & ALLOW_OPTIONAL_DOBJS):
            if not (self.ObjectAllowance & ALLOW_NO_DOBJS):
                if len(P.AP().CurrentPrepList) == 0:
                    return Complain(SCase("what would you like to " + P.CVN() + "?"))
                else:
                    return Complain(SCase("what would you like to " +P.CVN() + " " + \
                                          string.join(P.AP().CurrentPrepList) + "?"))

        
        #-----------------------------
        # Check for NO indirect object
        #-----------------------------

        # If no indirect objects are left but one or more was expected, say
        # a complaint (Dig what? Take what?) and return FAILURE.

        if len(P.IOL()) == 0:
            if not (self.ObjectAllowance & ALLOW_NO_IOBJS):
                return Complain(SCase(P.CVN() + " " + \
                                      P.DOL()[0].NamePhrase + " " + \
                                      string.join(P.AP().CurrentPrepList) + \
                                      " what?"))

        
        #-----------------
        # Congratulations!
        #-----------------

        # If you got this far you've got a disambiguated list of direct and 
        # indirect objects and can now perform a sanity check.

        return SUCCESS

class ClassSystemVerb(ClassBasicVerb):
    """
    System verbs are just basic verbs that are OK to use in the dark. We set
    up a special class simply to save us the effort of setting each and
    every system verb's OkInDark property to true.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.OkInDark = TRUE
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS

class ClassTravelVerb(ClassBasicVerb):
    """
    Travel verbs are: up, down, north, etc. This verb's action basically
    finds the room or string in the current actor's location map and either
    enters the room or (if a string) says it and returns FAILURE.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.TravelDirection = None
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    def Action(self):
        """Action for this verb."""
        
        if P.CA().Where() == None: return TURN_ENDS
        return P.CA().Travel(self.TravelDirection)


class ClassActivateVerb(ClassBasicVerb):
    """
    This verb allows the player to activate an object (usually a light
    source). The way we define LightWithVerb below is interesting, notice
    the change to ObjectAllowance. LightWithVerb otherwise uses the standard
    ClassActivateVerb.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE   # most definitely!
    
    def Action(self):
        Multiple = len(P.DOL()) > 1

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            if hasattr(Object, Object.ActivationProperty):
                Object.Activate(Multiple)

        return TURN_CONTINUES
        
class ClassCloseVerb (ClassBasicVerb):
    """Defines a verb to close an object."""
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE
    
    def Action(self):

        Multiple = (len(P.DOL()) > 1)

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()

            if not hasattr(Object, "Close"):
                return Complain("I don't know how to close %s." % Object.ADesc())

            Object.Close(Multiple)

        return TURN_CONTINUES

class ClassConfigureTerminalVerb(ClassSystemVerb):
    """Configure Terminal verb"""
    
    def Action(self):
        """Action performed for Configure Terminal"""

        Terminal.Configure()

        #----------------------
        # Return TURN_CONTINUES
        #----------------------

        return TURN_CONTINUES

class ClassDeactivateVerb (ClassBasicVerb):
    """
    This verb allows the player to deactivate an object (usually a light
    source). Note how we create Extinguish with by merely changing the
    verb's ObjectAllowance property.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE   # inconceivable, but might as well allow it
    
    def Action(self):

        Multiple = len(P.DOL()) > 1

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            if hasattr(Object, Object.ActivationProperty):
                Object.Deactivate(Multiple)

        return TURN_CONTINUES

class ClassDebugVerb(ClassSystemVerb):
    """
    Toggles debug mode.
    """

    def Action(self):
        """Debug action"""

        if Global.Production:
            return Complain("Debug is only active in TEST versions of this game.")
        else:
            Say("Debug verb is active")

        Global.Debug = not Global.Debug

        if Global.Debug:
            Say("Debug is ON")
        else:
            Say("Debug is OFF")

        return TURN_CONTINUES

class ClassDropVerb(ClassBasicVerb):
    """
    This verb allows actors to drop things they're carrying. Notice how this
    verb has synonyms, "drop/release" or "set down/throw down". To do this
    we instantiated a second verb with the ClassDropVerb class to handle
    the "down" preposition.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    def Action(self):
        """
        This action does a great deal without appearing to. Let's examine
        the coding tricks used.
        """

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------
        
        # If the player drops a rock the computer will say "Dropped". But if the
        # player drops a rock and a coin the computer will say:
        #
        # Rock: Dropped.
        # Coin: Dropped.
        #
        # The secret lies in the Multiple argument passed to the object's Drop
        # method. We use an "implied if" coding trick to make the code 1 line
        # instead of 5!
        #
        # If you examine the expression you see it's the same one you'd
        # put on an if test. The expression evaluates to 1 or 0, in other words,
        # TRUE or FALSE

        Multiple = (len(P.DOL()) > 1)

        #----------------------------------
        # For each direct object in command
        #----------------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            if hasattr(Object,"Drop"): Object.Drop(Multiple)

        return TURN_CONTINUES
    
    def SanityCheck(self):
        """Sanity declares drop all would be actor's contents"""    

        #------------------------
        # Reassign "Them" Pronoun
        #------------------------
    
        # Normally "Them" refers to the ROOM'S contents. However, if you're
        # dropping something then "Them" (aka "all" or "everything") should
        # refer to the CURRENT ACTOR'S contents.

        P.AP().PronounsDict[THEM] = P.CA().Contents

        #-------------------------------
        # Call The "normal" Sanity Check
        #-------------------------------
    
        # The normal check for sanity is found in ClassBasicVerb, so return the
        # result of that sanity check. This insures that sanity runs in the 
        # family... :)

        return ClassBasicVerb.SanityCheck(self)
    
class ClassFeelVerb(ClassBasicVerb):
    """
    This verb allows actors to feel things or their location if they don't
    supply a direct object.
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS

    
    def Action(self):

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0:
            P.CA().Where().DescribeSelf("FEEL")
            return TURN_ENDS

        #----------------------------
        # One or more direct objects?
        #----------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("FEEL")

        return TURN_CONTINUES

class ClassGoVerb(ClassBasicVerb):
    """Creates verb for go/walk/run/climb command."""
    
    #---------------
    # Set Properties
    #---------------

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    def Action(self):
        """
        Go action. This verb can respond appropriately to "go" or "go east
        west" or "go east" (complaining in the first two instances).
        """

        #----------------------------------
        # No direction/multiple directions?
        #----------------------------------

        if len(P.DOL()) == 0: return Complain("Which way?")
        if len(P.DOL()) > 1:  return Complain("Make up your mind!")

        #--------------------
        # Travel in direction
        #--------------------

        return P.CA().Travel(Global.CurrentDObjList[0])

class ClassHelloVerb(ClassBasicVerb):
    """Creates verb to handle Hello."""
    
    def SetMyProperties(self):
        """Sets default instance properties"""

        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + \
                               ALLOW_NO_IOBJS + \
                               ALLOW_OPTIONAL_DOBJS

        self.OkInDark = TRUE
    
    def Action(self):
        """Hello Action"""

        if len(P.DOL()) == 0:
            if P.CA() == Global.Player:
                return Complain("Taking to yourself?")
            else:
                Say(P.CA().HelloDesc())
                return TURN_ENDS

        #----------------------------
        # One or more direct objects?
        #----------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("HELLO")

        return TURN_ENDS

class ClassHelpVerb(ClassSystemVerb):
    """Help Verb"""

    def Action(self):
        """Help action"""

        Say(Game.HelpText)
        return TURN_ENDS

class ClassInsertVerb (ClassBasicVerb):
    """Defines a verb to put an object into a container."""
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_ONE_IOBJ
        self.OkInDark = TRUE
        self.ExpectedPreposition = "inside"
    
    def Action(self):
        Multiple = len(P.DOL()) > 1
        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.Insert(P.IOL()[0],Multiple)

        return TURN_CONTINUES

class ClassInventoryVerb(ClassSystemVerb):
    """
    This verb allows actors to take inventory.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    def Action(self):
        """Take inventory"""
        P.CA().DescribeSelf("CONTENT")
        return TURN_CONTINUES

class ClassListenVerb(ClassBasicVerb):
    """
    This verb allows actors to listen to their location. A different verb
    (ListenToVerb) is used to listen to objects.
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    def Action(self):
        """Listen (to location) action"""

        P.CA().Where().DescribeSelf("SOUND")
        return TURN_ENDS

class ClassListenToVerb(ClassBasicVerb):
    """
    This verb allows actors to listen to things (but NOT their location,
    see ListenVerb above).
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE

    def Action(self):
        """Listen To action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0: return Complain("Listen to what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("SOUND")

        return TURN_ENDS

class ClassLockVerb(ClassBasicVerb):
    """Defines a verb to lock an object (that doesn't require a key."""
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_NO_IOBJS
        self.OkInDark = TRUE
    
    def Action(self):
        DirectObject = P.DOL()[0]
        DirectObject.MakeCurrent()
        Object.MarkPronoun()

        if not hasattr(DirectObject, "Lock"):
            return Complain("I don't know how to lock " + DirectObject.ADesc())

        return DirectObject.Lock(None)

class ClassLockWithVerb(ClassBasicVerb):
    """Defines a verb to lock an object (that requires a key)."""

    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_ONE_IOBJ
        self.OkInDark = TRUE

    
    def Action(self):
        DirectObject = P.DOL()[0]
        IndirectObject = P.IOL()[0]
        DirectObject.MakeCurrent()
        Object.MarkPronoun()

        if not hasattr(DirectObject, "Lock"):
            return Complain("I don't know how to lock " + DirectObject.ADesc())

        return DirectObject.Lock(IndirectObject)

class ClassLookVerb(ClassBasicVerb):
    """Handles Look command"""

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_NO_DOBJS + ALLOW_NO_IOBJS

    def Action(self):
        """Look action"""
        
        #--------------------------
        # Force Temporary Verbosity
        #--------------------------

        # The look command says the FULL room description, regardless of the
        # current verbosity (or visited status) of the room. However, we can't
        # simply turn on the verbosity flag, that might contradict the player's
        # desire (always rude!)
        #
        # So we save the old verbosity setting before turning verbosity on.

        OldVerbosity = Global.Verbose
        Global.Verbose = TRUE
        
        #----------------------
        # Call Room Description
        #----------------------

        # The SmartDescribeSelf method for a room describes the room completely,
        # it's the same method used when a player enters a room.

        P.CA().Where().SmartDescribeSelf()
        
        #----------------------
        # Restore Old Verbosity
        #----------------------

        # Now that we are done it's time to put away our toys. We restore the
        # global verbosity flag to the value it was before we turned it on.
        #
        # This brings up an important point. If you plan to change a global
        # setting (like Global.Verbose) it's a good idea to save the orignal
        # setting so you can restore it when you're finished. This is espcially
        # important if your change is temporary.

        Global.Verbose = OldVerbosity

        return TURN_ENDS

class ClassLookAtVerb(ClassBasicVerb):
    """
    This verb allows actors to look at things (but NOT their location, see
    LookVerb above).
    """
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS

    def Action(self):
        """Look At action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0: return Complain("Look at what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("LONG")

        return TURN_ENDS

class ClassLookDeepVerb(ClassBasicVerb):
    """
    Look deep action (Look into/under/behind).
    """

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_NO_IOBJS
        self.OkInDark = FALSE
        self.ExpectedPreposition = "inside"

    
    def Action(self):
        Multiple = len(P.DOL()) > 1

        #-----------------------
        # For Each Direct Object
        #-----------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.LookDeep()

        return TURN_ENDS

class ClassQuitVerb(ClassSystemVerb):
    """Quit verb"""

    def Action(self):
        """Action performed for Quit"""

        #------------------------------
        # Change Game State To Finished
        #------------------------------

        # If you examine the game loop code you notice the WHILE loop runs
        # until the game's state changes to FINISHED. This is the code that
        # changes the game state to finished.

        Global.GameState = FINISHED

        #----------------------
        # Return TURN_CONTINUES
        #----------------------
        
        # Why TURN_CONTINUES, why not TURN_ENDS?
        #
        # Remember, the Action method returns whatever you want TurnHandler
        # to return. If the TurnHandler gets TURN_CONTINUES, the AfterTurnHandler
        # won't run.
        #
        # If we're quitting the game we want to quit RIGHT NOW, we don't want
        # any additional turn handling to occur. This is true of any game
        # controlling verb (quit, save, restore, etc).

        return TURN_CONTINUES

class ClassOpenVerb (ClassBasicVerb):
    """Open Verb"""
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS
        self.OkInDark = TRUE
    
    def Action(self):

        Multiple = (len(P.DOL()) > 1)

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()

            if not hasattr(Object, "Open"):
                return Complain("I don't know how to open " + Object.ADesc())

            Object.Open(Multiple)

        return TURN_CONTINUES

class ClassReadVerb(ClassBasicVerb):
    """Read Verb"""

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_NO_IOBJS

    def Action(self):
        """Read action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0: return Complain("Read what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("READ")

        return TURN_ENDS

class ClassRestoreVerb(ClassSystemVerb):
    """Restore verb"""

    def Action(self):
        """Action performed for Restore"""

        #---------------
        # Restore Global
        #---------------
        
        # Toggle the transcribe property (which controls logging). If it was 
        # saved as TRUE set it to FALSE, if it was FALSE set it to TRUE. Then
        # call the Transcribe verb action, just as if the player had typed 
        # TRANSCRIBE. That will *re*-toggle the transcription. The end result 
        # will be if the game was saved with logging turned on, logging will be
        # turned on, and if the game was saved with logging turned off, then
        # logging will be turned off.

        if Engine.RestoreFunction(Global.GameModule):
            Global.Transcribe = not Global.Transcribe
            TranscribeVerb.Action()
            Say("Restored")
                                        
        #----------------------
        # Return TURN_CONTINUES
        #----------------------

        return TURN_CONTINUES

class ClassSaveVerb(ClassSystemVerb):
    """Save verb"""

    def Action(self):
        """Action performed for Save"""

        if Engine.SaveFunction(Global.GameModule):
            Say("Saved")

        #----------------------
        # Return TURN_CONTINUES
        #----------------------

        return TURN_CONTINUES

class ClassSayVerb(ClassBasicVerb):

    def SetMyProperties(self):
        """Sets default instance properties"""

        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + \
                               ALLOW_NO_IOBJS + \
                               ALLOW_OPTIONAL_DOBJS
                               
        self.OkInDark = TRUE
   
    def Action(self):
        """Say action"""
        if not Global.Debug:
            P.AP().SaidText = string.replace(P.AP().SaidText,"{","[")
            P.AP().SaidText = string.replace(P.AP().SaidText,"}","]")

        Say(P.AP().SaidText[len(self.NamePhrase):])
        return TURN_CONTINUES

class ClassScoreVerb(ClassSystemVerb):
    """Scoring verb"""

    def Action(self):
        """Action performed for Score"""

        #------------------------
        # Display Score To Player
        #------------------------

        # Notice we use the str() function to convert the numeric score into a
        # string that the % function can handle properly.

        Say("Your score is %s points out of a possible %s." % \
           (str(Global.CurrentScore),str(Global.MaxScore)))

        #----------------------
        # Return TURN_CONTINUES
        #----------------------

        return TURN_CONTINUES
        
class ClassSmellVerb(ClassBasicVerb):
    """Sniff Verb"""

    def SetMyProperties(self):
        """Sets default instance properties"""

        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + \
                               ALLOW_NO_IOBJS + \
                               ALLOW_OPTIONAL_DOBJS

        self.OkInDark = TRUE

    def Action(self):
        """Smell/Sniff action"""

        if len(P.DOL()) == 0:
            P.CA().Where().DescribeSelf("ODOR")
            return TURN_ENDS


        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("ODOR")

        return TURN_CONTINUES

class ClassTakeVerb(ClassDropVerb):
    """Handles Take/Pick Up command."""

    def Action(self):
        """Take action"""

        #--------------------
        # No Direct Objects?
        #--------------------
        
        if len(P.DOL()) == 0: return Complain("Take what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------
        
        # If the player drops a rock the computer will say "Taken". But
        # if the player drops a rock and a coin the computer will say:
        #
        # Rock: Taken.
        # Coin: Taken.
        #
        # The secret lies in the Multiple argument passed to the object's
        # Take method. We use an "implied if" coding trick to make the code
        # 1 line instead of 5!
        #
        # If you examine the expression you see it's the same one you'd
        # put on an if test. The expression evaluates to 1 or 0, in other
        # words, TRUE or FALSE

        Multiple = (len(P.DOL()) > 1)

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            if hasattr(Object,"Take"): Object.Take(Multiple)

        return TURN_CONTINUES

class ClassTasteVerb(ClassBasicVerb):
    """Taste Verb"""

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + \
                               ALLOW_NO_IOBJS + \
                               ALLOW_OPTIONAL_DOBJS
    
    def Action(self):
        """Taste action"""

        #------------
        # No Objects?
        #------------

        if len(P.DOL()) == 0: return Complain("Taste what?")

        #-------------------------
        # Multiple Direct Objects?
        #-------------------------

        for Object in P.DOL():
            Object.MakeCurrent()
            Object.MarkPronoun()
            Object.DescribeSelf("TASTE")

        return TURN_CONTINUES
                
class ClassTerseVerb(ClassSystemVerb):
    """Sets game to play in terse (default) mode."""

    def Action(self):
        Global.Verbose = FALSE
        Say("Show Brief descriptions on return visits.")
        return TURN_CONTINUES

class ClassTranscribeVerb(ClassSystemVerb):
    """Toggle Logging On/Off Verb"""

    def Action(self):
        """Transcribe action"""

        Global.Transcribe = not Global.Transcribe

        if Global.Transcribe:
            Global.LogFile = open(Global.GameModule+".log","a")
            Global.DebugFile = open(Global.GameModule+".dbg","a")
            Say("""
                Logging turned ON. Transcripts appear in %s.log and debugging 
                information appears in %s.dbg.
                """ % (Global.GameModule.encode(), Global.GameModule.encode()))
        else:
            try:
                Global.DebugFile.close()
                Global.LogFile.close()
            except:
                pass
            Say("Logging turned OFF")

        return TURN_CONTINUES

class ClassUnlockVerb(ClassBasicVerb):
    """Defines a verb to unlock an object."""

    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_NO_IOBJS
        self.OkInDark = TRUE
    
    def Action(self):
        DirectObject = P.DOL()[0]
        IndirectObject = P.IOL()[0]

        DirectObject.MakeCurrent()
        Object.MarkPronoun()

        if not hasattr(DirectObject, "Unlock"):
            return Complain("I don't know how to unlock " + DirectObject.ADesc())

        return DirectObject.Unlock(IndirectObject)

class ClassUnlockWithVerb(ClassBasicVerb):
    """Unlock With Verb."""
    
    def SetMyProperties(self):
        """Sets default instance properties"""
        self.ObjectAllowance = ALLOW_ONE_DOBJ + ALLOW_ONE_IOBJ
        self.OkInDark = TRUE
            
    def Action(self):
        DirectObject = P.DOL()[0]
        IndirectObject = P.IOL()[0]

        DirectObject.MakeCurrent()
        Object.MarkPronoun()

        if not hasattr(DirectObject, "Unlock"):
            return Complain("I don't know how to unlock " + DirectObject.ADesc())

        return DirectObject.Unlock(IndirectObject)

class ClassVerboseVerb(ClassSystemVerb):
    """Sets game to play in verbose mode."""

    def Action(self):
        Global.Verbose = TRUE
        Say("Show full descriptions on return visits. ~n")
        P.CA().Where().SmartDescribeSelf()
        return TURN_CONTINUES

#********************************************************************************
#                        U N I V E R S E   D A T A
#
C="""
  With the exception of the direction objects needed for ClassRoom, we
  haven't set any data or defined any objects yet. In this section we set a 
  couple of variables and replace some Engine methods with new ones.
  """

#--- Universe Copyright - Don't change this!

UniverseCopyright = """
                    Copyright (c) 1998 - 2008 by Roger Plowman and Kevin
                    Russell
                    """


#--- Universe Version - Don't change this!

UniverseVersion = "2.03"

#--- Replace Build Status Line And Set Up Game Methods

Engine.BuildStatusLine = Universe_BuildStatusLine
Engine.SetUpGame = Universe_SetUpGame

#********************************************************************************
#                       P A R S E R   E X T E N S I O N S
#
C="""
  In this section we append new properties to the Parser object, which you
  can freely use just as though they were added in the Core.py module. This
  hides the internal workings of the parser from the game author (you) so
  you don't have to worry which parts are from Core and which parts are from 
  Universe.
 
  P.AP() is a reference to the parser, AP() stands for Active Parser.
  Although Universe does not replace the parser (merely extends it), it is
  entirely possible to override the Core parser with one of your own
  construction, although this is a job for professionals!
  """

P.AP().Nonsense = "That doesn't make sense."
P.AP().NotADirection = "{You()} can't go that way!"
P.AP().NotAnActor = "You have lost your mind."
P.AP().ObjectNotHere = "There's no %s here."
P.AP().OnlyOneDObj = "You can only use one direct object with this verb."
P.AP().OnlyOneIObj = "You can only use one indirect object with this verb."
P.AP().TooDark = "It's too dark to see how."

#********************************************************************************
#                G L O B A L   O B J E C T   E X T E N S I O N S
#
C="""
  In this section we append new properties to the Global object, which, like
  our additions to Parser above, the game author can use freely without
  having to worry if they're Core stuff or Universe stuff.
  """

#--- Actor List

C="""
  This list is constructed by the Engine.SetUpGame() method. It contains a 
  list of all objects that have Actor as a class. It's a quick way to limit
  your search to just actors.
  """
  
Global.ActorList = []

#--- All Objects List

C="""
  Lists all objects. Useful for scanning all objects or setting up the game
  locations.
  """

Global.AllObjectsList = []

#--- Current Score

C="""
  You guessed it, the player's current score. This is the value displayed on
  the status line.
  """

Global.CurrentScore = 0

#--- Current Turn

C="""
  This is the turn count displayed on the status line, it controls fuses,
  daemons, etc.
  """
Global.CurrentTurn = 0

#--- Floating Location Object List

C="""
  This list is constructed by the CEngine.SetUpGame() method. It contains a
  list of all "floating location" objects. A floating location object is one
  that has no fixed location, it can move with the player.

  Floating objects are handy for creating floors, ceilings, walls, etc. 
  They're kind of like Scenery for the Me object, invisible but always
  around so the player can say things like "Climb walls".
  """
  
Global.FloatingLocationList = []

#--- Item List

# Lists all Item (takeable) objects. Useful for the "take/drop all" pronoun.

Global.ItemList = []

#--- Light Source List

C="""
  This list is constructed by the Engine.SetUpGame() method. It contains a 
  list of all objects that have a true IsLightSource property. This list is
  used anywhere we need to scan a list of light sources.
  """

Global.LightSourceList = []

#--- Lit Parent List

C="""
  This list is maintained by the AfterTurnHandler, it contains a list of
  all parent objects (containers or rooms) that are illuminated by a light
  source--excluding naturally lit rooms like the outdoors, or a room with
  a window to the outdoors.
  """

Global.LitParentList = []

#--- Maximum Score

# You guessed it, the player's maximum (winning) score.

Global.MaxScore = 0

#--- Restarting Game?

C="""
  This is either true or false, it's used by certain commands to know
  whether or not the game is in the process of being restarted.
  """

Global.Restarting = FALSE

#--- Scenery List

# Lists all scenery (non-takable) objects.

Global.SceneryList = []

#--- Verbose

C="""
  Verbose is either TRUE or FALSE. If true then room long descriptions will
  always be said whether or not the player has already been in the room. The
  default is FALSE, so the long description is only said # the first time
  the player vists a room, or types "look".
  """
  
Global.Verbose = FALSE

#--- Verb Agreement Dictionary For Irregular Verbs

C="""
  VerbAgreementTable is a dictionary of the verb forms that can't be
  predicted by the general rule and have to be listed.  The agree()
  procedure will first check to see if the verb it's dealing with is in
  VerbAgreementTable and will only apply the regular rule if it's not.
  """
  
Global.VerbAgreementDict = {"be":             ["are", "is"],
                            "do":             ["do", "does"],
                            "go":             ["go", "goes"],
                            "have":           ["have", "has"],
                            "contractedbe":   ["'re", "'s"],
                            "contractedhave": ["'ve", "'s"]}

#--- Compass Direction List

C="""
  This list contains 8 directions. These directions are actually objects
  defined above. They represent the 8 horizontal compass points, and are 
  used mainly to set the DefaultMap horizontal directions to the same error
  message (see DefaultMap below).

  Notice directions are listed starting with north and continuing in a
  clockwise circle. Thus North is always 0, Northwest is always 7.

  Finally, notice we're adding this to the Global object. This lets us
  easily access it.
  """
  
Global.CompassList = [North,
                      Northeast,
                      East,
                      Southeast,
                      South,
                      Southwest,
                      West,
                      Northwest]

#--- Global Default Map

C="""
  The default map is used when a room's map doesn't contain a given
  direction. For example, when North is undefined in the room map then North
  is searched for in the default map.
 
  The default map is intended to reduce the game author's work load. You can
  define a class that changes the default map to have all eight horizontal
  directions say "There is a wall there." instead of "You can't go that
  way."
 
  The default map primarily allows a way for you to set up a default error
  message for a given direction, without having to fill each room's map over
  and over again.
 
  Notice we add this property to the global object.
   """
Global.DefaultMap = {North:      "You can't go that way.",
                     Northeast:  "You can't go that way.",
                     East:       "You can't go that way.",
                     Southeast:  "You can't go that way.",
                     South:      "You can't go that way.",
                     Southwest:  "You can't go that way.",
                     West:       "You can't go that way.",
                     Northwest:  "You can't go that way.",
                     Up:         "There's nothing climbable here.",
                     Down:       "There's no way down.",
                     Upstream:   "There's no stream here.",
                     Downstream: "There's no stream here.",
                     In:         "There's nothing here to enter.",
                     Out:        "There's nothing here to exit."} 

#********************************************************************************
#                           V E R B   V O C A B U L A R Y
#
C="""
  Now that we've created all the verb blueprints, it's time to actually
  create the vocabulary words for verbs.
 
  Certain verbs require more than a vocabulary definition. Travel verbs, for
  example also need to know the direction object that's associated with the
  verb. 
 
  Other verbs may need to update the Global object or the parser. All verbs
  are listed alphabetically so you can find them easily.
  """

AgainVerb = ClassSystemVerb("g,again")
P.AP().Again = AgainVerb
ClimbVerb = ClassGoVerb("climb")
CloseVerb = ClassCloseVerb("close,shut")
ConfigureTerminalVerb = ClassConfigureTerminalVerb("configure","terminal")
DebugVerb = ClassDebugVerb("debug")
DownVerb = ClassTravelVerb("down,d,descend")
DownVerb.TravelDirection = Down
DownstreamVerb = ClassTravelVerb("downstream,ds")
DownstreamVerb.TravelDirection = Downstream
DropVerb = ClassDropVerb("drop,release")
DropDownVerb = ClassDropVerb("put,set,throw","down")
EastVerb = ClassTravelVerb("east,e")
EastVerb.TravelDirection = East
ExamineVerb = ClassLookAtVerb("examine,inspect,x")
ExtinguishVerb = ClassDeactivateVerb("deactivate,extinguish,douse")
ExtinguishWithVerb = ClassDeactivateVerb("extinguish,douse","with")
ExtinguishWithVerb.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_ONE_IOBJ
FeelVerb = ClassFeelVerb("feel,touch")
FeelAroundVerb = ClassFeelVerb("feel","around")
GoVerb = ClassGoVerb("go,walk,run,move")
GoToVerb = ClassGoVerb("go,walk,run,move","to")
GoTowardVerb = ClassGoVerb("go,walk,run,move","toward")
HangOnVerb = ClassInsertVerb("hang","on")
HangOnVerb.ExpectedPreposition = "on"
HelloVerb = ClassHelloVerb("hello,hi")
HelloThereVerb = ClassHelloVerb("hello,hi","there")
HelpVerb = ClassHelpVerb("help,assist")
InventoryVerb = ClassInventoryVerb("inventory,inven,i")
InVerb = ClassTravelVerb("in,enter,ingress")
InVerb.TravelDirection = In
LightVerb = ClassActivateVerb("light,activate")
LightVerb.ActivationProperty = "IsLit"
LightWithVerb = ClassActivateVerb("light","with")
LightWithVerb.ObjectAllowance = ALLOW_MULTIPLE_DOBJS + ALLOW_ONE_IOBJ
LightWithVerb.ActivationProperty = "IsLit"
ListenVerb = ClassListenVerb("listen")
ListenToVerb = ClassListenToVerb("listen","to")
LockVerb = ClassLockVerb("lock,latch,hook")
LockWithVerb = ClassLockWithVerb("lock","with")
LookVerb = ClassLookVerb("look,gaze,l")
LookAroundVerb = ClassLookVerb("look,l","around")
LookAtVerb = ClassLookAtVerb("look,l","at")
LookBehindVerb = ClassLookDeepVerb("look,search","behind")
LookBehindVerb.ExpectedPreposition = "behind"
LookInsideVerb = ClassLookDeepVerb("look,search","in,inside,into")
LookOnVerb = ClassLookDeepVerb("look,search","on")
LookOnVerb.ExpectedPreposition = "on"
LookUnderVerb = ClassLookDeepVerb("look,search","under,underneath,beneath")
LookUnderVerb.ExpectedPreposition = "under"
NorthVerb = ClassTravelVerb("north,n")
NorthVerb.TravelDirection = North
NortheastVerb = ClassTravelVerb("northeast,ne")
NortheastVerb.TravelDirection = Northeast
NorthwestVerb = ClassTravelVerb("northwest,nw")
NorthwestVerb.TravelDirection = Northwest
OpenVerb = ClassOpenVerb("open")
OutVerb = ClassTravelVerb("out,outside,exit")
OutVerb.TravelDirection = Out
PickUpVerb = ClassTakeVerb("pick","up")
PutBehindVerb = ClassInsertVerb("put,place,hide,set", "behind")
PutBehindVerb.ExpectedPreposition = "behind"
PutInVerb = ClassInsertVerb("put,place,insert,set","in,into,inside")
PutOntoVerb = ClassInsertVerb("put,place,pile,stack,set,use","on,onto,with")
PutOntoVerb.ExpectedPreposition = "on"
PutOutVerb = ClassDeactivateVerb("put","out")
PutUnderVerb = ClassInsertVerb("put,place,hide,set","under,underneath,beneath")
PutUnderVerb.ExpectedPreposition = "under"
QuitVerb = ClassQuitVerb("quit")
ReadVerb = ClassReadVerb("read")
RestoreVerb = ClassRestoreVerb("restore")
SaveVerb = ClassSaveVerb("save")
SayVerb = ClassSayVerb("say")
P.AP().SayVerb = SayVerb
ScoreVerb = ClassScoreVerb("score")
SmellVerb = ClassSmellVerb("smell,sniff")
SouthVerb = ClassTravelVerb("south,s")
SouthVerb.TravelDirection = South
SoutheastVerb = ClassTravelVerb("southeast,se")
SoutheastVerb.TravelDirection = Southeast
SouthwestVerb = ClassTravelVerb("southwest,sw")
SouthwestVerb.TravelDirection = Southwest
TakeVerb = ClassTakeVerb("take,get,remove,steal")
TakeInventoryVerb = ClassInventoryVerb("take","inventory")
TakeStockVerb = ClassInventoryVerb("take","stock")
TasteVerb = ClassTasteVerb("taste,lick")
TerseVerb = ClassTerseVerb("terse,brief")
TranscribeVerb = ClassTranscribeVerb("transcribe")
TurnOffVerb = ClassDeactivateVerb("turn","off")
TurnOnVerb = ClassActivateVerb("turn","on")
TurnOnVerb.ActivationProperty = "IsActivated"
UnlockVerb = ClassUnlockVerb("unlock,unhook,unlatch")
UnlockWithVerb = ClassUnlockWithVerb("unlock","with")
UpVerb = ClassTravelVerb("up,u,ascend")
UpVerb.TravelDirection = Up
UpstreamVerb = ClassTravelVerb("upstream,us")
UpstreamVerb.TravelDirection = Upstream
VerboseVerb = ClassVerboseVerb("verbose")
WestVerb = ClassTravelVerb("west,w")
WestVerb.TravelDirection = West

#********************************************************************************
#                     U N I V E R S E     O B J E C T S
#
C="""
  Like the directions defined just before ClassRoom, and the verbs defined
  immediately above, the following lines define *objects*. Game, for
  example, holds the actual game data like your name, copyright, etc.
 
  Universe uses these objects directly to impact your game. And while your
  game may replace these objects, they are still fully functional and you 
  could write a game using them.
  """
#--- Game Object

C="""
  The game object is pretty simple, really. It's used at the beginning of
  the game to print the banner, the introduction, and supply a bit of
  information. Other than that, it doesn't do anything.
  """
  
Game = ClassGameObject()

#--- Player Object

C="""
  The player object is absolutely critical. It is the represenation of the
  player in the game, literally the eyes and ears of the player. Note we 
  record the player object in Global, so it can be accessed by the Core file
  and your game file.
  """

UniverseMe = ClassPlayer("me,myself")
Global.Player = UniverseMe

#--- The Ground

C="""
  Whenever the player says something like "examine floor" or "examine
  ground" this object will use the current actor's location's GroundDesc()
  property instead. If Take or Taste is used then these descriptions are 
  used, otherwise the default descriptions assigned to BasicThing are used.
 
  Note if you want a special Ground object for certain rooms you can set the
  HasGround property to FALSE, then create (another) ground object (maybe
  MyGround or something) with a new Landmark property set to TRUE. That way
  you can implement all the sensory methods for your MyGround object.
 
  The landmark property is "HasGround".
  """

Ground = ClassLandmark("ground,floor")
Ground.Landmark = "Ground"

Ground.SetDesc("L","{P.CA().Where().GroundDesc()}")
Ground.SetDesc("Take","You must be joking.")
Ground.SetDesc("Taste","No!")
Ground.SetDesc("Feel","It feels like ordinary ground to {Me()}")

#--- No Wall

C="""
  Whenever HasWall is FALSE, this object will appear.
  """
  
NoWall = ClassLandmarkMissing("wall")
NoWall.Landmark = "Wall"
NoWall.NamePhrase = "Non-Existent Wall"

NoWall.SetDesc("L","There's no wall here.")
NoWall.SetDesc("Take","You can't take what doesn't exist.")
NoWall.SetDesc("Taste","How exactly do you taste something that doesn't exist?")
NoWall.SetDesc("Sound","The (non-existent) wall makes no (non-existant) noise.")
NoWall.SetDesc("Odor","The (non-existent) wall has no odor. Hardly surprizing, really.")

#--- Space Time

C="""
  Because of the way the code works Rooms have to be "somewhere", ie all
  rooms have to be contained in something. That something is SpaceTime, an
  otherwise unused object that is never referred to by the game to the
  player, and can't be referred to by the player. Notice that we 
  DELIBERATELY used propercase in defining SpaceTime's noun? That means the
  parser will always ignore it, the parser is looking only for things in
  lower case.
  """
  
SpaceTime = ClassBasicThing("SpaceTime")
SpaceTime.IsLit = TRUE

#--- The Sky

C="""
  Whenever the player says something like "examine sky" or "examine ceiling"
  this object will use the current actor's location's SkyDesc() property
  instead.
 
  Note if you want a special Sky object for certain rooms you can set the
  HasSky property to FALSE, then create (another) sky object (maybe MySky or
  something) with a new Landmark property set to TRUE. That way you can
  implement all the sensory methods for your MySky object.
  """
  
Sky = ClassLandmark("sky,ceiling,air","thin")
Sky.Landmark = "Sky"

Sky.SetDesc("L","{P.CA().Where().SkyDesc()}")
Sky.SetDesc("Feel","""
                   {You()} wave your hand vaugely in front of {You()}.
                   There. Satisfied?
                   """)
Sky.SetDesc("Take","You must be joking.")
Sky.SetDesc("Taste","Very poetic, but extremely impractical.")
Sky.SetDesc("Sound","{P.CA().Where().SoundDesc()}")
Sky.SetDesc("Odor","{P.CA().Where().OdorDesc()}")

#--- Wall

C="""
  Whenever the player says something like "examine wall" this object will 
  use the current actor's location's WallDesc() property instead.

  Note if you want a special Wall object for certain rooms you can set the
  HasWall property to FALSE, then create (another) Wall object (maybe MyWall
  or something) with a new Landmark property set to TRUE. That way you can
  implement all the sensory methods for your MyWall object.
  """

Wall = ClassLandmark("wall")
Wall.Landmark = "Wall"

Wall.SetDesc("L","{P.CA().Where().WallDesc()}")
Wall.SetDesc("Take","You must be joking.")
Wall.SetDesc("Taste","No!")
Wall.SetDesc("Sound","The wall is silent.")
Wall.SetDesc("Odor","The wall has no particular smell.")

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#                                End of Universe Library                        #
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%