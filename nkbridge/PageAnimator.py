from functools import partial
import sys
from PySide.QtGui import *
from PySide.QtCore import *

class PageAnimator( QWidget ):
    '''A widget that takes other widgets and animates them with a sliding motion'''
    def __init__( self, parent=None ):
        super( PageAnimator, self ).__init__( parent )
        self.pages = []
        self.visibleWidget = None
        self.end = 0

    def addPage( self, widget, startPage=False ):
        '''Add this widget to the animator. If startPage is notTrue hide the widget'''
        widget.setParent( self )
        if not startPage:
            # POSITION TOOL PAGES OFF SCREEN
            widget.setGeometry(0,
                               -widget.sizeHint().height(), 
                               widget.sizeHint().width(), 
                               widget.sizeHint().height())

            self.pages.append( widget )
            widget.hide()
        else:
            self.visibleWidget = widget

    def change( self, newWidget ):
        '''Slide in the new widget and slide out the old one'''

        if newWidget == self.visibleWidget:
            return

        # Slide in
        newSize = QSize( newWidget.sizeHint().width(), self.height() )
        self.resize( newSize ) # SET VIEWPORT
        newWidget.show()

        self.animGroup = QParallelAnimationGroup()       
        slideInAnimation = self.getMoveAnimation( newWidget, -newWidget.sizeHint().height(), 0 )
        self.animGroup.addAnimation( slideInAnimation )

        # Slide out
        oldWidget = self.visibleWidget
        if oldWidget:
            slideOutAnimation = self.getMoveAnimation( oldWidget, 0, newWidget.sizeHint().height() )
            self.animGroup.addAnimation( slideOutAnimation )
            slideOutAnimation.finished.connect( oldWidget.hide )

        self.animGroup.start()
        self.visibleWidget = newWidget
            
    def getMoveAnimation(self, widget, start, end):
        '''
        Horizontal animation, moves the widget 
        from "start" y-position to "end" y-position.
        '''
        moveAnimation = QPropertyAnimation(widget, 'pos')
        moveAnimation.setDuration( 700 )
        moveAnimation.setStartValue( QPoint( 0, start ) )
        moveAnimation.setEndValue( QPoint( 0, end ) )
        moveAnimation.setEasingCurve( QEasingCurve.OutCubic )
        return moveAnimation
    

    
if __name__ == '__main__':
    app = QApplication( sys.argv )

    def changePage( pageAnimator ):
        p = QLineEdit('page 2', parent=pageAnimator)
        pageAnimator.change( p )

    mainW = QWidget()
    pageAnimator = PageAnimator()
    btn = QPushButton( 'change page' )
    
    mainW.setLayout( QVBoxLayout() )
    mainW.layout().addWidget( btn )
    mainW.layout().addWidget( pageAnimator )

    pageAnimator.addPage( QLineEdit('page 1'), startPage=True )

    btnCallback = partial( changePage, pageAnimator )
    btn.clicked.connect( btnCallback )


    mainW.setMinimumSize( 500, 200 )
    mainW.show()
    sys.exit( app.exec_() )
