from setuptools import setup
setup(
  name = 'drv8830pico',
  packages = ['drv8830pico'],
  version = '1.0',
  license='MIT',
  description = 'Library for controlling the DRV8830 module from Raspberry Pico',
  author = 'Wojciech Musialkiewicz',
  author_email = 'wojtechnical@gmail.com',
  url = 'https://github.com/WojTechnical/drv8830pico',
  download_url = 'https://github.com/joelbarmettlerUZH/Scrapeasy/archive/pypi-0_1_3.tar.gz',
  keywords = ['pico', 'drv8830'],
  install_requires=[],
  classifiers=[  # Optional
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: MicroPython',
  ],
)