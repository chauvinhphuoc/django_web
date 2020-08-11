from django.shortcuts import render
from .models import *
import requests
from bs4 import BeautifulSoup


# Create your views here.
def list_job(request):
    def get_page_tree(p=1):
        resp = requests.get(
            "https://github.com/awesome-jobs/vietnam/issues?page={}".format(p)
        )
        return BeautifulSoup(resp.text, "lxml")

    def extract_time(jobnode):
        return jobnode.find("relative-time", class_="no-wrap").text.strip()

    page = 1
    while True:
        root = get_page_tree(page)
        # if a page not contains this class, there is no job
        # we reached last page
        if not root.find("div", attrs={"role": "group"}):
            break

        for j in root.find_all("div", class_="Box-row"):
            job = j.find("div", class_="flex-auto").find("a")
            path = job.get("href")
            fullurl = "https://github.com/{}".format(path).strip()

            jobinfo = Job(title=job.text, time=extract_time(j), url=fullurl)
            jobinfo.save()

        page = page + 1

    for row in Job.objects.all().reverse():
        if Job.objects.filter(url=row.url).count() > 1:
            row.delete()

    return render(request, "jobs/list.html", {"jobs": Job.objects.all()})

