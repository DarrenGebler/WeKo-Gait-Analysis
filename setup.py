from setuptools import setup, find_packages
from os import path
from codecs import open

user_path = path.abspath(path.dirname(__file__))

with open(path.join(user_path, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]


setup(
    name='WeKo Gait Analysis',
    version='1.0.0',
    packages=find_packages(),
    install_requires=install_requires,
    dependency_links=dependency_links,
    include_package_data=True,
    url='weko.health/wekogait',
    license='MIT',
    author='Darren Gebler',
    author_email='darreng968@gmail.com',
    description='WeKo\'s Gait Analysis Project. Predicting the requirement for surgery based on video uploaded by user'
)
