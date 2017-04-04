#!/bin/bash
#
# 	Part of DoAllWithPDF_servicemenu version 1.2.0
# 	Copyright (C) 2015 Mathieu PICOT <picotmathieu@gmail.com>
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#



#### languages strings messages #################
# Syntax for strings name is: msg_[$action]_$window_[$section]


load_language_commons(){
#$1:$lang (2 letters)
case "$1" in
    en )
        #dependencies
        msg_depend_title="dependencies error"
        
        #terminal echos for conversion
        msg_term_title_conversion="%s Conversion"
        msg_first_echo_conversion="%s conversion of :"
        msg_term_conversion='conversion'
        msg_term_from='    from :'
        msg_term_to__='      to :'
        
        #Notification errors
        msg_notification_error_title="Errors on files"
        msg_notification_error="Fail to create files :"
        
        #Name for Command at the top right of each dialog box
        msg_command="Command"
        msg_commands="Commands"
        
        #commons to many windows
        msg_choose_folder="Choose the folder for the new files"
        msg_wrong_fields="You entered incorrect fields, repeat !"
        msg_wrong_fields_title="Incorrects fields"
        msg_processing_file="processing file"
        msg_terminal_error="There were errors, press a button to close the terminal"
        
        #outputFileNameIt;outputFileNameIt_convert
        msg_outFile_saveFile_title="Save file ..."
        msg_outFile_unwritable_dir="%s isn't writable, repeat !" 
        msg_outFile_unwritable_dir_title="Permissions Error"
        msg_outFile_sameInOut="Output file can't be the same one as input file."$'\n'"Try again !"
        msg_outFile_sameInOut_title="Same File !"
        msg_outFile_existingFile="\"%s\" already exists."$'\n'"Do you want to overwrite it ?"
        msg_outFile_existingFile_title="Existing File"
        
        #Notification titles
        msg_new_file_many="new %s files :"
        msg_new_file_one="new %s file :"
        msg_new_pdfdoc_one="New PDF document :"
        msg_new_pdfdoc_many="New PDF documents :"
        msg_new_pdfdoc_newdir="%i New PDF documents in :"
        msg_new_image_one="New %s image :"
        msg_new_image_many="New %s images :"
        msg_new_txt_one="New text file :"
        msg_new_txt_many="New text files :"
        msg_new_djvu_one="New DjVu document :"
        msg_new_djvu_many="New DjVu documents :"
        msg_new_html_one="New HTML file :"
        msg_new_html_many="New HTML files :"
        msg_new_postscript_one="New PostScript file :"
        msg_new_postscript_many="New PostScript files :"
        msg_new_odt_one="new ODT document :"
        msg_new_odt_many="new ODT documents :"
        msg_new_docx_one="new Word document :"
        msg_new_docx_many="new Word documents :"
        msg_new_ods_one="new ODS sheet :"
        msg_new_ods_many="new ODS sheets  :"
        msg_new_xlsx_one="new Excel sheet :"
        msg_new_xlsx_many="new Excel sheets :"
        msg_new_odp_one="new ODP presentation :"
        msg_new_odp_many="new ODP presentations :"
        msg_new_pptx_one="new PowerPoint presentation :"
        msg_new_pptx_many="new PowerPoint presentations :"
        msg_new_csv_one="new CSV file :"
        msg_new_csv_many="new CSV files :"
        
        msg_new_Images_one="New Image :"
        msg_new_Images_many="New Images :"
        msg_new_Images_InDir="New Images in :"
        msg_noti_rotate_90_many="Images turned to the right:"
        msg_noti_rotate_90_one="Image turned to the right :"
        msg_noti_rotate_180_many="Images turned down :"
        msg_noti_rotate_180_one="Image turned down :"
        msg_noti_rotate_270_many="Images turned to the left :"
        msg_noti_rotate_270_one="Image turned to the left :"
        msg_noti_rotate_angle_many="Images turned with an angle of %s° :"
        msg_noti_rotate_angle_one="Image turned with an angle of %s° :"
        msg_noti_mirror_horizontal_many="Images with horizontal mirror :"
        msg_noti_mirror_horizontal_one="Image with horizontal mirror :"
        msg_noti_mirror_vertical_many="Images with vertical mirror :"
        msg_noti_mirror_vertical_one="Image with vertical mirror :"
        
        msg_new_burst="Burst PDF documents in: "
        msg_new_unattach="Attachment extracted in: "
        msg_new_extracted_images="Images extracted in : "
        msg_new_print="Printing : "
        
        #print
        msg_print_choose_printer="Choose Printer:"
        msg_print_choose_printer_title="Printers"
        
        #OCR (common to DoAllWithPDF and imagemanipulation)
        msg_progress_OCR_title="Character Recognition"
        msg_depend_tesseract="tesseract is missing. Please install tesseract-ocr !"
        L_english="english"
        L_french="french"
        L_german="german"
        L_italian="italian"
        L_russian="russion"
        L_esperanto="esperanto"
        msg_OCR_choose_language1="Which language do you want to use for OCR ?"
        msg_OCR_choose_language2="To use an other language, <br>install tesseract package which name ends <br>by the first 3 letters of the language."
        msg_OCR_choose_language3="For example, <br>to install english language, install tesseract-ocr-eng package."
        msg_OCR_choose_language_title="Language"
        msg_OCR_OCR="Optical Character Recognition"
        msg_OCR_extracting_images="Extracting images from:"
        msg_OCR_image="image"

        ;;
    fr )

        #dependencies
        msg_depend_title="Erreur de dépendances"
        
        #echos de terminal pour la conversion
        msg_term_title_conversion="Conversion en %s"
        msg_first_echo_conversion="Conversion en %s de :"
        msg_term_conversion='conversion'
        msg_term_from='      de :'
        msg_term_to__='    vers :'
        
        #Notification d'erreur
        msg_notification_error_title="Erreurs sur les fichiers"
        msg_notification_error="Échec de la création des fichiers :"
        
        #Nom pour commande en haut à droite des fenêtres de dialogue
        msg_command="Commande"
        msg_commands="Commandes"
        
        #commons to many windows
        msg_choose_folder="Dans quel dossier enregistrer les nouveaux fichiers ?"
        msg_wrong_fields="<span style=\"color: #FF0000;\">Vous avez saisi des champs incorrects, recommencez !</span>"
        msg_wrong_fields_title="champs incorrects"
        msg_processing_file="traitement du fichier"
        msg_terminal_error="Il y a eu des erreurs, appuyez sur une touche pour fermer le terminal"
        
        
        #outputFileNameIt; outputFileNameIt_convert
        msg_outFile_saveFile_title="Sauver le fichier ..."
        msg_outFile_unwritable_dir="%s n'est pas inscriptible, recommencez !" 
        msg_outFile_unwritable_dir_title="Erreur de Permissions"
        msg_outFile_sameInOut="Le fichier de sortie ne peut pas être le même que le fichier d'entrée."$'\n'"Recommencez !"
        msg_outFile_sameInOut_title="Même Fichier !"
        msg_outFile_existingFile="Le fichier \"%s\" existe déjà."$'\n'"Êtes vous-sûr de vouloir l'écraser ?"
        msg_outFile_existingFile_title="Fichier existant"
        
        
        #Titre des notifications
        msg_new_file_many="fichiers %s créés :"
        msg_new_file_one="fichier %s créé :"
        msg_new_pdfdoc_one="document PDF créé :"
        msg_new_pdfdoc_many="documents PDF créés :"
        msg_new_pdfdoc_newdir="%i documents PDF créés dans :"
        msg_new_image_many="Images %s créées :"
        msg_new_image_one="Image %s créée :"
        msg_new_djvu_one="document DjVu créé :"
        msg_new_djvu_many="documents DjVu créés :"
        msg_new_html_one="fichier HTML créé :"
        msg_new_html_many="fichiers HTML créés :"
        msg_new_postscript_one="document PostScript créé :"
        msg_new_postscript_many="documents PostScript créés :"
        msg_new_odt_one="document ODT créé :"
        msg_new_odt_many="documents ODT créés :"
        msg_new_docx_one="document Word créé :"
        msg_new_docx_many="documents Word créés :"
        msg_new_ods_one="tableur ODS créé :"
        msg_new_ods_many="tableurs ODS créés  :"
        msg_new_xlsx_one="tableur Excel créé :"
        msg_new_xlsx_many="tableurs Excel créés :"
        msg_new_odp_one="présentation ODP créée :"
        msg_new_odp_many="présentations ODP créées :"
        msg_new_pptx_one="présentation PowerPoint créée :"
        msg_new_pptx_many="présentations PowerPoint créées :"
        msg_new_csv_one="fichier CSV créé :"
        msg_new_csv_many="fichiers CSV créés :"
        
        msg_new_Images_one="Image créée :"
        msg_new_Images_many="Images créées :"
        msg_new_Images_InDir="Images créées dans :"
        msg_noti_rotate_90_many="Images tournées vers la droite :"
        msg_noti_rotate_90_one="Image tournée vers la droite :"
        msg_noti_rotate_180_many="Images renversées :"
        msg_noti_rotate_180_one="Image renversée :"
        msg_noti_rotate_270_many="Images tournées vers la gauche :"
        msg_noti_rotate_270_one="Image tournée vers la gauche :"
        msg_noti_rotate_angle_many="Images tournées d'un angle de %s° :"
        msg_noti_rotate_angle_one="Image tournée d'un angle de %s° :"
        msg_noti_mirror_horizontal_many="Images avec miroir horizontal :"
        msg_noti_mirror_horizontal_one="Image avec miroir horizontal :"
        msg_noti_mirror_vertical_many="Images avec miroir vertical :"
        msg_noti_mirror_vertical_one="Image avec miroir vertical :"
        
        msg_new_txt_one="fichier texte créé :"
        msg_new_txt_many="fichiers texte créés :"
        msg_new_burst="Documents PDF éclatés dans :"
        msg_new_unattach="Pièces jointes extraites dans :"
        msg_new_extracted_images="Images extraites dans :"
        msg_new_print="Impression de :"
        
        #Imprimer (commun à DoAllWithPDF et OfficeConverter)
        msg_print_choose_printer="Choisissez l'imprimante:"
        msg_print_choose_printer_title="Imprimantes"
        
        #OCR (commun à DoAllWithPDF et imagemanipulation)
        msg_progress_OCR_title="Reconnaissance de Caractères"
        msg_depend_tesseract="Le programme tesseract est requis.
Installez tesseract-ocr !

Pensez aussi à installer tesseract-ocr-fra 
pour traiter des documents en français !"
        L_english="anglais"
        L_french="français"
        L_german="allemand"
        L_italian="italien"
        L_russian="russe"
        L_esperanto="espéranto"
        msg_OCR_choose_language1="Quelle langue voulez-vous utiliser pour la reconnaissance de caractères ?"
        msg_OCR_choose_language2="Pour utiliser une autre langue, <br>installez le paquet tesseract dont le nom termine <br>par les 3 premières lettres de cette langue."
        msg_OCR_choose_language3="Par exemple, <br>pour installer le français, installez le paquet tesseract-ocr-fra"
        msg_OCR_choose_language_title="Langue"
        msg_OCR_OCR="Reconnaissance Optique des Caractères"
        msg_OCR_extracting_images="Extraction des images de:"
        msg_OCR_image="image"
        
        ;;
    it )
        #dependencies
        msg_depend_title="Errore nelle dipendenze"
        
        #terminal echos for conversion
        msg_term_title_conversion="Conversione in %s"
        msg_first_echo_conversion="Conversione in %s di :"
        msg_term_conversion='conversione'
        msg_term_from='      da :'
        msg_term_to__='       a :'
        
        #Notification errors
        msg_notification_error_title="Errore nei files"
        msg_notification_error="Errore nella creazione dei files :"
        
        #Nom pour commande en haut à droite des fenêtres de dialogue
        msg_command="Comando"
        msg_commands="Comandi"
        
        #commons to many windows
        msg_choose_folder="Sgegli la cartella per i nuovi files"
        msg_wrong_fields="<span style=\"color: #FF0000;\">Hai inserito valori errati, riprendi !</span>"
        msg_wrong_fields_title="valori errati"
        msg_processing_file="elaborazione del file"
        msg_terminal_error="Ci sono stati degli errori, premi un pulsante per uscire dal terminale"
        
        #outputFileNameIt; outputFileNameIt_convert
        msg_outFile_saveFile_title="Salva il file ..."
        msg_outFile_unwritable_dir="%s non è scrivibile, riprendi !" 
        msg_outFile_unwritable_dir_title="Errore nei Permessi"
        msg_outFile_sameInOut="Il file di destinazione non può essere lo stesso del file d'inizio."$'\n'"Riprova !"
        msg_outFile_sameInOut_title="Stesso File !"
        msg_outFile_existingFile="Il file \"%s\" esiste già."$'\n'"Lo vuoi sovrascrivere ?"
        msg_outFile_existingFile_title="File esistente"
        
        #Notification title
        msg_new_file_many="files %s creati :"
        msg_new_file_one="file %s creato :"
        msg_new_pdfdoc_one="Nuovo documento PDF :"
        msg_new_pdfdoc_many="Nuovi documenti PDF :"
        msg_new_pdfdoc_newdir="%i Nuovi documenti PDF in :"
        msg_new_image_one="Nuova immagine %s :"
        msg_new_image_many="Nuove immagini %s :"
        msg_new_txt_one="Nuovo file di testo :"
        msg_new_txt_many="Nuovi files di testo :"
        msg_new_djvu_one="Nuovo documento DjVu :"
        msg_new_djvu_many="Nuovi documenti DjVu :"
        msg_new_html_one="Nuovo file HTML :"
        msg_new_html_many="Nuovi files HTML :"
        msg_new_postscript_one="Nuovo file PostScript :"
        msg_new_postscript_many="Nuovi files PostScript :"
        msg_new_odt_one="documento ODT creato :"
        msg_new_odt_many="documenti ODT creati :"
        msg_new_docx_one="documento Word creato :"
        msg_new_docx_many="documenti Word creati :"
        msg_new_ods_one="foglio di calcolo ODS creato :"
        msg_new_ods_many="fogli di calcolo ODS creati  :"
        msg_new_xlsx_one="foglio di calcolo Excel creato :"
        msg_new_xlsx_many="fogli di calcolo Excel creati :"
        msg_new_odp_one="presentazione ODP creata :"
        msg_new_odp_many="presentazioni ODP create :"
        msg_new_pptx_one="presentazione PowerPoint creata :"
        msg_new_pptx_many="presentazioni PowerPoint create :"
        msg_new_csv_one="file CSV creato :"
        msg_new_csv_many="files CSV creati :"
        
        msg_new_Images_one="Nuova Immagine :"
        msg_new_Images_many="Nuove Immagini :"
        msg_new_Images_InDir="Nuove Immagini in :"
        msg_noti_rotate_90_many="Immagini ruotate a destra :"
        msg_noti_rotate_90_one="Immagine ruotata a destra :"
        msg_noti_rotate_180_many="Immagini capovolte :"
        msg_noti_rotate_180_one="Immagine capovolta :"
        msg_noti_rotate_270_many="Immagini ruotate a sinistra :"
        msg_noti_rotate_270_one="Immagine ruotata a sinistra :"
        msg_noti_rotate_angle_many="Images turned with an angle of %s° :"
        msg_noti_rotate_angle_one="Image turned with an angle of %s° :"
        msg_noti_mirror_horizontal_many="Images with horizontal mirror :"
        msg_noti_mirror_horizontal_one="Image with horizontal mirror :"
        msg_noti_mirror_vertical_many="Images with vertical mirror :"
        msg_noti_mirror_vertical_one="Image with vertical mirror :"
        
        msg_new_burst="Separa i documenti PDF in : "
        msg_new_unattach="Estrai gli allegati in :"
        msg_new_extracted_images="Estrai le immagini in :"
        msg_new_print="Stampa :"
        
        #print
        msg_print_choose_printer="Seleziona la stampante:"
        msg_print_choose_printer_title="Stampanti"
        
        #OCR (common to DoAllWithPDF and imagemanipulation)
        msg_progress_OCR_title="Riconoscimento Ottico"
        L_english="inglese"
        L_french="francese"
        L_german="tedesco"
        L_italian="italiano"
        L_russian="russo"
        L_esperanto="esperanto"
        msg_OCR_choose_language1="Quale lingua vuoi utilizzare per l'OCR ?"
        msg_OCR_choose_language2="Per utilizzare un'altra lingua, <br>installa il pacchetto tesseract il cui nome termina <br>con le prime 3 lettere della lingua."
        msg_OCR_choose_language3="Ad esempio, <br>per installare la lingua inglese, installa il pacchetto tesseract-ocr-eng."
        msg_OCR_choose_language_title="Lingua"
        msg_OCR_OCR="Riconoscimento Ottico dei Caratteri"
        msg_OCR_extracting_images="Estrazione di immagini da :"
        msg_OCR_image="immagine"
        
        ;;
    de )
        #that's all we have now
        
        #print
        msg_print_choose_printer="Wählen Sie Drucker"
        msg_print_choose_printer_title="Printers"
        ;;
    ru )
        #that's all we have now
        
        #print
        msg_print_choose_printer="Выберите принтер:"
        msg_print_choose_printer_title="Printers"
        ;;
esac
}
################################################


#for sed substitution, input (in sed 's/x/y/')
meta_zap_in(){
    echo "$1"|sed 's/\\/\\\\/g' |sed -e 's/\^/\\^/g' -e 's/\$/\\$/g' -e 's/\./\\./g' -e 's/\*/\\*/g' -e 's/\[/\\[/g' -e 's/\]/\\]/g' -e 's/\//\\\//g'
}

#for sed substitution, output
meta_zap_out(){
    echo "$1"|sed 's/\\/\\\\/g'|sed -e 's|/|\\/|g' -e 's/&/\\&/g' 
}

#prevent html code
meta_H(){
    echo "$1"|sed -e 's/&/\&amp;/g' -e 's/</\&lt;/g' -e 's/>/\&gt;/g' 
}

tabstolines(){
    for arg;do
        echo "$arg"
    done
}

#kreadconfig
krc(){
    Parameter=$(kreadconfig --file "$ScriptConfigFile" --group "$1" --key "$2")
    [ -n "$ConfRead" ] && echo "$Parameter" || echo "$3"
}

#kwriteconfig
kwc(){
    kwriteconfig --file "$ScriptConfigFile" --group "$1" --key "$2" "$3"
}

#kdialog, for less text and always attach to terminal
kdial(){
    DialTitle="$1"
    shift
    kdialog --attach "$Winid" --title "$DialTitle" "$@" 2>/dev/null
}

pydial(){
    pydir="$1"
    shift
    pyfile="$DataDir/$pydir/${0##*/}"
    
    if [ -f "$pyfile" ];then
        python3 "$pyfile" --attach "$Winid" "$@"
    else
        kdial "Missing files" --msgbox "missing file $pyfile , sorry !"
        false
    fi
}
    
get_datadir(){
    #$1:DataDir name
    InstallPath=('/usr' '/usr/local' "$HOME/.local")

    for InstallDir in "${InstallPath[@]}";do
        [ -d "$InstallDir/share/$1" ] && DataDir="$InstallDir/share/$1"
    done

    if [ -z "$DataDir" ];then
        kdial "Missing Files" --sorry "Missing Data Dir $1 in ${InstallPath[*]}"
        exit 1
    fi
    
    echo "$DataDir"
}

dependencies(){
    #$1:text on window
    #:$2-$3-*:executables
    dependencies_text="$1"
    shift
    if ! which "$@" >/dev/null;then
        kdial "$msg_depend_title" --sorry "$dependencies_text"
        exit 1
    fi
}

msg_command_total_it(){
    case $# in
        1 )
            msg_command_total="<small><div align=\"right\"><i> $msg_command : $1 </i><hr /></div></small>" ;;
        * )
            msg_command_total="<small><div align=\"right\"><i> $msg_commands : $@ </i><hr /></div></small>"
    esac
}

burstDirIt(){
    #$1:outputDir
    #$2:complete file
    #$3:text to put between '()'
    baseFile="${2##*/}"
    DirName="${baseFile%.*} ($3)"
    TmpVar="$DirName"
    Ct=1

    while [ -e "$1/$TmpVar" ];do
        TmpVar="$DirName ($Ct)"
        ((Ct++))
    done
        
    DirName="$TmpVar"
    echo "$1/$DirName"
}

mkdir_for_a_lot(){
#fonction for making a dir and gives to output file the same name as original
#$1:message to put between '()'

if [ $HowManyFiles -ge 5 ];then
# if $AlotOfFiles;then
    outputDir="$outputDir/$msg_dir_for_a_lot ($1)"
    TmpVar="$outputDir"
    ct=1
    while [ -e "$TmpVar" ];do
        TmpVar="$outputDir ($ct)"
        ((ct++))
    done
    
    outputDir="$TmpVar"
    unset TmpVar ct
    mkdir "$outputDir"
    LotOfFiles_in_a_new_dir=true
fi
}

#Mute fonction ( if you want to echo something: echo whattoecho >/dev/stderr )
#get output file name
outputFileNameIt(){
#$1: Complete input file name
#$2: note between '()' to write in output file name

    if $LotOfFiles_in_a_new_dir ;then
        outFile="$outputDir/${1##*/}"
    else
        baseFile="${1##*/}"
        baseFileNoExt="${baseFile%.*}"
        Extension="${baseFile##*.}"
        outFile="$outputDir/${baseFileNoExt} ($2).$Extension"
        
#         outFile="$outputDir/$(echo "${1##*/}"|sed 's/\.pdf$//'|sed "s/$/ ($2).pdf/")"
        #Rename output file name if file already exists
        Ct=1
        TmpVar="$outFile"
        
        while [ -e "$TmpVar" ];do
            TmpVar="$outputDir/${baseFileNoExt} ($2) ($Ct).$Extension"
#             TmpVar=$(echo "$outFile"|sed 's/\.pdf$//'|sed "s/$/ ($Ct).pdf/")
            ((Ct++))
        done
        
        outFile="$TmpVar"
    fi
    
        #Dialog box to rename output file, only if there is only one file
    if $Onlyonefile;then
        TmpVar=$(echo "$outFile" |sed "s/\"/'/g")
    
        ExitLoop=false
        until $ExitLoop;do
#             MimeType=kmimetypefinder5 "$1"
            outFile=$(kdial "${msg_outFile_saveFile_title}" --icon document-save --getsavefilename "$TmpVar" )\
                    || return 1
            if [[ "$outFile" == "$1" ]];then
                kdial "$msg_outFile_sameInOut_title" --sorry "$msg_outFile_sameInOut"
            elif [ ! -w "${outFile%/*}" ];then
                kdial "$msg_outFile_unwritable_dir_title" --sorry "$(printf "$msg_outFile_unwritable_dir" "${outFile%/*}")"
            elif [ -e "$outFile" ];then
                kdial "$msg_outFile_existingFile_title" --dontagain $ScriptConfigFile:OverwriteExistingFile --warningcontinuecancel "$(printf "$msg_outFile_existingFile" "$outFile")" && ExitLoop=true
            else
                ExitLoop=true
            fi
        done
    fi
    
    echo "$outFile"
}

#Mute fonction ( if you want to echo something: echo whattoecho >/dev/stderr )
#get output file name
outputFileNameIt_convert(){

#$1: Complete input file name
#$2: extension
#$3: type MIME
#$4: Number between filename and extension (for convert to images) ##
    
    InFileBase="${1##*/}"
    outFile="$outputDir/${InFileBase%.*}"
    [ -n "$2" ] && outFile=$(echo "$outFile"|sed "s/$/.$2/")

    #Rename output file name if file already exists
    Ct=1
    TmpVar="$outFile"
    while [ -e "$TmpVar" ];do
        TmpVar=$(echo "$outFile"|sed "s/\.$2$//"|sed "s/$/ ($Ct).$2/")
        ((Ct++))
    done
    
    outFile="$TmpVar"
    echo "$outFile"
} 
    

exit_function_many(){
    progress_dialog close
    notification_dialog $1
    exit 0
}

inkonsoleit(){
    export DataDir houston_dir lang action action_option LotOfFiles_in_a_new_dir Onlyonefile AlotOfFiles \
           HowManyFiles outputDir AllFilesInLines
    
    until [ $# = 0 ];do
        if [[ "$1" == '--' ]];then 
            shift #remove '--'
            break
        fi
        export $1
        shift
    done
     
    get_konsole_title_and_first_echo "$action" "$action_option"
    "$houston_dir/ks_bug_workaround.py" --nofork --hide-tabbar --hide-menubar -p tabtitle="$konsole_title" \
                                    -p BlinkingCursorEnabled=true -e "$0"  //fast_main "$@" 2>/dev/null
    exit 0
}

progress_dialog(){
    if $AlotOfFiles;then
        case $1 in
            open )
                Cal=1
                ProgressPDF=$(kdial "$Progress_Title" --progressbar "$msg_processing_file $Cal/$HowManyFiles" $HowManyFiles 2>/dev/null)
                qdbus $ProgressPDF showCancelButton true >/dev/null
                ;;
            checkcancel )
                #$2:For Notification
                #$3_4_*:files or dirs to remove
                if $(qdbus $ProgressPDF wasCancelled);then
                    qdbus $ProgressPDF close >/dev/null
                    notification_dialog $2
                    rm -R "$3"
                    exit 0
                elif ! qdbus|grep -q ${ProgressPDF%/*};then
                    ProgressPDF=$(kdialog "$Progress_Title" --progressbar "$msg_processing_file $Cal/$HowManyFiles" $HowManyFiles 2>/dev/null)
                    qdbus $ProgressPDF showCancelButton true >/dev/null
                    qdbus $ProgressPDF value $Cal >/dev/null
                fi
                qdbus $ProgressPDF setLabelText "$msg_processing_file $Cal/$HowManyFiles" >/dev/null
                ;;
            end )
                qdbus $ProgressPDF value $Cal >/dev/null
                ((Cal++))
                if $(qdbus $ProgressPDF wasCancelled);then
                    qdbus $ProgressPDF close >/dev/null
                    notification_dialog $2
                    exit 0
                elif ! qdbus|grep -q ${ProgressPDF%/*};then
                    ProgressPDF=$(kdialog "$Progress_Title" --progressbar "$msg_processing_file $Cal/$HowManyFiles" $HowManyFiles 2>/dev/null)
                    qdbus $ProgressPDF showCancelButton true >/dev/null
                    qdbus $ProgressPDF value $Cal >/dev/null
                fi
                [ $Cal -le $HowManyFiles ] && qdbus $ProgressPDF setLabelText "$msg_processing_file $Cal/$HowManyFiles" >/dev/null
                ;;
            close )
                qdbus $ProgressPDF close >/dev/null
        esac
    fi
}

DialogNotIt(){
    PrettyFile=$(echo "$2"|sed "s/^$(meta_zap_in "$HOME")\//~\//")
    
    case $1 in
        0 )
            NotiFiles=$(echo "$NotiFiles"$'\n'"$PrettyFile"|sed '/^$/d')
            ;;
        * )
            ErrorNotiFiles="$ErrorNotiFiles"$'\n'"$PrettyFile"
            
            if [ -n "$4" ];then
                FullErrorDetails="$FullErrorDetails"$'\n'"from : $3"$'\n'"to : $2"$'\n'"via : $4"$'\n'$'\n'"$ErrorDetails"$'\n'$'\n'
            else
                FullErrorDetails="$FullErrorDetails"$'\n'"from : $3"$'\n'"to : $2"$'\n'$'\n'"$ErrorDetails"$'\n'$'\n'
            fi
            
            unset ErrorDetails
    esac
}

notification_dialog(){
    clean_notifiles(){
        if [ $NL = 1 ];then
            echo "$NotiFiles"
        else
            IFS=$'\n'
            for line in $NotiFiles;do
                DirLine="${line%/*}"
                echo "$DirLine/"
                break
            done
            
            
            for line in $NotiFiles;do
                echo "&#9658; ${line##*/}"
            done
        fi
    }        
    
    if [ -n "$NotiFiles" ];then
        NL=$(echo "$NotiFiles"|wc -l)
        NotiFiles=$(clean_notifiles)
        
        case $1 in
            pdf )
                KNTitleMany="$msg_new_pdfdoc_many"
                KNTitle="$msg_new_pdfdoc_one"
                NotiIcon=application-pdf
                
                if $LotOfFiles_in_a_new_dir;then
                    KNTitleMany=$(printf "$msg_new_pdfdoc_newdir" $NL)
                    NotiFiles=$(echo "$outputDir"|sed "s/^$(meta_zap_in "$HOME")\//~\//")
                    NotiIcon=folder-documents
                fi
                ;;
            html )
                KNTitleMany="$msg_new_html_many"
                KNTitle="$msg_new_html_one"
                NotiIcon=text-html
                ;;
            postscript )
                KNTitleMany="$msg_new_postscript_many"
                KNTitle="$msg_new_postscript_one"
                NotiIcon=application-postscript
                ;;
            txt )
                KNTitleMany="$msg_new_txt_many"
                KNTitle="$msg_new_txt_one"
                NotiIcon=text-plain
                ;;
            ppm )
                KNTitleMany="$msg_new_Images_many" 
                KNTitle="$msg_new_Images_one"
                NotiIcon=image
                [[ "$KNTitle" == "$msg_new_Images_InDir" ]] && NotiIcon=folder-image
                ;;
            djvu )
                KNTitleMany="$msg_new_djvu_many" 
                KNTitle="$msg_new_djvu_one"
                NotiIcon=image
                ;;
            odt )
                KNTitleMany="$msg_new_odt_many"
                KNTitle="$msg_new_odt_one"
                NotiIcon=application-vnd.oasis.opendocument.text
            ;;
            docx )
                KNTitleMany="$msg_new_docx_many"
                KNTitle="$msg_new_docx_one"
                NotiIcon=application-vnd.openxmlformats-officedocument.wordprocessingml.document
                ;;
            ods )
                KNTitleMany="$msg_new_ods_many"
                KNTitle="$msg_new_ods_one"
                NotiIcon=application-vnd.oasis.opendocument.spreadsheet
                ;;
            xlsx )
                KNTitleMany="$msg_new_xlsx_many"
                KNTitle="$msg_new_xlsx_one"
                NotiIcon=application-x-applix-spreadsheet
                ;;
            odp )
                KNTitleMany="$msg_new_odp_many"
                KNTitle="$msg_new_odp_one"
                NotiIcon=application-vnd.oasis.opendocument.presentation
                ;;
            pptx )
                KNTitleMany="$msg_new_pptx_many"
                KNTitle="$msg_new_pptx_one"
                NotiIcon=application-vnd.oasis.opendocument.presentation
                ;;
            csv )
                KNTitleMany="$msg_new_csv_many"
                KNTitle="$msg_new_csv_one"
                NotiIcon=text-csv
                ;;
            extract_images )
                KNTitle="$msg_new_extracted_images"
                NotiIcon=image
                ;;
            unattach )
                KNTitle="$msg_new_unattach"
                NotiIcon=archive-extract
                ;;
            print )
                KNTitle="$msg_new_print"
                NotiIcon=document-print
                ;;
            rotate_*)
                case "${1##*_}" in
                    90 )
                        KNTitleMany="$msg_noti_rotate_90_many"
                        KNTitle="$msg_noti_rotate_90_one"
                        NotiIcon=object-rotate-right
                        ;;
                    180 )
                        KNTitleMany="$msg_noti_rotate_180_many"
                        KNTitle="$msg_noti_rotate_180_one"
                        NotiIcon=reverse
                        ;;
                    270 )
                        KNTitleMany="$msg_noti_rotate_270_many"
                        KNTitle="$msg_noti_rotate_270_one"
                        NotiIcon=object-rotate-left
                        ;;
                    * )
                        KNTitleMany=$(printf "$msg_noti_rotate_angle_many" "${1##*_}")
                        KNTitle=$(printf "$msg_noti_rotate_angle_one" "${1##*_}")
                        NotiIcon=object-rotate-right
                esac
                ;;
            mirror_* )
                case "${1##*_}" in
                    horizontal )
                        KNTitleMany="$msg_noti_mirror_horizontal_many"
                        KNTitle="$msg_noti_mirror_horizontal_one"
                        NotiIcon=arrow-right-double
                        ;;
                    vertical )
                        KNTitleMany="$msg_noti_mirror_vertical_many"
                        KNTitle="$msg_noti_mirror_vertical_one"
                        NotiIcon=arrow-up-double
                        ;;
                esac
                ;;
            image )
                KNTitleMany="$msg_new_Images_many" 
                KNTitle="$msg_new_Images_one"
                NotiIcon=image
                ;;
            jpg|png|gif|tiff )
                KNTitleMany=$(printf "$msg_new_image_many" "${1^^}")
                KNTitle=$(printf "$msg_new_image_one" "${1^^}")
                NotiIcon=image-$1
                ;;
            txt )
                KNTitleMany="$msg_new_txt_many"
                KNTitle="$msg_new_txt_one"
                NotiIcon=text-plain
                ;;
            * )
                KNTitleMany=$(printf "$msg_new_file_many" "${1^^}")
                KNTitle=$(printf "$msg_new_file_one" "${1^^}")
                NotiIcon=unknown
        esac
        
        [ -z "$KNTitleMany" ] && KNTitleMany="$KNTitle"
        [ $NL -gt 1 ] && KNTitle="$KNTitleMany"
        
        if [ -x "$houston_dir/notifier.py" ];then
            "$houston_dir/notifier.py" --icon "$NotiIcon" --title "$KNTitle" --text "$NotiFiles"
        else
            kdialog --icon "$NotiIcon" --title "$KNTitle" --passivepopup "$NotiFiles" 3 2>/dev/null
        fi
    fi
    
    if [ -n "$ErrorNotiFiles" ];then
        kdial "$msg_notification_error_title" --detailederror "$msg_notification_error"$'\n'"$ErrorNotiFiles" "$FullErrorDetails"
    fi
  
}

fast_main(){
    Winid="$WINDOWID"
    
    load_language_commons en
    load_language_commons $lang
    load_language en
    load_language $lang
    
    echo ""
    get_konsole_title_and_first_echo "$action" "$action_option"
    echo "$AllFilesInLines"
#     qdbus org.kde.konsole $KONSOLE_DBUS_SESSION setTitle 1 "$konsole_title" &>/dev/null
    
    $action $action_option "$@"
}
    
    
main(){
    
    #to lanch konsole
    InKonsole=false
    case "$1" in
        //konsole )
            InKonsole=true
            shift
    esac
    
    #language choose
    case "$1" in
        -la)
            shift
            lang="$1"
            shift
            ;;
        *)
            lang="${LANG%_*}"
            [ -z "$lang" ] && lang=en
    esac

    #get action
    action="$1"
    shift
    
    #launch script in konsole if script isn't launch from konsole
    if ! $InKonsole && [ -z "$KONSOLE_DBUS_SESSION" ] && [[ " $InKonsoleFunctions " =~ " $action " ]];then
        "$houston_dir/ks_bug_workaround.py" --hide-tabbar --hide-menubar -p BlinkingCursorEnabled=true -e \
                                        "$0" //konsole -la "$lang" "$action" "$@" 2>/dev/null
        
#         konsole --hide-tabbar --hide-menubar -p BlinkingCursorEnabled=true -e \
#                 "$0" //konsole -la "$lang" "$action" "$@" 2>/dev/null
        exit 0
    fi
    
    #get action option if needed
    if [[ " $NeedFirstArgFunctions " =~ " $action " ]];then
        action_option="$1"
        shift
    #some actions are in fact subactions of normal_pdftk (DoAllWithPDF)
    elif [[ " ${AreSubActionsFunctions#* } " =~ " $action " ]];then
        action_option="$action"
        action="${AreSubActionsFunctions%% *}"
    fi
    
    #######################################
    # Now all arguments should be files ! #
    #######################################
    
    LotOfFiles_in_a_new_dir=false
    
    Onlyonefile=false
    [ $# = 1 ] && Onlyonefile=true

    AlotOfFiles=false
    [ $# -ge 3 ] && AlotOfFiles=true
    HowManyFiles=$#

    $InKonsole && Winid="$WINDOWID" || Winid=""
    
    load_language_commons en
    load_language_commons $lang
    load_language en
    load_language $lang
    
    echo ""
    get_konsole_title_and_first_echo "$action" "$action_option"
    
    $InKonsole && qdbus org.kde.konsole $KONSOLE_DBUS_SESSION setTitle 1 "$konsole_title" &>/dev/null

    Ct=1
    until [ $# = 0 ];do
        #if script is launch from terminal, get fullpath of files
        FileArg[$Ct]=$(readlink -e "$1")
    
        ManyInputDirs=false
        [ -z "$InputDir" ] && InputDir="${FileArg[$Ct]%/*}"
        [[ "${FileArg[$Ct]%/*}" == "$InputDir" ]] || ManyInputDirs=true

        if $ManyInputDirs;then
            [ -z "$CommonDir" ] && CommonDir="${FileArg[$Ct]%/*}"
            
            until [[ "${FileArg[$Ct]}" =~ ^"$CommonDir/" ]];do
                CommonDir="${CommonDir%/*}"
            done
        fi

        ((Ct++))
        shift
    done

    #get all files one many lines for the first echo
    AllFilesInLines=$(tabstolines "${FileArg[@]}"|sed "s/^$(meta_zap_in "$HOME")\//~\//"|sed 's/^/\t/')
    echo "$AllFilesInLines"
    echo ""

    if [[ ! " $NoOutFileFunctions " =~ " $action " ]];then
        #Mute fonction, choose output directory ( if you want to echo something: echo whattoecho >/dev/stderr )
        outputDirIt(){
            outputDir=""
            
            until [ -w "$outputDir" ];do
                outputDir=$(kdial "$msg_choose_folder" --getexistingdirectory "$1") || return 1
                if [ ! -w "$outputDir" ];then
                    kdial "$msg_outFile_unwritable_dir_title" --error \
                          "$(printf "$msg_outFile_unwritable_dir" "$outputDir")"
                fi
            done
            
            echo "$outputDir"
        }
            
        if $ManyInputDirs;then 
            outputDir=$(outputDirIt "$CommonDir") || exit 0
        else
            outputDir=$(dirname "${FileArg[1]}")
            if [ ! -w "$outputDir" ];then
                outputDir=$(outputDirIt "$HOME") || exit 0
            fi
        fi
    fi
    
    $action $action_option "${FileArg[@]}"
}


