import sys
from PySide.QtGui import *
from PySide.QtCore import *

class LoginPage( QWidget ):
    '''Simple Login Page'''   

    def __init__( self, parent = None ):
        super( LoginPage, self ).__init__( parent )
        # CREATE WIDGETS
        self.setLayout( QHBoxLayout() )
        self.userName = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode( QLineEdit.EchoMode(2) )
        self.submitBtn = QPushButton( 'login' )
        # LAYOUT
        self.layout().addWidget( self.userName )
        self.layout().addWidget( self.password )
        self.layout().addWidget( self.submitBtn )
        
        
if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = LoginPage()
    w.show()
    sys.exit( app.exec_() )
