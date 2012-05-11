from PySide.QtGui import *
from PySide.QtCore import *

class PageFader( QStackedWidget ):
    '''This is work in progress and not used in the main code yet. It's meant to replace FaderWidget
    with a simpler and easier to use widget
    
    Stack Widget that cross fades between pages'''

    def __init__( self, oldWidget, newWidget, parent=None ):
        super( PageFader, self ).__init__( parent )
        self.oldWidget = oldWidget
        self.newWidget = newWidget

    def setCurrentIndex( self, index ):
        QWidget.__init__( self, newWidget )
        self.fadePages( self.currentWidget(), self.widget( index ) )
        QStackedWidget.setCurrentIndex( self, index )

    def fadePages( self ):
        self.oldPixmap = QPixmap( newWidget.size() )
        oldWidget.render( self.oldPixmap )
        self.pixmapOpacity = 1.0
        self.resize( newWidget.size() )

        self.timeLine = QTimeLine()
        self.timeLine.valueChanged.connect( self.animate )
        self.timeLine.finished.connect( self.close )
        self.timeLine.setDuration( 700 )
        self.timeLine.start()

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
