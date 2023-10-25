# MUNICS SI Lab2

<div align="center">

***Information Security: Lab assignment II - Vector Commitment***

[![Python](https://img.shields.io/badge/Python-black?logo=python&logoColor=white&labelColor=grey&color=%233776AB)](<https://www.python.org/> "Python")
[![License: MIT](<https://img.shields.io/github/license/danielfeitopin/MUNICS-SI-Lab2>)](LICENSE "License")
[![GitHub issues](https://img.shields.io/github/issues/danielfeitopin/MUNICS-SI-Lab2)](<https://github.com/danielfeitopin/MUNICS-SI-Lab1> "Issues")
[![GitHub stars](https://img.shields.io/github/stars/danielfeitopin/MUNICS-SI-Lab2)](<https://github.com/danielfeitopin/MUNICS-SI-Lab1/stargazers> "Stars")

</div>

## Table of Contents

- [MUNICS SI Lab2](#munics-si-lab2)
  - [Table of Contents](#table-of-contents)
  - [Configuration](#configuration)
    - [Configure Files](#configure-files)
    - [Set up the virtual environment](#set-up-the-virtual-environment)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)


## Configuration

### Configure Files

Complete the [config.py](<src/commit/config.py>) file with the required configuration.

```py
# MQTT Conexion Configuration
MQTT_USER_NAME = # TODO
MQTT_PASSWORD = # TODO
MQTT_IP = # TODO
MQTT_PORT = # TODO
MQTT_KEEPALIVE = # TODO

ID_ALICE = # TODO MQTT topic for Alice
ID_BOB = # TODO MQTT topic for Bob
```

### Set up the virtual environment

A [Pipfile](<src/Pipfile>) is provided to create a virtual environment.

```sh
cd src
pipenv install
```

## Usage

Run the scripts [alice.py](<src/commit/alice.py>) and [bob.py](<src/commit/bob.py>) simultaneously:

```sh
cd commit
pipenv run alice.py
```

```sh
cd commit
pipenv run bob.py
```

Introduce the data required by [alice.py](<src/commit/alice.py>).

## Contributing

Contributions are welcome! If you have improvements, bug fixes, or new modules to add, feel free to submit a pull request.

## License

The content of this repository is licensed under the [MIT License](LICENSE).

## Contact

Feel free to get in touch with me!

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-%23181717?style=for-the-badge&logo=github&logoColor=%23181717&color=white)](<https://github.com/danielfeitopin>)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-white?style=for-the-badge&logo=linkedin&logoColor=white&color=%230A66C2)](<https://www.linkedin.com/in/danielfeitopin/>)

</div>