from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup

from .models import Links

def home(request):
    if request.method == 'POST':
        user_url = request.POST.get('page', '')
        try:
            response = requests.get(user_url)
            response.raise_for_status()  # Check for request errors
            soup = BeautifulSoup(response.text, 'html.parser')

            # Clear existing links in the database
            Links.objects.all().delete()

            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_name = link.string
                Links.objects.create(address=link_address, stringname=link_name)

            return HttpResponseRedirect('/')
        except requests.exceptions.RequestException as e:
            # Handle request errors here, e.g., display an error message to the user
            error_message = f"Error: {str(e)}"
            return render(request, 'home.html', {'error_message': error_message})
    else:
        data_values = Links.objects.all()

    return render(request, 'home.html', {'data_values': data_values})

# def clear_data(request):
#     # Clear all data in the Links model
#     Links.objects.all().delete()
#     return redirect('home')