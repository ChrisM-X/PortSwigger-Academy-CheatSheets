# This script will help to solve a Portswigger lab for Authentication Category
# The output of this can be used in Intruder to solve the lab
# Lab: https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block

# The Portswigger-Password-List.txt file holds the passwords given by Portswigger
# This needs to be provided manually, change name of file as needed
with open("Portswigger-Password-List.txt", "r") as istr:

    # This will be the file where the new data will be appended to
    with open("Portswigger-Password-List-Output.txt", "w") as ostr:

        # Will iterate every line of the file
        for i, line in enumerate(istr):

            # Get rid of the trailing newline (if any)
            line = line.rstrip("\n")

            # Basically after every single line it will append the String "peter"
            if i % 1 == 0:
                line += "\npeter"

            print(line, file=ostr)
