from django.shortcuts import render
from .forms import LoginForm
import sqlite3

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Vulnerable SQL query (no parameterized queries)
            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            query = f"SELECT * FROM accounts_user WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                return render(request, 'accounts/success.html', {'username': username})
            else:
                return render(request, 'accounts/failure.html')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})
