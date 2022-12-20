def parser(email):  
    mail=str(email)
    parsed_email=mail.split("@")
    filename=str(parsed_email[0])
    return filename