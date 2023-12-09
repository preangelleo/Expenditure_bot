# Expenditure_bot
A bot that automatically records my purchase receipts into a MySQL database with AI assistance.

# Step 1:
git clone https://github.com/preangelleo/Expenditure_bot.git

# Step 2:
cd Expenditure_bot

# Step 3:
conda create -n expenditure_ai python=3.9

# Step 4:
conda activate expenditure_ai

# Step 5:
pip3 install -r requirements.txt

About the auto-trading strategy:

The strategy for identifying today's hot coins on Binance unfolds through a meticulously crafted multi-step process:

1. **Unique Coin List Creation**: The process begins by querying a database table named `binance_ticker_top_30`. This table provides a distinct list of coins that have been traded in the last 30 days. In instances where this table is non-existent or empty, the fallback is an empty list.

2. **Data Acquisition and Initial Filtering**: The next step involves fetching the latest ticker data from Binance's API. This data is then filtered to focus on symbols that end with 'USDT'. Additional filters are applied to select coins with a positive price change percentage and a trading volume that surpasses a predefined threshold. The selection is further refined to include coins whose last price falls within a specific range.

3. **Sorting and Trimming the List**: Following the initial filtering, the data is sorted based on quote volume. The top 30 entries are then selected for further consideration. Any coins with 'USD' in their names or those included in a predetermined ignore list are excluded at this stage.

4. **Comparison with Previously Traded Coins**: The selected coins are compared against the unique coin list derived from the `binance_ticker_top_30` table. Coins that are already on this list are removed from consideration.

5. **Enhancement with Market Cap Data**: Each coin on the list is then enriched with additional data such as market cap, fully diluted market cap, and a specific ratio. This data is sourced from another function. Coins for which this additional information is not available are omitted.

6. **Final Selection Based on Market Cap**: A final filter is applied to retain only those coins with a market cap between 100 million and 10 billion USD.

7. **Database Update and Retrieval**: The refined list of coins is used to update the `binance_ticker_top_30` table with an incremented `update_id`. The list is then retrieved back from the table, now updated with the latest data.

8. **Output Presentation**: The culmination of this process is the generation of a list termed 'today's hot coins', which is presented in a formatted string.

