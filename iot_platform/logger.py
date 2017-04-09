import logging

def get_custom_logger(process_name, file_name = None):
    #logging related initializations
    logger = logging.getLogger(process_name)
    logger.setLevel(logging.DEBUG)

    if file_name is not None:
        file_name = '/var/www/html/' + file_name
        handler = logging.FileHandler(file_name)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    else:
        file_name = '/var/www/html/' + str(process_name) + '.log'
        handler = logging.FileHandler(file_name)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
