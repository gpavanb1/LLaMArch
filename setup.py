from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="LLaMArch",
    version="0.0.1",
    description="Building Block Architectures for GenAI",
    url="https://github.com/gpavanb1/llamarch-docs",
    author="gpavanb1",
    author_email="gpavanb@gmail.com",
    license="CC BY-NC 4.0 for non-commercial use, commercial license available",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["langchain"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="genai architecture ai patterns machine-learning llm langchain",
    project_urls={  # Optional
        "Bug Reports": "https://github.com/gpavanb1/llamarch-docs/issues",
        "Source": "https://github.com/gpavanb1/llamarch-docs/",
    },
    zip_safe=False
)
