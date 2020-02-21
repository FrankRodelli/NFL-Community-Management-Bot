import praw


subreddit = input('Please enter the name of the subreddit to pull users from: ')

r= praw.Reddit('bot for pulling list of approved contributors')
r.login()
req = r.get_contributors(subreddit,limit=None)
memberlist = []

def get_mlist():
    for u in req:
        username = str(u)
        memberlist.append(username)
    memberlist.reverse()
    return memberlist
def save_to_file():

    with open('approvedusers.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n\n'.join(memberlist))
        myfile.write('\n\n')

get_mlist()
save_to_file()
