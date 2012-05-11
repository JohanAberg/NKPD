import sys
from PySide.QtGui import *
from PySide.QtCore import *

# SHOULD MAKE THIS A SUB CLASS OF QStackedWidget TO SIMPLIFY MAIN CODE
# NEED TO FIGURE OUT WHY FIRST CLICK DOES NOT SHOW DISSOLVE ANIMATION

class FaderWidget( QWidget ):
    '''Cross fade between two widgets'''
    def __init__( self, oldWidget, newWidget ):
        QWidget.__init__( self, newWidget )
        print oldWidget
        print oldWidget.size()
        print newWidget
        print newWidget.size()
        self.oldPixmap = QPixmap( newWidget.size() )
        oldWidget.render( self.oldPixmap )
        self.pixmapOpacity = 1.0
        
        self.timeLine = QTimeLine()
        self.timeLine.valueChanged.connect( self.animate )
        self.timeLine.finished.connect( self.close )
        self.timeLine.setDuration( 2000 )
        self.timeLine.start()
        
        self.resize( newWidget.size() )
        #self.show()

    def paintEvent( self, event ):
        painter = QPainter()
        painter.begin( self )
        painter.setOpacity( self.pixmapOpacity )
        painter.drawPixmap( 0,0, self.oldPixmap )
        painter.end()
        
    def animate( self, value ):
        #print value
        self.pixmapOpacity = 1.0 - value
        self.repaint()
        
if __name__ == '__main__':

    app = QApplication( sys.argv )
    
    class TestWidget( QStackedWidget ):
        def __init__( self, startWidget, parent=None ):
            super( TestWidget, self ).__init__( parent )
        
            self.w1 = startWidget
            self.w2 = QCalendarWidget()
            self.addWidget( startWidget )
            self.addWidget( self.w2 )
            
            startWidget.clicked.connect( self.showCalendar )
        
        def setCurrentIndex( self, index ):
            FaderWidget( self.currentWidget(), self.widget(index) )
            QStackedWidget.setCurrentIndex( self, index )
        
        def showCalendar( self ):
            self.setCurrentIndex( 1 )

    btn = QPushButton( 'test' )
    btn.setMaximumSize( 50, 50 )
    w = TestWidget( btn )
    w.show()
    sys.exit( app.exec_() )

