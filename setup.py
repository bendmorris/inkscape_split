from setuptools import setup

setup(
    name='inkscape_split',
    py_modules=['inkscape_split'],
    entry_points={
        'console_scripts': ['inkscape_split = inkscape_split:main', ],
    },
)
