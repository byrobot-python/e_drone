@echo on

rem 이전 배포판 삭제
del /f /q .\dist\*.*

rem 빌드
"python.exe" setup.py sdist

rem wheel 빌드
"python.exe" setup.py bdist_wheel

rem PYPI 등록
"twine.exe" upload --skip-existing dist/*
rem "Scripts\twine.exe" upload --repository-url https://test.pypi.org/legacy/ dist/*

rem 설치
"pip.exe" install --upgrade e_drone

pause
