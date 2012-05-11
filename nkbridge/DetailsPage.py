import sys
from PySide.QtGui import *
from PySide.QtWebKit import *

class DetailsPage( QWidget ):
    '''Draw tools' details page'''
    def __init__( self, parent=None ):
        '''name will become part of the title label'''
        super( DetailsPage, self ).__init__( parent )
        self.name = ''
        self.author = ''
        # LAYOUT
        mainLayout = QVBoxLayout()
        btnLayout = QHBoxLayout()
        self.setLayout( mainLayout )
        mainLayout.addStretch()
        mainLayout.addLayout( btnLayout )

        # WIDGETS
        self.installBtn = QPushButton( 'Install' )
        self.stackBtn = QPushButton( 'Add To Stack' )
        self.favBtn = QPushButton( 'Add To Favorites' )
        self.backBtn = QPushButton( 'Back' )
        self.title = QLabel()
        self.webView = QWebView()

        for btn in ( self.backBtn, self.installBtn, self.stackBtn, self.stackBtn, self.favBtn ):
            btnLayout.addWidget( btn )
        mainLayout.addWidget( self.title )
        mainLayout.addWidget( self.webView )

    def setTitle( self, title ):
        self.title.setText( title )
    
    def setHtml( self, html ):
        '''set html string to render in WebView widget'''
        # TURN RELATIVE IMAGE LINKS INTO ABSOLUTE ONES - PLACEHOLDER - NEEDS TO BE REFINED
        processedHtml = html.replace( 'src="images', 'src="http://www.nukepedia.com/images')
        self.webView.setHtml( processedHtml )
        

if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = DetailsPage()
    w.setTitle( 'test' )
    w.setHtml( '<b> test html' )
    w.show()
    sys.exit( app.exec_() )
