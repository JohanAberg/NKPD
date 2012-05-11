import sys
from PySide.QtGui import *
from PySide.QtCore import *

class WidgetPage( QFrame ):
    '''
    Page to collect widgets in a grid and allows loading and saving of widget lists.
    Uses pagination to only show a certain amount of widgets.
    Used for Items View and Drop Stack.
    '''
    def __init__( self, parent=None ):
        '''Stack of widgets laid out in a grid'''
        super( WidgetPage, self ).__init__( parent )
        self.setLayout( QVBoxLayout() )
        ctrlBtnLayout = QHBoxLayout()
        self.layout().addLayout( ctrlBtnLayout )
        self.stack = QStackedLayout() # FOR PAGINATION

        self.layout().addLayout( self.stack )

        self.maxWidgets = 10 #START PAGINATION AFTER THIS
        self.maxColumns = 2 # START NEW ROW AFTER THIS

        self.addedWidgets = []
        self.addedPages = []

        self.startBtn = QPushButton( 'start' )
        self.startBtn.clicked.connect( self.showStartPage )
        self.prevBtn = QPushButton( '<' )
        self.prevBtn.clicked.connect( self.showPrevPage )
        self.nextBtn = QPushButton( '>' )
        self.nextBtn.clicked.connect( self.showNextPage )
        self.endBtn = QPushButton( 'end' )
        self.endBtn.clicked.connect( self.showEndPage )
        
        self.ctrlBtns = ( self.startBtn, self.prevBtn, self.nextBtn, self.endBtn )
        for btn in self.ctrlBtns:
            ctrlBtnLayout.addWidget( btn )
            btn.hide()

    def showStartPage( self ):
        self.stack.setCurrentIndex( 0 )

    def showEndPage( self ):
        self.stack.setCurrentIndex( self.stack.count()-1 )

    def showNextPage( self ):
        self.stack.setCurrentIndex( self.stack.currentIndex()+1 )

    def showPrevPage( self ):
        self.stack.setCurrentIndex( self.stack.currentIndex()-1 )

    def addWidget( self, widget ):
        '''Add this widget at the end of the current page or start a new page'''

        if not self.addedPages or len( self.addedWidgets )/len( self.addedPages ) >= self.maxWidgets:
            # ADD NEW PAGE
            self.curPage = self.__addPage()

        # ADD WIDGET
        grid = self.curPage.layout()
        currentCells = grid.count()
        xIndex = currentCells/self.maxColumns
        yIndex = currentCells%self.maxColumns
        grid.addWidget( widget, xIndex, yIndex )
        self.addedWidgets.append( widget )
        self.endBtn.setText( str( len( self.addedPages ) ) )

        # SHOW BUTTONS IF THERE IS MORE THAN ONE PAGE
        if len( self.addedPages ) > 1:
            for btn in self.ctrlBtns:
                btn.show()

    def __addPage( self ):
        page = QWidget()
        grid = QGridLayout()
        grid.setAlignment( Qt.AlignTop | Qt.AlignLeft )
        page.setLayout( grid )
        page.layout().setSpacing(1)
        self.addedPages.append( page )
        self.stack.addWidget( page )
        return page

    def clearStack( self ):
        '''Clear the stack of buttons and pages'''
        for p in self.addedPages[:]:
            for w in self.addedWidgets[:]:
                self.stack.removeWidget( w ) 
                w.setParent( None )
                self.addedWidgets.remove( w )

            self.stack.removeWidget( p ) 
            p.setParent( None )
            self.addedPages.remove( p )
    
    def loadStack( self ):
        '''Load a stack from a favorites list on Nukepedia'''
        pass
    
    def saveStack( self ):
        '''Save a stack to a favorites list on Nukepedia'''
        pass
            
            
if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = WidgetPage()
    for i in range(1):
        w.addWidget( QPushButton( str(i) ) )
    w.resize( 500, 500 )
    w.show()
    sys.exit( app.exec_() )