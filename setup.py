from setuptools import setup

setup(name='regex_enumerate',
      version='0.0.1a0',
      description='Enumerate Regular Expressions',
      url='http://github.com/leegao/RegexEnumerator',
      author='Lee Gao',
      author_email='lg342@cornell.edu',
      license='MIT',
      packages=['regex_enumerate'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
      ],
      keywords='regular expression combinatorics',
      install_requires=[
          'scipy',
          'sympy',
          'numpy',
          'pyoeis'
      ],
      include_package_data=True,
      zip_safe=False)