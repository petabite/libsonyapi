import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libsonyapi",
    version="1.0",
    description="Python binding for Sony Camera API",
    author="Philip Zhang",
    author_email="jmslca123@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/petabite/libsonyapi",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    install_requires=["requests"],
)
