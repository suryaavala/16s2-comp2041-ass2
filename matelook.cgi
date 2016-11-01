#!/usr/bin/env python3.5

# written by andrewt@cse.unsw.edu.au September 2016
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/matelook/

import cgi, cgitb, glob, os, os.path, datetime, codecs

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
    #display_keys = ['Name:&#09;','zid:&#09;&#09;','Studies:&#09;','Born on:&#09;','Lives in:&#09;', 'Friends:&#09;']
    # display_data = ''
    # for k in range(6):
    #   display_data += display_keys[k]
    #   try:
    #     display_data += user_data[relavent_keys[k]]
    #   except Exception:
    #     display_data += 'None'
    #   display_data += '\n'
    for k in range(6):
      try:
        temp = user_data[relavent_keys[k]]
      except Exception:
        user_data[relavent_keys[k]] = 'None'

    profile_name = os.path.join(user_to_show, "profile.jpg")
    if os.path.isfile(profile_name):
        profile = profile_name
    else:
      profile = 'http://d1stfaw6j21ccs.cloudfront.net/assets/main/profile/fallback/default-b382af9ae20b5183b2eb1d6b760714c580c0eca7236cced714946bc0a044b2e6.png'


    post_text = get_posts(user_to_show,user_data['full_name'])
    #display_string = display_data + '<br><br>Posts:<br>' + post_text


    mate_list = get_mates(user_to_show,user_data['mates'])
    return """
<div class="matelook_user_details container well">
  <div class="row">
    <div class="col-sm-3">
      <img src=%s alt="Profile Picture" class="img-thumbnail img-responsive" >
    </div>
    <div class="col-sm-9">
      <div class="table-responsive">
        <table class="table">
            <tr>
              <th>Name</th>
              <td>%s</td>
            </tr>
            <tr>
              <th>zid</th>
              <td>%s</td>
            </tr>
            <tr>
              <th>Program</th>
              <td>%s</td>
            </tr>
            <tr>
              <th>Birthday</th>
              <td>%s</td>
            </tr>
            <tr>
              <th>Home</th>
              <td>%s</td>
            </tr>
            <tr>
              <th>Friends</th>
              <td>%s</td>
            </tr>
        </table>
      </div>
    </div>
  </div>
  <div class="row well">
    <h3> Posts:</h3>
    %s
  </div>
</div>
<form method="POST" action="">
    <input type="hidden" name="n" value="%s">
    <input type="submit" value="Next user" class="matelook_button">
</form>
<form method="POST" action="">
    <input type="hidden" name="n" value="%s">
    <input type="submit" value="Previous user" class="matelook_button">
</form>

""" % (profile, user_data['full_name'],user_data['zid'],user_data['program'],user_data['birthday'],user_data['home_suburb'],mate_list,post_text, n + 1, n-1)

#
#Function to collect all posts and return a post string in reverse chron order
#
def get_posts(user_to_show,full_name):
  posts = {}
  post_dir = os.path.join(user_to_show,'posts/')
  for i in os.listdir(post_dir):
    post_filename = os.path.join(post_dir,i, "post.txt")
    time = ''
    message = ''
    with open(post_filename,'rb') as f:
      for line in f:
        l = line.decode('utf-8')
        l = ''.join([i if ord(i) < 128 else ' ' for i in l])
        #l = l.replace(u"\u2018", "'").replace(u"\u2019", "'").replace(u"\u2026","'")
        key, value = l.split('=')
        if key == 'message':
          message = value
        if key == 'time':
          time = str(value).strip('\\n')
          #print (time)
    f.close()
    posts[time] = message
  post_string = ''
  for k in sorted(posts,reverse=True):
    time = datetime.datetime.strptime(k[:-6],'%Y-%m-%dT%H:%M:%S')
    time_stamp = time.strftime('<b>%d-%m-%Y</b> (%H:%M)')
    #time_stamp = time.strftime('{%s} {%s}, {%s} at {%s}:{%s}'.format(%b,%d,%Y,%H,%M))
    message = str(posts[k])
    message = message.replace('\\n','')
    post_string += '<p><b>' + full_name + '</b> posted on '+time_stamp+ ' :<br>' + message

  return post_string


#
#Function to collect all mate for the person and return html string
#
def get_mates(user_to_show,mate_list):
  mates = {}
  mate_list = mate_list[1:-1].split(', ')
  for mate_zid in mate_list:
    mate_dir = os.path.join(user_to_show,'..',mate_zid)
    mate_pic = os.path.join(mate_dir,'profile.jpg')
    if os.path.isfile(mate_pic):
        mate_profile = mate_pic
    else:
      mate_profile = 'http://d1stfaw6j21ccs.cloudfront.net/assets/main/profile/fallback/default-b382af9ae20b5183b2eb1d6b760714c580c0eca7236cced714946bc0a044b2e6.png'
    mate_file = os.path.join(mate_dir,'user.txt')
    mate_name = ''
    with open(mate_file,'r') as f:
        for line in f:
          if 'full_name' in line:
            key, mate_name = line.split('=')
    f.close()
    mates[mate_name] = mate_profile
    nb_mates = len(mates)
  mate_generic = '<figure class="figure"><img src="{}" class="figure-img img-responsive" alt="Thumbnail for mate"><figcaption class="figure-caption text-md-center">{}</figcaption></figure>'
  mate_string = '<table class="table table-sm"><tr>'
  for m in sorted(mates):
    mate_string += '<td>' + mate_generic.format(mates[m],m) + '</td>'
  mate_string += '</tr></table>'
  return mate_string

#
# HTML placed at the top of every page
#

def page_header():
    return """Content-Type: text/html;charset=utf-8

<!DOCTYPE html>
<html lang="en">
<head>
<title>matelook</title>
<link href="http://cgi.cse.unsw.edu.au/~cs2041cgi/16s2/2041.css" rel="stylesheet">
</head>
<body>
<div class="matelook_heading container text-center jumbotron">
<div class="row">
<h1>matelook</h1>
</div>
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
