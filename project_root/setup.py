from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='root_relative',
    version='0.28',
    packages=['root_relative'],
    url='',
    license='MIT',
    author='liubomyr.ivanitskyi',
    author_email='',
    description='Module that allow to launch python module without requirements to start from working dir',
    long_description=readme(),
    long_description_content_type="text/markdown"
)
