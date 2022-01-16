# 참고자료
# http://swdeveloper.tistory.com/34
# https://code.tutsplus.com/ko/tutorials/how-to-share-your-python-packages--cms-26114
# https://code.tutsplus.com/ko/tutorials/how-to-write-your-own-python-packages--cms-26076

from setuptools import setup, find_packages

setup(
    name = "e_drone",
    version = "22.2.1",     # year. month. release number
    description = "Library for BYROBOT Drones.",
    author = "BYROBOT",
    author_email = "dev@byrobot.co.kr",
    url = "http://www.byrobot.co.kr",
    packages = find_packages(exclude=['tests']),
    install_requires = [
        'pyserial>=3.4',
        'colorama>=0.4.0'],
    long_description = open('README.md').read(),
    long_description_content_type='text/markdown',
)
