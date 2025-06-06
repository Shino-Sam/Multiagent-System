import os
import random
import time
import folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from streamlit_autorefresh import st_autorefresh
import streamlit as st
from scipy.optimize import linprog

# Set up your GitHub token for API access
token = os.getenv("GITHUB_TOKEN")

# Define the Azure DeepSeek API endpoint and model
endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"

# Set up the Azure DeepSeek API client
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def generate_completion(user_prompt):
    response = client.complete(
        messages=[SystemMessage("You are a helpful AI assistant."), UserMessage(user_prompt)],
        temperature=0.7,
        top_p=0.9,
        max_tokens=2048,
        model=model,
    )
    return response.choices[0].message.content

# --- Streamlit Configuration ---
st.set_page_config(page_title="🚛 Supply Chain Optimization Dashboard", page_icon="🚛", layout="wide")

# --- Title and Description ---
st.title("🚛 Real-Time Supply Chain Optimization + Delivery Routes")
st.markdown("""
- Real-time inventory monitoring 📦
- Delivery routes mapping 🗺️
- Truck tracking simulation 🚛
- Predictive analytics for delays ⏳
""")

# --- Real-Time Refresh every 5 seconds ---
count = st_autorefresh(interval=5 * 1000, key="auto_refresh")

# --- Simulate Real-Time Data ---
def simulate_real_time_data():
    demand = random.randint(100, 300)
    inventory = random.randint(20, 150)
    production_cost = random.randint(10, 30)
    supplier_cost = random.randint(15, 50)
    delivery_time = random.randint(2, 10)
    return demand, inventory, production_cost, supplier_cost, delivery_time

demand, inventory, production_cost, supplier_cost, delivery_time = simulate_real_time_data()

# --- Live Metrics ---
st.header("📈 Live Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Demand", f"{demand} units")
col2.metric("Inventory Level", f"{inventory} units", delta=f"{inventory - 100} units")
col3.metric("Production Cost", f"${production_cost}")
col4.metric("Supplier Cost", f"${supplier_cost}")

# 🚨 ALERT
if inventory < 50:
    st.error("⚠️ Inventory low! Act fast!")

# --- Define Multi-Agent System ---

class InventoryAgent:
    def __init__(self, inventory):
        self.inventory = inventory
    
    def check_inventory(self, demand):
        # If demand exceeds inventory, notify procurement agent
        if demand > self.inventory:
            return True
        return False

class ProcurementAgent:
    def __init__(self, supply_cost):
        self.supply_cost = supply_cost

    def order_materials(self, order_quantity):
        print(f"Procurement Agent: Ordering {order_quantity} units of material.")
        return order_quantity * self.supply_cost

class RouteOptimizationAgent:
    def __init__(self, delivery_time):
        self.delivery_time = delivery_time

    def optimize_route(self, destinations):
        print("Route Optimization Agent: Optimizing delivery routes...")
        return sorted(destinations, key=lambda x: x['distance'])

class SupplyChainCoordinator:
    def __init__(self, inventory_agent, procurement_agent, route_agent):
        self.inventory_agent = inventory_agent
        self.procurement_agent = procurement_agent
        self.route_agent = route_agent

    def coordinate(self, demand, destinations):
        # Check inventory and order materials if necessary
        if self.inventory_agent.check_inventory(demand):
            print("Inventory Agent: Inventory is low, notifying Procurement Agent.")
            self.procurement_agent.order_materials(demand)

        # Optimize delivery routes
        optimized_routes = self.route_agent.optimize_route(destinations)
        print("Supply Chain Coordinator: Coordinating agents...")
        return optimized_routes


# Example usage of Multi-Agent System
inventory_agent = InventoryAgent(inventory=100)
procurement_agent = ProcurementAgent(supply_cost=50)
route_agent = RouteOptimizationAgent(delivery_time=5)
coordinator = SupplyChainCoordinator(inventory_agent, procurement_agent, route_agent)

demand = 150
destinations = [{'city': 'Boston', 'distance': 200}, {'city': 'Philadelphia', 'distance': 150}]

# Coordinate the agents
optimized_routes = coordinator.coordinate(demand, destinations)
st.write(f"Optimized Routes: {optimized_routes}")

# --- Optimization ---
st.header("⚙️ Optimal Strategy")

c = [production_cost, supplier_cost]
A = [[1, 1]]
b = [max(demand - inventory, 0)]

result = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None), (0, None)], method="highs")

if result.success:
    production_units = int(result.x[0])
    supplier_units = int(result.x[1])
    total_cost = result.fun

    st.success(f"Optimal Plan Ready")
    col5, col6 = st.columns(2)
    col5.metric("Produce", production_units)
    col6.metric("Procure", supplier_units)

    st.info(f"💵 Estimated Total Cost: ${total_cost:.2f}")

# --- MAP SECTION 🚚🗺️ ---
st.header("🗺️ Warehouse to City Delivery Map")

# Warehouse and city coordinates (simulate)
warehouse_coords = (40.7128, -74.0060)  # New York warehouse
city_coords = {
    "Boston": (42.3601, -71.0589),
    "Philadelphia": (39.9526, -75.1652),
    "Washington D.C.": (38.9072, -77.0369)
}

m = folium.Map(location=warehouse_coords, zoom_start=6)

# Add warehouse marker
folium.Marker(warehouse_coords, popup="🏭 Warehouse", icon=folium.Icon(color="blue")).add_to(m)

# Add city markers
for city, coord in city_coords.items():
    folium.Marker(coord, popup=f"🚚 {city}", icon=folium.Icon(color="green")).add_to(m)
    folium.PolyLine([warehouse_coords, coord], color="red", weight=2.5, opacity=1).add_to(m)

st_folium(m, width=725)

# --- Supplier Health Monitoring 🏥 ---
st.header("🏥 Supplier Health Monitoring (Simulated)")

supplier_health = random.choice(["✅ Good", "⚠️ Warning", "❌ Bad"])
st.metric("Supplier Health Status", supplier_health)

if supplier_health == "⚠️ Warning":
    st.warning("Supplier performance degrading. Monitor closely!")
elif supplier_health == "❌ Bad":
    st.error("Supplier critical! Need alternative supplier!")

# --- Truck Tracking 🚛 ---
st.header("🚛 Live Truck Tracking (Slower Simulation)")

# Set the refresh interval (e.g., 5 seconds for updating truck data)
refresh_interval = 5  # seconds

# Set a limit for the simulation's movement speed (slower update)
truck_speed_limit = 0.2  # degrees per refresh, smaller values move trucks slower

# Initialize truck data
if "truck_data_refresh_time" not in st.session_state:
    st.session_state.truck_data_refresh_time = time.time()
    st.session_state.truck_locations = pd.DataFrame({
        "Truck ID": [f"T-{i}" for i in range(1, 6)],
        "Latitude": [40.7128 + random.uniform(-1, 1) for _ in range(5)],
        "Longitude": [-74.0060 + random.uniform(-1, 1) for _ in range(5)],
        "Speed (km/h)": [random.randint(40, 100) for _ in range(5)]
    })

# Refresh truck data only after the specified interval
if time.time() - st.session_state.truck_data_refresh_time > refresh_interval:
    # Update truck locations gradually by a small amount for slower movement
    for idx, row in st.session_state.truck_locations.iterrows():
        # Simulate gradual movement by adjusting latitude and longitude
        new_lat = row["Latitude"] + random.uniform(-truck_speed_limit, truck_speed_limit)
        new_lon = row["Longitude"] + random.uniform(-truck_speed_limit, truck_speed_limit)
        st.session_state.truck_locations.at[idx, "Latitude"] = new_lat
        st.session_state.truck_locations.at[idx, "Longitude"] = new_lon

    # Update the time of last refresh
    st.session_state.truck_data_refresh_time = time.time()

    # Display updated truck data
    st.dataframe(st.session_state.truck_locations)

    # Truck map
    truck_map = folium.Map(location=[40.7128, -74.0060], zoom_start=7)
    for idx, row in st.session_state.truck_locations.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=f"🚛 {row['Truck ID']} - {row['Speed (km/h)']} km/h",
            icon=folium.Icon(color="orange")
        ).add_to(truck_map)

    st_folium(truck_map, width=725)

else:
    st.info("Tracking trucks... Please wait for the next update.")

# --- Future Upgrades ---
st.markdown("---")
st.header("🔮 Future Plans")
st.markdown("""
- Live GPS integration 📡
- Automatic rescheduling based on traffic 🛣️
- Truck health monitoring 🛠️
- Predictive delays 📈
- Multi-city optimization 🌎
""")