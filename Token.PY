import threading
import praw 
import time
import datetime
import OAuth2Util
import asyncio
import discord
import random
import pymysql
import os

#Global Vars
run_match_thread = True
exists = False
bottime = time.strftime("%m-%d-%Y %H") #Sets bot time
run = True
run_match_thread = True
run_main = True
run_all = True
#reddit/discord config
SUBREDDIT = 'nflstreams_private'
r = praw.Reddit("Creates and maintains match threads. Created by /u/Astatutorygrape")
o = OAuth2Util.OAuth2Util(r)
subreddit=r.get_subreddit(SUBREDDIT)

#This function checks if game thread exists and creates one for each game if not
def create_threads():
    while run is True: 
        matches=open('matches.txt','r')
        for line in matches:
                exists=False
                matchtime = matches.readline()
                if bottime in matchtime:
                        matchtitle = matchtime.replace(bottime,'').strip()
                        for submission in subreddit.get_hot():
                                if matchtitle in submission.title:
                                    exists=True
                        if exists:
                                print('Thread Exists')
                        if not exists:
                                print('Creating Thread')
                                subreddit.submit(matchtitle, text=matchtitle)
                                posts=open('posts.txt','a')
                                postinsert=('\n{}\n').format(matchtitle)
                                posts.write(postinsert)
                                posts.close()
        matches.close()
        print('Finished creating threads. Waiting 20 minutes and trying agian')
        time.sleep(150)

def delete_threads():
    print ('Checking for old ass threads')
    run = True
    while run_all is True:
        #Creates loop for each reddit submission
        for submission in subreddit.get_hot():
            posttitledoc=open('posts.txt','r')#opens posts document for reference 
            for line in posttitledoc:
                    exists=False
                    posttitle = posttitledoc.readline()
                    if submission.title in posttitle:
                        exists=True

                    if exists:
                        print ('\nFound a duplicate.')
                        #Get's time of the submission and formats it correctly
                        time1 = submission.created
                        time2 = datetime.datetime.fromtimestamp(time1)
                        time3 = time2.strftime('%H')

                        #Sets current bot time in hours 
                        botHM = time.strftime('%H')
                        
                        #Calculates age of post (Negative means posted before current time on different day)
                        calc = int(botHM) - int(time3)
                        difference = calc+8#+8 for time offset 
                            
                        #Sets time and date of post to var
                        posttimedate = time2.strftime('%m-%d-%Y %H:%M')

                        #Prints information about post being analyzed
                        print (submission.title)
                        print ('The post date and time is: ',posttimedate)
                        print ('The current time is: ',botHM)
                        print ('The post is',difference,'hours old')

                        #Checks if post is 4 hours old and deletes 
                        if difference >= 4:
                            print ('\nGame over. Deleting thread.\n')
                            submission.remove()

                        else:
                            print('\nGame in progress\n')
                                            
                    if not exists:
                        print('No match')

        posttitledoc.close()
        print('Finished deleting threads. Sleeping for 1 minute')
        time.sleep(60)
        
#Function that monitors for token requests, stores tokens locally and on the MYSql DB, and sends them to user
def token_bot():
    os.system('token_bot.py')

def printme():
    while run_all is True:
        print ('LOOPING!')
#Function management/threading function
def main():
    thread = threading.Thread(target=token_bot)
    #Creates Threads
    thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
    thread.start()

    while run_main is True:
        global run_all #Imports global variable to stop functions from running before re-launching
        run_all = True
        thread = threading.Thread(target=create_threads)
        #Creates Threads
        thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        thread.start()
        
        print('Started Thread Creation Bot')
        time.sleep(5)

        thread = threading.Thread(target=delete_threads)
        #Creates Threads
        thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        thread.start()

        print('Created Thread Deletion Bot')
        time.sleep(5)
        
        print('\nAll bots launched in threads. Sleeping FOREVER!')
        time.sleep(86400)
        run_all = False

    
main()
