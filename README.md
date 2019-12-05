# Redis Garbage Collector

[![license: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

>A garbage collector for flow cache in redis.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Background

Flows Redis cache uses Redis sets to implement tags. These sets are by design persistent. To reduce memory usage references to expired keys need to be removed.

## Install

Using script locally
```bash
git clone https://github.com/t3n/redis-garbage-collector.git
cd redis-garbage-collector
pip install -r requirements.txt
```

Using docker
```bash
docker pull quay.io/t3n/redis-garbage-collector:0.2.0
```

## Usage

Using script locally
```bash
./rgc.py Cache --dry-run
./rgc.py Cache
```

Using docker
```bash
docker run --network="host" quay.io/t3n/redis-garbage-collector:0.2.0 Cache
docker run --network="host" quay.io/t3n/redis-garbage-collector:0.2.0 Cache --dry-run
```

## Contributing

PRs accepted.

Small note: If editing the Readme, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

[MIT](LICENSE)
