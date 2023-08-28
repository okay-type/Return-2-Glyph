# Previous Current Glyph
---

Remember your most recent currentGlyph and return to it using ⇧+,

---

### Version 1.0

Added a menu item in the Glyph menu to help remind me this tool exists

    # Glyph
    #     Next Glyph
    #     Previous Glyph
    #     ------------------------
    #     Return to *glyphname 0* 
    #     ------------------------





---

### Needed improvements

Figure out how to show the ⇧+, keyboard shortcut in the menu item

Instead of removing/rebuilding the menu every time, it's probably better to just change the title of the menu item. Unfortunately, everytime I did this the menu item would disable or lose the callback. 

Add a full Glyph History submenu. I have some of the pieces working, but updating the menu got too confusing.


    # Glyph
    #     Next Glyph
    #     Previous Glyph
    #     ---------------------------------
    #     Return to *glyphname 0*       ⇧+,
    #     Glyph History                 >
    #           *glyphname 0*
    #           *glyphname 1*
    #           *glyphname 2*
    #           *glyphname 3*
    #           *glyphname 4*
    #           *glyphname 5*
    #     ---------------------------------


