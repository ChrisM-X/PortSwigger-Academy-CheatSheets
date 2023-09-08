# This script will help to solve a Portswigger lab for Authentication Category
# The output of this can be used in Intruder to solve the lab
# Lab: https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block

# The Portswigger-Username-List.txt file holds the usernames given by Portswigger or 100 times the name "carlos" for this specific lab (to brute force a specific username copy/paste in text file easily then reference here)
# This needs to be provided manually, change name of file as needed
with open("Portswigger-Username-List-AllCarlos.txt", "r") as istr:

    # This will be the file where the new data will be appended to
    with open("Portswigger-Username-List-Output-AllCarlos.txt", "w") as ostr:

        # Will iterate every line of the file
        for i, line in enumerate(istr):

            # Get rid of the trailing newline (if any)
            line = line.rstrip("\n")

            # Basically after every single line it will append the String "wiener"
            if i % 1 == 0:
                line += "\nwiener"

            print(line, file=ostr)
