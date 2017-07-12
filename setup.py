from setuptools import setup

setup(
    name='deploy_message',
    version='0.0.1',
    packages=['deploy_message'],
    url='https://github.com/UIUCLibrary/sccm_deploy_message_generator',
    license='',
    install_requires=["PyYAML", "Jinja2"],
    author='University of Illinois at Urbana Champaign',
    author_email='hborcher@illinois.edu',
    description='Generates the message required for deployment',
    entry_points={
        "console_scripts": [
            "deploymessage =deploy_message.cli:main"
        ]
    }

)
