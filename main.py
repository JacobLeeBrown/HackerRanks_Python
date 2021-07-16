
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)10s - %(levelname)7s - %(message)s', level=logging.DEBUG
)


def main():
    logging.info("Hello World!")


if __name__ == "__main__":
    main()
