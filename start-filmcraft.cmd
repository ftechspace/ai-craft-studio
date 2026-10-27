@echo off
rem FilmCraft (fast release build) with the control channel open, so the film-editor agent can drive it.
rem Its error output (panic messages, backtraces) goes to output\filmcraft-errors.log, so a crash leaves a reason.
if not exist "%~dp0output" mkdir "%~dp0output"
set RUST_BACKTRACE=1
start "" /b cmd /c ""%~dp0apps\filmcraft\target\release\filmcraft.exe" --control 9876 2>>"%~dp0output\filmcraft-errors.log""
