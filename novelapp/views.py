from django.shortcuts import render
from novelapp.wuxia import wuxia_world_convertion,novel_full,custom_novel
from rest_framework.response import Response
from django.http import HttpResponse
import os

linklist = []
def homepage(request):
    con = {'title':"dbz"}
    if request.method == 'POST':
        source = request.POST.get('source')
        link = request.POST.get('link')
        filename = request.POST.get('novelName')

        if source == "wuxia":
            pathmap = wuxia_world_convertion(link)
            check = pathmap.get("check")
            if check:
                print(pathmap.get("path"))
                path = pathmap.get("path")
                file = open(path, "rb")
                data = file.read()
                file.close()
                response = HttpResponse(data, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename= '+filename+'.epub'
                if os.path.exists(path): os.remove(path)
                return response
            else:
                con["error"] = "error found check log"
        if source == "novelfull":
            pathmap = novel_full(link)
            check = pathmap.get("check")
            if check:
                path = pathmap.get("path")
                print(path)
                file = open(path, "rb")
                data = file.read()
                file.close()
                response = HttpResponse(data, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename= '+filename+'.epub'
                if os.path.exists(path): os.remove(path)
                return response
            else:
                con["error"] = "error found check log"
    return render(request,"newpage.html",con)

# Create your views here.
