from AppKit import NSApp, NSMenuItem
from mojo.subscriber import Subscriber
from mojo.subscriber import registerRoboFontSubscriber
from mojo.UI import SetCurrentGlyphByName
from mojo.UI import MenuBuilder
from lib.doodleMenus import BaseMenu

'''
keep track of the most recent currentGlyph and return to it using ⇧+,

recent update:
no longer tied to the edit glyph window - you can now close a glyph, open a new glyph, and then ⇧+, back to the previous glyph
'''

class previousCurrentGlyph(Subscriber):



    debug = False



    def build(self):
        self.history_max = 10
        self.previousGlyphs = [None, None]
        self.title_previous_glyph = 'Return to...'
        self.buildMenuItem()



    def glyphEditorDidSetGlyph(self, info):
        glyph = info['glyph']
        if glyph is None:
            return
        if glyph.name != self.previousGlyphs[0]:
            self.previousGlyphs.insert(0, glyph.name)
            if len(self.previousGlyphs) > self.history_max:
                self.previousGlyphs = self.previousGlyphs[:self.history_max]
            self.updateMenuItem()



    def glyphEditorDidKeyDown(self, info):
        deviceState = info['iterations'][0]['deviceState']
        keyDown = deviceState['keyDown']
        shiftDown = deviceState['shiftDown']
        if keyDown == '<' and shiftDown != 0 and self.previousGlyphs[1] is not None:
            self.backGlyph()



    def backGlyph(self, sender=None):
        SetCurrentGlyphByName(self.previousGlyphs[1])



    def backGlyphHistory(self, sender):
        print('backGlyphHistory', sender.title, sender)



    # Glyph
    #     Next Glyph
    #     Previous Glyph
    #     ---------------------
    #     Return to *glyphname 0*       ⇧+,
    #     Glyph History                 >
    #           *glyphname 0*
    #           *glyphname 1*
    #           *glyphname 2*
    #           *glyphname 3*
    #           *glyphname 4*
    #           *glyphname 5*
    #     ---------------------



    def buildMenuItem(self):
        self.menuAddReturnTo()
        # self.menuAddGlyphHistory()



    def updateMenuItem(self):
        if self.previousGlyphs[1] == None:
            return
        self.menuAddReturnTo()
        # self.menuAddGlyphHistory()



    def menuAddReturnTo(self):
        menu = self.getMenu()
        menu_index = menu.indexOfItemWithTitle_(self.title_previous_glyph)
        if menu_index > 0:
            menu.removeItemAtIndex_(menu_index)

        if self.previousGlyphs[1] == None:
            previous_glyph = '...'
        else:
            previous_glyph = ' /' + self.previousGlyphs[1]
        self.title_previous_glyph = 'Return to' + previous_glyph
        menuItems = [(self.title_previous_glyph, self.backGlyph)]

        insert_at = menu.indexOfItemWithTitle_('Previous Glyph') + 1
        self.menuController = BaseMenu()
        self.menuController.buildAdditionContextualMenuItems(menu, menuItems, insert=insert_at)



    def menuAddGlyphHistory(self):
        menu = self.getMenu()
        menu_index = menu.indexOfItemWithTitle_('Glyph History')
        if menu_index > 0:
            menu.removeItemAtIndex_(menu_index)

        g_list = []
        for g in self.previousGlyphs:
            if g != None:
                g_list.append((g, self.backGlyphHistory))

        menuItems = []
        if g_list != []:
            menuItems = [('Glyph History', g_list)]
            insert_at = menu.indexOfItemWithTitle_(self.title_previous_glyph)
            self.menuController = BaseMenu()
            self.menuController.buildAdditionContextualMenuItems(menu, menuItems, insert=insert_at)



    def getMenu(self):
        menuBar = NSApp().mainMenu()
        glyphMenu = menuBar.itemWithTitle_('Glyph')
        menu = glyphMenu.submenu()
        return menu


    # def glyphEditorDidKeyDown(self, info):
    #     print(info)




registerRoboFontSubscriber(previousCurrentGlyph)
