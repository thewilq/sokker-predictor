from setuptools import setup, find_packages

setup(name='sokker-predictor',
      version='0.1',
      description='The best app in the world',
      url='http://github.com/thewilq/sokker-predictor/',
      author='thewilq',
      author_email='wilquu@gmail.com',
      zip_safe=True,
      packages=['sokker-predictor'],
      include_package_data = True,
      install_requires=[
          'backports.entry-points-selectable==1.1.0'
          , 'beautifulsoup4==4.9.3'
          , 'bs4==0.0.1'
          , 'certifi==2021.5.30'
          , 'charset-normalizer==2.0.4'
          , 'click==7.1.2'
          , 'colorama==0.4.4'
          , 'commonmark==0.9.1'
          , 'distlib==0.3.2'
          , 'filelock==3.0.12'
          , 'gitdb==4.0.7'
          , 'GitPython==3.1.18'
          , 'idna==3.2'
          , 'install==1.3.4'
          , 'joblib==1.0.1'
          , 'numpy==1.20.3'
          , 'opencv-python==4.5.2.52'
          , 'pandas==1.2.4'
          , 'Pillow==8.2.0'
          , 'platformdirs==2.2.0'
          , 'Pygments==2.9.0'
          , 'python-dateutil==2.8.1'
          , 'pytz==2021.1'
          , 'requests==2.26.0'
          , 'rich==10.2.2'
          , 'scikit-learn==0.24.2'
          , 'scipy==1.7.1'
          , 'selenium==3.141.0'
          , 'six==1.16.0'
          , 'sklearn==0.0'
          , 'smmap==4.0.0'
          , 'soupsieve==2.2.1'
          , 'threadpoolctl==2.2.0'
          , 'typer==0.3.2'
          , 'typing-extensions==3.10.0.0'
          , 'urllib3==1.26.5'
          , 'virtualenv==20.7.2'
          , 'openpyxl==3.0.7'
          , 'et_xmlfile==1.1.0']
      )
