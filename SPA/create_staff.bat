@echo off
REM Script tạo tài khoản nhân viên cho SPA Mai Trâm
REM Sử dụng: create_staff.bat email password [name]
REM Ví dụ: create_staff.bat huong@maitramspa.com huong123456 "Hương"

cd /d "%~dp0"

if "%1"=="" (
    echo.
    echo ============================================
    echo SCRIPT TẠO TÀI KHOẢN NHÂN VIÊN SPA MAI TRÂM
    echo ============================================
    echo.
    echo Cách sử dụng:
    echo   create_staff.bat email matkhau [ten]
    echo.
    echo Ví dụ:
    echo   create_staff.bat huong@maitramspa.com huong123456 "Hương"
    echo   create_staff.bat linh@maitramspa.com linh123456 "Linh"
    echo.
    goto end
)

set email=%1
set password=%2
set name=%3

if "%name%"=="" (
    for /f "tokens=1 delims=@" %%A in ("%email%") do set name=%%A
)

echo.
echo Đang tạo tài khoản...
echo   Email: %email%
echo   Mật khẩu: %password%
echo   Tên: %name%
echo.

python manage.py create_staff %email% %password% --role staff --name "%name%"

echo.
echo ✓ Hoàn thành!
echo.

:end
pause

