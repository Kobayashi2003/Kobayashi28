@echo off & setlocal enabledelayedexpansion
for /f "delims=" %%i in ('dir /s/b *.*') do (
	set "foo=%%~nxi"
	set foo=!foo: =_!
	ren "%%~fi" "!foo!")