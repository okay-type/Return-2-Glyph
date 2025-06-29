from AppKit import NSApp, NSMenuItem, NSImage
from mojo.subscriber import Subscriber
from mojo.subscriber import registerRoboFontSubscriber
from mojo.UI import SetCurrentGlyphByName
from lib.doodleMenus import BaseMenu

import AppKit
from mojo.tools import CallbackWrapper



class returnToLastGlyph(Subscriber):

    debug = False

    def build(self):
        self.menu = self.getMenu()
        self.menu_insert_at_index = 0
        self.add_seperator = True
        self.menu_len = 0
        self.history_max = 13  # the history submenu only uses this -2, ignoring CurrentGlyph and last glyph
        self.previous_glyphs = [None, None]
        self.related_glyphs = []
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
        if glyph.name != self.previous_glyphs[0]:
            self.previous_glyphs.insert(0, glyph.name)
            if len(self.previous_glyphs) > self.history_max:
                self.previous_glyphs = self.previous_glyphs[:self.history_max]
            self.related_glyphs = self.find_related(glyph)
            self.updateMenuItem()

    def glyphEditorDidKeyDown(self, info):
        deviceState = info['iterations'][0]['deviceState']
        keyDown = deviceState['keyDown']
        shiftDown = deviceState['shiftDown']
        if keyDown == '<' and shiftDown != 0 and self.previous_glyphs[1] is not None:
            self.backGlyph()

    def backGlyph(self, sender=None):
        SetCurrentGlyphByName(self.previous_glyphs[1])

    def backGlyphHistory(self, sender):
        SetCurrentGlyphByName(sender.title())

    def toFamilyMember(self, sender):
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
    #     Glyph Family                 >
    #           *glyphname 0*
    #           *glyphname 1*
    #           *glyphname 2*
    #           *glyphname 3*
    #           *glyphname 4*
    #           *glyphname 5*
    #     ---------------------



    def buildMenuItem(self):
        self.menu_insert_at_index = self.menu.indexOfItemWithTitle_('Previous Glyph') + 1

        if self.previous_glyphs[1] == None:
            title_previous_glyph = 'Return to...'
        else:
            title_previous_glyph = 'Return to ' + self.previous_glyphs[1]

        menuItems = [
            dict(
                title=title_previous_glyph,
                image=NSImage.imageWithSystemSymbolName_accessibilityDescription_('arrowshape.turn.up.backward.fill', 'Go Back'),
                callback=self.backGlyph,
                enabled=True
            ),
            dict(
                title='Return to History',
                image=NSImage.imageWithSystemSymbolName_accessibilityDescription_('arrowshape.turn.up.backward.badge.clock.fill', 'Glyph History'),
                items=[],
                enabled=True
            ),
            dict(
                title='Go to Relatives',
                image=NSImage.imageWithSystemSymbolName_accessibilityDescription_('arrowshape.bounce.forward.fill', 'Related Glyphs'),
                items=[],
                enabled=True
            ),
        ]
        self.menu_len = len(menuItems)

        self.menuController = BaseMenu()
        self.menuController.buildAdditionContextualMenuItems(
            self.menu,
            menuItems,
            insert=self.menu_insert_at_index,
            shouldAddSeparatorItem=self.add_seperator
        )




    def updateMenuItem(self):
        if self.previous_glyphs[1] == None:
            return

        self.targets = []

        if self.add_seperator == True:
            menu_item_return_to = self.menu.itemAtIndex_(self.menu_insert_at_index+1)
            menu_item_history = self.menu.itemAtIndex_(self.menu_insert_at_index+2)
            menu_item_family = self.menu.itemAtIndex_(self.menu_insert_at_index+3)
        else:
            menu_item_return_to = self.menu.itemAtIndex_(self.menu_insert_at_index)
            menu_item_family = self.menu.itemAtIndex_(self.menu_insert_at_index+2)

        # update "return to" item
        if self.previous_glyphs[1] == None:
            menu_item_return_to_title = 'Return to...'
        else:
            menu_item_return_to_title = 'Return to ' + self.previous_glyphs[1]
        menu_item_return_to.setTitle_(menu_item_return_to_title)
        # menu_item_return_to.setEnabled_(True)

        # update "history" submenu
        menu_item_history_submenu = menu_item_history.submenu()
        menu_item_history_submenu.removeAllItems()
        for glyph_name in self.previous_glyphs[2:]:
            self.add_menuitem(menu_item_history_submenu, glyph_name, self.backGlyphHistory)

        # update "family" submenu
        menu_item_family_submenu = menu_item_family.submenu()
        menu_item_family_submenu.removeAllItems()
        for glyph_name in self.related_glyphs:
            self.add_menuitem(menu_item_family_submenu, glyph_name, self.toFamilyMember)

    def add_menuitem(self, menu, name, callback):
        if name is None:
            return
        i = len(menu.itemArray())
        if name == 'SEPARATOR':
            menu.insertItem_atIndex_(AppKit.NSMenuItem.separatorItem(), i)
        else:
            target = CallbackWrapper(callback)
            self.targets.append(target)
            newItem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(name, 'action:', '')
            newItem.setTarget_(target)
            menu.insertItem_atIndex_(newItem, i)

    def getMenu(self):
        menuBar = NSApp().mainMenu()
        glyphMenu = menuBar.itemWithTitle_('Glyph')
        menu = glyphMenu.submenu()
        return menu


    # def glyphEditorDidKeyDown(self, info):
    #     print(info)



    def find_related(self, g):
        if g == None:
            return

        # variables
        f = g.font
        glyph_order = f.glyphOrder
        g_components = g.components

        glyph_components = []
        glyph_dependents = []
        glyph_family = []

        # components
        for c in g_components:
            glyph_components.append(c.baseGlyph)

        # sort glyph_components by glyphOrder
        glyph_components = sorted(glyph_components, key=lambda x: glyph_order.index(x) if x in glyph_order else float('inf'))

        # dependents -  glyphs that use g as a component
        for glyph in glyph_order:
            test_glyph = f[glyph]
            test_glyph_components = test_glyph.components
            if len(test_glyph_components) > 1:
                for test_glyph_component in test_glyph_components:
                    if test_glyph_component.baseGlyph == g.name:
                        glyph_dependents.append(test_glyph.name)
                        continue

        # family - glyphs that use g's components as a component
        for i, glyph_component in enumerate(glyph_components):
            for glyph in glyph_order:
                test_glyph = f[glyph]
                test_glyph_components = test_glyph.components
                if len(test_glyph_components) > 1:
                    for test_glyph_component in test_glyph_components:
                        if test_glyph_component.baseGlyph == glyph_component:
                            glyph_family.append(test_glyph.name)
                            continue
            if i+1 < len(glyph_components):
                glyph_family.append('SEPARATOR')

        if len(glyph_components) > 0:
            if len(glyph_dependents) > 0 or len(glyph_components) > 0:
                glyph_components.append('SEPARATOR')

        if len(glyph_dependents) > 0 and len(glyph_components) > 0:
            glyph_dependents.append('SEPARATOR')

        return glyph_components + glyph_dependents + glyph_family



registerRoboFontSubscriber(returnToLastGlyph)
