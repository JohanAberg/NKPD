import sys
from PySide.QtGui import *
from PySide.QtCore import *

class WelcomePage( QFrame ):
    '''Info panel for after successful login'''
    def __init__( self, parent=None ):
        super( WelcomePage, self ).__init__( parent )
        self.setFrameStyle( QFrame.Box )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
        imageLabel = QLabel()
        image = QImage( '/Volumes/ohufx/consulting/Nukepedia/Nukepedia Kits/NukepediaLogo_bridge.png' )
        imageLabel.setPixmap( QPixmap.fromImage( image ) )
        infoText = QLabel( "Welcome to Nukepedia's Nuke Bridge" )
        
        layout = QVBoxLayout()
        layout.setAlignment( Qt.AlignCenter )
        self.setLayout( layout )
        #self.layout().addStretch()
        self.layout().addWidget( infoText )
        self.layout().addWidget( imageLabel )

if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = WelcomePage()
    w.resize( 500, 500 )
    w.show()
    sys.exit( app.exec_() )