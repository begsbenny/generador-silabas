"""Punto de entrada: `python -m silabas` o el comando `silabas`."""

from silabas import config
from silabas.gui import SilabasApp


def main():
    config.aplicar_tema()   # Debe ejecutarse antes de crear la ventana
    app = SilabasApp()
    app.mainloop()


if __name__ == "__main__":
    main()
