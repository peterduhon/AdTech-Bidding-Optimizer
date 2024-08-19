import sqlite3
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Connect to a sample SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect('adtech.db')
cursor = conn.cursor()

# Create a sample table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bids (
        bid_id INTEGER PRIMARY KEY,
        advertiser_id TEXT,
        bid_amount REAL,
        ssp_id TEXT,
        win INTEGER,
        timestamp DATETIME
    )
''')

# Generate sample data
advertisers = ['adv1', 'adv2', 'adv3', 'adv4', 'adv5']
ssps = ['ssp1', 'ssp2', 'ssp3']

# Insert sample data
for i in range(1000):  # Generate 1000 sample bids
    advertiser = random.choice(advertisers)
    ssp = random.choice(ssps)
    bid_amount = round(random.uniform(1.0, 10.0), 2)
    win = random.choice([0, 1])
    timestamp = datetime.now() - timedelta(days=random.randint(0, 30))
    
    cursor.execute('''
        INSERT INTO bids (advertiser_id, bid_amount, ssp_id, win, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (advertiser, bid_amount, ssp, win, timestamp))

conn.commit()

# Query 1: Calculate win rate for each SSP
print("Win rate for each SSP:")
cursor.execute('''
    SELECT ssp_id, 
           AVG(win) as win_rate, 
           COUNT(*) as total_bids,
           SUM(bid_amount) as total_bid_amount
    FROM bids
    GROUP BY ssp_id
''')

results = cursor.fetchall()
for row in results:
    print(f"SSP: {row[0]}, Win Rate: {row[1]:.2f}, Total Bids: {row[2]}, Total Bid Amount: ${row[3]:.2f}")

# Visualization for Query 1
ssps = [row[0] for row in results]
win_rates = [row[1] for row in results]

plt.figure(figsize=(10, 6))
plt.bar(ssps, win_rates, color='skyblue')
plt.xlabel('SSP ID')
plt.ylabel('Win Rate')
plt.title('Win Rate by SSP')
plt.show()

print("\n")

# Query 2: Top 3 advertisers by total spend
print("Top 3 advertisers by total spend:")
cursor.execute('''
    SELECT advertiser_id, SUM(bid_amount) as total_spend
    FROM bids
    WHERE win = 1
    GROUP BY advertiser_id
    ORDER BY total_spend DESC
    LIMIT 3
''')

results = cursor.fetchall()
for row in results:
    print(f"Advertiser: {row[0]}, Total Spend: ${row[1]:.2f}")

# Visualization for Query 2
advertisers = [row[0] for row in results]
total_spends = [row[1] for row in results]

plt.figure(figsize=(10, 6))
plt.bar(advertisers, total_spends, color='lightgreen')
plt.xlabel('Advertiser ID')
plt.ylabel('Total Spend ($)')
plt.title('Top 3 Advertisers by Total Spend')
plt.show()

print("\n")

# Query 3: Daily average bid amount for the past week
print("Daily average bid amount for the past week:")
cursor.execute('''
    SELECT DATE(timestamp) as date, AVG(bid_amount) as avg_bid
    FROM bids
    WHERE timestamp >= DATE('now', '-7 days')
    GROUP BY DATE(timestamp)
    ORDER BY date DESC
''')

results = cursor.fetchall()
for row in results:
    print(f"Date: {row[0]}, Average Bid: ${row[1]:.2f}")

# Visualization for Query 3
dates = [row[0] for row in results]
avg_bids = [row[1] for row in results]

plt.figure(figsize=(10, 6))
plt.plot(dates, avg_bids, marker='o', color='coral')
plt.xlabel('Date')
plt.ylabel('Average Bid ($)')
plt.title('Daily Average Bid Amount for the Past Week')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Close the connection
conn.close()
