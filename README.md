# Computationally-feasible uncertainty quantification in model-based landslide risk assessment

Anil Yildiz $^{1, *}$, Hu Zhao $^1$, Julia Kowalski $^1$

$^1$ Methods for Model-based Development in Computational Engineering, RWTH Aachen University, Aachen, Germany
$^*$ Corresponding author: [yildiz@mbd.rwth-aachen.de](mailto:yildiz@mbd.rwth-aachen.de)

[![doi](https://img.shields.io/badge/doi-10.3389%2Ffeart.2022.1032438-success)](https://dx.doi.org/10.3389/feart.2022.1032438)

----

This repository presents the publication titled [Computationally-feasible uncertainty quantification in model-based landslide risk assessment](https://www.frontiersin.org/articles/10.3389/feart.2022.1032438) published in [Frontiers in Earth Science: Geohazards and Georisks](https://www.frontiersin.org/research-topics/26949/physics-and-modelling-of-landslides) in a Python package format. This package helps to reproduce the results, and perform further analyses.

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

6. Install the package using the following command

```bash
$ poetry install
```

## Usage

- TODO

## License

`frontiers_yildizetal` was created by [Anil Yildiz](https://www.anilyildiz.info). It is licensed under the terms of the GNU General Public License v3.0 license. The paper is published under a [CC BY 4.0 license](https://creativecommons.org/licenses/by/4.0/).

## Credits

`frontiers_yildizetal` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
