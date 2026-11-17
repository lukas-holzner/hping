# 🌐 hping - Ping but for HTTP

<div align="center">

[![CI](https://github.com/lukas-holzner/hping/actions/workflows/ci.yml/badge.svg)](https://github.com/lukas-holzner/hping/actions/workflows/ci.yml)
[![Release](https://github.com/lukas-holzner/hping/actions/workflows/release.yml/badge.svg)](https://github.com/lukas-holzner/hping/actions/workflows/release.yml)
[![Python Version](https://img.shields.io/badge/python-3.11%20--%203.15-blue.svg)](https://python.org)
[![PyPI Version](https://img.shields.io/pypi/v/hping.svg)](https://pypi.org/project/hping/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![PyPI Downloads](https://img.shields.io/pypi/dm/hping.svg)](https://pypi.org/project/hping/)
[![GitHub Stars](https://img.shields.io/github/stars/lukas-holzner/hping.svg)](https://github.com/lukas-holzner/hping/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/lukas-holzner/hping.svg)](https://github.com/lukas-holzner/hping/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/lukas-holzner/hping.svg)](https://github.com/lukas-holzner/hping/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/lukas-holzner/hping.svg)](https://github.com/lukas-holzner/hping/pulls)

</div>

`hping` is a command-line tool that works like `ping`, but instead of sending ICMP packets, it repeatedly makes HTTP requests to check if a website or service is available.

## ✨ Key Features

- 🔄 **Continuous monitoring** - Send periodic HTTP requests like traditional ping
- 📊 **Real-time statistics** - View response times, success rates, and packet loss
- ⚡ **Lightweight & fast** - Minimal resource usage with quick response times and HTTP/2 support
- 🎯 **Simple interface** - Familiar ping-like command-line experience
- 🐍 **Python 3.11 – 3.15** - Modern Python with type hints and clean code

## 📦 Installation

### Requirements

- Python 3.11 or higher (tested up to Python 3.15)
- Internet connection

### Install from PyPI

```bash
pip install hping
```

### Install from Source

```bash
git clone https://github.com/lukas-holzner/hping.git
cd hping
poetry install
```

## 🚀 Usage

To use `hping`, simply run it from the command line followed by the URL you want to ping:

```bash
hping https://www.example.com
```

## ⚙️ Options

- `-i`, `--interval`: Interval in seconds between requests (default: `1.0`).
- `-c`, `--count`: Number of pings to send (default: unlimited).
- `-X`, `--method`: HTTP method to use (`GET`, `POST`, `PUT`, `DELETE`, `HEAD`, `PATCH`; default: `GET`).
- `--timeout`: Request timeout in seconds (default: `10.0`).
- `-H`, `--header`: Custom HTTP header in `'Name: Value'` format (can be specified multiple times).
- `-d`, `--data`: Request body data (auto-detects JSON format).
- `--no-follow-redirects`: Disable following HTTP redirects.
- `--max-redirects`: Maximum number of redirects to follow (default: `5`).
- `--http2`: Force HTTP/2 usage.

## 💡 Example

```bash
hping https://www.example.com -i 2 -c 5 --http2
```

This will send 5 HTTP/2 GET requests to `https://www.example.com` every 2 seconds.

## 📋 About

`hping` is a simple tool for monitoring the availability and responsiveness of websites by sending periodic HTTP GET requests.

## 🛠️ Development

For development setup with devcontainer support and pre-commit hooks, see `CONTRIBUTING.md`.

### Quick Development Setup

```bash
# Using devcontainer (recommended)
# Open in VS Code and select "Reopen in Container"

# Or manual setup
poetry install
pre-commit install
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

- Check out the [Contributing Guide](CONTRIBUTING.md) for development setup
- Browse [open issues](https://github.com/lukas-holzner/hping/issues) for ways to help
- Read about our [commit conventions](CONTRIBUTING.md#commit-message-guidelines)

## 📄 License

This project is licensed under the MIT License - see the [MIT License](https://opensource.org/licenses/MIT) for details.

## 🌟 Support

If you find this tool useful, please consider:

- ⭐ Starring the repository
- 🐛 [Reporting issues](https://github.com/lukas-holzner/hping/issues)
- 💡 [Suggesting enhancements](https://github.com/lukas-holzner/hping/issues)
- 📢 Sharing with others
