import sys
from FaderWidget import *
from LoginPage import *
from WelcomePage import *
from PySide.QtGui import *
from PySide.QtCore import *

# NEED TO RECONCILE THIS WITH A NEW VERSION OF FaderWidget

class IntroPanel( QStackedWidget ):
    '''Cross fade between LoginPage and WelcomePage'''

    def __init__( self, parent=None ):
        super( IntroPanel, self ).__init__( parent )
        self.loginPage = LoginPage( self )
        self.welcomePage = WelcomePage( self )
        self.addWidget( self.loginPage )
        self.addWidget( self.welcomePage )
        self.loginBtn = self.widget(0).submitBtn
        self.loginBtn.clicked.connect( self.sendLoginRequest )

    def setCurrentIndex( self, index ):
        self.faderWidget = FaderWidget( self.currentWidget(), self.widget( index ) )
        QStackedWidget.setCurrentIndex( self, index )

    def setPageA( self ):
        self.CurrentIndex( 0 )

    def setPageB( self ):
        self.setCurrentIndex( 1 )

    def sendLoginRequest( self ):
        '''
        Needs to send login request and verify that user has a pro-account.
        Once verified, store details and move on.
        Also needs mechanism for failed login.
        NOT YET IMPLEMENTED
        '''
        # PRETEND LOGIN WAS SUCCESSFULL
        self.setPageB()

if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = IntroPanel()

    w.show()
    sys.exit( app.exec_() )

