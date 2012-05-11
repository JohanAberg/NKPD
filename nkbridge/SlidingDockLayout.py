import sys
from PySide.QtGui import *
from PySide.QtCore import *

class SlidingDockLayout( QVBoxLayout ):
    
    ANIMATION_DURATION = 1000
    
    def __init__( self, parent=None ):
        super( SlidingDockLayout, self ).__init__( parent )

        self.setContentsMargins( 0, 0, 0, 0 )
        
        # INTERNAL OBJECTS
        self._container = None
        self._widget = None
        self._topDock = None
        self._bottomDock = None
        self._topPlaceHolder = QWidget()
        self._bottomPlaceHolder = QWidget()
        self._parallelAnimationGroup = QParallelAnimationGroup()
        self._topAnimation =QPropertyAnimation()
        self._bottomAnimation = QPropertyAnimation()
        
        # PRECONFIGURE ANIMATION
        for anim in ( self._topAnimation, self._bottomAnimation ):
            anim.setPropertyName( 'pos' )
            anim.setDuration( self.ANIMATION_DURATION )
            anim.setEasingCurve( QEasingCurve.OutCubic )
            self._parallelAnimationGroup.addAnimation( anim )
        self._parallelAnimationGroup.finished.connect( self.hideDockWidgets )


        # PREPARE PLACEHOLDERS
        self._topPlaceHolder.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Fixed )
        self._bottomPlaceHolder.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Fixed )
        self.addWidget( self._topPlaceHolder, 0 )
        self.addWidget( self._bottomPlaceHolder, 0 )
        
    def containerWidget( self ):
        '''Creates a container widget so this layout can be inserted anywhere as a widget'''
        
        self._container = self._container or QWidget()
        self._container.setLayout( self )
        return self._container

    def setGeometry( self, rect ):
        self.resetGeometry( rect=rect )
        super(SlidingDockLayout, self).setGeometry( rect )

    def resetAnimations( self ):
        if self._topDock:
            self._topAnimation.setTargetObject( self._topDock )
            self._topAnimation.setStartValue( QPoint( 0, self._topDock.height() * -1 ) )
            self._topAnimation.setEndValue( QPoint( 0, 0) )
            
        if self._bottomDock:
            self._bottomAnimation.setTargetObject( self._bottomDock )
            self._bottomAnimation.setStartValue( QPoint( 0, self.parentWidget().height() ) )
            self._bottomAnimation.setEndValue( QPoint( 0, self.parentWidget().height() - self._bottomDock.height() ) )

    def resetGeometry( self, rect=None ):
        rect = rect or self.parentWidget().childrenRect()
        
        if self._topDock:
            height = self._topDock.sizeHint().height()
            self._topDock.setFixedSize( rect.width(), height )
            
            if self._topPlaceHolder.size().height() != height:
                self._topPlaceHolder.setFixedHeight( height )

            if self._topPlaceHolder.minimumSize() != self._topDock.layout().minimumSize():
                self._topPlaceHolder.setMinimumSize( self._topDock.layout().minimumSize() )
            
            if self._bottomDock:
                height =  self._bottomDock.sizeHint().height()
                self._bottomDock.setFixedSize( rect.width(), height )
                
                if self._bottomDock.isVisible():
                    self._bottomDock.setGeometry( 0, rect.height() - height, rect.width(), height )
                
                if self._bottomPlaceHolder.size().height() != height:
                    self._bottomPlaceHolder.setFixedHeight( height )
                
                if self._bottomPlaceHolder.minimumSize() != self._bottomDock.layout().minimumSize():
                    self._bottomPlaceHolder.setMinimumSize( self._bottomDock.layout().minimumSize() )

        self.resetAnimations()

    def setWidget( self, widget ):
        '''Set the central widget'''
        assert isinstance( widget, QWidget )
        
        self._widget = widget
        self.insertWidget( 1, self._widget, 1 )

    def setTopDock( self, topDock ):
        '''Set the widget in top dock'''
        assert isinstance( topDock, QWidget )
        self._topDock = topDock
        self._topDock.hide()
        self.resetAnimations()
        self.resetGeometry()

    def setBottomDock( self, bottomDock ):
        '''Set the widget in bottom dock'''
        assert isinstance( bottomDock, QWidget )
        self._bottomDock = bottomDock
        self._bottomDock.hide()
        self.resetAnimations()
        self.resetGeometry()


    def showDocks( self ):
        '''Slides the top and bottom dock into view'''
        if self._parallelAnimationGroup.state() == QAbstractAnimation.Running:
            self._parallelAnimationGroup.pause()

        self._topDock.show()
        self._bottomDock.show()
        
        self.resetAnimations()
        self._parallelAnimationGroup.setDirection( QAbstractAnimation.Forward )
        self._parallelAnimationGroup.start()
        
    def hideDocks( self ):
        '''Slides the top and bottom docks out of view'''
        if self._parallelAnimationGroup.state() != QAbstractAnimation.Stopped:
            self._parallelAnimationGroup.stop()

        self.resetAnimations()
        self._parallelAnimationGroup.setDirection( QAbstractAnimation.Backward )
        self._parallelAnimationGroup.start()

    def hideDockWidgets( self ):
        if ( ( self._parallelAnimationGroup.state() == QAbstractAnimation.Stopped ) and
            ( self._parallelAnimationGroup.direction() == QAbstractAnimation.Backward) ):
            self._topDock.hide()
            self._bottomDock.hide()


if __name__ == '__main__':
    app = QApplication( sys.argv )
    w = QMainWindow()
    dockLayout = SlidingDockLayout()
    btn = QPushButton( 'slide in docks' )
    topDock = QFrame( w )
    topDock.setLayout( QVBoxLayout() )
    bottomDock = QFrame( w )
    bottomDock.setLayout( QVBoxLayout() )
    topDock.setFrameStyle( QFrame.Box )
    bottomDock.setFrameStyle( QFrame.Box )

    dockLayout.setWidget( btn )    
    w.setCentralWidget( dockLayout.containerWidget() )

    dockLayout.setTopDock( topDock )
    dockLayout.setBottomDock( bottomDock )

    btn.clicked.connect( dockLayout.showDocks )
    
    w.resize( 650, 800 )
    w.show()
    sys.exit( app.exec_() )