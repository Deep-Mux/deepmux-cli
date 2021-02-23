import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepmux-cli",
    version="0.0.15",
    author="DeepMux",
    author_email="dev@deepmux.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Deep-Mux/deepmux-cli",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyyaml',
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points={
        'console_scripts': ['deepmux=deepmux.__main__:main'],
    },
)
