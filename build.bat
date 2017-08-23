@echo on

rem 이전 배포판 삭제
del /f /q .\dist\*.*

rem 삭제
"C:\Users\Sanghyo Lee\Anaconda3\Scripts\pip.exe" uninstall petrone_v2 -q

rem 빌드
"C:\Users\Sanghyo Lee\Anaconda3\python.exe" setup.py sdist

rem wheel 빌드
"C:\Users\Sanghyo Lee\Anaconda3\python.exe" setup.py bdist_wheel

rem PYPI 등록
"C:\Users\Sanghyo Lee\Anaconda3\Scripts\twine.exe" upload dist/*
rem "C:\Users\Sanghyo Lee\Anaconda3\Scripts\twine.exe" upload --repository-url https://test.pypi.org/legacy/ dist/*

rem 설치
"C:\Users\Sanghyo Lee\Anaconda3\Scripts\pip.exe" --no-cache-dir install petrone_v2

pause
