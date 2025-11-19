# Password Generator CLI

A robust, secure, and easy-to-use Command Line Interface (CLI) tool for generating strong passwords. Built with Python, it leverages cryptographic strength randomness to ensure your passwords are safe.

## Features

- **Secure Generation**: Uses Python's `secrets` module for cryptographically strong random numbers.
- **Customizable**: Control password length and character composition (symbols, numbers, uppercase).
- **Cross-Platform**: Works on Windows, macOS, and Linux.
- **User Friendly**: Simple command-line arguments and colored output.

## Prerequisites

- Python 3.6 or higher.

## Installation

1.  **Clone the repository** (if applicable) or navigate to the project directory:
    ```bash
    cd password-generator
    ```

2.  **Install dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script directly using Python:

```bash
python cli.py [OPTIONS]
```

### Options

- `-l, --length INTEGER`: Length of the password (default: 16).
- `--no-symbols`: Exclude symbols from the password.
- `--no-numbers`: Exclude numbers from the password.
- `--no-uppercase`: Exclude uppercase letters from the password.
- `--help`: Show this message and exit.

### Examples

**Generate a default secure password (16 chars, all types):**
```bash
python cli.py
```

**Generate a 20-character password:**
```bash
python cli.py -l 20
```

**Generate a password without symbols:**
```bash
python cli.py --no-symbols
```

**Generate a simple alphanumeric password (no symbols, no uppercase - wait, usually you want uppercase, but just as an example):**
```bash
python cli.py --no-symbols --no-uppercase
```
*(Note: Removing too many character sets reduces security. Use with caution.)*

## Security

This tool uses the `secrets` module, which is designed for security-critical applications. Unlike the standard `random` module, `secrets` handles the secure generation of random numbers, making it suitable for passwords, account authentication, security tokens, and related secrets.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT](https://choosealicense.com/licenses/mit/)
