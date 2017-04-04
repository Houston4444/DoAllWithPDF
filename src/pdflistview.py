#!/usr/bin/python3

from PyQt5.QtWidgets import QListWidget, QListWidgetItem

class PDFListView(QListWidget):
    def __init__(self, parent):
        QListWidget.__init__(self)
        #self.setSortingEnabled(True)
        #self.setAcceptDrops(True)
        #self.mimeTypes().append('application/pdf')
        
    #def mimeTypes(self):
        #mimetypes = QListWidget.mimeTypes(self)
        #mimetypes.append('application/pdf')
        #print('ukulélé')
        #return mimetypes
    
    #def dropMimeData(self, index, data, action):
        #print('roula', index, data, action)
        #if data.hasText():
            #self.addItem(data.text())
            #return True
        #else:
            #print('ejri')
            #return QListWidget.dropMimeData(self, index, data, action)
        
    def dropEvent(self, event):
        QListWidget.dropEvent(self, event)
        just_moved_item = self.takeItem(self.currentRow())
        for i in range(self.count()):
            if self.item(i).type() == QListWidgetItem.Type:
                toremove = self.takeItem(i)
                del toremove
                self.insertItem(i, just_moved_item)
                break
        self.setCurrentRow(-1)
            
        
