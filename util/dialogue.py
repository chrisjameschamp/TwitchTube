import logging

logger = logging.getLogger(__name__)

from util import constants, functions

def intro():
    logger.info('Welcome to TwitchTube')
    functions.checkVersion()
    logger.info('Along the way you will have to answer a few questions')
    logger.info('All questions are required, however some have a default answer which will be defined as (Default: x) after the prompt, or in the case of a yes / no question, the Capital option will be the default (Y/n) or (y/N)')

def query(type, question, min=0, max=0, prePrint='', default='', errorMsg='', options=[]):
        if prePrint:
            logger.info(prePrint)
        while True:
            logger.info(question)
            if default:
                user_input = input('>>> ') or default
            else:
                user_input = input('>>> ')

            # Yes or No Answers
            if type == 'Y/N':
                if user_input.lower() in ('yes', 'no', 'y', 'n'):
                    return user_input.lower()
                else:
                    logger.warning('Please just answer with either Yes or No')

            # Options
            elif type == 'Options':
                if user_input.lower() in options:
                    return(user_input.lower())
                else:
                    if errorMsg:
                        logger.error(errorMsg)
                    else:
                        logger.error('Please just answer with one of the defined responses')

            # Time
            elif type == 'Time':
                if functions.isValidTimeFormat(user_input):
                    return(functions.seconds(user_input))
                else:
                    if errorMsg:
                        logger.error(errorMsg)
                    else:
                        logger.error('Please enter a valid time input using the format 00h00m00s, IE 1h25m22s or 1m15s')

            # Required
            elif type == 'Required':
                if user_input:
                    return user_input

            # Is Numeric
            elif type == 'Numeric':
                if not user_input and default!='':
                    return default
                if max > 0 and min > 0:
                    if user_input.isnumeric() and min <= int(user_input) <= max:
                        return user_input
                    else:
                        if errorMsg:
                            logger.error(errorMsg)
                        else:
                            logger.error('Please enter a number between {} and {}', min, max)
                elif max > 0:
                    if user_input.isnumeric() and int(user_input) <= max:
                        return user_input
                    else:
                        if errorMsg:
                            logger.error(errorMsg)
                        else:
                            logger.error('Please enter a number less than {}', max)
                elif min > 0:
                    if user_input.isnumeric() and int(user_input) <= max:
                        return user_input
                    else:
                        if errorMsg:
                            logger.error(errorMsg)
                        else:
                            logger.error('Please enter a number greater than {}', min)
                else:
                    if user_input.isnumeric():
                        return user_input
                    else:
                        if errorMsg:
                            logger.error(errorMsg)
                        else:
                            logger.error('Please enter a number')

            else:
                return user_input

            
