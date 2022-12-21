# Computationally-feasible uncertainty quantification in model-based landslide risk assessment

Anil Yildiz, Hu Zhao, Julia Kowalski

----

![code style: oitnb](https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw)

Python package used in the publication *Computationally-feasible uncertainty quantification in model-based landslide risk assessment* submitted to Frontiers in Earth Science: Geohazards and Georisks as part of the research topic *Physics and Modelling of Landslides*.

## Installation

We strongly recommend to work on an isolated virtual environment, and we suggest to use a [Conda](https://docs.conda.io/en/latest/) environment.

1. Clone the repository hosted on Github https://github.com/yildizanil/frontiers_yildizetal
2. If you have not already installed, download your preferred installation of Conda. You can try [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)
3. Create a virtual environment with the dependencies given in the ```environment.yml``` file.
```bash
$ conda env create --file environment.yml
```
4. Once the installation is complete, activate the environment
```bash
$ conda activate yildizetal2022
```
5. Install [Poetry](https://python-poetry.org/docs/basic-usage/) using the [official installer](https://python-poetry.org/docs/#installing-with-the-official-installer)

6. Install the package using the following command:

```bash
$ poetry install
```

## Usage

- TODO

## License

`frontiers_yildizetal` was created by Anil Yildiz. It is licensed under the terms of the GNU General Public License v3.0 license.

## Credits

`frontiers_yildizetal` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
