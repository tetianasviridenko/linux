import os
import typer

app = typer.Typer()

def print_environment():
    for key, value in os.environ.items():
        print(f"{key}={value}")

def print_help():
    help_text = """
    Usage:
    -h, --help           Show this help message and exit.
    -i <variable>, --info <variable>  Show the value of the specified environment variable.
    -s <variable=value>, --set <variable=value>  Set the specified environment variable to the given value.
    -a <variable>, --assign <variable> -v <value>, --value <value>  Assign a value to the specified environment variable.
    -d <variable>, --del <variable>  Delete the specified environment variable.
    -с, --clear           Clear all environment variables.
    """
    print(help_text)

@app.command()
def main(
    h: bool = typer.Option(False, "-h", "--help", help="Show help"),
    i: str = typer.Option(None, "-i", "--info", help="Show value of the specified variable"),
    s: str = typer.Option(None, "-s", "--set", help="Set environment variable to a value"),
    a: str = typer.Option(None, "-a", "--assign", help="Assign a value to the environment variable"),
    v: str = typer.Option("", "-v", "--value", help="Value for the environment variable"),
    d: str = typer.Option(None, "-d", "--del", help="Delete the specified environment variable"),
    c: bool = typer.Option(False, "-c", "--clear", help="Clear all environment variables"),
):
    if h:
        print_help()
        return

    if i:
        value = os.getenv(i)
        if value:
            print(f"{i}={value}")
        else:
            print(f"{i} не знайдена в оточенні.")

    elif s:
        var, value = s.split("=")
        os.environ[var] = value
        print(f"{var}={value} встановлено.")

    elif a:
        if not v and a:
            os.environ[a] = ""
            print(f"{a} присвоєно порожній рядок.")
        elif a and v:
            os.environ[a] = v
            print(f"{a}={v} присвоєно.")
        else:
            print("Не вказано змінну або значення.")

    elif d:
        if d in os.environ:
            del os.environ[d]
            print(f"Змінну {d} видалено.")
        else:
            print(f"{d} не знайдена в оточенні.")

    elif c:
        os.environ.clear()
        print("Оточення очищено.")

    else:
        print_environment()

if __name__ == "__main__":
    app()

