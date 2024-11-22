# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout



def home(request):
    return render(request, 'accounts/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

from io import BytesIO
import matplotlib.pyplot as plt
from pymongo import MongoClient
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from bson import ObjectId

# MongoDB connection string
client = MongoClient("mongodb+srv://awaisamjad:N4VgJEMhoLvwcPld@cluster0.zmzyi.mongodb.net/")

# Access the database and collection
db = client["user"]
users_collection = db["user1"]

class UserProgressView(APIView):
    def get(self, request, user_id):
        """
        Fetches the user's progress and returns a combined image with horizontal bar and donut charts.
        """
        try:
            # Validate user_id format
            if not ObjectId.is_valid(user_id):
                return JsonResponse({"error": "Invalid user_id format"}, status=400)

            # Fetch user data from MongoDB
            user = users_collection.find_one({"_id": ObjectId(user_id)})
            if not user:
                return JsonResponse({"error": "User not found"}, status=404)

            # Extract relevant data
            completed_courses = len(user.get("completed_courses", []))
            current_courses = len(user.get("current_courses", []))
            wishlist_courses = len(user.get("wishlist", []))

            # Prepare data for plotting
            categories = ["Completed", "Current", "Wishlist"]
            values = [completed_courses, current_courses, wishlist_courses]

            # Updated color scheme
            colors = ['#ff9800', '#8bc34a', '#3f51b5']  # New color scheme: Orange, Green, Blue

            # Create a figure with two subplots (horizontal bar and donut chart)
            fig, axs = plt.subplots(1, 2, figsize=(14, 6))

            # Horizontal Bar Chart
            axs[0].barh(categories, values, color=colors)
            axs[0].set_title(f"User Progress: {user.get('fName', 'N/A')} {user.get('lName', 'N/A')}")
            axs[0].set_xlabel("Number of Courses")
            axs[0].set_ylabel("Category")
            axs[0].grid(axis='x', linestyle='--', alpha=0.7)

            # Donut Chart
            wedges, texts, autotexts = axs[1].pie(values, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops=dict(width=0.4))
            axs[1].set_title("User Progress (Donut)")

            # Adjust layout
            plt.tight_layout()

            # Save the plot to a BytesIO object
            buf = BytesIO()
            plt.savefig(buf, format="png")
            plt.close()  # Close the plot to free memory
            buf.seek(0)

            # Return the plot as an HTTP response
            return HttpResponse(buf.getvalue(), content_type="image/png")

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": "Error generating user progress", "details": str(e)}, status=500)



