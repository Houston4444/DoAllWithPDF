#!/usr/bin/python3

import os
import sys
from typing import Optional

import dbus
import PyPDF2
from PyQt5.QtCore import (
    QProcess, QTimer, QLocale, QTranslator, QSettings,
    QThread, QObject, pyqtSignal)
from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QDialog, QListWidgetItem,
    QLineEdit, QMessageBox)

import ui_terminalDialog, ui_order_dialog, ui_password, ui_extract

VERSION = '1.4.0'

MIN_FOR_MKDIR = 5

ERR_OK = 0
ERR_NOT_PDF = 1
ERR_NO_PW = 2


def prettyFileName(filename: str):
    home = os.getenv('HOME')
    if filename.startswith(home + '/'):
        return filename.replace(home + '/', '~/', 1)
    return filename


class AbstractAction:
    def __init__(self):
        self.actions = {
            'extract_odd_even': self.extractOddEven,
            'extract': self.extract,
            'compress': self.compress,
            'uncompress': self.uncompress,
            'watermark': self.watermark,
            'stamp': self.stamp,
            'burst': self.burst,
            'join': self.join
        }
    
    def extractOddEven(self):
        ...
    def extract(self):
        ...
    def compress(self):
        ...
    def uncompress(self):
        ...
    def watermark(self):
        ...
    def stamp(self):
        ...
    def burst(self):
        ...
    def join(self):
        ...


class Action(AbstractAction):
    def __init__(self, name: str):
        AbstractAction.__init__(self)
        
        print(f'initing action "{name}"')
        self.main_win = None
        
        self.name = name
        self.file_label = ''
        self.terminal_title = ''
        self.show_progress = True
        
        self.makes_new_dir = False
        self.makes_out_file = True
        self.makes_burst = False
        
        self.output_dir = None
        
        self.save_dialog = True
        
        self.notif_title_1 = _translate(
            'Notification', 'new PDF Document :')
        self.notif_title_2 = _translate(
            'Notification', 'new PDF Documents :')
        self.notif_title_3 = _translate(
            'Notification', '%i new PDF Documents in :')
        self.notif_icon = 'application-pdf'
        
        self.last_pdf_password = None
        
        if name not in self.actions.keys():
            print('Unknown action : %s' % name, file=sys.stderr)
            sys.exit(1)
        
        self.actions[name]()
    
    def start(self):
        self.checkAllFiles()
        if self.main_win:
            self.main_win.start()
        else:
            startScript()
    
    def checkAllFiles(self):
        many_dirs  = False
        common_dir = None
        self.output_dir = files[0].dirname
        
        #SET OUTPUT DIRECTORY
        for file in files:
            if file.dirname != self.output_dir:
                many_dirs = True
            
            if many_dirs:
                while not file.name.startswith(self.output_dir + '/'):
                    self.output_dir = os.path.dirname(self.output_dir)
        
        if self.makes_out_file:
            if many_dirs:
                tmp_dir = ''
                while not os.access(tmp_dir, os.W_OK):
                    tmp_dir, ok = QFileDialog.getExistingDirectory(None, 
                                                                _translate('Dialog', 'Choose Output Directory'), self.output_dir)
                    if not ok:
                        sys.exit(0)
                self.output_dir = tmp_dir
                
            elif len(files) >= 2:
                if not os.access(self.output_dir, os.W_OK):
                    output_dir, ok = QFileDialog.getExistingDirectory(None, 
                                                                _translate('Dialog', 'Choose Output Directory'), self.output_dir)
                    if not ok:
                        sys.exit(0)
        
        #CHANGE OUTPUT DIRECTORY IF A NEW DIRECTORY WILL BE CREATED
        if self.makes_new_dir:
            if len(files) >= MIN_FOR_MKDIR:
                self.output_dir = "%s/PDFs (%s)" % (self.output_dir, self.file_label)
                tmp_dir = self.output_dir
                
                n=1
                while os.path.exists(tmp_dir):
                    tmp_dir = "%s (%i)" % (self.output_dir, n)
                    n+=1
                
                self.output_dir = tmp_dir
            else:
                self.makes_new_dir = False
        
        #CHECK PDF INTEGRITY AND DECRYPT THEM IF NEEDED
        for file in files:
            file.unlockPdf()
            if file.error in (ERR_NOT_PDF, ERR_NO_PW):
                bad_files.append(file)
                bad_indexes.append(files.index(file))
                
        bad_indexes.reverse()
            
        for i in bad_indexes:
            files.__delitem__(i)
    
    #####################
    
    def compress(self):
        self.makes_new_dir  = True
        self.file_label     = _translate('File', 'compressed')
        self.terminal_title = _translate('Dialog', 'PDF compression')
        
    def uncompress(self):
        self.makes_new_dir  = True
        self.file_label     = _translate('File', 'uncompressed')
        self.terminal_title = _translate('Dialog', 'PDF decompression')
    
    def watermark(self):
        self.main_win = WatermarkDialog()
        
        self.makes_new_dir  = True
        self.file_label     = _translate('File', 'watermark')
        self.terminal_title = _translate('Dialog', 'PDF Watermark')
        
    def stamp(self):
        self.main_win = StampDialog()
        
        self.makes_new_dir  = True
        self.file_label     = _translate('File', 'stamp')
        self.terminal_title = _translate('Dialog', 'PDF Stamp')
    
    def extract(self):
        self.main_win = ExtractDialog()
        
        self.makes_new_dir  = True
        self.terminal_title = _translate('Dialog', 'PDF Extraction')
    
    def extractOddEven(self):
        self.file_label     = _translate('File', 'odd')
        self.terminal_title = _translate('Dialog', 'PDF Split Odd & Even')
        self.save_dialog = False
        
    def join(self):
        self.main_win = OrderDialog()
        
        self.show_progress  = False
        self.makes_out_file = False #Wrong, but it's used to don't ask for an output dir
        self.save_dialog    = False #Because, it has its own way to pre-name output file
        
        self.file_label     = _translate('File', 'join')
        self.terminal_title = _translate('Dialog', 'PDF Join')
        
    def burst(self):
        self.makes_burst   = True
        self.save_dialog   = False
        
        self.notif_title_1  = _translate('Notification', 'PDF Document Burst In:')
        self.notif_title_2  = _translate('Notification', 'PDF Documents Burst In:')
        self.notif_title_3  = _translate('Notification', '%i PDF Documents Burst In :')
        self.file_label     = _translate('File', 'burst')
        self.terminal_title = _translate('Dialog', 'PDF Burst')
        self.notif_icon     = 'folder'
    
class File(object):
    def __init__(self, path):
        self.path = os.path.realpath(path)
        self.dirname, sl, self.basename = self.path.rpartition('/')
        self.short,  pt, self.extension = self.basename.rpartition('.')
        
        if not self.short:
            #if file basename doesn't contains any '.'
            self.short, self.extension = self.extension, ''
        
        self.pretty_path = prettyFileName(self.path)
        
        self.out_path   = ''
        self.pretty_out = ''
        
        self.file_label = ''
        
        self.arguments = []
        
        self.pdf = None
        self.password = None
        self.error = ERR_OK
        
        #needed for extract pages
        self.export_line = ''
        self.line_edited = False
        
    def unlockPdf(self):
        try:
            self.pdf = PyPDF2.PdfFileReader(self.path)
        except:
            self.error = ERR_NOT_PDF
            return
        
        if not self.pdf.isEncrypted:
            return
            
        if action.last_pdf_password:
            if self.pdf.decrypt(action.last_pdf_password):
                self.password = action.last_pdf_password
                return
        
        password_dialog = PasswordDialog(self)
        if password_dialog.exec():
            self.password = password_dialog.getPassword()
            action.last_pdf_password = self.password
            return
        
        self.error = ERR_NO_PW
    
    def setOutPath(self, out_path):
        self.out_path = out_path
        self.pretty_out = prettyFileName(out_path)
    
    def generateOutPath(self):
        out_file = ''
        if action.makes_new_dir:
            if not os.path.exists(action.output_dir):
                os.mkdir(action.output_dir)
            
            out_file = "%s/%s" % (action.output_dir, self.basename)
        else:
            file_label = self.file_label
            if not file_label:
                file_label = action.file_label
            
            out_file = "%s/%s (%s).%s" % (action.output_dir, self.short, file_label, self.extension)
            
            n=1
            tmp_file = out_file
            while os.path.exists(tmp_file):
                tmp_file = "%s/%s (%s) (%i).%s" % (action.output_dir, self.short, file_label, n,  self.extension)
                n+=1
            out_file = tmp_file
                
        self.setOutPath(out_file)
        
class PasswordDialog(QDialog):
    def __init__(self, file):
        QDialog.__init__(self)
        self.ui = ui_password.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.labelFileName.setText(file.pretty_path)
        self.ui.labelWrongPassword.setText('')
        self.ui.checkBox.stateChanged.connect(self.showPassword)
        self.ui.pushButtonOk.clicked.connect(self.checkOk)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.pushButtonAbort.clicked.connect(sys.exit)
        
        self.file = file
        
        self.wpw_timer = QTimer()
        self.wpw_timer.setSingleShot(True)
        self.wpw_timer.setInterval(1000)
        self.wpw_timer.timeout.connect(self.hideWrongPassword)
        
        if len(files) < 2:
            self.ui.pushButtonAbort.setVisible(False)
        
    def showPassword(self, state):
        if state:
            self.ui.lineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.lineEdit.setEchoMode(QLineEdit.Password)
    
    def hideWrongPassword(self):
        self.ui.labelWrongPassword.setText('')
    
    def checkOk(self):
        pw = self.ui.lineEdit.text()
        if self.file.pdf.decrypt(pw):
            self.accept()
        else:
            self.ui.labelWrongPassword.setText(_translate('Dialog', 'Wrong Password !'))
            self.wpw_timer.start()
        
    def getPassword(self):
        return self.ui.lineEdit.text()

class TerminalDialog(QDialog):
    def __init__(self):
        if action.main_win:
            QDialog.__init__(self, action.main_win)
        else:
            QDialog.__init__(self)
            
        self.ui = ui_terminalDialog.Ui_Dialog()
        self.ui.setupUi(self)
        
        main_script.sig.init_terminal.connect(self.initTerminal)
        main_script.sig.change_file.connect(self.changeFile)
        main_script.sig.update_stderr.connect(self.updateStandardError)
        main_script.sig.update_stdout.connect(self.updateStandardOutput)
        main_script.sig.new_info.connect(self.addInfoText)
        main_script.sig.finished.connect(self.endOfAllProcesses)
        main_script.sig.up_progress.connect(self.setSubProgress)
        main_script.sig.dont_close.connect(self.dontCloseAfterFinished)
        
        self.pointTimer = QTimer()
        self.pointTimer.setInterval(1000)
        self.pointTimer.timeout.connect(self.addPoint)
        
        self.rejected.connect(self.shutOff)
        
        self.next_n = 0
        self.hasError = False
        self.finished = False
        
        self.close_after_finished = True
    
    def initTerminal(self):
        self.setWindowTitle(action.terminal_title)
        if action.makes_burst:
            self.ui.progressLabel.setText(_translate('Dialog', 'treating file %i/%i') % (1, len(files)) )
        else:
            self.ui.progressLabel.setText(_translate('Dialog', 'Create file %i/%i') % (1, len(files)) )
        
        if len(files) <= 1 or not action.show_progress:
            self.ui.progressBar.setVisible(False)
            self.ui.progressLabel.setVisible(False)
            
        self.show()
        
        if not files:
            self.endOfAllProcesses()
            return
    
    def cleanExit(self):
        if self.parent():
            self.parent().accept()
        else:
            self.accept()
    
    def dontCloseAfterFinished(self):
        self.close_after_finished = False
    
    def changeFile(self, file):
        i = files.index(file)
        if action.makes_burst:
            self.ui.progressLabel.setText(_translate('Dialog', 'Treating file %i/%i') % (i+1, len(files)) )
        else:
            self.ui.progressLabel.setText(_translate('Dialog', 'Create file %i/%i') % (i+1, len(files)) )
            
        self.ui.progressBar.setValue( (i * 100) / len(files) )
        
        if action.makes_burst:
            text = _translate('Terminal', 'treating %s') % file.pretty_path
        else:
            text = _translate('Terminal', 'creation of %s') % file.pretty_out
        self.addInfoText(text)
    
    def pleaseWait(self):
        self.addText(_translate('Terminal', 'please wait...'))
        self.pointTimer.start()
        
    def setSubProgress(self, float):
        current_value = self.ui.progressBar.value()
        interval = 100/len(files)
        value = current_value + float*interval
        self.ui.progressBar.setValue(value)
    
    def addPoint(self):
        self.ui.terminalDisplay.moveCursor(QTextCursor.End)
        self.ui.terminalDisplay.insertPlainText('.')
        self.ui.terminalDisplay.moveCursor(QTextCursor.End)
    
    def addText(self, text):
        self.pointTimer.stop()
        self.ui.terminalDisplay.appendHtml(text)
    
    def addInfoText(self, text):
        self.addText('')
        self.addText('<strong><div style=\'color: green\'>' + text + '</div></strong>')
        self.pleaseWait()
    
    def updateStandardOutput(self, text):
        self.pointTimer.stop()
        if text.endswith('\n'):
            text = text[:-1]
        self.ui.terminalDisplay.appendPlainText(text)
        
    def updateStandardError(self, text):
        self.pointTimer.stop()
        if text.endswith('\n'):
            text = text[:-1]
        self.ui.terminalDisplay.appendPlainText(text)
        
    def endOfAllProcesses(self):
        self.ui.progressLabel.setText(_translate('Dialog', 'Finished'))
        self.ui.progressBar.setValue(100)
        
        sendNotify()
        
        if self.close_after_finished and not bad_files:
            self.cleanExit()
            
        self.addText('<br>')
        
        for file in bad_files:
            if file.error == ERR_NOT_PDF:
                self.addText('<div style=\'color:red\'>' +  _translate('Terminal', '%s is not a valid PDF file, sorry !') % ('<strong>' + file.pretty_path + '</strong>') + '</div>')
            elif file.error == ERR_NO_PW:
                self.addText('<div style=\'color:red\'>' +  _translate('Terminal', 'You didn\'t enter a correct password for %s') % ('<strong>' + file.pretty_path + '</strong>') + '</div>')
        
        self.finished = True
            
    def shutOff(self):
        main_script.killCurrentProcess()
        
        if script_thread.isRunning():
            script_thread.terminate()
            
        if not self.finished:
            self.endOfAllProcesses()
        self.cleanExit()
        
class CustomDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        
    def closeEvent(self, event):
        if self.isVisible():
            t_dialog.shutOff()
        QDialog.closeEvent(self, event)

#Join Window
class PDFWidget(QListWidgetItem):
    def __init__(self, file):
        QListWidgetItem.__init__(self, None, QListWidgetItem.UserType)
        self.file = file
        self.setText(self.file.basename)
            
        pages = self.file.pdf.getNumPages()
        
        if pages == 1:
            pages_str = _translate('Tooltip', '1 page')
        else:
            pages_str = _translate('Tooltip', '%i pages') % pages
            
        self.setToolTip(self.file.pretty_path + '<br>' + pages_str)

class OrderDialog(CustomDialog):
    def __init__(self):
        CustomDialog.__init__(self)
        self.ui = ui_order_dialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowIcon(pdf_icon)
        
        self.ui.pushButtonJoin.clicked.connect(self.setOutPath)
        self.ui.pushButtonCancel.clicked.connect(sys.exit)
        
        self.out_path = ''
        
        self.show()
    
    def start(self):
        for file in files:
            pdf_widget = PDFWidget(file)
            self.ui.listWidget.addItem(pdf_widget)
        if self.ui.listWidget.count() < 2:
            QMessageBox.critical(self, _translate('Dialog', 'Not Enought Files'), _translate('Dialog', 'You need at least 2 PDF files to join them !'))
            sys.exit(0)
    
    def lockItems(self):
        self.ui.pushButtonJoin.setEnabled(False)
        self.ui.listWidget.setEnabled(False)
        self.ui.checkBoxShuffle.setEnabled(False)
    
    def setOutPath(self):
        #find common regex for all file names
        common_regex = self.ui.listWidget.item(0).file.basename
        
        for i in range(self.ui.listWidget.count()):
            basename = self.ui.listWidget.item(i).file.basename
            n = len(common_regex) if len(common_regex) < len(basename) else len(basename)
            for j in range(n):
                if basename[j] != common_regex[j]:
                    common_regex = common_regex[:j]
                    break
        
        
        if len(common_regex) < 3: #less than the 3 firsts letters are not the same
            common_regex = _translate('File', 'join')
        
        #change file name if exists
        n=1
        tmp_string = common_regex
        while os.path.exists("%s/%s.pdf" % (action.output_dir, common_regex)):
            common_regex = "%s (%i)" % (tmp_string, n)
            n+=1
        
        outfile_name = "%s/%s.pdf" % (action.output_dir, common_regex)
        
        filenames = []
        for file in files:
            filenames.append(file.path)
        
        #display file chooser
        exit_loop = False
        while not exit_loop:
            outfile_name, ok = QFileDialog.getSaveFileName(self, None, outfile_name, 'PDF (*.pdf)')
            
            if not ok:
                sys.exit(0)
                
            if not os.access(os.path.dirname(outfile_name), os.W_OK):
                QMessageBox.critical(self, _translate('Dialog', 'Permissions Error'), _translate('Dialog', 'You have no permission to write %s') % outfile_name)
            elif outfile_name in filenames:
                QMessageBox.critical(self, _translate('Dialog', 'Permissions Error'), _translate('Dialog', "You can't overwrite an input file !"))
            else:
                exit_loop = True
        
        self.out_path = outfile_name
        
        self.setEnabled(False)
        #self.lockItems()
        startScript()
        
    def getPdftkArguments(self):
        pdftk_args = []
        for i in range(self.ui.listWidget.count()):
            pdf_widget = self.ui.listWidget.item(i)
            pdftk_args.append(pdf_widget.file.path)
            
        for i in range(self.ui.listWidget.count()):
            pdf_widget = self.ui.listWidget.item(i)
            pdftk_args.append('input_pw')
            if pdf_widget.file.pdf.isEncrypted:
                pdftk_args.append(pdf_widget.file.password)
            else:
                pdftk_args.append('')
                
        if self.ui.checkBoxShuffle.isChecked():
            pdftk_args.append('shuffle')
        else:
            pdftk_args.append('cat')
            
        pdftk_args.append('output')
        pdftk_args.append(self.out_path)
        pdftk_args.append('verbose')
        
        return pdftk_args
    
    def getOutPath(self):
        return self.out_path


#extract window
class ExtractDialog(CustomDialog):
    def __init__(self):
        CustomDialog.__init__(self)
        self.ui = ui_extract.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.lineEdit.textEdited.connect(self.lineEditEdited)
        
        #self.ui.pushButtonOk.clicked.connect(self.accept)
        self.ui.actionNext.triggered.connect(self.nextFile)
        self.ui.pushButtonApplyAll.clicked.connect(self.applyAll)
        self.ui.toolButtonNext.setDefaultAction(self.ui.actionNext)
        self.ui.toolButtonNext.setFocus()
        
        self.ui.toolButtonPrevious.setDefaultAction(self.ui.actionPrevious)
        self.ui.actionPrevious.triggered.connect(self.previousFile)
        self.ui.toolButtonPrevious.setEnabled(False)
        
        self.ui.pushButtonCancel.clicked.connect(sys.exit)
        
        
        self.orig_next_text = self.ui.toolButtonNext.text()
        self.orig_next_icon = self.ui.toolButtonNext.icon()
        
        self.n_file = 0
        self.current_file = None
        
        self.show()
    
    def hideApplyAll(self):
        self.ui.pushButtonApplyAll.setVisible(False)
    
    def start(self):
        if len(files) < 2:
            self.ui.pushButtonApplyAll.setVisible(False)
            self.ui.toolButtonPrevious.setVisible(False)
            self.ui.labelFileNN.setVisible(False)
            
        if not files:
            print('Hey, there are no files !!!', file=sys.stderr)
            return
        
        self.current_file = files[self.n_file]
        self.updateLabelsAndButtons()
    
    def saveCurrentFile(self):
        if not self.current_file:
            return
        
        if not self.isTextValid(self.ui.lineEdit.text()):
            self.current_file.export_line = ''
            return
        
        self.current_file.arguments.clear()
        self.current_file.arguments.append(self.current_file.path)
        self.current_file.arguments.append('cat')
        
        file_label = ''
        n=0
        
        for arg in self.ui.lineEdit.text().split(' '):
            if arg:
                self.current_file.arguments.append(arg)
                file_label  += arg + ' '
                if '-' in arg:
                    n+=2
                else:
                    n+=1
                
        file_label  = file_label[:-1]
        
        if n >= 2:
            self.current_file.file_label = _translate('File', 'pages %s') % file_label
        else:
            self.current_file.file_label = _translate('File', 'page %s') % file_label
                
        self.current_file.generateOutPath()
        
        self.current_file.arguments.append('output')
        self.current_file.arguments.append(self.current_file.out_path)
        self.current_file.arguments.append('verbose')
        
        self.current_file.export_line = file_label
    
    def updateLabelsAndButtons(self, warning_max_page=False):
        #LABELS
        num_pages = self.current_file.pdf.getNumPages()
        
        if warning_max_page:
            if num_pages == 1:
                text = _translate('Dialog', "%s contains only 1 page.") % ('<strong>' + self.current_file.pretty_path + '</strong>')
            else:
                text = _translate('Dialog', "%(file)s contains only %(pages)s pages.") % {
                                    'file': '<strong>' + self.current_file.pretty_path + '</strong>', 
                                    'pages': '<strong>' + str(num_pages) + '</strong>'}
                
            text = '<div style="color: red">' + text + '</div>'
        else:
            if num_pages == 1:
                text = _translate('Dialog', "%s contains 1 page.") % ('<strong>' + self.current_file.pretty_path + '</strong>')
            else:
                text = _translate('Dialog', "%(file)s contains %(pages)s pages.") % {
                                    'file': '<strong>' + self.current_file.pretty_path + '</strong>', 
                                    'pages': '<strong>' + str(num_pages) + '</strong>'}
            
        self.ui.labelFilePages.setText(text)
        
        self.ui.labelLineEdit.setText(_translate('Dialog', "Enter the pages to extract from %s") % '<strong>' +   self.current_file.basename + '</strong>')
        
        self.ui.labelFileNN.setText(_translate('Dialog', 'File %i/%i') % (self.n_file +1, len(files)))
        
        
        #BUTTONS
        self.ui.toolButtonPrevious.setEnabled(bool(self.n_file > 0))
        
        if self.n_file >= len(files):
            self.accept()
            return
        
        if self.n_file +1 == len(files):
            self.ui.toolButtonNext.setText(_translate('Dialog', 'Ok'))
            self.ui.toolButtonNext.setIcon(QIcon.fromTheme('dialog-ok'))
            self.ui.pushButtonApplyAll.setEnabled(False)
        else:
            self.ui.toolButtonNext.setText(self.orig_next_text)
            self.ui.toolButtonNext.setIcon(self.orig_next_icon)
            self.ui.pushButtonApplyAll.setEnabled(True)
            
        #LINE_EDIT
        if self.current_file.export_line:
            self.ui.lineEdit.setText(self.current_file.export_line)
        else:
            self.ui.lineEdit.setText("1-%i" % self.current_file.pdf.getNumPages())
        
        
    def previousFile(self):
        if self.n_file == 0:
            print('hey, first file is yet selected', file=sys.stderr)
            return
        
        self.saveCurrentFile()
        self.n_file -=1
        self.current_file = files[self.n_file]
        self.updateLabelsAndButtons()
        
    def nextFile(self):
        self.saveCurrentFile()
        self.n_file +=1
        
        if self.n_file >= len(files):
            self.setEnabled(False)
            startScript()
            return
        
        self.current_file = files[self.n_file]
        self.updateLabelsAndButtons()
        
    def isTextValid(self, text):
        at_least_one_str = False
        
        for string in text.split(' '):
            if not string:
                continue
            
            at_least_one_str = True
            
            if '-' in string:
                if len(string.split('-')) != 2:
                    return False
                
                first, second = string.split('-')
                second_digit = ''
                
                if not ( first and second ):
                    return False
                
                if not ( first.isdigit() or first == 'end' ):
                    return False
                
                if first.isdigit() and not 0 < int(first) <= self.current_file.pdf.getNumPages():
                    return False
                
                if not ( second[0].isdigit() or second.startswith('end') ):
                    return False
                
                if second.startswith('end'):
                    second = second[3:]
                else:
                    while second and second[0].isdigit():
                        second_digit += second[0]
                        second = second[1:]
                    
                if second_digit and not 0 < int(second_digit) <= self.current_file.pdf.getNumPages():
                    return False
                
                if second.startswith('odd'):
                    second = second[3:]
                elif second.startswith('even'):
                    second = second[4:]
                    
                if second and not second in ('north', 'south', 'east', 'west', 'left', 'right', 'down'):
                    return False
                    
            else:
                string_digit = ''
                starts_with_end = False
                
                if not ( string[0].isdigit() or string.startswith(('end', 'odd', 'even')) ):
                    return False
                    
                if string.startswith('end'):
                    string = string[3:]
                    starts_with_end = True
                    
                if string.startswith('odd'):
                    string = string[3:]
                elif string.startswith('even'):
                    string = string[4:]
                elif not starts_with_end:
                    while string and string[0].isdigit():
                        string_digit += string[0]
                        string = string[1:]
                    
                if string_digit and not 0 < int(string_digit) <= self.current_file.pdf.getNumPages():
                    return False
                
                if string.startswith('odd'):
                    second = second[3:]
                    if string_digit and not int(string_digit) % 2:
                        return False
                    
                elif string.startswith('even'):
                    second = second[4:]
                    if string_digit and int(string_digit) % 2:
                        return False
                    
                if string and not string in ('north', 'south', 'east', 'west', 'left', 'right', 'down'):
                    return False
            
            
        if not at_least_one_str:
            return False
        
        return True
      
    def lineEditEdited(self, text):
        bool = self.isTextValid(text)
        self.ui.toolButtonNext.setEnabled(bool)
        self.ui.pushButtonApplyAll.setEnabled(bool and self.n_file+1 < len(files))
        self.current_file.line_edited = bool
        
    def checkLineEdit(self, text):
        bool = self.isTextValid(text)
        self.ui.toolButtonNext.setEnabled(bool)
        self.ui.pushButtonApplyAll.setEnabled(bool and self.n_file+1 < len(files))
        return bool
                    
    def applyAll(self):
        self.saveCurrentFile()
        
        while self.n_file < len(files):
            self.current_file = files[self.n_file]
            
            if not self.checkLineEdit(self.ui.lineEdit.text()):
                self.updateLabelsAndButtons(True)
                return
            
            if not self.current_file.line_edited:
                self.saveCurrentFile()
            
            self.n_file += 1
        
        self.setEnabled(False)
        startScript()

#watermark dialog

class WatermarkDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.watermark = settings.value('WatermarkPath', os.getenv('HOME'))
        
    def start(self):
        self.watermark, ok = QFileDialog.getOpenFileName(None, 
                                                    _translate('Dialog', 'Choose file to use as watermark'), 
                                                    self.watermark, 
                                                    _translate('Dialog', 'PDF Files (*.pdf)'))
        
        if not ok:
            sys.exit(0)
        settings.setValue('WatermarkPath', self.watermark)    
        
        startScript()

class StampDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.stamp = settings.value('StampPath', os.getenv('HOME'))
        
    def start(self):
        self.stamp, ok = QFileDialog.getOpenFileName(None, 
                                                    _translate('Dialog', 'Choose file to use as stamp'), 
                                                    self.stamp, 
                                                    _translate('Dialog', 'PDF Files (*.pdf)'))
        
        if not ok:
            sys.exit(0)
        settings.setValue('StampPath', self.stamp)    
        
        startScript()

    
class Process(QProcess):
    def __init__(self, command: str, arguments: list[str], notify: Optional[str]=None):
        QProcess.__init__(self)
        self.readyReadStandardError.connect(self.updateStderr)
        self.readyReadStandardOutput.connect(self.updateStdout)
        
        self.setProgram(command)
        self.setArguments(arguments)
        self.notify = notify
    
    def updateStderr(self):
        main_script.sig.update_stderr.emit(self.readAllStandardError().data().decode('utf-8'))
        
    def updateStdout(self):
        main_script.sig.update_stdout.emit(self.readAllStandardOutput().data().decode('utf-8'))


class Signaler(QObject):
    init_terminal = pyqtSignal()
    change_file = pyqtSignal(File)
    update_stdout = pyqtSignal(str)
    update_stderr = pyqtSignal(str)
    new_info = pyqtSignal(str)
    finished = pyqtSignal()
    up_progress = pyqtSignal(float)
    dont_close = pyqtSignal()
    close_terminal = pyqtSignal()

    
class MainScript(AbstractAction):    
    def __init__(self):
        AbstractAction.__init__(self)
        self.current_process = None
        self.sig = Signaler()
        
    def start(self):
        self.sig.init_terminal.emit()
        if action.name in self.actions:
            self.actions[action.name]()
        self.sig.finished.emit()
    
    def execute(self, command: str, arguments: str, notify: Optional[str]):
        del self.current_process
        self.current_process = Process(command, arguments, notify)
        self.current_process.start()
        self.current_process.waitForFinished(-1)
        
        if self.current_process.exitCode() == 0:
            if self.current_process.notify:
                notification_files.append(self.current_process.notify)
        else:
            self.sig.dont_close.emit()
    
    def killCurrentProcess(self):
        if self.current_process and self.current_process.state():
            self.current_process.kill()
    
    ##################
    
    def burst(self):
        for file in files:
            burst_dir = '%s/%s (%s)' % (action.output_dir, file.short, action.file_label)
            
            n=1
            while os.path.exists(burst_dir):
                burst_dir = '%s/%s (%s) (%i)' % (action.output_dir, file.short, action.file_label, n)
                n+=1
            
            os.mkdir(burst_dir)
            
            suffix = '%0' + ('%id' % len(str(file.pdf.getNumPages())) )
            file.setOutPath('%s/%s (%s).pdf' % (burst_dir, file.short, _translate('File', 'page %s') % suffix))
            pretty_out = prettyFileName(os.path.dirname(file.out_path))
            
            self.sig.change_file.emit(file)
            
            arguments = [file.path]
            if file.password:
                arguments += [ 'input_pw', file.password ]
            arguments += ['burst', 'output', file.out_path, 'verbose' ]
            
            self.execute('pdftk', arguments, pretty_out)
            
            doc_data = '%s/doc_data.txt' % os.path.dirname(file.out_path)
            if os.path.exists(doc_data):
                os.remove(doc_data)
            
    def join(self):
        arguments  = action.main_win.getPdftkArguments()
        pretty_out = prettyFileName(action.main_win.getOutPath())
        self.sig.new_info.emit(_translate('Terminal', 'Create %s') % pretty_out)
        self.execute('pdftk', arguments, pretty_out)
    
    def watermark(self):
        watermark = action.main_win.watermark
            
        for file in files:
            self.change_file.emit(file)
            
            arguments = [file.path]
            if file.password:
                arguments += ['input_pw', file.password ]
            arguments += ['background', watermark, 'output', file.out_path, 'verbose' ]
            
            self.execute('pdftk', arguments, file.pretty_out)
    
    def stamp(self):
        stamp = action.main_win.stamp
            
        for file in files:
            self.sig.change_file.emit(file)
            
            arguments = [file.path]
            if file.password:
                arguments += ['input_pw', file.password ]
            arguments += ['stamp', stamp, 'output', file.out_path, 'verbose' ]
            
            self.execute('pdftk', arguments, file.pretty_out)
    
    def compress(self):
        for file in files:
            self.sig.change_file.emit(file)
            
            arguments = []
            arguments.append(file.path)
            if file.password:
                arguments += [ 'input_pw', file.password ]
            arguments += ['output', file.out_path, 'compress', 'verbose' ]
            
            self.execute('pdftk', arguments, file.pretty_out)
    
    def uncompress(self):
        for file in files:
            self.sig.change_file.emit(file)
            
            arguments = []
            arguments.append(file.path)
            if file.password:
                arguments += [ 'input_pw', file.password ]
            arguments += ['output', file.out_path, 'uncompress', 'verbose' ]
            
            self.execute('pdftk', arguments, file.pretty_out)
    
    def extract(self):
        for file in files:
            self.sig.change_file.emit(file)
            self.execute('pdftk', file.arguments, file.pretty_out)
    
    def extractOddEven(self):
        for file in files:
            self.sig.change_file.emit(file)
            
            arguments = [file.path]
            if file.password:
                arguments += [ 'input_pw', file.password ]
            arguments += [ 'cat', '1-endodd', 'output', file.out_path, 'verbose' ]
            
            self.execute('pdftk', arguments, file.pretty_out)
            
            self.sig.up_progress.emit(1/2)
            
            if file.pdf.getNumPages() < 2:
                self.new_info.emit(_translate('Terminal', "%s doesn't contains any even page") % file.pretty_path)
                continue
            
            file.file_label = _translate('File', 'even')
            file.generateOutPath()
            
            self.sig.new_info.emit(_translate('Terminal', 'create %s') % file.pretty_out)
            
            arguments = [file.path]
            if file.password:
                arguments += [ 'input_pw', file.password ]
            arguments += [ 'cat', '1-endeven', 'output', file.out_path, 'verbose' ]
            
            self.execute('pdftk', arguments, file.pretty_out)
 
class AThread(QThread):
    def __init__(self):
        QThread.__init__(self)
    
    def run(self):
        main_script.start()

def startScript():
    for file in files:
        file.generateOutPath()
    
        if action.save_dialog and len(files) == 1:
            exit_loop = False
            
            while not exit_loop:
                out_path, ok = QFileDialog.getSaveFileName(
                    None, None, file.out_path, 'PDF Files (*.pdf)')

                if not ok:
                    sys.exit(0)
                
                if out_path == file.path:
                    QMessageBox.critical(
                        None,
                        _translate('Dialog', 'Permissions Error'),
                        _translate('Dialog', "You can't overwrite an input file !"))
                elif not os.access(os.path.dirname(out_path), os.W_OK):
                    QMessageBox.critical(
                        None, _translate('Dialog', 'Permissions Error'),
                        _translate('Dialog', 'You have no permission to write %s') % out_path)
                else:
                    exit_loop = True
            
            file.setOutPath(out_path)
    
    script_thread.start()

def sendNotify():
    notif_text = ''
            
    if action.makes_new_dir:
        notif_title = action.notif_title_3 % len(notification_files)
        notif_text  = action.output_dir
        notif_icon  = 'folder'
    else:
        for string in notification_files:
            notif_text += string + '<br>'
        notif_text = notif_text[:-4]
        
        notif_title = action.notif_title_1 if len(notification_files) == 1 else action.notif_title_2
        notif_icon  = action.notif_icon
    
    if notification_files:
        bus = dbus.SessionBus()
        
        #Notify
        notif = bus.get_object(
            "org.freedesktop.Notifications", "/org/freedesktop/Notifications")
        notify = dbus.Interface(notif, "org.freedesktop.Notifications")
        anything = notify.Notify(
            'doallwithpdf_%s' % action.name, 0, notif_icon, 
            notif_title, notif_text, '', '', 0)
        
        #Refresh all Dolphin Windows
        dolphin_dbus_objects = []
        for service in bus.list_names():
            if service.startswith('org.kde.dolphin-'):
                dolphin_dbus_objects.append(service)
                
        for service in dolphin_dbus_objects:
            dbus_object = bus.get_object(service, "/dolphin/Dolphin_1/actions/reload")
            dbus_itface = dbus.Interface(dbus_object, 'org.qtproject.Qt.QAction')
            dbus_reload = dbus_itface.trigger()

#####MAIN######

if __name__ == '__main__':
    print('maraoko', sys.argv)
    pdf_icon = QIcon.fromTheme('application-pdf')
    
    app = QApplication(sys.argv)
    app.setWindowIcon(pdf_icon)
    app.setApplicationName("DoAllWithPDF")
    app.setApplicationVersion(VERSION)
    app.setOrganizationName("DoAllWithPDF")
    
    ## Translation process
    locale = QLocale.system().name()
    appTranslator = QTranslator()
    if appTranslator.load(
            "%s/locale/doallwithpdf_%s" %
                (os.path.dirname(os.path.dirname(sys.argv[0])), locale)):
        app.installTranslator(appTranslator)
    _translate = app.translate
    
    settings = QSettings()
    
    if len(sys.argv) <= 2:
        print('Not enought arguments, nothing to do.', file=sys.stderr)
        sys.exit()
    
    
    action = Action(sys.argv[1])
    
    #store files
    files = list[File]()
    bad_files = list[File]()
    bad_indexes = list[int]()
    notification_files = []
    
    for path in sys.argv[2:]:
        file = File(path)
        files.append(file)
    
    if not files:
        print('Not enought arguments, nothing to do.', file=sys.stderr)
        sys.exit()
    
    main_script = MainScript()
    t_dialog = TerminalDialog()
    script_thread = AThread()
    action.start()
    app.exec()
    del app
    
    
    
