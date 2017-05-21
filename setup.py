from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(name='dream',
      use_scm_version=True,
      setup_requires=['setuptools_scm'],
      description='An interactive art project using Google DeepDream for idea generation',
      long_description=readme,
      author='Chandler Watson',
      author_email='watson@facni.com',
      url='https://github.com/useanalias/dream',
      license=license,
      packages=find_packages(exclude=('tests', 'docs')),
      scripts=['bin/dream']
)
