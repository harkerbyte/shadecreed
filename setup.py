from setuptools import setup, find_packages

setup(
    name="shadecreed",
    version="0.13.6",
    description="A CLI framework for web application assessments and penetration testing — built with modularity, continuous maintenance, and frequent updates in mind.",
    author="Shade",
    author_email="adesolasherifdeen3@gmail.com",
    packages=find_packages(),
    install_requires=[
        'httpx',
        'html5lib',
        'jinja2',
        'selenium==4.9.1',
        'beautifulsoup4',
    ],
    entry_points={
        "console_scripts": [
            "shadecreed=shadecreed.__main__:start",
            "shadecreed-scan=shadecreed.core.utils.build:runAnalyzeHeaders",
            "shadecreed-xss=shadecreed.core.utils.build:runBuildXss",
            "shadecreed-inject=shadecreed.core.headers.argue:runHeaderEditor",
            "shadecreed-brute=shadecreed.core.utils.assemble:runStartAssembling",
            "shadecreed-test=shadecreed.__test__:send_json",
        ]
    },
    include_package_data=True,
    python_requires='>=3.11',
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "GitHub": "https://github.com/harkerbyte",
        "Facebook": "https://facebook.com/harkerbyte",
        "Whatsapp" : "https://whatsapp.com/channel/0029Vb5f98Z90x2p6S1rhT0S",
        "Youtube" : "https://youtube.com/@harkerbyte",
        "Instagram": "https://instagram.com/harkerbyte"
    },
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)