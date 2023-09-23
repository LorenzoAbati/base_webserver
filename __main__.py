from service.ServiceApp import ServiceApp
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s.%(msecs)03d|%(levelname)-8s|%(filename)s:%(lineno)d|%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def main():
    app = ServiceApp()


if __name__ == "__main__":
    main()


