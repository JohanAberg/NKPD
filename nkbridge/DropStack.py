import sys
from WidgetPage import *
from FancyButton import FancyButtonSmall
from Container import ContainerButton
from PySide.QtGui import *
from PySide.QtCore import *

def getIcon( fType ):
    '''Needs to return the correct icon for fType (Image, Filter, Transform etc) - Not yet implemented'''
    return '/Volumes/ohufx/consulting/Nukepedia/icons/NukeBridge/containers_gizmos.png'

class DropStack( WidgetPage ):
    '''Stack of buttons dropped interactively or loaded from data online. Each button can only exist once in the DropStack'''
    def __init__( self, parent=None ):
        '''item is a dictionary representing a downloadable tool'''
        super( DropStack, self ).__init__( parent )    
        self.setAcceptDrops( True )
        self.setFrameStyle( QFrame.Panel | QFrame.Sunken )
        self.maxWidgets = 40
        self.maxColumns = 100


    def dragEnterEvent( self, event ):
        event.accept()

    def dropEvent( self, event ):
        droppedItem = event.source().item
        if droppedItem in [ w.item for w in self.addedWidgets ]:
            # WIDGET ALREADY EXISTS
            return

        smallBtn = FancyButtonSmall( event.source().item )
        smallBtn.setIcon( getIcon( event.source().item['filetype'] ) )
        #smallBtn = ItemButton( event.source().item )
        self.addWidget( smallBtn )
        event.setDropAction( Qt.MoveAction )
        event.accept()
        
class DropStackArea( QWidget ):
    '''Drop Stack to hold selections and favorites'''
    def __init__( self, parent=None ):
        super( DropStackArea, self ).__init__( parent )
        
        #LAYOUTS
        layout = QGridLayout()
        btnLayout = QVBoxLayout()

        # STACK
        stack = DropStack()

        # BUTTONS
        btnLoad = ContainerButton()
        btnLoad.setCName( 'load' )
        btnSave = ContainerButton()
        btnSave.setCName( 'save' )
        btnClear = ContainerButton()
        btnClear.setCName( 'clear' )      
        
        # CONNECTIONS
        btnClear.clicked.connect( stack.clearStack )
        btnLoad.clicked.connect( stack.loadStack )

        # ADD BUTTONS
        for b in ( btnLoad, btnSave, btnClear ):
            btnLayout.addWidget( b )
        
        # ADD TO LAYOUT
        layout.addWidget( stack, 0, 1 )
        layout.setColumnStretch(0,10)
        layout.setColumnStretch(1,50)
        layout.addLayout( btnLayout, 0, 0 )
        self.setLayout( layout )


if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = DropStackArea()
    w.show()
    sys.exit( app.exec_() )
