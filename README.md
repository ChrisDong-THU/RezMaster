<p align="center">
  <img width="18%" align="center" src="./assets/logo.png" alt="logo">
</p>
  <h1 align="center">
  RezMaster
  </h1>
<p align="center">
  An awesome UI for visual model deployment based on PyQt5
</p>

<div align="center">

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/ChrisDong-THU/RezMaster?include_prereleases)
![GitHub last commit](https://img.shields.io/github/last-commit/ChrisDong-THU/RezMaster)
![GitHub issues](https://img.shields.io/github/issues-raw/ChrisDong-THU/RezMaster)
![GitHub](https://img.shields.io/github/license/ChrisDong-THU/RezMaster)

</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#quickstart">Quickstart</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

# Installation
1. Create a conda environment.
   ```shell
   conda create -n qt python=3.9.13
   ```
2. Install the dependent packages.
   ```shell
   pip install -r requirements.txt
   pip install -r requirements-extra.txt
   ```
3. Download the model file and unzip it to the model folder.

> **Note**: Please first modify `requirements-extra.txt` for appropriate Pytorch version according to the CUDA. For further development, it is necessary to install some additional packages, such as `PyQt5-tools`. 

# Quickstart
1. Simply run the script.
   ```shell
   python main.py
   ```
2. Follow the on-screen instructions to operate.
   
   ![Banner](./assets/usage.png)

# Roadmap

- [x] Release the main-feature available version v1.0.0

# License
RezMaster is released under [GPLv3](./LICENSE) license.

# Acknowledgments
- [PyQt-Fluent-Widgets](https://qfluentwidgets.com/)
- [PyQtImageViewer](https://github.com/marcel-goldschen-ohm/PyQtImageViewer)
