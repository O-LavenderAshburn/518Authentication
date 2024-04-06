def check_sequential(password):
    # Check for repetitive characters
    seen = set()
    for char in password:
        if char in seen:
            return False
        seen.add(char)
    
    # Check for sequential characters
    for i in range(len(password) - 2):
        if ord(password[i]) == ord(password[i+1]) - 1 == ord(password[i+2]) - 2:
            return False
        if ord(password[i]) == ord(password[i+1]) + 1 == ord(password[i+2]) + 2:
            return False
    
    return True


def check_compromised_password(password, filename):
    with open(filename, 'r') as file:
        compromised_passwords = file.readlines()
        compromised_passwords = [pwd.strip() for pwd in compromised_passwords]
        if password in compromised_passwords:
            return True
        else:
            return False
        

