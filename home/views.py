from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html', {'page_indicator': 'Home', 'menu_name': 'main'})


def child1ofchild1(request):
    return render(request, 'home/home.html', {'page_indicator': 'child1ofchild1'})


def child1(request):
    return render(request, 'home/home.html', {'page_indicator': 'child1'})



def child2(request):
    return render(request, 'home/home.html', {'page_indicator': 'child2'})


def child2ofchild1(request):
    return render(request, 'home/home.html', {'page_indicator': 'child2ofchild1'})


def page1(request):
    return render(request, 'home/home.html', {'page_indicator': 'page1'})


def page2(request):
    return render(request, 'home/home.html', {'page_indicator': 'page2'})
