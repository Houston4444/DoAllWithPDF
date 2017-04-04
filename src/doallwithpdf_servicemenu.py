#!/usr/bin/python3

import PyPDF2, os, sys, dbus
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog, QListWidgetItem, QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import QProcess, QTimer, QLocale, QTranslator
from PyQt5.QtGui import QTextCursor, QIcon
import ui_terminalDialog, ui_order_dialog


def prettyFileName(filename):
    home = os.getenv('HOME')
    if filename.startswith(home + '/'):
        return filename.replace(home + '/', '~/', 1)
    return filename

def ended():
    sys.exit(0)

class PDFWidget(QListWidgetItem):
    def __init__(self, filename):
        QListWidgetItem.__init__(self, None, QListWidgetItem.UserType)
        try:
            self.pdf       = PyPDF2.PdfFileReader(filename)
            self.valid_pdf = True
            self.filename  = filename
            self.dirname   = filename.rpartition('/')[0]
            self.basename  = filename.rpartition('/')[2]
            self.password  = None
            
            self.setText(os.path.basename(filename))
            #self.setIcon(pdf_icon)
            
            self.updateToolTip()
        except:
            self.valid_pdf = False
            
    def updateToolTip(self):
        if not self.pdf.isEncrypted or self.password:
            pages = self.pdf.getNumPages()
            
            if pages == 1:
                pages_str = _translate('Tooltip', '1 page')
            else:
                pages_str = _translate('Tooltip', '%i pages') % pages
                
            self.setToolTip(prettyFileName(self.filename) + '<br>' + pages_str)
    
    def isEncrypted(self):
        return self.pdf.isEncrypted
        
    def tryPassword(self, password):
        if password and self.pdf.decrypt(password):
            self.password = password
            self.updateToolTip()
            return True
        
        return False


class OrderDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = ui_order_dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(pdf_icon)
        
        self.last_pw = None
        self.ui.pushButtonJoin.clicked.connect(self.join)
        self.ui.pushButtonCancel.clicked.connect(sys.exit)
        
        self.pdftk_process   = QProcess()
        self.terminal_dialog = TerminalDialog()
        self.terminal_dialog.rejected.connect(self.pdftk_process.kill)
        
        self.outfile_name    = None
        
        self.show()
        
        #check if pdf are encrypted, add them to dialog
        for filename in filenames:
            pdf_widget = PDFWidget(filename)
            if pdf_widget.valid_pdf:
                good_pw = True
                if pdf_widget.isEncrypted():
                    if not pdf_widget.tryPassword(self.last_pw):
                        good_pw = False
                        
                        while not good_pw:
                            pw, ok = QInputDialog.getText(self, _translate('Dialog', 'Encrypted PDF'), _translate('Dialog', '<p>Please insert password for:</p><p>%s</p>') % prettyFileName(filename), QLineEdit.Password)
                            if not ok:
                                break
                                
                            good_pw = pdf_widget.tryPassword(pw)
                            
                        self.last_pw = pw
                
                if good_pw:
                    self.ui.listWidget.addItem(pdf_widget)
   
    #def hasEnoughtFiles(self):
        if self.ui.listWidget.count() < 2:
            QMessageBox.critical(self, _translate('Dialog', 'Not Enought Files'), _translate('Dialog', 'You need at least 2 PDF files to join them !'))
            sys.exit(0)
                
    def getPdftkList(self):
        pdftk_list = []
        for i in range(self.ui.listWidget.count()):
            pdf_widget = self.ui.listWidget.item(i)
            pdftk_list.append(pdf_widget.filename)
            
        for i in range(self.ui.listWidget.count()):
            pdf_widget = self.ui.listWidget.item(i)
            pdftk_list.append('input_pw')
            if pdf_widget.isEncrypted():
                pdftk_list.append(pdf_widget.password)
            else:
                pdftk_list.append('')
                
        if self.ui.checkBoxShuffle.isChecked():
            pdftk_list.append('shuffle')
        else:
            pdftk_list.append('cat')
            
        pdftk_list.append('output')
                
        return pdftk_list
    
    def getJoinedFileName(self):
        #find common dir for all files
        output_dirs = self.ui.listWidget.item(0).dirname.split('/')
        
        for i in range(self.ui.listWidget.count()):
            dirnames = self.ui.listWidget.item(i).dirname.split('/')
            n = len(output_dirs) if len(output_dirs) < len(dirnames) else len(dirnames)
            for j in range(n):
                if dirnames[j] != output_dirs[j]:
                    output_dirs = output_dirs[:j]
                    break
        
        output_dir = ''
        for dir in output_dirs:
            output_dir += dir + '/'
        
        #find common regex for all file names
        common_regex = self.ui.listWidget.item(0).basename
        
        for i in range(self.ui.listWidget.count()):
            basename = self.ui.listWidget.item(i).basename
            n = len(common_regex) if len(common_regex) < len(basename) else len(basename)
            for j in range(n):
                if basename[j] != common_regex[j]:
                    common_regex = common_regex[:j]
                    break
        
        
        if not common_regex:
            common_regex = _translate('File', 'join')
        
        #change file name if exists
        n=1
        tmp_string = common_regex
        while os.path.exists("%s%s.pdf" % (output_dir, common_regex)):
            common_regex = "%s (%i)" % (tmp_string, n)
            n+=1
        
        return "%s%s.pdf" % (output_dir, common_regex)
        
    def join(self):
        self.outfile_name = self.getJoinedFileName()
    
        exit_loop = False
        while not exit_loop:
            self.outfile_name, ok = QFileDialog.getSaveFileName(self, None, self.outfile_name, 'PDF (*.pdf)')
            
            if not ok:
                sys.exit(0)
                
            if not os.access(os.path.dirname(self.outfile_name), os.W_OK):
                QMessageBox.critical(self, _translate('Dialog', 'Permissions Error'), _translate('Dialog', 'You have no permission to write %s') % self.outfile_name)
            elif self.outfile_name in filenames:
                QMessageBox.critical(self, _translate('Dialog', 'Permissions Error'), _translate('Dialog', "You can't overwrite an input file !"))
            else:
                exit_loop = True
        
        pdftk_args = self.getPdftkList()
        pdftk_args.append(self.outfile_name)
        pdftk_args.append('verbose')
        
        self.terminal_dialog.show()
        self.terminal_dialog.addText(_translate('Terminal', 'creation of %s') % prettyFileName(self.outfile_name))
        self.terminal_dialog.addText(_translate('Terminal', 'please wait...'))
        
        self.pdftk_process.readyReadStandardError.connect(self.terminal_dialog.updateStandardError)
        self.pdftk_process.readyReadStandardOutput.connect(self.terminal_dialog.updateStandardOutput)
        self.pdftk_process.finished.connect(self.processFinished)
        self.pdftk_process.start('pdftk', pdftk_args)
        
    def processFinished(self, exit_code):
        if exit_code == 0:
            bus = dbus.SessionBus()
            notif = bus.get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
            notify = dbus.Interface(notif, "org.freedesktop.Notifications")
            koko = notify.Notify('doallwithpdf_join', 0, 'application-pdf', 
                                 _translate('Notification', 'new PDF Document :'), 
                                 prettyFileName(self.outfile_name), '', '', 0)
            sys.exit(0)
        elif exit_code == 9: #process has been killed
            sys.exit(0)
        else:
            self.terminal_dialog.addText(_translate('Dialog', 'Failed'))

class TerminalDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = ui_terminalDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.pointTimer = QTimer()
        self.pointTimer.setInterval(1000)
        self.pointTimer.timeout.connect(self.addPoint)
        
    def addPoint(self):
        self.ui.terminalDisplay.moveCursor(QTextCursor.End)
        self.ui.terminalDisplay.insertPlainText('.')
        self.ui.terminalDisplay.moveCursor(QTextCursor.End)
    
    def addText(self, text):
        self.pointTimer.start()
        self.ui.terminalDisplay.appendPlainText(text)
    
    def updateStandardOutput(self):
        self.pointTimer.stop()
        text = order_dialog.pdftk_process.readAllStandardOutput().data().decode('utf-8')
        if text.endswith('\n'):
            text = text[:-1]
        self.ui.terminalDisplay.appendPlainText(text)
        
    def updateStandardError(self):
        self.pointTimer.stop()
        text = order_dialog.pdftk_process.readAllStandardError().data().decode('utf-8')
        if text.endswith('\n'):
            text = text[:-1]
        self.ui.terminalDisplay.appendPlainText(text)

if __name__ == '__main__':
    pdf_icon = QIcon.fromTheme('application-pdf')
    
    app = QApplication(sys.argv)
    app.setWindowIcon(pdf_icon)
    
    ## Translation process
    locale = QLocale.system().name()
    appTranslator = QTranslator()
    if appTranslator.load("%s/locale/doallwithpdf_%s" % (os.path.dirname(os.path.dirname(sys.argv[0])), locale)):
        app.installTranslator(appTranslator)
    _translate = app.translate
    
    #get all full filenames
    filenames = []
    for filename in sys.argv[1:]:
        filenames.append(os.path.realpath(filename))
    
    order_dialog = OrderDialog()
    app.exec()
    
    del app
    
    
    
