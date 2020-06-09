class UIuserFunction() :
    def clearLayout(layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().setParent(None)
                    
    def deleteLayout(layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()  
                elif child.layout() is not None:
                    UIuserFunction.deleteLayout(child.layout() )
                    
    