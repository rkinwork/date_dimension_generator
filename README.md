# Date Dim generator

Python script to generate date dimension and insert to Postgres.

To populate holidays we use [github.com/xmlcalendar/data](https://github.com/xmlcalendar/data)

### Prerequisites

This script has been developed using  `python == 3.8`

Have installed:
* [git](https://git-scm.com/)
* [pyenv](https://github.com/pyenv/pyenv)
* [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)

### Installing

Prepare execution environment
```bash
git clone 
pyenv install 3.8.2
cd date_dimension_generator
pyenv virtualenv 3.8.2 date_dimension_generator
pyenv activate date_dimension_generator
```

Install dependencies

```bash
pip3 install -r requirements.txt
``` 

