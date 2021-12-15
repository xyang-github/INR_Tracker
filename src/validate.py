import re

from PyQt5.QtSql import QSqlQuery


def validate_new_indication(new_indication):
    """Validates line edit widget and returns an error message. Error message is blank if passes validation."""
    string_format = "^[\w() -]{2,}$"  # Allow words, spaces, hyphens, and parenthesis
    error_message = ""

    # Validate line edit widget
    if not re.match(string_format, new_indication):
        error_message += "Indication name can only contain words, spaces, hyphens, and parenthesis; must be " \
                         "at least 2 characters in length.\n"
    else:
        query = QSqlQuery()
        bOk = query.exec("SELECT indication_id, indication_name FROM indication")
        if bOk:
            all_indications = []
            while query.next():
                all_indications.append((query.value('indication_id'), query.value('indication_name')))

            # Check for duplicate entries
            for indication in all_indications:
                if new_indication == indication[1]:
                    error_message += "This indication already exists.\n"

    return error_message