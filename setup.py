from setuptools import setup

with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="llm_osint",
    version="0.0.0",
    description="",
    url="https://github.com/sshh12/llm_osint",
    author="Shrivu Shankar",
    license="MIT",
    packages=["llm_osint"],
    include_package_data=True,
    install_requires=required,
)
