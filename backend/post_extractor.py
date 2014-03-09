import praw

def retrieve_posts(school_name):
    posts = r.get_subreddit(school_name).get_hot(limit=1000)
    fout = open('data/'+school_name, 'w')
    for x in posts:
        score = int(str(x).split('::')[0])
        text = str(x).split('::')[1].lower()

        # throw away none ascii strings
        try:
            text.decode('ascii')
            for i in range(0, 1+score/10):
                fout.write(text)
        except UnicodeDecodeError:
            print 'None ASCII: ' + text
    fout.close()

r = praw.Reddit(user_agent="flagship-map by wayne8798")
f = open('flagship_list.dat')
for line in f.readlines():
    if line[0] != '#':
        school_name = line.split()[1]
        retrieve_posts(school_name)
        print 'Finish fetching ' + school_name
f.close()
