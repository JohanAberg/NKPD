import os
import sys
from PySide.QtGui import *
from PySide.QtCore import *

# REPLACED IN MAIN CODE BY FancyButton

class ItemButton( QPushButton ):
    '''REPLACED BY FANCYBUTTON - DELETE WHEN DONE. A custom button object that is dragable and holds an item which represents the data for the respective tool'''

    def __init__( self, item, parent=None ):
        '''item is a dictionary representing a downloadable tool'''
        super( ItemButton, self ).__init__( parent )
        self.iconPath = '/Volumes/ohufx/consulting/Nukepedia/NukeBridge/icons'
        self.item = item
        self.setText( item['filetitle'] )
        self.setMinimumSize( 260, 80 )
        iconPath = os.path.join( self.iconPath, item['filetype'][0].lower() + item['filetype'][1:] + '.png' )
        self.setIcon( QIcon( iconPath ) )
        self.setAcceptDrops( True )

    def openDetailsPage( self ):
        print 'Opens Item page for %s - not yet implemented' % self.item

    def mouseMoveEvent( self, event ):
        '''Enable drag&drop of buttons'''
        self.startDragPos = event.pos()
        self.setDown( False ) #PREVENT THE BUTTON FORM STAYING DOWN
        mimeData = QMimeData() # IMPLEMENT THIS TO BE ABLE TO DROP INTO NUKE
        drag = QDrag( self )
        drag.setMimeData( mimeData )
        drag.setHotSpot( event.pos() - self.rect().topLeft() )
        dropAction = drag.start( Qt.CopyAction )

    def dragEnterEvent( self, event ):
        event.accept()

    def dropEvent( self, event ):
        try:
            point = event.pos() - self.startDragPos
            if point.manhattanLength() < 10:
                # EXECUTE MOUSE CLICK EVEN IF CURSOR MOVED A LITTLE BIT DURING CLICK
                self.openDetailsPage()
            event.accept()

        except AttributeError:
            '''if one buttons is dragged onto another'''
            pass

    def mouseReleaseEvent( self, event ):
        '''when button is released after static click (no drag)'''
        QPushButton.mousePressEvent( self, event ) # NEEDED TO MAKE BUTTON APPEAR TO BE PRESSED
        if event.button() == Qt.LeftButton:
            self.openDetailsPage()
            self.setDown( False )

if __name__ == '__main__':
    app = QApplication( sys.argv )
    dataItem = dict( filetitle = 'tool name',
                     filetype = 'gizmo',
                     fileauthor = 'me',
                     filedate = '01/02/2012',
                     downloads=1234,
                     smalldesc ='this is a nuke gizmo')
    w = ItemButton( dataItem )
    w.show()
    sys.exit( app.exec_() )
