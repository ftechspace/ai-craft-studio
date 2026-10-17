@echo off
rem FilmCraft (fast release build) with the control channel open, so the film-editor agent can drive it.
start "" "%~dp0apps\filmcraft\target\release\filmcraft.exe" --control 9876
