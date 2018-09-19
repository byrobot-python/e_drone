# 참고자료
# http://swdeveloper.tistory.com/34
# https://code.tutsplus.com/ko/tutorials/how-to-share-your-python-packages--cms-26114
# https://code.tutsplus.com/ko/tutorials/how-to-write-your-own-python-packages--cms-26076
from setuptools import setup, find_packages

setup(
    name = "e_drone",
    version = "0.1.7",
    description = "Library for E-DRONE",
    author = "BYROBOT",
    author_email = "dev@byrobot.co.kr",
    url = "http://www.byrobot.co.kr",
    packages = find_packages(exclude=['tests']),
    install_requires = ['pyserial', 'numpy', 'colorama'],
    long_description = open('README.md').read(),
)
