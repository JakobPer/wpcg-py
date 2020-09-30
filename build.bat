@echo off
echo - cleaning up
python -m fbs clean
echo - building
python -m fbs freeze
echo - creating installer
python -m fbs installer
echo - done