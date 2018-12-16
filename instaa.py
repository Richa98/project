import csv
from InstagramScraper import InstagramScraper
k = InstagramScraper()
n=input("Enter the number: ")
for i in range(int(n)):
        name=input("Enter the id : ")
        k.profile_page_metrics('https://www.instagram.com/'+name+'/')
        k.profile_page_recent_posts('https://www.instagram.com/'+name+'/')

    # print(results)


posts_list = []

with open('Data.csv','r') as f:
	reader = csv.reader(f)
	count=0
	for row in reader:
		if count==0:
			count+=1
			continue;
		posts_list.append(row)

#print('Caption of second post : ')
print(len(posts_list))


bio_detail_list = []

with open('Data1.csv','r') as f:
	reader = csv.reader(f)
	count=0
	for row in reader:
		if count<2:
			count+=1
			continue
		bio_detail_list.append(row)
#print('No of followers : ')
print(len(bio_detail_list))
#print(bio_detail_list[0][5])


