CHCP 65001
@echo off
cd /d C:\OtherFiles\hugo
set /p torg=制作tama.host版本(T)或制作github版本(G)：
if "%torg%"=="T" copy C:\OtherFiles\hugo\config.tamahost.toml C:\OtherFiles\hugo\config.toml
if "%torg%"=="G" copy C:\OtherFiles\hugo\config.github.toml C:\OtherFiles\hugo\config.toml
C:\OtherFiles\hugo\hugo.exe -D
set /p hub=是否导入Github文件夹:(Y/N)
if "%hub%"=="Y" xcopy C:\OtherFiles\hugo\public\*.* C:\OtherFiles\Github\navi /y /e
if "%in%"=="N" echo "结束"
del C:\OtherFiles\hugo\config.toml
pause