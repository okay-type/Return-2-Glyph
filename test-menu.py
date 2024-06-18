from vanilla import *
from AppKit import NSApp, NSMenuItem, NSImage
from mojo.UI import MenuBuilder
from lib.doodleMenus import BaseMenu
import AppKit

# print(help(MenuBuilder))

class testMenu():

    def __init__(self):
        self.menu = self.getMenu()
        self.menu_insert_at_index = 0
        self.add_seperator = True
        self.menu_len = 0
        self.i = 0

        self.w = Window((100, 50, 200, 200))
        self.w.add = Button((0, 0, -0, 20), 'Add Menu', self.menu_add)
        self.w.update = Button((0, 20, -0, 20), 'Update Menu', self.menu_update)
        self.w.update.enable(False)
        self.w.remove = Button((0, 40, -0, 20), 'Remove Menu', self.menu_remove)
        self.w.remove.enable(False)
        self.w.open()

    def window_close(self, sender):
        self.menu_remove()

    def menu_add(self, sender=None):
        self.w.add.enable(False)
        self.w.update.enable(True)
        self.w.remove.enable(True)
        self.w.bind('close', self.window_close)

        self.menu_insert_at_index = self.menu.indexOfItemWithTitle_('Previous Glyph') + 1

        # # menuItems = [('Test Menu Item', self.menu_callback)]
        menuItems = [
            dict(
                title='test menu ' + str(self.i),
                enabled=True,
                image=NSImage.imageWithSystemSymbolName_accessibilityDescription_('chevron.backward', 'Do Back'),
                # identifier='testtesttesttesttesttest',
                # binding=('x', ['shift']),
                callback=self.menu_callback,
            ),
            dict(
                title='test menu history',
                enabled=True,
                image=NSImage.imageWithSystemSymbolName_accessibilityDescription_('chevron.backward.2', 'Do Back'),
                # identifier='historyhistoryhistory',
                items=[
                    ('glyphname', self.menu_callback),
                ],
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

        print('menu added')
        self.i += 1

    def menu_update(self, sender=None):
        if self.add_seperator == True:
            menu_item_return_to = self.menu.itemAtIndex_(self.menu_insert_at_index+1)
            menu_item_history = self.menu.itemAtIndex_(self.menu_insert_at_index+2)
        else:
            menu_item_return_to = self.menu.itemAtIndex_(self.menu_insert_at_index)
            menu_item_history = self.menu.itemAtIndex_(self.menu_insert_at_index+1)

        menu_item_return_to_title = menu_item_return_to.title()
        menu_item_return_to_title = menu_item_return_to_title[:-1] + str(self.i)
        menu_item_return_to.setTitle_(menu_item_return_to_title)
        # menu_item_return_to.setEnabled_(True)

        test_list = ['d','e','f','g','h','i','j','k']
        menu_item_history_submenu = menu_item_history.submenu()

        # make menu items for any new list items
        difference = len(test_list[1:]) - len(menu_item_history_submenu.itemArray())
        if difference > 0:
            for i in range(0, difference):
                new_item = [dict(
                    title='glyphname',
                    enabled=True,
                    callback=self.menu_callback,
                )]

                menuController = BaseMenu()
                menuController.buildAdditionContextualMenuItems(
                    menu_item_history_submenu,
                    new_item,
                    shouldAddSeparatorItem=False
                )

        # update menu items with list item names
        for i, item in enumerate(test_list[1:]):
            history_item = menu_item_history_submenu.itemAtIndex_(i)
            history_item.setTitle_(item)
            # history_item.setEnabled_(True)

        print('menu updated')
        self.i += 1

    def menu_remove(self, sender=None):
        self.w.add.enable(True)
        self.w.update.enable(False)
        self.w.remove.enable(False)
        self.w.unbind('close', self.window_close)
        # remove each item in the menu list
        for i in range(0, self.menu_len):
            self.menu.removeItemAtIndex_(self.menu_insert_at_index)
        # if shouldAddSeparatorItem=True , remove a third item
        if self.add_seperator == True:
            self.menu.removeItemAtIndex_(self.menu_insert_at_index)
        print('menu removed')

    def getMenu(self):
        menu_main = NSApp().mainMenu()
        menu_glyph = menu_main.itemWithTitle_('Glyph')
        menu_glyph_submenu = menu_glyph.submenu()
        return menu_glyph_submenu

    def menu_callback(self, sender):
        print('menu_callback')
        print('menu_callback title', sender.title())
        # print('menu_callback title', sender.identifier())
        # print(dir(sender))

testMenu()



