import os
import sys
from DetailsPage import *
from FaderWidget import *
from functools import partial
from PySide.QtGui import *
from PySide.QtCore import *


class ContainerButton( QPushButton ):
    '''
    Button for containers holds extra cName attribute to hold the container name without showing the label.
    The icon is derived from cName and self.iconPath
    '''
    def __init__( self ):
        super( ContainerButton, self ).__init__()
        self.iconPath = '/Volumes/ohufx/consulting/Nukepedia/NukeBridge/icons'
        self.cName = None
        self.setIconSize( QSize(24, 24) )

    def setCName( self, cName ):
        self.cName = cName
        cIcon = QIcon( os.path.join( self.iconPath, '%s' % cName ) )
        self.setIcon( cIcon )
        self.setToolTip( cName )

class ContainerPage( QStackedWidget ):
    '''Fades between Items View and Details Page'''
    
    def __init__( self, startWidget, parent=None ):
        super( ContainerPage, self ).__init__( parent )
        self.detailsPage = DetailsPage( self )
        self.addWidget( startWidget )
        self.addWidget( self.detailsPage )
        # CONNECT WEB VIEW BUTTONS
        backBtnCallback = partial( self.setCurrentIndex, 0 )
        self.detailsPage.backBtn.clicked.connect( backBtnCallback )

    def setCurrentIndex( self, index ):
        self.faderWidget = FaderWidget( self.currentWidget(), self.widget( index ) )
        QStackedWidget.setCurrentIndex( self, index )

    def showDetailsPage( self, item, html ):
        '''
        Show the details page for item.
        Item is a dictionary containing the db query result for the requested tool.
        '''
        self.detailsPage.setTitle( '<big><b>%s</b></big> <small>written by %s</small>' % (item['filetitle'], item['fileauthor']) )
        self.detailsPage.setHtml( html )
        self.setCurrentIndex( 1 )

    def showToolsPage( self ):
        self.setCurrentIndex( 0 )


if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = ContainerPage( QFrame() )
    #w = ContainerButton()
    #w.setCName( 'test' )
    w.show()
    sys.exit( app.exec_() )

    