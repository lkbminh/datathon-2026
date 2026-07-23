# EDA Report (dataset excluding sample_submission)

## Dataset Inventory
- **customers.csv**: 121,930 rows x 7 columns
- **geography.csv**: 39,948 rows x 4 columns
- **inventory.csv**: 60,247 rows x 17 columns
- **order_items.csv**: 714,669 rows x 7 columns
- **orders.csv**: 646,945 rows x 8 columns
- **payments.csv**: 646,945 rows x 4 columns
- **products.csv**: 2,412 rows x 8 columns
- **promotions.csv**: 50 rows x 10 columns
- **returns.csv**: 39,939 rows x 7 columns
- **reviews.csv**: 113,551 rows x 7 columns
- **sales.csv**: 3,833 rows x 3 columns
- **shipments.csv**: 566,067 rows x 4 columns
- **web_traffic.csv**: 3,652 rows x 7 columns

## Per-table Profiling

### customers.csv
- Shape: 121,930 x 7
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - customer_id: 121,930 unique (100.00% of rows)
- Missing values: none
- Date coverage:
  - signup_date: 100.00% parseable, range 2012-01-17 to 2022-12-31
- Numeric columns (key stats, top 8):
  - customer_id: mean=78736.899, median=78784.500, min=1.000, max=157563.000
  - zip: mean=50990.166, median=49835.000, min=1001.000, max=99950.000
- Categorical distributions (top values):
  - gender: Female: 59,640; Male: 57,457; Non-binary: 4,833
  - age_group: 25-34: 36,342; 35-44: 31,920; 45-54: 23,172
  - acquisition_channel: organic_search: 36,450; social_media: 24,448; paid_search: 24,285

### geography.csv
- Shape: 39,948 x 4
- Full-row duplicates: 0 (0.00%)
- Missing values: none
- Numeric columns (key stats, top 8):
  - zip: mean=50895.085, median=49876.500, min=1.000, max=99950.000
- Categorical distributions (top values):
  - region: East: 18,929; Central: 14,512; West: 6,507

### inventory.csv
- Shape: 60,247 x 17
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - product_id: 1,624 unique (2.70% of rows)
- Missing values: none
- Date coverage:
  - snapshot_date: 100.00% parseable, range 2012-07-31 to 2022-12-31
- Numeric columns (key stats, top 8):
  - product_id: mean=1311.408, median=1223.000, min=1.000, max=2412.000
  - stock_on_hand: mean=189.298, median=62.000, min=3.000, max=2673.000
  - units_received: mean=18.047, median=6.000, min=1.000, max=817.000
  - units_sold: mean=15.418, median=6.000, min=1.000, max=670.000
  - stockout_days: mean=1.161, median=1.000, min=0.000, max=28.000
  - days_of_supply: mean=912.678, median=240.000, min=5.200, max=68100.000
  - fill_rate: mean=0.961, median=0.967, min=0.067, max=1.000
  - stockout_flag: mean=0.673, median=1.000, min=0.000, max=1.000
- Categorical distributions (top values):
  - category: Streetwear: 31,020; Outdoor: 21,050; GenZ: 4,674
  - segment: Activewear: 18,290; Everyday: 13,598; Performance: 7,673

### order_items.csv
- Shape: 714,669 x 7
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - order_id: 646,945 unique (90.52% of rows)
  - product_id: 1,598 unique (0.22% of rows)
  - promo_id: 50 unique (0.01% of rows)
- Missing values (top 8):
  - promo_id_2: 714,463 (99.97%)
  - promo_id: 438,353 (61.34%)
- Numeric columns (key stats, top 8):
  - order_id: mean=411615.077, median=409306.000, min=1.000, max=834397.000
  - product_id: mean=1234.931, median=990.000, min=1.000, max=2412.000
  - quantity: mean=4.496, median=4.000, min=1.000, max=8.000
  - unit_price: mean=5114.690, median=4257.770, min=392.570, max=43056.000
  - discount_amount: mean=1048.887, median=0.000, min=0.000, max=35235.470
- Categorical distributions (top values):
  - promo_id_2: nan: 714,463; PROMO-0015: 132; PROMO-0025: 74

### orders.csv
- Shape: 646,945 x 8
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - order_id: 646,945 unique (100.00% of rows)
  - customer_id: 90,246 unique (13.95% of rows)
- Missing values: none
- Date coverage:
  - order_date: 100.00% parseable, range 2012-07-04 to 2022-12-31
- Numeric columns (key stats, top 8):
  - order_id: mean=417189.470, median=417211.000, min=1.000, max=834397.000
  - customer_id: mean=84906.204, median=87279.000, min=1.000, max=157563.000
  - zip: mean=55410.740, median=54129.000, min=1001.000, max=99950.000
- Categorical distributions (top values):
  - order_status: delivered: 516,716; cancelled: 59,462; returned: 36,142
  - payment_method: credit_card: 356,352; paypal: 97,018; cod: 96,681
  - device_type: mobile: 291,482; desktop: 258,855; tablet: 96,608
  - order_source: organic_search: 181,495; paid_search: 141,652; social_media: 129,710

### payments.csv
- Shape: 646,945 x 4
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - order_id: 646,945 unique (100.00% of rows)
- Missing values: none
- Numeric columns (key stats, top 8):
  - order_id: mean=417189.470, median=417211.000, min=1.000, max=834397.000
  - payment_value: mean=24238.334, median=17229.440, min=389.740, max=331570.400
  - installments: mean=3.448, median=3.000, min=1.000, max=12.000
- Categorical distributions (top values):
  - payment_method: credit_card: 356,352; paypal: 97,018; cod: 96,681

### products.csv
- Shape: 2,412 x 8
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - product_id: 2,412 unique (100.00% of rows)
- Missing values: none
- Numeric columns (key stats, top 8):
  - product_id: mean=1206.500, median=1206.500, min=1.000, max=2412.000
  - price: mean=4928.216, median=4399.605, min=9.057, max=40950.000
  - cogs: mean=3868.347, median=3184.934, min=5.184, max=38902.500
- Categorical distributions (top values):
  - category: Streetwear: 1,320; Outdoor: 743; Casual: 201
  - segment: Activewear: 598; Everyday: 405; Performance: 347
  - size: S: 603; M: 603; L: 603
  - color: orange: 242; black: 242; silver: 241

### promotions.csv
- Shape: 50 x 10
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - promo_id: 50 unique (100.00% of rows)
- Missing values (top 8):
  - applicable_category: 40 (80.00%)
- Date coverage:
  - start_date: 100.00% parseable, range 2013-01-31 to 2022-11-18
  - end_date: 100.00% parseable, range 2013-03-01 to 2022-12-31
- Numeric columns (key stats, top 8):
  - discount_value: mean=18.500, median=16.500, min=10.000, max=50.000
  - stackable_flag: mean=0.240, median=0.000, min=0.000, max=1.000
  - min_order_value: mean=46000.000, median=0.000, min=0.000, max=200000.000
- Categorical distributions (top values):
  - promo_type: percentage: 45; fixed: 5
  - applicable_category: nan: 40; Streetwear: 5; Outdoor: 5
  - promo_channel: all_channels: 19; online: 13; email: 7

### returns.csv
- Shape: 39,939 x 7
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - return_id: 39,939 unique (100.00% of rows)
  - order_id: 36,062 unique (90.29% of rows)
  - product_id: 1,286 unique (3.22% of rows)
- Missing values: none
- Date coverage:
  - return_date: 100.00% parseable, range 2012-07-11 to 2022-12-31
- Numeric columns (key stats, top 8):
  - order_id: mean=409061.984, median=404254.000, min=2.000, max=833351.000
  - product_id: mean=1244.233, median=992.000, min=3.000, max=2412.000
  - return_quantity: mean=2.744, median=2.000, min=1.000, max=8.000
  - refund_amount: mean=12784.459, median=7888.880, min=458.810, max=160937.940
- Categorical distributions (top values):
  - return_reason: wrong_size: 13,967; defective: 8,020; not_as_described: 7,035

### reviews.csv
- Shape: 113,551 x 7
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - review_id: 113,551 unique (100.00% of rows)
  - order_id: 111,369 unique (98.08% of rows)
  - product_id: 1,412 unique (1.24% of rows)
  - customer_id: 48,676 unique (42.87% of rows)
- Missing values: none
- Date coverage:
  - review_date: 100.00% parseable, range 2012-07-10 to 2022-12-31
- Numeric columns (key stats, top 8):
  - order_id: mean=408999.520, median=406841.000, min=1.000, max=833296.000
  - product_id: mean=1232.019, median=981.000, min=3.000, max=2412.000
  - customer_id: mean=85694.343, median=89755.000, min=2.000, max=157563.000
  - rating: mean=3.936, median=4.000, min=1.000, max=5.000
- Categorical distributions (top values):
  - review_title: Very satisfied: 11,450; Highly recommend: 11,407; Great quality: 11,218

### sales.csv
- Shape: 3,833 x 3
- Full-row duplicates: 0 (0.00%)
- Missing values: none
- Date coverage:
  - Date: 100.00% parseable, range 2012-07-04 to 2022-12-31
- Numeric columns (key stats, top 8):
  - Revenue: mean=4286584.030, median=3647303.900, min=279813.940, max=20905271.350
  - COGS: mean=3695134.495, median=3161112.990, min=236576.310, max=16535857.670

### shipments.csv
- Shape: 566,067 x 4
- Full-row duplicates: 0 (0.00%)
- ID cardinality:
  - order_id: 566,067 unique (100.00% of rows)
- Missing values: none
- Date coverage:
  - ship_date: 100.00% parseable, range 2012-07-04 to 2022-12-29
  - delivery_date: 100.00% parseable, range 2012-07-06 to 2022-12-31
- Numeric columns (key stats, top 8):
  - order_id: mean=415816.870, median=415866.000, min=1.000, max=834325.000
  - shipping_fee: mean=4.963, median=1.730, min=0.000, max=32.000

### web_traffic.csv
- Shape: 3,652 x 7
- Full-row duplicates: 0 (0.00%)
- Missing values: none
- Date coverage:
  - date: 100.00% parseable, range 2013-01-01 to 2022-12-31
- Numeric columns (key stats, top 8):
  - sessions: mean=25041.768, median=23633.500, min=7973.000, max=50947.000
  - unique_visitors: mean=19031.404, median=17924.000, min=6136.000, max=40430.000
  - page_views: mean=108615.225, median=101010.500, min=30451.000, max=275560.000
  - bounce_rate: mean=0.004, median=0.004, min=0.003, max=0.006
  - avg_session_duration_sec: mean=210.283, median=209.200, min=100.100, max=319.900
- Categorical distributions (top values):
  - traffic_source: organic_search: 1,090; paid_search: 784; social_media: 632

## Cross-table Integrity Checks
- order_items.order_id matching orders.order_id: 714,669/714,669 (100.00%)
- payments.order_id matching orders.order_id: 646,945/646,945 (100.00%)
- shipments.order_id matching orders.order_id: 566,067/566,067 (100.00%)
- returns.order_id matching orders.order_id: 39,939/39,939 (100.00%)
- reviews.order_id matching orders.order_id: 113,551/113,551 (100.00%)
- order_items.product_id matching products.product_id: 714,669/714,669 (100.00%)
- orders.customer_id matching customers.customer_id: 646,945/646,945 (100.00%)
- orders.zip found in geography.zip: 646,945/646,945 (100.00%)
- shipments with delivery_date >= ship_date: 566,067/566,067 (100.00%)
- reviews rating outside [1,5]: 0
- returns with negative refund_amount: 0

## Key Observations
- payments has same row count as orders, suggesting near 1:1 payment records per order.
- shipments rows are 0.87x orders; likely many orders have not yet shipped or shipment data is partial.
- returns are 5.59% of order_item rows (rough proxy return incidence).
- reviews are 17.55% of orders (engagement signal).
- web_traffic and sales are compact time-series tables and suitable for date-level modeling/attribution after harmonizing date columns.

## Business KPI Snapshot
- Order status mix (%): delivered: 79.87%; cancelled: 9.19%; returned: 5.59%; shipped: 2.13%; paid: 2.1%; created: 1.12%
- Promo usage in order_items (promo_id non-null): 38.66%
- Stacked promo usage (promo_id_2 non-null): 0.03%
- Gross item value (qty*unit_price): 16,430,476,585.53
- Discount total (order_items): 749,607,320.10
- Net item value proxy: 15,680,869,265.43
- Total payment_value: 15,680,869,265.43
- Avg payment per order: 24,238.33
- Orders with at least one return: 36,062 (5.57%)
- Total refund amount: 510,598,506.55
- Shipping lead time (days): mean=4.50, median=4.00, p90=7.00
- Rating distribution (%): 1*: 5.08%; 2*: 8.01%; 3*: 14.99%; 4*: 32.07%; 5*: 39.86%
- Orders from 2012 to 2022: 32,051 -> 36,004 (+12.33%)
- Revenue from 2012 to 2022: 741,497,748.02 -> 1,169,748,831.69 (+57.75%)
- Sessions from 2013 to 2022: 6,801,940 -> 11,063,658 (+62.65%)
