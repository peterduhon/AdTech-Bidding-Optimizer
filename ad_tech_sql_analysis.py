import sqlite3
import random
from datetime import datetime, timedelta

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

# Close the connection
conn.close()
