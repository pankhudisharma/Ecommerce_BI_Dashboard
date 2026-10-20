import pandas as pd
                            #to activate the venv  .\.venv\Scripts\Activate.ps1
# Load the dataset
df = pd.read_excel("data/raw/sample_-_superstore.xls")

# -----------------------------------
# BASIC DATASET INFORMATION
# -----------------------------------

print("Dataset shape:")
print(df.shape)

print("\nDataset information:")
print(df.info())

# -----------------------------------
# MISSING VALUES
# -----------------------------------

print("\nMissing values:")
print(df.isnull().sum())

# -----------------------------------
# UNIQUE COUNTS
# -----------------------------------

print("\nUnique Orders:")
print(df["Order ID"].nunique())

print("\nUnique Customers:")
print(df["Customer ID"].nunique())

print("\nUnique Products:")
print(df["Product ID"].nunique())

print("\nUnique Categories:")
print(df["Category"].nunique())    #no. of unique categories

print("\nCategories:")
print(df["Category"].unique())

# -----------------------------------
# DATE RANGE
# -----------------------------------

print("\nOrder Date range:")
print("Earliest:", df["Order Date"].min())
print("Latest:", df["Order Date"].max())

print("\nShip Modes:")
print(df["Ship Mode"].unique())

print("\nSegments:")
print(df["Segment"].unique())

print("\nRegions:")
print(df["Region"].unique())

print("\nSub-Categories:")
print(df["Sub-Category"].unique())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nDiscount range:")
print(df["Discount"].min(), "to", df["Discount"].max())

print("\nQuantity range:")
print(df["Quantity"].min(), "to", df["Quantity"].max())

print("\nSales range:")
print(df["Sales"].min(), "to", df["Sales"].max())

print("\nProfit range:")
print(df["Profit"].min(), "to", df["Profit"].max())

print("\nInvalid date order:")
print((df["Ship Date"] < df["Order Date"]).sum())

print("\nDuplicate Row IDs:")
print(df["Row ID"].duplicated().sum())

print("\nDuplicate Order + Product combinations:")
print(df.duplicated(subset=["Order ID", "Product ID"]).sum())

print("\nDuplicate Order + Product records:")

duplicate_order_products = df[
    df.duplicated(subset=["Order ID", "Product ID"], keep=False)
]

print(
    duplicate_order_products[
        [
            "Row ID",
            "Order ID",
            "Product ID",
            "Product Name",
            "Quantity",
            "Sales",
            "Discount",
            "Profit"
        ]
    ].sort_values(["Order ID", "Product ID"]).to_string(index=False) #arrange in order
)
print("\nSuspicious duplicate transaction:")

suspicious = df[
    (df["Order ID"] == "CA-2023-153623") &         #we got one suspicious transaction
    (df["Product ID"] == "FUR-FU-10002501")            #checking both conditions Order ID must be this AND Product ID must be this.
]

print(
    suspicious[
        [
            "Row ID",
            "Order ID",
            "Order Date",
            "Ship Date",
            "Customer ID",
            "Customer Name",
            "Product ID",
            "Product Name",
            "Quantity",
            "Sales",
            "Discount",
            "Profit"
        ]
    ].to_string(index=False) #it just makes the printed output look cleaner or shows the entire table
)

print("\nCleaning duplicate transactions...")

df_clean = df.drop_duplicates(
    subset=[
        "Order ID",
        "Order Date",
        "Ship Date",
        "Customer ID",
        "Product ID",
        "Quantity",
        "Sales",
        "Discount",
        "Profit"
    ]
).copy() #Make a separate DataFrame called df_clean.

print("Original rows:", len(df))
print("Cleaned rows:", len(df_clean))
print("Rows removed:", len(df) - len(df_clean)) #2

print("\nCategorical value counts:")

categorical_columns = [ #These are the columns whose categories I want to count.
    "Ship Mode",
    "Segment",
    "Country/Region",
    "Region",
    "Category",
    "Sub-Category"
]

for column in categorical_columns:
    print(f"\n{column}:")
    print(df_clean[column].value_counts()) #Tell me how many times each category appears.for ex-Office Supplies    6128
print("\nNumerical sanity checks:")

print("Negative sales:", (df_clean["Sales"] < 0).sum()) #How many transactions have negative sales?
print("Zero or negative quantity:", (df_clean["Quantity"] <= 0).sum())
print("Invalid discount:", ((df_clean["Discount"] < 0) | (df_clean["Discount"] > 1)).sum()) #discount is stored like 0.8 = 80%

print("\nPotential Sales outliers:")

Q1 = df_clean["Sales"].quantile(0.25)
Q3 = df_clean["Sales"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

sales_outliers = df_clean[
    (df_clean["Sales"] < lower_bound) |
    (df_clean["Sales"] > upper_bound)
]

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)
print("Potential sales outliers:", len(sales_outliers))

# -----------------------------------
# BUSINESS KPIs
# -----------------------------------

print("\n========== BUSINESS KPIs ==========")

# Total Revenue
total_revenue = df_clean["Sales"].sum()

# Total Orders
total_orders = df_clean["Order ID"].nunique()

# Unique Customers
unique_customers = df_clean["Customer ID"].nunique()

# Average Order Value
average_order_value = total_revenue / total_orders

# Total Profit
total_profit = df_clean["Profit"].sum()

# Profit Margin
profit_margin = (total_profit / total_revenue) * 100

print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Unique Customers:", unique_customers)
print("Average Order Value:", average_order_value)
print("Total Profit:", total_profit)
print("Profit Margin:", profit_margin, "%")

# -----------------------------------
# SALES ANALYSIS
# -----------------------------------

print("\n========== SALES ANALYSIS ==========")

# Make sure Order Date is a datetime
df_clean["Order Date"] = pd.to_datetime(df_clean["Order Date"])

# Create Year and Month columns
df_clean["Year"] = df_clean["Order Date"].dt.year
df_clean["Month"] = df_clean["Order Date"].dt.month

yearly_sales = df_clean.groupby("Year")["Sales"].sum()

print("\nYearly Sales:")
print(yearly_sales)

monthly_sales = (
    df_clean
    .groupby(df_clean["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

print("\nMonthly Sales:")
print(monthly_sales)

# Month-over-Month Growth
monthly_growth = monthly_sales.pct_change() * 100

print("\nMonth-over-Month Sales Growth:")
print(monthly_growth)

# -----------------------------------
# QUARTERLY SALES
# -----------------------------------

quarterly_sales = (
    df_clean
    .groupby(df_clean["Order Date"].dt.to_period("Q"))["Sales"]
    .sum()
)

print("\nQuarterly Sales:")
print(quarterly_sales)

# -----------------------------------
# QUARTERLY SALES COMPARISON
# -----------------------------------

quarterly_comparison = quarterly_sales.copy()

quarterly_comparison.index = quarterly_comparison.index.astype(str)

quarterly_comparison = quarterly_comparison.reset_index()

quarterly_comparison["Year"] = quarterly_comparison["Order Date"].str[:4]
quarterly_comparison["Quarter"] = quarterly_comparison["Order Date"].str[-2:]

quarterly_comparison = quarterly_comparison.pivot(
    index="Quarter",
    columns="Year",
    values="Sales"
)

print("\nQuarterly Sales Comparison:")
print(quarterly_comparison)

quarterly_yoy_growth = quarterly_comparison.pct_change(axis=1) * 100

print("\nQuarterly Year-over-Year Growth:")
print(quarterly_yoy_growth)

# -----------------------------------
# DAILY SALES
# -----------------------------------

daily_sales = (
    df_clean
    .groupby("Order Date")["Sales"]
    .sum()
)

print("\nDaily Sales:")
print(daily_sales)

print("\nHighest Sales Day:")
print(daily_sales.idxmax(), daily_sales.max())

print("\nLowest Sales Day:")
print(daily_sales.idxmin(), daily_sales.min())

print("\nOrders on Highest Sales Day:")

highest_sales_day = daily_sales.idxmax()

print(
    df_clean[df_clean["Order Date"] == highest_sales_day][
        [
            "Order ID",
            "Customer Name",
            "Product Name",
            "Category",
            "Quantity",
            "Sales",
            "Discount",
            "Profit"
        ]
    ].sort_values("Sales", ascending=False).to_string(index=False)
)
"""
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))

plt.plot(
    monthly_sales.index.astype(str),
    monthly_sales.values
)

plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=90)
plt.tight_layout()

plt.show()

"""
# -----------------------------------
# PRODUCT ANALYSIS
# -----------------------------------

print("\n========== PRODUCT ANALYSIS ==========")

category_sales = (
    df_clean
    .groupby("Category")["Sales"]
    .sum()
)

print("\nSales by Category:")
print(category_sales)         

category_profit = (
    df_clean
    .groupby("Category")["Profit"]
    .sum()
)

print("\nProfit by Category:")
print(category_profit)

# -----------------------------------
# SUB-CATEGORY ANALYSIS
# -----------------------------------

sub_category_sales = (
    df_clean
    .groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Sub-Category:")
print(sub_category_sales)


sub_category_profit = (
    df_clean
    .groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\nProfit by Sub-Category:")
print(sub_category_profit)

# -----------------------------------
# PRODUCT-LEVEL ANALYSIS
# -----------------------------------

product_sales = (
    df_clean
    .groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop Products by Sales:")
print(product_sales.head(10))


product_profit = (
    df_clean
    .groupby("Product Name")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop Products by Profit:")
print(product_profit.head(10))

# -----------------------------------
# PRODUCT SALES vs PROFIT
# -----------------------------------

product_performance = pd.concat(
    [product_sales, product_profit],
    axis=1
)

product_performance.columns = ["Sales", "Profit"]

print("\nProduct Sales vs Profit:")
print(product_performance)

# -----------------------------------
# HIGH SALES BUT LOW PROFIT PRODUCTS
# -----------------------------------

sales_median = product_performance["Sales"].median()

high_sales_low_profit = product_performance[
    (product_performance["Sales"] > sales_median) &
    (product_performance["Profit"] <= 0)
].sort_values("Sales", ascending=False)

print("\nHigh Sales but Low/Negative Profit Products:")
print(high_sales_low_profit)

# -----------------------------------
# LOW SALES BUT HIGH PROFIT PRODUCTS
# -----------------------------------

profit_median = product_performance["Profit"].median()

low_sales_high_profit = product_performance[
    (product_performance["Sales"] <= sales_median) &
    (product_performance["Profit"] > profit_median)
].sort_values("Profit", ascending=False)

print("\nLow Sales but High Profit Products:")
print(low_sales_high_profit)

# -----------------------------------
# PRODUCT PROFIT MARGIN
# -----------------------------------

product_performance["Profit Margin"] = (
    product_performance["Profit"] /
    product_performance["Sales"]
) * 100

print("\nProduct Profit Margin:")
print(
    product_performance
    .sort_values("Profit Margin", ascending=False)
)

# -----------------------------------
# PRODUCT PROFIT MARGIN - SIGNIFICANT SALES
# -----------------------------------

significant_products = product_performance[
    product_performance["Sales"] >= 500
]

print("\nProducts with Sales >= $500:")
print(
    significant_products
    .sort_values("Profit Margin", ascending=False)
)

# -----------------------------------
# PRODUCT QUANTITY ANALYSIS
# -----------------------------------

product_quantity = (
    df_clean
    .groupby("Product Name")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop Products by Quantity Sold:")
print(product_quantity.head(10))

# -----------------------------------
# PRODUCT PERFORMANCE: QUANTITY + SALES + PROFIT
# -----------------------------------

product_performance = pd.concat(
    [
        product_sales,
        product_quantity,
        product_profit
    ],
    axis=1
)

product_performance.columns = [
    "Sales",
    "Quantity",
    "Profit"
]

print("\nComplete Product Performance:")
print(product_performance)

# -----------------------------------
# SALES PER UNIT
# -----------------------------------

product_performance["Sales per Unit"] = (
    product_performance["Sales"] /
    product_performance["Quantity"]
)

print("\nProduct Sales per Unit:")
print(
    product_performance
    .sort_values("Sales per Unit", ascending=False)
)

# -----------------------------------
# PROFIT PER UNIT
# -----------------------------------

product_performance["Profit per Unit"] = (
    product_performance["Profit"] /
    product_performance["Quantity"]
)

print("\nProduct Profit per Unit:")
print(
    product_performance
    .sort_values("Profit per Unit", ascending=False)
)


# -----------------------------------
# CUSTOMER ORDER FREQUENCY
# -----------------------------------

customer_orders = (
    df_clean
    .groupby("Customer ID")["Order ID"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nOrders per Customer:")
print(customer_orders.head(20))

# -----------------------------------
# REPEAT VS ONE-TIME CUSTOMERS
# -----------------------------------

one_time_customers = (customer_orders == 1).sum()
repeat_customers = (customer_orders > 1).sum()

print("\nOne-Time Customers:", one_time_customers)
print("Repeat Customers:", repeat_customers)

# Percentages
total_customers = len(customer_orders)

one_time_percentage = (one_time_customers / total_customers) * 100
repeat_percentage = (repeat_customers / total_customers) * 100

print("One-Time Customer %:", one_time_percentage)
print("Repeat Customer %:", repeat_percentage)

# -----------------------------------
# CUSTOMER SPENDING
# -----------------------------------

customer_sales = (
    df_clean
    .groupby("Customer ID")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop Customers by Total Sales:")
print(customer_sales.head(20))

# -----------------------------------
# AVERAGE SPENDING PER CUSTOMER
# -----------------------------------

average_customer_spending = customer_sales.mean()

print("\nAverage Sales per Customer:", average_customer_spending)

# -----------------------------------
# CUSTOMER PROFIT
# -----------------------------------

customer_profit = (
    df_clean
    .groupby("Customer ID")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop Customers by Profit:")
print(customer_profit.head(20))

# -----------------------------------
# CUSTOMER PERFORMANCE TABLE
# -----------------------------------

customer_performance = pd.concat(
    [customer_orders, customer_sales, customer_profit],
    axis=1
)

customer_performance.columns = [
    "Orders",
    "Sales",
    "Profit"
]

print("\nCustomer Performance:")
print(customer_performance.head(20))

# -----------------------------------
# CUSTOMER PROFIT MARGIN
# -----------------------------------

customer_performance["Profit Margin"] = (
    customer_performance["Profit"] /
    customer_performance["Sales"]
) * 100

print("\nTop Customers by Profit Margin:")
print(
    customer_performance
    .sort_values("Profit Margin", ascending=False)
    .head(20)
)

# -----------------------------------
# RFM SEGMENTATION
# STEP 1: RECENCY
# -----------------------------------

customer_recency = (
    df_clean
    .groupby("Customer ID")["Order Date"]
    .max()
)

print("\nLast Purchase Date:")
print(customer_recency.head(20))

# Step 2: Calculate Recency

reference_date = df_clean["Order Date"].max()

customer_recency = (
    reference_date - customer_recency
).dt.days

print("\nReference Date:", reference_date)
print("\nDays Since Last Purchase:")
print(customer_recency.head(20))

# Step 3: Combine Recency, Frequency, and Monetary values

rfm = pd.concat(
    [
        customer_recency.rename("Recency"),
        customer_orders.rename("Frequency"),
        customer_sales.rename("Monetary")
    ],
    axis=1
)

print("\nRFM Table:")
print(rfm.head(20))

# --------------------------------
# GEOGRAPHIC PERFORMANCE ANALYSIS
# --------------------------------

# Sales by Region
region_sales = (
    df_clean.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Region:")
print(region_sales)

# Profit by Region
region_profit = (
    df_clean.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\nProfit by Region:")
print(region_profit)

# Orders by Region
region_orders = (
    df_clean.groupby("Region")["Order ID"]
    .nunique()
    .sort_values(ascending=False)
)

print("\nOrders by Region:")
print(region_orders)

# Sales by State
state_sales = (
    df_clean.groupby("State/Province")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 States by Sales:")
print(state_sales.head(10))

# Profit by State
state_profit = (
    df_clean.groupby("State/Province")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 States by Profit:")
print(state_profit.head(10))

# Lowest-profit states
print("\nBottom 10 States by Profit:")
print(state_profit.tail(10))

# --------------------------------
# CITY-LEVEL ANALYSIS
# --------------------------------

# Sales by City
city_sales = (
    df_clean.groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Cities by Sales:")
print(city_sales.head(10))


# Profit by City
city_profit = (
    df_clean.groupby("City")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Cities by Profit:")
print(city_profit.head(10))


# Lowest-profit cities
print("\nBottom 10 Cities by Profit:")
print(city_profit.tail(10))

# --------------------------------
# DISCOUNT AND PROFITABILITY ANALYSIS
# --------------------------------

# Average sales and profit at each discount level
discount_analysis = (
    df_clean.groupby("Discount")
    .agg(
        Transactions=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Average_Sales=("Sales", "mean"),
        Total_Profit=("Profit", "sum"),
        Average_Profit=("Profit", "mean")
    )
    .sort_index()
)

print("\nDiscount Analysis:")
print(discount_analysis)

# Calculate profit margin for each discount level

discount_analysis["Profit_Margin"] = (
    discount_analysis["Total_Profit"]
    / discount_analysis["Total_Sales"]
) * 100

print("\nProfit Margin by Discount:")
print(
    discount_analysis[
        ["Total_Sales", "Total_Profit", "Profit_Margin"]
    ].round(2)
)


# --------------------------------
# CATEGORY-WISE DISCOUNT ANALYSIS
# --------------------------------

category_discount_analysis = (
    df_clean.groupby(["Category", "Discount"])
    .agg(
        Transactions=("Order ID", "count"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    )
    .reset_index()
)

category_discount_analysis["Profit_Margin"] = (
    category_discount_analysis["Total_Profit"]
    / category_discount_analysis["Total_Sales"]
) * 100

print("\nCategory-wise Discount Analysis:")

print(
    category_discount_analysis.round(2).to_string(index=False)
)
