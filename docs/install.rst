#################
Installation
#################

*distinctipy* is tetsted on Python 3.7 - 3.10 (on Linux, Windows and Mac) and can be installed from PyPI using pip::

    pip install distinctipy

Alternatively, to install it from source::

    git clone https://github.com/alan-turing-institute/distinctipy.git
    cd distinctipy
    pip install .

=======================
Optional Dependencies
=======================

Starting in version 1.2.1 `distinctipy` no longer bundles `matplotlib` or `pandas` in the default installation,
to keep its footprint as small as possible. If you wish to view colours (e.g. with`distinctipy.color_swatch`)
or examples you will need `matplotlib` and `pandas` installed. To do this, either install `distinctipy` with the
optional flag::
    
    pip install 'distinctipy[optional]'

Or install them separately::

    pip install matplotlib pandas
