# 참고자료
# http://swdeveloper.tistory.com/34
# https://code.tutsplus.com/ko/tutorials/how-to-share-your-python-packages--cms-26114
# https://code.tutsplus.com/ko/tutorials/how-to-write-your-own-python-packages--cms-26076
from setuptools import setup, find_packages

setup(
    name = "petrone_v2",
    version = "0.1.53",
    description = "Library for BYROBOT PETRONE V2",
    author = "BYROBOT",
    author_email = "dev@byrobot.co.kr",
    url = "http://www.byrobot.co.kr",
    packages = find_packages(exclude=['tests']),
    install_requires = ['pyserial', 'numpy'],
    long_description = open('README.md').read(),
)
