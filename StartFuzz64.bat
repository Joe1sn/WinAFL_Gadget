@echo off
echo AFL Helping Tool Gadget
echo By Joe1sn

:: 接受用户输入
set /p target_module=traget excutable : 
set /p in_dir=Test Case Input Dir: 
set /p out_dir=Test Case Output Dir: 
set /p target_offset=traget offset :

:: 输出用户输入的内容
echo target_module, %target_module%!
echo Test Case Input Dir, %in_dir%!
echo Test Case Output Dir, %out_dir%!
echo target offset, %target_offset%!

cd "D:\HackTools\Fuzz\__FuzzWork\winafl\build_x64\bin\Release"
"D:\HackTools\Fuzz\__FuzzWork\winafl\build_x64\bin\Release\afl-fuzz.exe" ^
-i %in_dir% ^
-o %out_dir% ^
-D "D:\HackTools\Fuzz\__FuzzWork\dynamorio\build_x64\bin64" ^
-I 100000+ -t 20000 -- ^
-target_module %target_module% ^
-target_offset %target_offset% ^
-fuzz_iterations 5000 -nargs 2 -- ^
%target_module% @@