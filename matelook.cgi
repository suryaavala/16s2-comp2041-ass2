#!/usr/bin/env python3.5

# written by andrewt@cse.unsw.edu.au September 2016
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/matelook/

import cgi, cgitb, glob, os, os.path

def main():
    print(page_header())
    cgitb.enable()
    users_dir = "dataset-medium"
    parameters = cgi.FieldStorage()
    print(user_page(parameters, users_dir))
    print(page_trailer(parameters))


#
# Show unformatted user for user "n".
# Increment parameter n and store it as a hidden variable
#
def user_page(parameters, users_dir):
    n = int(parameters.getvalue('n', 0))
    users = sorted(glob.glob(os.path.join(users_dir, "*")))
    user_to_show  = users[n % len(users)]
    user_filename = os.path.join(user_to_show, "user.txt")
    with open(user_filename) as f:
        user = f.read()
    user_data = {}
    for i in user.split('\n'):
      try:
        field, value = i.split('=')
        user_data[field] = value
      except Exception:
        continue
    relavent_keys = ['full_name','zid','program','birthday','home_suburb','mates']
    display_keys = ['Name:&#09;','zid:&#09;&#09;','Studies:&#09;','Born on:&#09;','Lives in:&#09;', 'Friends:&#09;']
    display_data = ''
    for k in range(6):
      display_data += display_keys[k]
      try:
        display_data += user_data[relavent_keys[k]]
      except Exception:
        display_data += 'None'
      display_data += '\n'
    profile_name = os.path.join(user_to_show, "profile.jpg")
    if os.path.isfile(profile_name):
        profile = profile_name
    else:
      profile = 'http://d1stfaw6j21ccs.cloudfront.net/assets/main/profile/fallback/default-b382af9ae20b5183b2eb1d6b760714c580c0eca7236cced714946bc0a044b2e6.png'

    return """
<div class="matelook_user_details">
<img src=%s alt="Profile Picture">
%s
</div>
<p>
<form method="POST" action="">
    <input type="hidden" name="n" value="%s">
    <input type="submit" value="Next user" class="matelook_button">
</form>
<form method="POST" action="">
    <input type="hidden" name="n" value="%s">
    <input type="submit" value="Previous user" class="matelook_button">
</form>
""" % (profile, display_data, n + 1, n-1)


#
# HTML placed at the top of every page
#
def page_header():
    return """Content-Type: text/html;charset=utf-8

<!DOCTYPE html>
<html lang="en">
<head>
<title>matelook</title>
<link href="matelook.css" rel="stylesheet">
</head>
<body>
<div class="matelook_heading">
matelook
</div>
"""


#
# HTML placed at the bottom of every page
# It includes all supplied parameter values as a HTML comment
# if global variable debug is set
#
def page_trailer(parameters):
    html = ""
    if debug:
        html += "".join("<!-- %s=%s -->\n" % (p, parameters.getvalue(p)) for p in parameters)
    html += "</body>\n</html>"
    return html

if __name__ == '__main__':
    debug = 1
    main()
