from setuptools import setup

setup(author='Matthew Egan',
      author_email='matthewj.egan@hotmail.com',
      description='A cli tool used for checking the existance of different types of web resources',
      name='wtfuzz',
      py_modules=[
          'wtfuzz.wtfuzz',
      ],
      entry_points={
            'console_scripts': [
                  'wtfuzz = wtfuzz.wtfuzz:main'
            ]
      },
      install_requires=[
            'crayons==0.1.2',
            'requests==2.13.0',
      ],
      url='https://github.com/mattjegan/wtfuzz',
      version='0.0.10'
)
