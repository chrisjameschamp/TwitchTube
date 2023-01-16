from util import constants, functions

def intro():
    print('Welcome to TwitchTube\nVersion '+str(constants.VERSION)+'\n\nAlong the way you will have to answer a few questions.  All questions are required, however some have a default answer which will be defined as (Default: x) after the prompt, or in the case of a yes / no question, the Capital option will be the default (Y/n) or (y/N)\n')

def query(type, question, min=0, max=0, prePrint='', default='', errorMsg='', options=[]):
        if prePrint:
            print(prePrint)
        while True:
            if default:
                user_input = input(question) or default
            else:
                user_input = input(question)

            # Yes or No Answers
            if type == 'Y/N':
                if user_input.lower() in ('yes', 'no', 'y', 'n'):
                    print('')
                    return user_input.lower()
                else:
                    print('Please just answer with either Yes or No')

            # Options
            elif type == 'Options':
                if user_input.lower() in options:
                    print('')
                    return(user_input.lower())
                else:
                    if errorMsg:
                        print(errorMsg)
                    else:
                        print('Please just answer with either one of the defined responses')

            # Time
            elif type == 'Time':
                if functions.isValidTimeFormat(user_input):
                    print('')
                    return(functions.seconds(user_input))
                else:
                    if errorMsg:
                        print(errorMsg)
                    else:
                        print('Please enter a valid time input using the format 00h00m00s, IE 1h25m22s or 1m15s')

            # Required
            elif type == 'Required':
                if user_input:
                    print('')
                    return user_input

            # Is Numeric
            elif type == 'Numeric':
                if not user_input and default!='':
                    print('')
                    return default
                if max > 0 and min > 0:
                    if user_input.isnumeric() and min <= int(user_input) <= max:
                        print('')
                        return user_input
                    else:
                        if errorMsg:
                            print(errorMsg)
                        else:
                            print('Please enter a number between '+str(min)+' and '+str(max))
                elif max > 0:
                    if user_input.isnumeric() and int(user_input) <= max:
                        print('')
                        return user_input
                    else:
                        if errorMsg:
                            print(errorMsg)
                        else:
                            print('Please enter a number less than '+max)
                elif min > 0:
                    if user_input.isnumeric() and int(user_input) <= max:
                        print('')
                        return user_input
                    else:
                        if errorMsg:
                            print(errorMsg)
                        else:
                            print('Please enter a number greater than '+min)
                else:
                    if user_input.isnumeric():
                        print('')
                        return user_input
                    else:
                        if errorMsg:
                            print(errorMsg)
                        else:
                            print('Please enter a number')

            else:
                print('')
                return user_input

            
