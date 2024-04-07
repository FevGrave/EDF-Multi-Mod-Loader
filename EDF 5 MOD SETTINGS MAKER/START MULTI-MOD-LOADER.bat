@echo off
setlocal enabledelayedexpansion
TITLE V 1.0.0-001 --- Earth Defense Force Multi-Mod-Loader --- by FevGrave --- %time% --- %cd%
::=================================================================
color 0A
MODE 150,60

set CFGLANG=EN
REM echo 1. EN, 2. CN, 3. KR, 4. JA
REM set /p CFGLANG="Enter the language to use (1-4 or EN/CN/KR/JA): "
REM if "%CFGLANG%"=="1" set CFGLANG=EN
REM if "%CFGLANG%"=="2" set CFGLANG=CN
REM if "%CFGLANG%"=="3" set CFGLANG=KR
REM if "%CFGLANG%"=="4" set CFGLANG=JA
REM python "ConfigBuilder.py"
REM python "ConfigTextBuilder.py" %CFGLANG%
REM python "ConfigWeaponTablesBuilder.py" %CFGLANG% "%cd%"
python "Config-Test-Builder.py"
REM python "WEAPON_data_names_only_print.py" "%cd%"
REM echo WEAPON_data_names_only_print file layout output_data_file.txt
REM python "WEAPON_text_names_only_print.py" "%cd%"
REM echo WEAPON_text_names_only_print file layout output_text_file.txt
pause