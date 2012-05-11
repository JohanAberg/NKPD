from functools import partial
import sys
from PySide.QtGui import *
from PySide.QtCore import *

# SHOULD MAKE THIS A SUB CLASS OF QStackedWidget TO SIMPLIFY MAIN CODE

class FaderWidget( QStackedWidget ):
    '''Cross fade between two widgets'''
    def __init__( self, parent=None ):
        super( FaderWidget, self ).__init__( parent )
        self.pixmapOpacity = 1.0
        
        self.timeLine = QTimeLine()
        self.timeLine.valueChanged.connect( self.animate )
        self.timeLine.finished.connect( self.close )
        self.timeLine.setDuration( 700 )       
   
    def paintEvent( self, event ):
        painter = QPainter()
        painter.begin( self )
        painter.setOpacity( self.pixmapOpacity )
        painter.drawPixmap( 0,0, self.oldPixmap )
        painter.end()
        
    def animate( self, value ):
        print value
        self.pixmapOpacity = 1.0 - value
        self.repaint()

    def setCurrentIndex( self, index ):
        oldWidget = self.currentWidget()
        newWidget = self.widget( index )
        
        QWidget.__init__( self, newWidget )
        self.resize( newWidget.size() )
        
        self.oldPixmap = QPixmap( newWidget.size() )
        oldWidget.render( self.oldPixmap )

        self.timeLine.start()
        QStackedWidget.setCurrentIndex( self, index )


if __name__ == '__main__':

    app = QApplication( sys.argv )
    

    widget1 = QPushButton( 'test' )
    widget2 = QCalendarWidget()
    w = FaderWidget()
    w.addWidget( widget1 )
    w.addWidget( widget2 )
    
    def changePage( faderWidget, index ):
        faderWidget.setCurrentIndex( index )
    changePageCallback = partial( changePage, w, 1 )
    widget1.clicked.connect( changePageCallback )


    w.show()
    sys.exit( app.exec_() )

