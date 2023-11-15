import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="Game-World-Navigator",
    version="0.0.2",
    author="NanJunLYS",
    author_email="18906571516@163.com",
    description="A framework for game automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JunNanLYS/GameWorldNavigator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
