@echo off
:: 接受用户输入
set /p target_module=traget excutable : 
set /p target_offset=traget offset : 
set /p sample=pins sample: 

:: 输出用户输入的内容
echo target_module, %target_module%!
echo target_offset, %target_offset%!
echo sample, %sample%!


D:\HackTools\Fuzz\__FuzzWork\dynamorio\build_x64\bin64\drrun.exe ^
-c D:\HackTools\Fuzz\__FuzzWork\winafl\build_x64\bin\Release\winafl.dll -debug ^
-target_module %target_module% ^
-target_offset %target_offset% ^
-fuzz_iterations 10 -nargs 2 -- ^
%target_module% %sample%