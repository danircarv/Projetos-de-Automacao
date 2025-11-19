import secrets
import string
import click
from colorama import Fore, Style, init

init(autoreset=True)

def generate_password(length, use_symbols, use_numbers, use_uppercase):
    """Generates a secure password based on the provided criteria."""
    alphabet = string.ascii_lowercase
    if use_uppercase:
        alphabet += string.ascii_uppercase
    if use_numbers:
        alphabet += string.digits
    if use_symbols:
        alphabet += string.punctuation

    if not alphabet:
        raise click.UsageError("At least one character type must be selected.")

    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (use_uppercase and not any(c.isupper() for c in password)) or \
           (use_numbers and not any(c.isdigit() for c in password)) or \
           (use_symbols and not any(c in string.punctuation for c in password)):
            continue
        return password

@click.command()
@click.option('-l', '--length', default=16, help='Length of the password (default: 16).')
@click.option('--no-symbols', is_flag=True, help='Exclude symbols from the password.')
@click.option('--no-numbers', is_flag=True, help='Exclude numbers from the password.')
@click.option('--no-uppercase', is_flag=True, help='Exclude uppercase letters from the password.')
def cli(length, no_symbols, no_numbers, no_uppercase):
    """
    A CLI tool to generate secure passwords.
    """
    try:
        password = generate_password(
            length=length,
            use_symbols=not no_symbols,
            use_numbers=not no_numbers,
            use_uppercase=not no_uppercase
        )
        click.echo(f"{Fore.GREEN}Generated Password: {Style.BRIGHT}{password}")
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")

if __name__ == '__main__':
    cli()
