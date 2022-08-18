'''
for install requirments type the following in cmd after run it as adminstrator in the current path
    pip install -r requirments.txt


This code for get transcript for ted.com videos

'''
#import libraries
from bs4 import BeautifulSoup
import csv
import requests

#for filter transcript
def filter_(script):
    skip = 0
    j = -1
    transcript = ''
    while( j < len(script) ):
        j += 1
        skip = 0
        if(j >= len(script)):
            break
        if script[j] == '<':
            while(1):
                if(j >= len(script)):
                    break
                if(script[j] == '>'):
                    j+=1
                    break
                j+=1
        if(j >= len(script)):
            break
        if (script[j] >= '0' and script[j] <= '9') or script[j] == ':' or script[j] == '\n' or script[j] == '\t':
            skip = 1
        if skip == 1:
            continue
        transcript += script[j] 
    return transcript

TED_TALK_URL = 'https://www.ted.com/index.php/talks/'


#this function is for reaquest an url
# we use in this project web scraping
def get_html(url):
    html = requests.get(url) 
    soup = BeautifulSoup(html.content, 'html.parser')
    return soup	

# for Get TED trascripts for videos
def get_transcript(talk_url):
    talk_url = talk_url[:(len(talk_url)-12)]
    if not talk_url.startswith('https://'):
        talk_url = TED_TALK_URL + talk_url
    talk_url = talk_url  + '/transcript?language=en'
    print(talk_url)
    soup = get_html(talk_url)
    script = soup.find_all('div', class_='Grid Grid--with-gutter d:f@md p-b:4')
    return filter_(str(script))

# load our data set
with open('data.csv', encoding='UTF8') as file_obj:
    # Create reader object by passing the file
    # object to DictReader method
    reader_obj = csv.DictReader(file_obj)

    # Iterate over each row in the csv file
    # using reader object
    record = dict()
    i = 0
    for row in reader_obj:
        record['id'] = i
        record['title'] = row['title']
        record['author'] =  row['speaker_name']
        record['date'] = row['posted_date']
        record['views'] = row['views']
        record['tags'] = row['tags']
        record['link'] = row['Link']

        # get transcript for videos by web scraping from TED.com 
        transcript = get_transcript(row["Link"])
        #print(transcript)
        record['transcript'] = transcript
        #write transcript into new csv file
        with open('d.csv', 'a', encoding='UTF8')as f:
            # create the csv writer
            writer = csv.writer(f)
            # write a row to the csv file
            writer.writerow([ record['id'], record['title'], record['author'], record['date'], record['views'], record['tags'], record['link'], record['transcript']])
        i += 1
        print(record)
