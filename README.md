# Technologies for Information Systems - Ethics Analysis

## Introduction

This is an integrative project for the course *[Technologies for Information Systems](https://www11.ceda.polimi.it/schedaincarico/schedaincarico/controller/scheda_pubblica/SchedaPublic.do?&evn_default=evento&c_classe=787593&polij_device_category=DESKTOP&__pj0=0&__pj1=c549e1e5e76cd55fb4f6b5591c1170fe)* at Politecnico di Milano. 
The development of this project has been supervised by **Chiara Criscuolo** ([@chiaracriscuolo](https://github.com/chiaracriscuolo)), **Tommaso Dolci** ([@TommasoD](https://github.com/TommasoD)) and **Mattia Salnitri** ([@MattiaSalnitri](https://github.com/MattiaSalnitri)).

The objective of this project is to create a user-friendly notebook for health researchers who may lack expertise in computer science or data science.
The notebook is designed to analyze the ethical and biased aspects of a given dataset, with an emphasis on fairness.

To achieve this goal, we have combined three distinct notebooks that were originally created by **Daniel Caputo** ([@DanielCaputo111296](https://github.com/DanielCaputo111296)) for analyzing a diabetes dataset.
This work is based on the paper **Criscuolo, C., Dolci, T., Salnitri, M. (2022). Towards Assessing Data Bias in Clinical Trials. In: , et al. Heterogeneous Data Management, Polystores, and Analytics for Healthcare**, which is available [here](https://doi.org/10.1007/978-3-031-23905-2_5).

The final notebook has been designed to be adaptable to various datasets.
Users can adjust input parameters (such as column names, protected variables, sensitive attributes, target variables, etc.) before running the notebook.
This flexibility allows researchers to use the notebook with different datasets and apply the techniques to evaluate fairness in various scenarios.

## 📦 Installation

### [Google Colab](https://colab.research.google.com)

In order to execute the notebook on Google Colab you need to:

1. Download this project and upload the whole folder to your google drive
2. Enter the project and open the notebook using google colab
3. Configure the setup cell to install the requirements and set the `path_to_project` variable (**\*check the **💡 TIP**\***)
4. Enjoy!

The requirements are defined in the `requirements.colab.txt` file, the notebook will install them automatically in the google setup cell. Make sure to set the `path_to_project` and update the pip installation command based on your google drive folder structure.

**💡 TIP**: Use the file explorer on the left of google colab to navigate to the project folder and copy the path.

### [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

```bash
conda create -n <name> python=3.9.6
conda activate <name>
pip install -r requirements.txt
```

If you are running the project on an **_Apple Silicon_** chip you can use the `requirements.osx-arm64.txt` file:

- Make sure that the `conda-forge` channel is added:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```

- Create the environment

```bash
conda create -n <name> python=3.9.6
conda activate <name>
conda install --file requirements.osx-arm64.txt
```

### [pip](https://pypi.org/project/pip/)

You can just install the requirements by running:

```bash
pip install -r requirements.txt
```

#### List of requirements

In order to create the list of requirements you can run:

```bash
pip list --format=freeze > requirements.txt
```

or if you are using conda and an **_Apple Silicon_** chip:

```bash
conda list -e > requirements.osx-arm64.txt
```

## 🧐 What is this notebook about?

The [notebook](ethics_analysis.ipynb) uses various techniques and technologies, such as [AIF360](https://github.com/Trusted-AI/AIF360), [fairlearn](https://github.com/fairlearn/fairlearn), [RankingFacts](https://github.com/DataResponsibly/RankingFacts), and [scikit-learn](https://github.com/scikit-learn/scikit-learn), to preprocess and analyze the data, and to train and evaluate machine learning models. The notebook also includes visualizations and statistics to help understand the distribution and correlations of the data, and to identify any potential biases.

This notebook has been created starting from these three notebooks:

- [Diabetes FairLearn](original_versions/Diabetes_FairLearn.ipynb)
- [Diabetes AIF360](original_versions/Diabetes_AIF360.ipynb)
- [Diabetes RankingFacts](original_versions/Diabetes_RankingFacts.ipynb)

## ⚙️ Data configuration

**PLEASE NOTE**: The notebook must be configured with a dataset and some configuration variables, in the `Configure the notebook` section. Regarding the attribute selection and weighting, the notebook automatically computes the weights based on the 3 selected attributes with the hightest correlation to the target variable.
It is possible to insert manually the selected attribute and the corresponding weight in the `Configure the notebook` section.

The **_protected attributes_** must be categorical and binary (0,1), but the original column must be mantained as a continuous variable.

## 📂 Folder structure

```
tis-project-diabetes-analysis
├── data
|   └── Diabetes_dataset.csv     // Pre-processed dataset
├── old_notebooks
│   ├── Diabetes_FairLearn.ipynb
│   ├── Diabetes_AIF360.ipynb
│   └── Diabetes_RankingFacts.ipynb
├── RankingFacts                 // RankingFacts library
│   ├── FAIR
│   └── ...
├── utils
│   ├── data_preprocessing.py    // Data preprocessing functions
│   ├── print_util.py            // Print and visualization functions
│   └── util.py                  // Utility logic functions
├── ethics_analysis_diabetes_example.ipynb
├── ethics_analysis.ipynb
├── README.md
├── requirements.colab.txt
├── requirements.osx-arm64.txt
└── requirements.txt
```

## 📚 Resources

- [RankingFacts](https://github.com/DataResponsibly/RankingFacts)
- [AIF360](https://github.com/Trusted-AI/AIF360)
- [fairlearn](https://github.com/fairlearn/fairlearn)
- [scikit-learn](https://github.com/scikit-learn/scikit-learn)

## 👨🏼‍💻 Group Members
- **Andrea Prisciantelli** ([@priscia99](https://github.com/priscia99))
- **Mattia Redaelli** ([@redaellimattia](https://github.com/redaellimattia))
