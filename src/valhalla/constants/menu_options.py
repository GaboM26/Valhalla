
###########################################################################################################################
# Configurable Menu Options
# Take the form: {option_number: (function_name, description)}
# NOTE: The function_name should be a method of the MenuClient class
SUPPORTED_OPTIONS = {
    1: ('new_entry', 'Insert a new account+password'),
    2: ('view_accounts', 'View available accounts'),
    3: ('get_entry', 'Get an entry for a specific account'),
    4: ('update_entry', 'Update an entry for a specific account'),
    5: ('delete_entry', 'Delete an entry for a specific account'),
    'q': ('', 'Exit Valhalla')
}

##########################################################################################################################
# Fun constants

VALHALLA_BANNER = """
|\     /|(  ___  )( \      |\     /|(  ___  )( \      ( \      (  ___  )
| )   ( || (   ) || (      | )   ( || (   ) || (      | (      | (   ) |
| |   | || (___) || |      | (___) || (___) || |      | |      | (___) |
( (   ) )|  ___  || |      |  ___  ||  ___  || |      | |      |  ___  |
 \ \_/ / | (   ) || |      | (   ) || (   ) || |      | |      | (   ) |
  \   /  | )   ( || (____/\| )   ( || )   ( || (____/\| (____/\| )   ( |
   \_/   |/     \|(_______/|/     \||/     \|(_______/(_______/|/     \|
"""
VALHALLA_CREDITS = 'Password Manager Created by Gabriel Millares Bellido (@gabo_m26)'

NUM_POINTS = 3
SUSPENSE_CREATOR_AMOUNT = 1
STARLINE = '******************************************************************************************************'

ODIN_PERMISSIONS= '**************************************ODIN PERMISSIONS GRANTED****************************************'