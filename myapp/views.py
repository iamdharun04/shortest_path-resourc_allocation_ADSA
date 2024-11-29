from django.shortcuts import render
from .forms import GearPlannerForm
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'backpacking_planner'
}

# Function to retrieve gear data from MySQL
def retrieve_gear_data(trip_duration, weather_condition, terrain_type, max_weight):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Convert max_weight from kilograms to grams
        max_weight_grams = max_weight * 1000  # 1 kg = 1000 grams

        query = ("SELECT id, name, min_trip_duration, max_trip_duration, weather_condition, terrain_type, weight "
                 "FROM gear "
                 "WHERE %s BETWEEN min_trip_duration AND max_trip_duration "
                 "  AND (weather_condition = %s OR weather_condition = 'Any') "
                 "  AND (terrain_type = %s OR terrain_type = 'Any') "
                 "  AND weight <= %s")

        cursor.execute(query, (trip_duration, weather_condition, terrain_type, max_weight_grams))
        gear_items = cursor.fetchall()

        cursor.close()
        conn.close()

        return gear_items

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

def knapsack_solver(items, max_weight):
    n = len(items)
    dp = [[0] * (max_weight + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            weight = items[i - 1][6]  # weight of the current item
            if weight > w:
                dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = max(dp[i - 1][w], items[i - 1][6] + dp[i - 1][w - weight])

    selected_items = []
    w = max_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= items[i - 1][6]

    print(f"Selected {len(selected_items)} items after solving the knapsack problem.")
    return selected_items

# View function to handle gear planner form submission
def gear_planner_view(request):
    if request.method == 'POST':
        form = GearPlannerForm(request.POST)
        if form.is_valid():
            trip_duration = form.cleaned_data['trip_duration']
            weather_condition = form.cleaned_data['weather_condition']
            terrain_type = form.cleaned_data['terrain_type']
            max_weight_kg = form.cleaned_data['max_weight']  # Assuming user inputs weight in kilograms

            # Convert max_weight from kilograms to grams
            max_weight_grams = max_weight_kg * 1000  # 1 kg = 1000 grams

            print(f"Form data: trip_duration={trip_duration}, weather_condition={weather_condition}, terrain_type={terrain_type}, max_weight={max_weight_kg} kg")

            gear_items = retrieve_gear_data(trip_duration, weather_condition, terrain_type, max_weight_grams)

            if gear_items:
                selected_items = knapsack_solver(gear_items, max_weight_grams)
                return render(request, 'myapp/results.html', {'selected_items': selected_items})
            else:
                print("No gear items found matching the criteria.")
                return render(request, 'myapp/no_items_found.html')
        else:
            print("Form is not valid:", form.errors)
    else:
        form = GearPlannerForm()

    return render(request, 'myapp/form.html', {'form': form})

# Other view functions (home, about, plan_trip) as needed
def home(request):
    return render(request, 'myapp/home.html')

def about(request):
    return render(request, 'myapp/about.html')

def plan_trip(request):
    return render(request, 'myapp/plan_trip.html')
