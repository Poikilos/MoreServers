from setuptools import setup, find_packages

setup(
    name="moreservers",
    version="1.0.0",
    description="A plugin manager GUI for managing server plugins in Java jar files.",
    author="Jake Gustafson",
    author_email="7557867+poikilos@users.noreply.github.com",
    url="https://github.com/Poikilos/MoreServers",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'gui_scripts': [
            'moreservers-launch=moreservers.moreserverstk:main',
        ],
    },
    install_requires=[
        'setuptools',  # Ensure setuptools is available
        'tkinter',     # GUI framework (usually part of standard Python installations)
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications :: GTK",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Systems Administration",
    ],
    # python_requires='>=3.7',
)
