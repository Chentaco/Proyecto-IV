from setuptools import setup

setup(name='MOBAgestor',
      version='0.01',
      description='Gestiona tus equipos y tus partidas para tus MOBAS favoritos',
      url='https://github.com/Chentaco/Proyecto-IV',
      author='Ramon Sanchez Garcia',
      author_email='chentaco@correo.ugr.es',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=['MOBAgestor'],
      install_requires=[
          'django'
      ],
      zip_safe=False)
