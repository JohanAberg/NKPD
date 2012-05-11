################################################################################
# Nukepedia NukeBridge interface
# written by Frank Rueter 2012
#
# Huge thanks for help with code and design go out to:
# Ivan Busquets, Jan Dubberke, Aaron Richiger, Tibold Kandrai, Sebastian Elsner, Johan Aberg
################################################################################

from functools import partial
import os
import sys
import copy
from nkbridge.Container import ContainerButton
from nkbridge.Container import ContainerPage
from nkbridge.DetailsPage import DetailsPage
from nkbridge.DropStack import DropStack
from nkbridge.DropStack import DropStackArea
from nkbridge.DropStack import getIcon
from nkbridge.FaderWidget import FaderWidget
from nkbridge.FancyButton import FancyButton
from nkbridge.FancyButton import FancyButtonSmall
from nkbridge.IntroPanel import IntroPanel
from nkbridge.ItemButton import ItemButton
from nkbridge.LoginPage import LoginPage
from nkbridge.PageAnimator import PageAnimator
from nkbridge.SlidingDockLayout import SlidingDockLayout
from nkbridge.SortWidget import SortWidget
from nkbridge.WelcomePage import WelcomePage
from nkbridge.WidgetPage import WidgetPage

#from NukepediaDB2 import NPDB
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *

def getMainWindow():
    tops = QApplication.topLevelWidgets()
    for top in tops:
        if isinstance(top, QMainWindow):
            return top

class ToolBrowser( QMainWindow ):
    '''Panel to browse tools in online repository'''
    def __init__( self, data, parent=None ):
        super( ToolBrowser, self ).__init__( parent )
        self.data = data
        self.activeContainer = None
        self.pageDict = {}
        self.initUI()

    def __createContainers( self ):
        for container in sorted( self.data ):
            if container == 'misc':
                continue
            # CREATE PAGE
            itemsPage = WidgetPage( self )
            # CREATE CONTAINER BUTTON AND LINK IT TO PAGE
            containerButton = ContainerButton()
            containerButton.setCName( container )
            self.pageDict[containerButton] = itemsPage
            containerButton.clicked.connect( self.containerChangeRequest )
            self.containerLayout.addWidget( containerButton )

            # CREATE BUTTONS FOR EACH ITEM IN CONTAINER
            for item in self.data[container]:
                btn = FancyButton( item, parent=itemsPage )
                btn.setIcon( getIcon( item['filetype'] ) )
                #btn = ItemButton( item, parent=itemsPage )
                infoCallback = partial( self.__openDetailsPage, item, btn.parent() )
                installCallback = partial( self.__installItem, item )
                #btn.clicked.connect( infoCallback )
                btn.clickedInfo.connect( infoCallback )
                btn.clickedInstall.connect( installCallback )
                itemsPage.addWidget( btn )

            # ADD PAGE TO ANIMATOR WIDGET
            self.pageAnimator.addPage( itemsPage )

    def __createSearchBar( self ):
        sortWidgetDict = {}
        sortByList = ( 'category', 'name', 'downloads', 'date', 'author', 'rating' )
        
        # STORE SORT WIDGETS IN DICTIONARY SO WE CAN ACCESS THEM LATER
        #for s in sortByList:
            #w = SortWidget( s )
            #sortWidgetDict[ s ] = w
        # CREATE SORT WIDGET
        self.sortWidget = QComboBox()
        self.sortWidget.addItems( sortByList )
        
        # CREATE FILTER COMBOBOX
        self.filterWidget = QComboBox()
        #self.filterWidget.addItems( self.__getCategories( None ) )

        # CREATE SEARCH WIDGET
        self.searchBox = QLineEdit()
        self.searchButton = QPushButton( 'search' )

        # ADD TO LAYOUT
        #for i, s in enumerate( sortByList ):
            #if i:
                #self.searchLayout.addWidget( QLabel('|') )
            #self.searchLayout.addWidget( sortWidgetDict[ s ] )
        self.searchLayout.addWidget( QLabel( 'sort by' ) )
        self.searchLayout.addWidget( self.sortWidget )
        self.searchLayout.addWidget( QLabel( 'show' ) )
        self.searchLayout.addWidget( self.filterWidget )
        self.searchLayout.addWidget( self.searchBox )
        self.searchLayout.addWidget( self.searchButton )

    def __installItem( self, item ):
        print 'installing item %s' % item
        
    def __openDetailsPage( self, item, currentContainer ):
        '''NEEDS TO QUERY DATA BASE FOR DESCRIPTION FIELD. USING SMALLDESC AS PLACEHOLDER'''
        print 'opening details page for %s' % item
        self.containerPage.showDetailsPage( item, item['smalldesc'] )

    def initUI( self ):
        '''Build UI of the MainWindow'''
        ###### CREATE MAIN LAYOUTS ###################################################################

        self.dockLayout = SlidingDockLayout()
        self.setCentralWidget( self.dockLayout.containerWidget() )

        # PREP MAIN AREA AND DOCKS
        self.topDockWidget = QWidget( self )
        self.bottomDockWidget = QWidget( self )
        self.centreWidget = QFrame( self ) # HOLDS LOGIN AND INFO PANE AS WELL AS TOOLS AND DETAILS PAGE
        #self.centreWidget.setFrameStyle( QFrame.Box )
        #self.centreWidget.setLineWidth( 1 )
        self.centreWidget.setMinimumHeight( 500 )
        # PAGE ANIMATOR FOR MAIN TOOL BROWSING (SLIDING PAGES)
        self.pageAnimator = PageAnimator( self )        
        
        # LAYOUTS IN DOCKS        
        self.topDockLayout = QVBoxLayout() # LAYOUT FOR TOP DOCK (FOR CONTAINER BUTTONS AND SEARCH BAR)
        self.topDockWidget.setLayout( self.topDockLayout )
        self.bottomDockLayout = QHBoxLayout() # LAYOUT FOR BOTTOM DOCK (FOR DROP STACK)
        self.bottomDockWidget.setLayout( self.bottomDockLayout )
        self.containerLayout = QHBoxLayout() # LAYOUT FOR CONTAINER BUTTONS IN TOP DOCK
        self.searchLayout = QHBoxLayout() # LAYOUT FOR SEARCH AND FLITER BAR
        self.topDockLayout.addLayout( self.containerLayout ) # ADD CONTAINER LAYOUT TO DOCK
        self.topDockLayout.addLayout( self.searchLayout ) # ADD SEARCH LAYOUT TO DOCK

        ###### CREATE WIDGETS ###################################################################
        # CREATE SORT AND SEARCH AREA
        self.__createSearchBar()

        # CREATE DROP STACK
        self.bottomDockLayout.addWidget( DropStackArea() )

        # CENTRE WIDGET
        self.dockLayout.setWidget( self.centreWidget )
        centreLayout = QGridLayout()
        self.centreWidget.setLayout( centreLayout )

        # TOP AND BOTTOM DOCKS
        self.dockLayout.setTopDock( self.topDockWidget )
        self.dockLayout.setBottomDock( self.bottomDockWidget )

        # CREATE BUTTONS IN TOP DOCK AND PAGES IN CENTRE LAYOUT BASED ON SUPPLIED DATA
        self.__createContainers()

        # SET LOGIN/INFO PAGE (CROSS FADING WIDGET) AS THE PAGE ANIMATOR'S START PAGE
        introPane = IntroPanel( self )
        self.pageAnimator.addPage( introPane, startPage=True )
        #loginPage = LoginPage()
        #welcomePage = WelcomePage()
        #introPage = PageFader( loginPage, welcomePage )
        #self.pageAnimator.addPage( introPage, startPage=True )

        introPane.loginBtn.clicked.connect( self.dockLayout.showDocks ) # NEEDS TO CONNECT TO A FUNCTION THAT MONITORS SUCCESS OF LOGIN ATTEMPT
        #loginPage.submitBtn.clicked.connect( self.dockLayout.showDocks ) # NEEDS TO CONNECT TO A FUNCTION THAT MONITORS SUCCESS OF LOGIN ATTEMPT
        
        self.containerPage = ContainerPage( self.pageAnimator ) #COMMENT OUT TO FIX CRASH WHEN APP IS CLOSED
        centreLayout.addWidget( self.containerPage ) #COMMENT OUT TO FIX CRASH WHEN APP IS CLOSED
        #centreLayout.addWidget( self.pageAnimator ) #ACTIVATE TO FIX CRASH WHEN APP IS CLOSED

        # FINAL BITS
        self.resize( 650, 800 )
        self.setWindowTitle('Tool Browser')

    def containerChangeRequest( self ):
        '''The user wants to change the visible page'''
        # GET REQUESTED CONTAINER PAGE AND SEND IT TO ANIMATOR
        button = self.sender()
        page = self.pageDict[ button ]
        self.pageAnimator.change( page )

        # UPDATE FILTER WIDGET
        self.filterWidget.clear()
        containerName = button.cName
        toolTypes = set( [ tool['filetype'] for tool in self.data[ containerName ] ] )
        filterList = sorted( toolTypes )
        filterList.insert( 0, 'All' )

        self.filterWidget.addItems( filterList )


#------ END ToolBrowser ------------------------------------------------------------------------------------------

def main():
    
    #npdb = NPDB()
    #npdb.setUser( '' )
    #npdb.setPwd( '' )
    #data = npdb.getTools()
    ## TEST DATA:
    data = {}
    for c in ( 'gizmos', 'plugins', 'python', 'toolsets', 'presets', 'misc'):
        data[c] = []
        for t in ( 'Image', 'Filter', 'Transform', '3D' ):
            for i in xrange( 3 ):
                data[c].append( dict( filetitle='%sA%s(%s)' % ( c[:2], i, t ),
                                      filetype=t,
                                      fileauthor='John Doe',
                                      smalldesc='this is a short description but it could be quite long too'+100*'yadda',
                                      filedate = '01/05/2011',
                                      downloads=123))


    app = QApplication( sys.argv )
    ex = ToolBrowser( data )
    ex.show()

    sys.exit( app.exec_() )
 
 
if __name__ == '__main__':
    main()
    

