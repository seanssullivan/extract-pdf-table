# main.py

# Standard Imports
import logging

# create and configure main logger
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# create console handler with a higher log level
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handler to the logger
log.addHandler(handler)


def main():
    log.info("Executing main.py script.")
    pass


if __name__ == "__main__":
    main()
