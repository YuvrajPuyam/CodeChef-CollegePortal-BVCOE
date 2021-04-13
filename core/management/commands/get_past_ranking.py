from django.core.management.base import BaseCommand
from core.models import rank, pastcontest, pastrank
from datetime import datetime


import requests, json, time

class Command(BaseCommand):
    help = "Updates College Contest Ranks"
    def add_arguments(self, parser):
        parser.add_argument('access_token', type=str, help='Indicates a valid access token to use the CodeChef API.')

    def handle(self, *args, **options):
        access_token = options['access_token']
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
        
        pastcontest.objects.all().delete()
        pastrank.objects.all().delete()
        # temp = rank.objects.filter(username = 'dj').first()
        

        url = 'https://api.codechef.com/contests?status=past&limit=40'
        
        contests = requests.get(url, headers = headers).json()['result']['data']['content']['contestList']
        
        val = 1
        for contest in contests:
            pcontest = pastcontest(name=contest['name'],code=contest['code'])
            date_time_str = contest['startDate']
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            pcontest.date = date_time_obj
        
            
            url_contest = f'https://api.codechef.com/rankings/{pcontest.code}?institution=Bharati%20Vidyapeeth%20College%20of%20Engineering'
            userlist = (requests.get(url_contest, headers = headers).json()['result']['data'])
            
            print(val)
            val +=1
            if userlist['code'] == 9000:
                print(f"No Participation in contest {pcontest.code}")
            else : 
                print(f"Participated in contest {pcontest.code}")
                pcontest.save()
                userlist = userlist['content']
                for user in userlist:
                    temp = rank.objects.filter(username = user['username']).first()
                    if temp == None: 
                        print(f"Not in Database {user['username']}")
                        continue
                    print(temp.username, pcontest.code ,user['rank'],user['totalScore'])
                    p_rank = pastrank(user = temp, pastcontest = pcontest, contest_rank = user['rank'], totalScore = float(user['totalScore']) )
                    p_rank.save()
        
            time.sleep(10)
       