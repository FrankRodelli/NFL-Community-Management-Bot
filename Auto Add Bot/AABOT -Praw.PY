import praw
import time
import os
users = open('users.txt' , 'r')


SUBREDDIT = input('Enter the name of the subreddit you are adding users to: ')
r=praw.Reddit('script for adding users as approved submitters')
r.login(disable_warning=True)


subreddit=r.get_subreddit(SUBREDDIT)
def main():
    for line in users:
            try:
                username = users.readline()
                subreddit.add_contributor(username)
                print(username,'added!')
            except praw.errors.APIException:
                print('Error, trying again in 20 minutes')
                time.sleep(1200)
main()
print('Complete')
