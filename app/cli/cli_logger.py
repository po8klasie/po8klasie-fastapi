import logging

CLI_LOGGER_NAME = "cli_logger"
CLI_LOGGER_LEVEL = logging.INFO

cli_logger = logging.getLogger(CLI_LOGGER_NAME)

cli_logger.setLevel(CLI_LOGGER_LEVEL)

ch = logging.StreamHandler()
ch.setLevel(CLI_LOGGER_LEVEL)

cli_logger.addHandler(ch)
