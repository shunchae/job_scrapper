from bs4 import BeautifulSoup
import requests

def extract_jobs_remoteok(term):
  url = f"https://remoteok.com/remote-{term}-jobs"
  request = requests.get(url, headers={"User-Agent": "Kimchi"})
  if request.status_code == 200:
    soup = BeautifulSoup(request.text, "html.parser")
    # write your ✨magical✨ code here
    results = []
    jobs = soup.find_all('tr', class_="job")
    for job in jobs:
      job_post = job.find_all('td', class_="company")
      for post in job_post:
        position = post.find('h2')
        company = post.find('h3')
        
        number_class_location = len(post.find_all('div', class_='location'))
        if number_class_location>1:
          location = post.find_all('div', class_='location')
          nth_location = []
          for n in range(0, number_class_location-1):
            nth_location.append(location[n].string)
          location = ", ".join(nth_location)

        payment = post.find_all('div', class_='location')[-1]  
        link = post.find('a')['href']

        job_data = {
          'position' : position.string[1:-1],
          'company' : company.string[1:-1],
          'location' : location,
          'link' : f"https://remoteok.com{link}",
          'payment' : payment.string
        }
        results.append(job_data)
      
  else:
    print("Can't get jobs.")

  return results
