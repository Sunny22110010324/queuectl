
## Queuectl 🛠️

A command-line tool for managing background job queues.



![Python](https://img.shields.io/badge/python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Click](https://img.shields.io/badge/Click-000000?style=for-the-badge&logo=python&logoColor=white)



## About

`queuectl` is a command-line interface (CLI) tool designed to simplify the management and monitoring of background job queues. It provides a centralized interface for interacting with various queue systems, such as Redis Queue (RQ), Celery, and others. The tool aims to solve the problem of managing multiple queue systems with different interfaces, offering a unified approach for developers and system administrators.

The primary target audience includes developers, DevOps engineers, and system administrators who work with background job queues in their applications. It is particularly useful for those who need to monitor queue status, enqueue jobs, manage workers, and perform other queue-related tasks efficiently.

The tool is built using Python and leverages the `Click` library for creating the command-line interface. The architecture involves modular components for interacting with different queue systems, allowing for easy extension and support for new queue types. The core idea is to abstract away the complexities of individual queue systems, providing a consistent and user-friendly experience.

## ✨ Features

- 🎯 **Queue Monitoring**: Real-time monitoring of queue status, including queue length, worker status, and job statistics.
- ⚡ **Job Management**: Enqueue new jobs, retry failed jobs, and cancel pending jobs.
- 🔒 **Authentication**: Secure access to queue systems with configurable authentication credentials.
- 🎨 **User-Friendly Interface**: Intuitive command-line interface with clear and concise output.
- 🛠️ **Extensible**: Modular architecture allows for easy addition of support for new queue systems.
- 📱 **Cross-Platform**: Works on Linux, macOS, and Windows.

## 🎬 Demo

While a live demo isn't currently available, here are some example screenshots showcasing the tool's interface: https://drive.google.com/file/d/1tk8AmRbuM1bAQAfpL0dqsAg3MhI7Znx6/view?usp=sharing



## 🚀 Quick Start

Install and run in 2 steps:

```bash
pip install queuectl
queuectl --help
```

## 📦 Installation

### Prerequisites
- Python 3.7+
- pip

### Installation Steps

```bash
pip install queuectl
```


## ⚙️ Configuration

`queuectl` can be configured using environment variables or command-line options.




## 📁 Project Structure

```
queuectl/
├── queuectl/
│   ├── __init__.py
│   ├── cli.py         # Main CLI entry point
│   ├── commands/      # Subcommands
│   │   ├── status.py
│   │   ├── enqueue.py
│   │   └── ...
│   ├── queue_backends/ # Queue system implementations
│   │   ├── redis_queue.py
│   │   └── ...
│   ├── config.py      # Configuration management
│   └── utils.py       # Utility functions
├── tests/             # Test suite
├── README.md          # Project documentation
├── LICENSE            # License file
└── setup.py           # Installation script
```



### Development Setup

```bash
git clone https://github.com/Sunny22110010324/queuectl.git
cd queuectl
pip install -e .[dev]  # Install in editable mode with development dependencies
```

### Code Style
- Follow PEP 8 conventions.
- Use `flake8` and `pylint` for linting.
- Add tests for new features.
- Update documentation as needed.



## Deployment

`queuectl` can be deployed as a command-line tool on any system with Python installed.

1.  Install the package using `pip`.
2.  Configure the necessary environment variables or command-line options.
3.  Use the tool as described in the [Usage](#usage) section.




## 🙏 Acknowledgments

- 📚 **Libraries used**:
  - [Click](https://github.com/pallets/click) - For creating the command-line interface.
  - [Redis](https://github.com/redis/redis-py) - For Redis queue support.
