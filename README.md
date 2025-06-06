# Multiagent-System

# 🤖 Multi-Agent System Using DeepSeek API

This repository contains three AI-powered agents built using GitHub's DeepSeek API and Streamlit. Each agent is designed for a specific domain but they can collaborate in a multi-agent system.

---

## 1️⃣ Trip Planner Agent

Plan your dream trip with AI assistance covering itineraries, hotels, flights, weather, local events, and security tips.

### Features

- Detailed daily trip plans based on user preferences  
- Hotel, flight, weather, event suggestions  
- Travel safety and fraud prevention tips  
- Interactive chatbot for custom trip queries  
- Downloadable trip plan  

### Tech Stack

- Python 3.8+  
- Streamlit  
- Azure AI Inference SDK  
- DeepSeek-V3-0324 model  

### Usage

- Input destination, days, travelers, interests  
- Select options like hotels, flights, weather, etc.  
- Generate plan and download results  
- Chat with the AI for custom questions  

---

## 2️⃣ Resume Builder Agent

Upload your resume (TXT format) and get professional AI review, improvement suggestions, and restructured resume generation.

### Features

- Resume upload and preview  
- AI review for improvements and error fixes  
- Generate a professional resume from prompts  
- Download improved resume  

### Tech Stack

- Python 3.8+  
- Streamlit  
- Azure AI Inference SDK  
- DeepSeek-V3-0324 model  

### Usage

- Upload your resume in TXT  
- Use AI actions to review or rebuild resume  
- Download the improved resume  

---

## 3️⃣ Supply Chain Optimizer Agent

Optimize your supply chain operations including inventory, demand forecasting, logistics, and procurement.

### Features

- Inventory and distribution optimization  
- Logistics bottleneck analysis  
- Demand forecasting based on product and region  
- Cost-effective procurement and shipping suggestions  
- Export optimized supply chain plans  

### Tech Stack

- Python 3.8+  
- Streamlit  
- Azure AI Inference SDK  
- DeepSeek-V3-0324 model  

### Usage

- Input product and location data  
- Select constraints (cost, delivery time, warehouse limits)  
- Generate optimized supply chain strategies  
- Export plans for use  

---

## Common Setup Instructions

1. **Clone repository:**

```bash
git clone https://github.com/yourusername/multi-agent-system.git
cd multi-agent-system

2. Create .env file with your GitHub token:
GITHUB_TOKEN=your_github_token_here

3. Install dependencies:
pip install -r requirements.txt

4. Run agent app:
streamlit run trip_planner.py
# .....
streamlit run resume_builder.py
#.....
streamlit run supply_chain_optimizer.py

License
MIT License. Feel free to use and modify for personal, academic, or commercial purposes.

