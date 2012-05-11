import sys
import copy
from PySide.QtGui import *
from PySide.QtCore import *

class FancyButtonSmall( QWidget ):
    clicked = Signal()

    def __init__( self, item, icon=None, parent=None ):
        '''item is a dictionary representing a downloadable tool'''
        super( FancyButtonSmall, self ).__init__( parent )
        
        # LAYOUT
        layout = QHBoxLayout()
        layout.setSpacing( 0 )
        self.setLayout( layout )
        self.setMinimumWidth( 50 )
        self.setMinimumHeight( 50 )

        self.setSizePolicy( QSizePolicy.Fixed, QSizePolicy.Fixed )

        # BUTTON STATES
        self.mainButtonDown = False

        # BUTTON COLOURS
        self.btnColMainUp = QColor(50, 50, 50)
        self.btnColMainDown = QColor(35, 35, 35)

        # LABELS
        self.titleCol = QColor( 255, 95, 0 )
        self.textCol = QColor( 150, 150, 150 )
        
        self.item = item
        self.title = item['filetitle']
        self.subTitle = item['filetype']
        self.desc = 'Uploaded by %s on %s\ndownloads: %s' % ( item['fileauthor'], item['filedate'], item['downloads'] )
        
        self.setToolTip( self.__wrapText( item['smalldesc'] ) )
        self.icon = icon

    def __wrapText( self, text, maxChar = 50 ):
        '''wrap text to only contain maxChar per line'''
        i = 1
        charList = list( text )
        while i*maxChar < len( charList ):
            charList.insert( i*maxChar, '\n' )
            i += 1
        return ''.join( charList )

    def mousePressEvent( self, event ):
        painter = QPainter()
        # MAIN BUTTON DOWN
        self.mainButtonDown = True

        self.update()

    def mouseReleaseEvent( self, event ):
        self.clicked.emit()

        self.mainButtonDown = False
        self.update()

    def setDown( self, state ):
        self.mainButtonDown = state
        self.update()

    def paintEvent( self, event ):
        painter = QPainter( self )

        # DEFINE MAIN RECT
        self.mainArea = ( 0, 0, self.geometry().width(), self.geometry().height() )
        self.mainRect = QRect( *self.mainArea )
        padding = 10
        paddedRect = QRect( self.mainArea[0]+padding, self.mainArea[1]+padding, self.mainArea[2]-padding, self.mainArea[3]-padding )

        # ASSIGN COLOURS
        if self.mainButtonDown:
            painter.fillRect( self.mainRect, self.btnColMainDown )

        else:
            painter.fillRect( self.mainRect, self.btnColMainUp )

        ## ASSIGN COLOURS
        #painter.setRenderHint( painter.Antialiasing )

        # PREPARE AREAS FOR ICON AND TEXT
        iconSize = QSize( 25, 25 )
        titleRect = copy.copy( paddedRect )
        descRect = copy.copy( paddedRect )
        descRect.setRight( 0 )

        # DRAW ICON
        self.drawIcon( painter, QPoint(paddedRect.x(), paddedRect.y()), iconSize )
        # DRAW TITLE
        painter.setPen( self.titleCol )
        painter.setFont( QFont( 'Helvetica', 12, QFont.Bold) )
        painter.drawText( titleRect, Qt.AlignLeft | Qt.AlignTop, self.title )
        # DRAW SUBTITLE
        painter.setPen( self.textCol )
        painter.setFont( QFont( 'Helvetica', 10, QFont.Normal) )
        painter.drawText( titleRect.x(), titleRect.y()+25, self.subTitle )
        # DRAW DESCRIPTION
        painter.drawText( descRect, self.desc )


    def drawIcon( self, painter, pos, size ):
        '''Draw icon with status'''
        enabledStatus = QIcon.Normal
        if self.mainButtonDown:
            enabledStatus = QIcon.Disabled
        icon = QIcon( self.icon )
        pixmap = icon.pixmap( size, enabledStatus, QIcon.On )
        painter.drawPixmap( pos, pixmap )
  
    def minimumSizeHint( self ):
        return QSize( 50, 50 )
    
    def sizeHint( self ):
        return QSize( 80, 80 )
    
    def setIcon( self, icon ):
        self.icon = QIcon( icon )


class FancyButton( QWidget ):
    clickedInfo = Signal()
    clickedInstall = Signal()

    def __init__( self, item, icon=None, parent=None ):
        '''item is a dictionary representing a downloadable tool'''
        super( FancyButton, self ).__init__( parent )
        
        # LAYOUT
        layout = QHBoxLayout()
        layout.setSpacing( 0 )
        self.setLayout( layout )
        self.setMinimumWidth( 200 )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )

        # BUTTON STATES
        self.mainButtonDown = False
        self.installBtnDown = False
        # BUTTON COLOURS
        self.btnColMainUp = QColor(50, 50, 50)
        self.btnColMainDown = QColor(35, 35, 35)
        self.btnColInstallUp = QColor( 60, 60, 60 )
        self.btnColInstallDown = QColor( 0, 75, 0 )
        # LABELS
        self.titleCol = QColor( 255, 95, 0 )
        self.textCol = QColor( 150, 150, 150 )
        
        self.item = item
        self.title = item['filetitle']
        self.subTitle = item['filetype']
        self.desc = 'Uploaded by %s on %s\ndownloads: %s' % ( item['fileauthor'], item['filedate'], item['downloads'] )
        
        self.setToolTip( self.__wrapText( item['smalldesc'] ) )
        self.icon = icon

    def __wrapText( self, text, maxChar = 50 ):
        '''wrap text to only contain maxChar per line'''
        i = 1
        charList = list( text )
        while i*maxChar < len( charList ):
            charList.insert( i*maxChar, '\n' )
            i += 1
        return ''.join( charList )

    def mousePressEvent( self, event ):
        painter = QPainter()
        if QRect( *self.InstallBtnArea ).contains( event.pos() ):
            # INSTALL BUTTON DOWN
            self.installBtnDown = True
        else:
            # MAIN BUTTON DOWN
            self.mainButtonDown = True

        self.update()

    def mouseReleaseEvent( self, event ):
        if QRect( *self.InstallBtnArea ).contains( event.pos() ):
            # INSTALL BUTTON DOWN
            self.clickedInstall.emit()
        else:
            # MAIN BUTTON DOWN
            self.clickedInfo.emit()

        self.installBtnDown = False
        self.mainButtonDown = False
        self.update()

    def mouseMoveEvent( self, event ):
        '''Enable drag&drop of buttons'''
        self.setDown( False )
        self.startDragPos = event.pos()
        mimeData = QMimeData() # IMPLEMENT THIS TO BE ABLE TO DROP INTO NUKE
        drag = QDrag( self )
        drag.setMimeData( mimeData )
        drag.setHotSpot( event.pos() - self.rect().topLeft() )
        dropAction = drag.start( Qt.CopyAction )

    def dragEnterEvent( self, event ):
        event.accept()

    def dropEvent( self, event ):
        try:
            point = event.pos() - self.startDragPos
            if point.manhattanLength() < 10:
                # EXECUTE MOUSE CLICK EVEN IF CURSOR MOVED A LITTLE BIT DURING CLICK
                self.openDetailsPage()
            event.accept()

        except AttributeError:
            '''if one buttons is dragged onto another'''
            pass

    def setDown( self, state ):
        self.installBtnDown = state
        self.mainButtonDown = state
        self.update()

    def paintEvent( self, event ):
        painter = QPainter( self )

        # DEFINE MAIN RECT
        self.mainArea = ( 0, 0, self.geometry().width(), self.geometry().height() )
        self.mainRect = QRect( *self.mainArea )
        padding = 10
        paddedRect = QRect( self.mainArea[0]+padding, self.mainArea[1]+padding, self.mainArea[2]-padding, self.mainArea[3]-padding )

        # ASSIGN COLOURS
        if self.mainButtonDown:
            painter.fillRect( self.mainRect, self.btnColMainDown )

        else:
            painter.fillRect( self.mainRect, self.btnColMainUp )

        # DEFINE INSTALL BUTTON RECT
        self.InstallBtnArea = ( self.mainArea[2]*.75, self.geometry().height()*.3, self.geometry().width()*.2, self.geometry().height()*.35 )
        self.InstallBtnRect = QRect( *self.InstallBtnArea )
        # ASSIGN COLOURS
        painter.setRenderHint( painter.Antialiasing )
        if self.installBtnDown:
            painter.setBrush( self.btnColInstallDown )
            painter.drawRoundRect( QRect( self.InstallBtnRect ), 30, 30 )
        else:
            painter.setBrush( self.btnColInstallUp )
            painter.drawRoundRect( QRect( self.InstallBtnRect ), 30, 30 )

        # PREPARE AREAS FOR ICON AND TEXT
        iconSize = QSize( 25, 25 )
        titleRect = copy.copy( paddedRect )
        titleRect.setLeft( iconSize.width()+25 )
        descRect = copy.copy( paddedRect )
        descRect.setTop( iconSize.height()+25 )
        descRect.setRight( self.InstallBtnArea[0]-3 )

        # DRAW ICON
        self.drawIcon( painter, QPoint(paddedRect.x(), paddedRect.y()), iconSize )
        # DRAW TITLE
        painter.setPen( self.titleCol )
        painter.setFont( QFont( 'Helvetica', 12, QFont.Bold) )
        painter.drawText( titleRect, Qt.AlignLeft | Qt.AlignTop, self.title )
        # DRAW SUBTITLE
        painter.setPen( self.textCol )
        painter.setFont( QFont( 'Helvetica', 10, QFont.Normal) )
        painter.drawText( titleRect.x(), titleRect.y()+25, self.subTitle )
        # DRAW DESCRIPTION
        painter.drawText( descRect, self.desc )
        # DRAW INSTALL TEXT
        painter.setFont( QFont( 'Helvetica', 10, QFont.Bold) )
        painter.drawText( self.InstallBtnRect, Qt.AlignCenter, 'ADD' )

    def drawIcon( self, painter, pos, size ):
        '''Draw icon with status'''
        enabledStatus = QIcon.Normal
        if self.mainButtonDown:
            enabledStatus = QIcon.Disabled
        icon = QIcon( self.icon )
        pixmap = icon.pixmap( size, enabledStatus, QIcon.On )
        painter.drawPixmap( pos, pixmap )

  
    def minimumSizeHint( self ):
        return QSize( 150, 50 )
    
    def sizeHint( self ):
        return QSize( 300, 80 )
    
    def setIcon( self, icon ):
        self.icon = QIcon( icon )
        
if __name__ == '__main__':
    app = QApplication( sys.argv )
    dataItem = dict( filetitle = 'tool name',
                     filetype = 'gizmo',
                     fileauthor = 'me',
                     filedate = '01/02/2012',
                     downloads=1234,
                     smalldesc ='this is a nuke gizmo')
    w = FancyButtonSmall( dataItem )
    w.show()
    sys.exit( app.exec_() )
