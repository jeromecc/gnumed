; Script generated by the HM NIS Edit Script Wizard.
VAR PYTHON_PATH
VAR POSTGRES_PATH
; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "GNUmed-server"
!define PRODUCT_VERSION "v6"
!define PRODUCT_SUBREV "0"
!define PRODUCT_PUBLISHER "Sebastian Hilbert"
!define PRODUCT_WEB_SITE "http://www.gnumed.org"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; postinst action
!define MUI_FINISHPAGE_RUN "$INSTDIR\bootstrap\bootstrap-latest.bat"
!define MUI_FINISHPAGE_RUN_TEXT $(RunExeDesc)

!include "gnumed_util_checkprerequisites_server.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME

; License page
!define MUI_LICENSEPAGE_CHECKBOX
!insertmacro MUI_PAGE_LICENSE $(MUILicense)

; Directory page
!insertmacro MUI_PAGE_DIRECTORY

; Instfiles page
!insertmacro MUI_PAGE_INSTFILES

; db bootstrap environment page
Page custom BootstrapMode EvaluateBootstrapMode

; db bootstrap environment page
;Page custom SilentBootstrap ValidateBootstrap

; Finish page
!insertmacro MUI_PAGE_FINISH

; Language files
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "German"

LicenseLangString MUILicense ${LANG_ENGLISH} "gnumed-head\GnuPublicLicense.txt"
LicenseLangString MUILicense ${LANG_GERMAN} "gnumed-head\GnuPublicLicense_de.txt"

LangString RunExeDesc ${LANG_ENGLISH} "bootstrap GNUmed database now"
LangString RunExeDesc ${LANG_GERMAN} "GNUmed Datenbank jetzt erzeugen"
LangString PGsuperusername ${LANG_ENGLISH} "Please enter database superuser name."
LangString PGsuperusername ${LANG_GERMAN} "Bitte den PostgreSQL-Hauptnutzernamen eingeben"
LangString PGsuperuserpasswd ${LANG_ENGLISH} "You entered no password for the database superuser "
LangString PGsuperuserpasswd ${LANG_GERMAN} "Sie haben kein Passwort f�r den PostgreSQL-Hauptnutzer eingeben"
LangString GMsuperusername ${LANG_ENGLISH} "Please enter GNUmed database username"
LangString GMsuperusername ${LANG_GERMAN} "Bitte den GNUmed-Hauptnutzernamen eingeben"
LangString GMsuperuserpasswd ${LANG_ENGLISH} "Please enter GNUmed superuser password."
LangString GMsuperuserpasswd ${LANG_GERMAN} "Bitte das GNUmed-Hauptnutzerpasswort eingeben"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}.${PRODUCT_VERSION}.${PRODUCT_SUBREV}.exe"
InstallDir "$PROGRAMFILES\GNUmed-server"
ShowInstDetails show

Function .onInit
  !insertmacro MUI_LANGDLL_DISPLAY
  
  ;Extract InstallOptions INI files
  InitPluginsDir
  File /oname=$TEMP\temp1.ini "bootstrap-noninteractive.ini"
  File /oname=$TEMP\temp2.ini "bootstrap-interactive.ini"
  File /oname=$TEMP\temp.ini "bootstrap-preferences.ini"
  Call CheckDependencies
  Call GetPythonPath
  Call GetPostgresPath
FunctionEnd
;---------------------
Function GetPythonPath

  ReadRegStr $R0 HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\Python.exe" ""
  StrCpy $PYTHON_PATH $R0 -11

FunctionEnd
;---------------------
Function GetPostgresPath

  StrCpy $0 0
  EnumRegKey $1 HKLM SOFTWARE\PostgreSQL\Installations 0
  ReadRegStr $2 HKLM "SOFTWARE\PostgreSQL\Installations\$1\" "Bin Directory"
  StrCpy $POSTGRES_PATH $2
  ;MessageBox MB_OK "$POSTGRES_PATH"

FunctionEnd
;---------------------
Function BootstrapMode
  
  ;Display bootstrap perefrences dialog
  InstallOptions::dialog "$TEMP\temp.ini"

FunctionEnd
;---------------------
Function EvaluateBootstrapMode

  ReadINIStr $R0 "$TEMP\temp.ini" "Field 3" "State" ; bootstrap mode
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-archive.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-amis.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "installation" interactive $R0
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "installation" interactive $R0

  ReadINIStr $R1 "$TEMP\temp.ini" "Field 5" "State" ; bootstrap host
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-archive.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-amis.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "server local host" name $R1
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "server local host" name $R1

  ReadINIStr $R2 "$TEMP\temp.ini" "Field 7" "State" ; postgres port
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-archive.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-amis.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "server local host" port $R2
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "server local host" port $R2

  ReadINIStr $R3 "$TEMP\temp.ini" "Field 9" "State" ; template database
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-archive.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-amis.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "server local host" "template database" $R3
  WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "server local host" "template database" $R3
  
  ReadINIStr $R4 "$TEMP\temp.ini" "Field 11" "State" ; gnumed database
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-archive.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-amis.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "server local host" "template database" $R4
  ;WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "server local host" "template database" $R4

FunctionEnd
;---------------------
Function SilentBootstrap

  ; show db bootstrap environment page -or not
  ReadINIStr $R0 "$TEMP\temp.ini" "Field 3" "State" ; bootstrap mode
  StrCmp $R0 "yes" 0 interactive
  ;MessageBox MB_ICONEXCLAMATION|MB_OK "chose install mode $R1"
        InstallOptions::dialog "$TEMP\temp2.ini"
  interactive:
        InstallOptions::dialog "$TEMP\temp1.ini"
FunctionEnd
;---------------------
Function ValidateBootstrap
  ;Validate prerequisites dialog
  ReadINIStr $R0 "$TEMP\temp1.ini" "Field 4" "State" ; database superuser
  StrCmp $R0 "" 0 writePgSUString
    MessageBox MB_ICONEXCLAMATION|MB_OK $(PGsuperusername)
    Abort
  writePgSUString:
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "user postgres" name $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "user postgres" name $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "user postgres" name $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "user postgres" name $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "user postgres" name $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "user postgres" name $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "user postgres" name $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "user postgres" name $R0
  ;-------------------
  ReadINIStr $R0 "$TEMP\temp1.ini" "Field 6" "State" ; database superuser password
  ;;StrCmp $R0 "" 0 ;writePgSUPasswdString
    ;;MessageBox MB_ICONEXCLAMATION|MB_OK $(PGsuperuserpasswd)
    ;;Abort
  ;;writePgSUPasswdString:
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "user postgres" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "user postgres" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "user postgres" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "user postgres" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "user postgres" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "user postgres" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "user postgres" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "user postgres" "password" $R0
  ;-------------------
  ReadINIStr $R0 "$TEMP\temp1.ini" "Field 8" "State" ; gnumed database user
  StrCmp $R0 "" 0 writeGMSUString
    MessageBox MB_ICONEXCLAMATION|MB_OK $(GMsuperusername)
    Abort
  writeGMSUString:
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "user GNUmed owner" "name" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "user GNUmed owner" "name" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "user GNUmed owner" "name" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "user GNUmed owner" "name" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "user GNUmed owner" "name" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "user GNUmed owner" "name" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "user GNUmed owner" "name" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "user GNUmed owner" "name" $R0
  ;-------------------
  ReadINIStr $R0 "$TEMP\temp1.ini" "Field 10" "State" ; gnumed database user password
  ;;StrCmp $R0 "" 0 writeGMSUPasswdString
    ;;MessageBox MB_ICONEXCLAMATION|MB_OK $(GMsuperuserpasswd)
    ;;Abort
  ;;writeGMSUPasswdString:
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_first.conf" "user GNUmed owner" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-monolithic_core.conf" "user GNUmed owner" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-de.conf" "user GNUmed owner" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-es.conf" "user GNUmed owner" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-ca.conf" "user GNUmed owner" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-au.conf" "user GNUmed owner" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-test_data.conf" "user GNUmed owner" "password" $R0
    WriteINIStr "$INSTDIR\bootstrap\bootstrap-local_last.conf" "user GNUmed owner" "password" $R0
FunctionEnd
;---------------------

LangString BootstrapLnkName ${LANG_ENGLISH} "bootstrap GNUmed database"
LangString BootstrapLnkName ${LANG_GERMAN} "GNUmed Datenbank erzeugen"
LangString LogfileLnkName ${LANG_ENGLISH} "view bootstrap logfile"
LangString LogfileLnkName ${LANG_GERMAN} "Protokoll der Datenbankerstellung"


Section -!$(Sec2Name) SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File /r gnumed-head\gnumed\server\*
  CreateDirectory "$SMPROGRAMS\GNUmed\server"
  SetOutPath "$INSTDIR\bootstrap"
  CreateShortCut "$SMPROGRAMS\GNUmed\server\$(BootstrapLnkName).lnk" "$INSTDIR\bootstrap\bootstrap-latest.bat"
  CreateShortCut "$SMPROGRAMS\GNUmed\server\$(LogfileLnkName).lnk" "$INSTDIR\bootstrap\bootstrap-latest.log"
  ;MessageBox MB_OK "$TEMP"
SectionEnd

;------------------------------
Section -!$(Sec2Name) SEC02
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon"
  SetOverwrite ifnewer
  File "gnumed-head\gnumed\client\pycommon\*.py"
  File "gnumed-head\gnumed\client\pycommon\__init__.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools"
  File "gnumed-head\gnumed\client\pycommon\tools\*.py"
  SetOutPath "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon"
  File "gnumed-head\gnumed\client\pycommon\__init__.py"
SectionEnd

Section -AdditionalIcons
  SetOutPath $INSTDIR
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateDirectory "$SMPROGRAMS\GNUmed\server"
  CreateShortCut "$SMPROGRAMS\GNUmed\server\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\GNUmed\server\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) wurde erfolgreich deinstalliert."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "M�chten Sie $(^Name) und alle seinen Komponenten deinstallieren?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools\*.pyc"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools\CVS\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\*.py"
  Delete "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\*.pyc"
  
  Delete "$SMPROGRAMS\GNUmed\server\$(BootstrapLnkName).lnk"
  Delete "$SMPROGRAMS\GNUmed\server\$(LogfileLnkName).lnk"

  RMDir "$SMPROGRAMS\GNUmed\server"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon\tools"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed\pycommon"
  RMDir "$PYTHON_PATH\Lib\site-packages\Gnumed"

  RMDir "$INSTDIR\locale\fr_FR\LC_MESSAGES"
  RMDir "$INSTDIR\locale\fr_FR"
  RMDir "$INSTDIR\locale\fr\LC_MESSAGES"
  RMDir "$INSTDIR\locale\fr"
  RMDir "$INSTDIR\locale\es_ES\LC_MESSAGES"
  RMDir "$INSTDIR\locale\es_ES"
  RMDir "$INSTDIR\locale\es\LC_MESSAGES"
  RMDir "$INSTDIR\locale\es"
  RMDir "$INSTDIR\locale\de_DE\LC_MESSAGES"
  RMDir "$INSTDIR\locale\de_DE"
  RMDir "$INSTDIR\locale\de\LC_MESSAGES"
  RMDir "$INSTDIR\locale\de"
  RMDir "$INSTDIR\locale"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd