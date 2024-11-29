from django.shortcuts import render
from .forms import CityForm
import pymysql as mysql
import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from io import BytesIO
import base64
from heapq import heappop, heappush

# Database connection details
db_config = {
    'user': 'root',
    'password': '0000',
    'host': 'localhost',
    'database': 'touring_places_db'
}


def fetch_touring_places_from_db(city):
    connection = mysql.connect(user=db_config['user'], password=db_config['password'], host=db_config['host'],
                               database=db_config['database'])
    cursor = connection.cursor()
    query = "SELECT name, latitude, longitude FROM touring_places WHERE city = %s"
    cursor.execute(query, (city,))
    places = cursor.fetchall()
    cursor.close()
    connection.close()
    return places


def create_graph(places):
    G = nx.Graph()

    # Add nodes to the graph
    for place in places:
        G.add_node(place[0], pos=(place[1], place[2]))

    # Calculate distances and add edges with weights (in kilometers)
    for i in range(len(places)):
        for j in range(i + 1, len(places)):
            # Calculate distance in kilometers
            distance_km = geodesic((places[i][1], places[i][2]), (places[j][1], places[j][2])).kilometers
            G.add_edge(places[i][0], places[j][0], weight=distance_km)

    return G


def plot_graph(G, title):
    pos = nx.spring_layout(G)  # Example using spring layout

    # Customize node appearance
    node_size = 2000
    node_color = "skyblue"
    node_edge_color = "black"
    node_alpha = 0.8

    # Customize edge appearance
    edge_color = "gray"
    edge_width = 1.5

    # Draw graph with labels
    nx.draw(G, pos, with_labels=True, node_size=node_size, node_color=node_color, font_size=12, font_weight="bold",
            alpha=node_alpha, edge_color=edge_color, width=edge_width)

    # Draw edge labels with distances (in kilometers)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

    # Set title and adjust plot margins
    plt.title(title, fontsize=15)
    plt.margins(0.1)

    # Convert plot to image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    # Convert image to base64 for rendering in template
    image_base64 = base64.b64encode(image_png).decode('utf-8')
    return image_base64


def prim_algorithm(G):
    """
    Computes the Minimum Spanning Tree (MST) using Prim's algorithm.
    """
    mst = nx.Graph()
    visited = set()

    # Start from an arbitrary node, here we choose the first node
    start_node = list(G.nodes())[0]
    visited.add(start_node)

    # Create a priority queue to store the edges with their weights
    edges = []
    for to, attributes in G[start_node].items():
        heappush(edges, (attributes['weight'], start_node, to))

    while edges:
        weight, frm, to = heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.add_edge(frm, to, weight=weight)

            for next_to, next_attributes in G[to].items():
                if next_to not in visited:
                    heappush(edges, (next_attributes['weight'], to, next_to))

    return mst


def plan_tour(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            places = fetch_touring_places_from_db(city)
            if not places:
                return render(request, 'tourplan/plan_tour.html', {
                    'form': form,
                    'error': f"No touring places found for city: {city}"
                })

            G = create_graph(places)
            graph_image = plot_graph(G, f"Touring Places in {city.capitalize()}")

            mst = prim_algorithm(G)
            mst_image = plot_graph(mst, f"Minimum Spanning Tree (MST) for {city.capitalize()}")

            return render(request, 'tourplan/plan_tour.html', {
                'form': form,
                'graph_image': graph_image,
                'mst_image': mst_image,
            })
    else:
        form = CityForm()

    return render(request, 'tourplan/plan_tour.html', {'form': form})
