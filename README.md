# Expenditure_bot
An automated trading bot that can also record receipt details into a MySQL database with AI assistance.

# Preparation:
Ensure Python3 and NPM are installed on your system.
If not, please consult ChatGPT for installation instructions.

Make sure deposit 100,000 USDT into your Binance account. Or any amount of initial fund you prefer.

Reference to my [ChatGPT Conversation](https://chat.openai.com/share/5640285f-4e84-4922-92c6-ed48094c3e74)

# Step 1: Setting Up the Environment
1. Navigate to the root directory:
   ```bash
   cd /root
   ```
2. Clone the Expenditure_bot repository:
   ```bash
   git clone https://github.com/preangelleo/Expenditure_bot.git
   ```
3. Enter the Expenditure_bot directory:
   ```bash
   cd Expenditure_bot
   ```
4. Create a new Conda environment named 'expenditure_ai' with Python 3.9:
   ```bash
   conda create -n expenditure_ai python=3.9
   ```
5. Activate the newly created environment:
   ```bash
   conda activate expenditure_ai
   ```
6. Install required Python packages:
   ```bash
   pip3 install -r requirements.txt
   ```

# Step 2: Database Creation
Install and set up your MySQL database on your Ubuntu server.
Or [Amazon AWS Lightsail](https://lightsail.aws.amazon.com/ls/webapp/home/databases)

How to install or create database? Reference to my [ChatGPT Conversation](https://chat.openai.com/share/2dcc78a6-34b1-4b6b-938e-9d630cf57a86)

# Step 3: Configuration
1. Copy the .env.template file to create a new .env file:
   ```bash
   cp .env.template .env
   ```
2. Open the .env file with nano for editing:
   ```bash
   nano .env
   ```
   - Enter your credentials in the .env file. Make sure the Initial fund amount is less or equal to the USDT balance of your Binance.
   - Alternatively, copy the content of .env.template to a text editor, complete your personal credentials, and then paste it back into the .env file on your server.

# Step 4: Database and Table Creation
1. In the Expenditure_bot folder, run the script to create the database and tables:
   ```bash
   python3 Database_create.py
   ```
2. Wait for the confirmation message: "All tables created successfully!"

# Step 5: Launch the Bot
Start the bot using the following command:
   ```bash
   python3 Telegram_bot.py
   ```

# Step 6: Ensure Continuous Bot Operation
1. Use NPM to keep the bot running:
   ```bash
   pm2 start Telegram_bot.py --name ep --interpreter python3
   ```
2. To restart the bot, use:
   ```bash
   pm2 start ep
   ```

# Step 7: Setting Up Crontab Automation
1. Copy the content from `crontab_template.txt`.
2. On your Ubuntu Server Terminal, open the crontab editor:
   ```bash
   crontab -e
   ```
3. Paste the copied content into the editor.
4. To save and exit, press `Ctrl + X`, then press `Y` and `Enter` to confirm the crontab jobs.

Now, everything is set up and ready to go!

---

![Initial Fund](net_profit_daily_record/Initial_fund.png)

![Telegram Bot Menu](net_profit_daily_record/Telegram_bot_menu.png)
---

# About the auto-trading strategy:

The strategy for identifying today's hot coins on Binance unfolds through a meticulously crafted multi-step process:

1. **Unique Coin List Creation**: The process begins by querying a database table named `binance_ticker_top_30`. This table provides a distinct list of coins that have been traded in the last 30 days. In instances where this table is non-existent or empty, the fallback is an empty list.

2. **Data Acquisition and Initial Filtering**: The next step involves fetching the latest ticker data from Binance's API. This data is then filtered to focus on symbols that end with 'USDT'. Additional filters are applied to select coins with a positive price change percentage and a trading volume that surpasses a predefined threshold. The selection is further refined to include coins whose last price falls within a specific range.

3. **Sorting and Trimming the List**: Following the initial filtering, the data is sorted based on quote volume. The top 30 entries are then selected for further consideration. Any coins with 'USD' in their names or those included in a predetermined ignore list are excluded at this stage.

4. **Comparison with Previously Traded Coins**: The selected coins are compared against the unique coin list derived from the `binance_ticker_top_30` table. Coins that are already on this list are removed from consideration.

5. **Enhancement with Market Cap Data**: Each coin on the list is then enriched with additional data such as market cap, fully diluted market cap, and a specific ratio. This data is sourced from another function. Coins for which this additional information is not available are omitted.

6. **Final Selection Based on Market Cap**: A final filter is applied to retain only those coins with a market cap between 100 million and 10 billion USD.

7. **Database Update and Retrieval**: The refined list of coins is used to update the `binance_ticker_top_30` table with an incremented `update_id`. The list is then retrieved back from the table, now updated with the latest data.

8. **Output Presentation**: The culmination of this process is the generation of a list termed 'today's hot coins', which is presented in a formatted string.

