from AppKit import NSApp, NSMenuItem, NSImage
from mojo.subscriber import Subscriber
from mojo.subscriber import registerRoboFontSubscriber
from mojo.UI import SetCurrentGlyphByName
from lib.doodleMenus import BaseMenu



class returnToLastGlyph(Subscriber):

    debug = False

    def build(self):
        self.menu = self.getMenu()
        self.menu_insert_at_index = 0
        self.add_seperator = True
        self.menu_len = 0
        self.history_max = 13  # the history submenu only uses this -2, ignoring CurrentGlyph and last glyph
        self.previousGlyphs = [None, None]

        self.buildMenuItem()


    def destroy(self):
        # remove each item in the menu list
        for i in range(0, self.menu_len):
            self.menu.removeItemAtIndex_(self.menu_insert_at_index)
        # if shouldAddSeparatorItem=True , remove a third item
        if self.add_seperator == True:
            self.menu.removeItemAtIndex_(self.menu_insert_at_index)



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
        SetCurrentGlyphByName(sender.title())



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
        self.menu_insert_at_index = self.menu.indexOfItemWithTitle_('Previous Glyph') + 1

        if self.previousGlyphs[1] == None:
            title_previous_glyph = 'Return to...'
        else:
            title_previous_glyph = 'Return to ' + self.previousGlyphs[1]

        submenu = []
        for i in range(2, self.history_max):
            submenu.append(dict(title='glyphname', enabled=False, callback=self.backGlyphHistory))
        menuItems = [
            dict(
                title=title_previous_glyph,
                image=NSImage.imageWithSystemSymbolName_accessibilityDescription_('chevron.backward', 'Go Back'),
                callback=self.backGlyph,
                enabled=True
            ),
            dict(
                title='Return to History',
                image=NSImage.imageWithSystemSymbolName_accessibilityDescription_('chevron.backward.2', 'Go Back History'),
                # items=[],
                items=submenu,  # putting blanks in because if we add them later they are not enabled
                enabled=True
            ),
        ]
        self.menu_len = len(menuItems)

            # menu builder does not seem to let enabled=True
        # builder = MenuBuilder(
        #     items=menuItems,
        #     title='Return to glyph',
        #     menu=self.menu,
        #     insert=self.menu_insert_at_index,
        #     shouldAddSeparatorItem=self.add_seperator,
        #     )
        # return_menu = builder.getMenu()

        self.menuController = BaseMenu()
        self.menuController.buildAdditionContextualMenuItems(
            self.menu,
            menuItems,
            insert=self.menu_insert_at_index,
            shouldAddSeparatorItem=self.add_seperator
        )



    def updateMenuItem(self):
        if self.previousGlyphs[1] == None:
            return

        if self.add_seperator == True:
            menu_item_return_to = self.menu.itemAtIndex_(self.menu_insert_at_index+1)
            menu_item_history = self.menu.itemAtIndex_(self.menu_insert_at_index+2)
        else:
            menu_item_return_to = self.menu.itemAtIndex_(self.menu_insert_at_index)
            menu_item_history = self.menu.itemAtIndex_(self.menu_insert_at_index+1)

        # update "return to" item
        if self.previousGlyphs[1] == None:
            menu_item_return_to_title = 'Return to...'
        else:
            menu_item_return_to_title = 'Return to ' + self.previousGlyphs[1]
        menu_item_return_to.setTitle_(menu_item_return_to_title)
        # menu_item_return_to.setEnabled_(True)

        # update "history" submenu
        menu_item_history_submenu = menu_item_history.submenu()
        # make menu items for any new list items
        difference = len(self.previousGlyphs[2:]) - len(menu_item_history_submenu.itemArray())
        if difference > 0:
            for i in range(0, difference):
                new_item = [dict(
                    title='glyphname',
                    enabled=False,
                    callback=self.backGlyphHistory,
                )]
                menuController = BaseMenu()
                menuController.buildAdditionContextualMenuItems(
                    menu_item_history_submenu,
                    new_item,
                    shouldAddSeparatorItem=False
                )
        # update menu items with list item names
        for i, item in enumerate(self.previousGlyphs[2:]):
            if item:
                history_item = menu_item_history_submenu.itemAtIndex_(i)
                history_item.setTitle_(item)
                history_item.setEnabled_(True)



    def getMenu(self):
        menuBar = NSApp().mainMenu()
        glyphMenu = menuBar.itemWithTitle_('Glyph')
        menu = glyphMenu.submenu()
        return menu


    # def glyphEditorDidKeyDown(self, info):
    #     print(info)




registerRoboFontSubscriber(returnToLastGlyph)
