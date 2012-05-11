import sys
from PySide.QtGui import *
from PySide.QtCore import *

class SortWidget( QLabel ):
    '''A clickable Label - NO LONGER IN USE'''
    def __init__( self, parent=None ):
        super( SortWidget, self).__init__( parent )

    def mousePressEvent( self, event ):
        event.accept()
        print 'I was clicked'

if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = SortWidget()
    w.setText( 'click me' )
    w.show()
    sys.exit( app.exec_() )
    