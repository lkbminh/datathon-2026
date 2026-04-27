# %%
import pandas as pd
import os
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# %%
data_path = "dataset/"
files = {}
for f in os.listdir(data_path):
    name = f.replace(".csv", "")
    files[name] = pd.read_csv(data_path + f)
    print(f"{name}: {files[name].shape} | nulls: {files[name].isnull().sum().sum()}")

# %%
files['web_traffic']

# %%
files['sales']['Date'] = pd.to_datetime(files['sales']['Date'])
files['web_traffic']['date'] = pd.to_datetime(files['web_traffic']['date'])

# %%
date_map = {
    'sales': 'Date',
    'web_traffic': 'date',
    'orders': 'order_date',
    'inventory': 'snapshot_date',
    'returns': 'return_date',
    'reviews': 'review_date',
    'shipments': 'ship_date',
    'customers': 'signup_date',
    'promotions': 'start_date'
}

daily = files['sales'].copy()
daily = daily[['Date', 'Revenue']]
daily['Date'] = pd.to_datetime(daily['Date'])

for name, date_col in date_map.items():
    if name == 'sales' or name not in files:
        continue

    df = files[name].copy()
    if date_col not in df.columns:
        continue

    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])

    # Keep numeric columns only, then aggregate by day
    num_cols = df.select_dtypes(include='number').columns.tolist()
    if not num_cols:
        continue

    agg = df.groupby(date_col)[num_cols].mean().reset_index()
    agg = agg.rename(columns={date_col: 'Date'})
    agg = agg.rename(columns={c: f"{name}__{c}" for c in num_cols})

    daily = daily.merge(agg, on='Date', how='left')

feature_cols = [c for c in daily.columns if c != 'Date']
daily[feature_cols] = daily[feature_cols].fillna(daily[feature_cols].median(numeric_only=True))
corr = daily.drop(columns=['Date']).corr(numeric_only=True)

rev_corr = corr['Revenue'].drop('Revenue').sort_values(key=lambda s: s.abs(), ascending=False)
print(rev_corr.head(15))

fig = px.imshow(
    corr,
    text_auto='.2f',
    aspect='auto',
    color_continuous_scale='RdBu_r',
    zmin=-1, zmax=1,
    title='Date-aligned Cross-file Correlation Matrix'
)
fig.update_layout(width=1100, height=900)
fig.show()

# %%

# 1. Setup
threshold = 0.75
target = 'Revenue'

# 2. Get the full absolute correlation matrix
# We need the full matrix to check against Revenue later
abs_corr = daily.drop(columns=['Date']).corr().abs()

# 3. Identify pairs that exceed the threshold
# We use the upper triangle to avoid checking (A,B) and then (B,A)
upper_tri = abs_corr.where(np.triu(np.ones(abs_corr.shape), k=1).astype(bool))

to_drop = set()

for column in upper_tri.columns:
    # Find which rows in this column are above the threshold
    correlated_with_col = upper_tri.index[upper_tri[column] > threshold].tolist()
    
    for row_feature in correlated_with_col:
        # Skip if either is the target (we never want to drop Revenue)
        if column == target or row_feature == target:
            continue
            
        # Compare their relationship with Revenue
        corr_col_to_target = abs_corr.loc[column, target]
        corr_row_to_target = abs_corr.loc[row_feature, target]
        
        # Add the "weaker" feature to the drop set
        if corr_col_to_target < corr_row_to_target:
            to_drop.add(column)
        else:
            to_drop.add(row_feature)

# 4. Final cleaning
final_daily = daily.drop(columns=list(to_drop))

print(f"Smart Drop identified {len(to_drop)} redundant features.")
print(f"Features removed: {list(to_drop)}")

# %%
corr_final = final_daily.corr(numeric_only=True)

# %%
corr_final

# %%
fig = px.imshow(
    corr_final,
    text_auto='.2f',
    aspect='auto',
    color_continuous_scale='RdBu_r',
    zmin=-1, zmax=1,
    title='Date-aligned Cross-file Correlation Matrix'
)
fig.update_layout(width=1100, height=900)
fig.show()

# %%
important_cols=corr_final['Revenue'].sort_values(ascending=False)
important_cols

# %%
selected_features = final_daily[['web_traffic__sessions', 'inventory__units_received']]

# %%
files['promotions']['start_date'] = pd.to_datetime(files['promotions']['start_date'])
files['promotions']['end_date'] = pd.to_datetime(files['promotions']['end_date'])

# %%
inv = files['inventory'].groupby('snapshot_date')['units_received'].max().reset_index()
inv['snapshot_date'] = pd.to_datetime(inv['snapshot_date'])
inv

# %%
fig = make_subplots()
fig.add_trace(go.Scatter(x=files['sales']['Date'], y=files['sales']['Revenue'], mode='lines', name='Revenue'))
fig.add_trace(go.Scatter(x=files['web_traffic']['date'], y=files['web_traffic']['sessions'], mode='lines', opacity=0.6, name='Web Traffic Sessions', yaxis='y2', marker_color='red'))
fig.add_trace(go.Scatter(x=inv['snapshot_date'], y=inv['units_received'], opacity=0.6, name='Items in Inventory', yaxis='y4', marker_color='orange'))

duration_ms = (files['promotions']['end_date'] - files['promotions']['start_date']).dt.total_seconds() * 1000

# 2. Calculate the 'center' of the bar so it sits correctly on the timeline
start_dates = pd.to_datetime(files['promotions']['start_date'])
center_dates = start_dates + (files['promotions']['end_date'] - start_dates) / 2

fig.add_trace(go.Bar(
    x=center_dates,         # Position of the bar on the timeline
    y=files['promotions']['discount_value'],
    width=duration_ms,      # Width in milliseconds
    name='Promotion',
    yaxis='y3',
    opacity=0.5,
    marker_color='rgba(255, 100, 100, 0.6)'
))

fig.update_xaxes(
    tickformat="%b %Y",  # Result: "Jan 2023"
    dtick="M1",           # Forces a tick at every 1 month interval
    tickfont=dict(size=7), 
    domain=[0, 0.9]
)

fig.update_layout(
    autosize=False,
    width=1500,
    height=500,
    margin=dict(l=50, r=50, b=100, t=100, pad=4), # Optional: adjust margins

    yaxis2=dict(
        title="Web Traffic Sessions",
        overlaying='y',
        side='right',
        showgrid=False,
        tickfont=dict(size=7)
    ),
    yaxis3=dict(
        title="Promotion",
        overlaying='y',
        side='right',
        showgrid=False,
        tickfont=dict(size=7),
        anchor="free",
        position=0.94
    ),
    yaxis4=dict(
        title="Items in Inventory",
        overlaying='y',
        side='right',
        showgrid=False,
        tickfont=dict(size=7),
        anchor="free",
        position=0.98
    )
)   

fig.show()

# %%
# Non-time-based correlation analysis (order-level)
# Target: order_revenue derived from order_items

oi = files['order_items'].copy()
orders = files['orders'].copy()
payments = files['payments'].copy()
returns = files['returns'].copy()
shipments = files['shipments'].copy()
products = files['products'].copy()

# 1) Build revenue at line level, then aggregate to order level
oi['line_revenue'] = oi['quantity'] * oi['unit_price'] - oi['discount_amount'].fillna(0)
oi['has_promo'] = ((oi['promo_id'].notna()) | (oi['promo_id_2'].notna())).astype(int)

order_core = (
    oi.groupby('order_id', as_index=False)
      .agg(
          order_revenue=('line_revenue', 'sum'),
          total_quantity=('quantity', 'sum'),
          avg_unit_price=('unit_price', 'mean'),
          total_discount=('discount_amount', 'sum'),
          promo_line_ratio=('has_promo', 'mean'),
          product_variety=('product_id', 'nunique')
      )
)

# 2) Add product-side economics at order level (price/cogs)
oi_prod = oi.merge(products[['product_id', 'price', 'cogs']], on='product_id', how='left')
order_prod = (
    oi_prod.groupby('order_id', as_index=False)
           .agg(
               avg_list_price=('price', 'mean'),
               avg_cogs=('cogs', 'mean')
           )
)

# 3) Add payment, returns, and shipping signals
pay_agg = payments.groupby('order_id', as_index=False).agg(
    payment_value=('payment_value', 'sum'),
    installments=('installments', 'mean')
)

ret_agg = returns.groupby('order_id', as_index=False).agg(
    refund_amount=('refund_amount', 'sum'),
    return_quantity=('return_quantity', 'sum')
)

ship_agg = shipments.groupby('order_id', as_index=False).agg(
    shipping_fee=('shipping_fee', 'sum')
)

# 4) Merge all numeric features
order_df = (
    order_core
    .merge(order_prod, on='order_id', how='left')
    .merge(pay_agg, on='order_id', how='left')
    .merge(ret_agg, on='order_id', how='left')
    .merge(ship_agg, on='order_id', how='left')
)

# Optional: customer/location numeric signals
if {'order_id', 'customer_id', 'zip'}.issubset(orders.columns):
    cust_cols = ['customer_id']
    if 'age_group' in files['customers'].columns:
        cust_cols.append('age_group')

    orders_small = orders[['order_id', 'customer_id', 'zip']].copy()
    cust_small = files['customers'][cust_cols].copy()

    order_df = order_df.merge(orders_small, on='order_id', how='left')
    order_df = order_df.merge(cust_small, on='customer_id', how='left')

    if 'age_group' in order_df.columns:
        order_df['age_group_code'] = pd.Categorical(order_df['age_group']).codes

# 5) Correlation to target
num = order_df.select_dtypes(include='number').copy()
num = num.drop(columns=['order_id'], errors='ignore')
num = num.fillna(num.median(numeric_only=True))

corr_non_time = num.corr(numeric_only=True)
rev_corr_non_time = corr_non_time['order_revenue'].drop('order_revenue').sort_values(key=lambda s: s.abs(), ascending=False)

print('Top non-time-based correlations with order_revenue:')
print(rev_corr_non_time.head(15))

# Keep for quick access
order_level_corr = rev_corr_non_time

# %%
# Predicting sales.csv Revenue (correct target)
# Build X/y at daily level with sales['Revenue'] as y

# 1) Target table
target_df = files['sales'][['Date', 'Revenue']].copy()
target_df['Date'] = pd.to_datetime(target_df['Date'], errors='coerce')

# 2) Daily feature blocks from each source
# Web traffic
wt = files['web_traffic'].copy()
wt['date'] = pd.to_datetime(wt['date'], errors='coerce')
wt_num = wt.select_dtypes(include='number').columns.tolist()
wt_daily = wt.groupby('date', as_index=False)[wt_num].mean().rename(columns={'date': 'Date'})
wt_daily = wt_daily.rename(columns={c: f"web_traffic__{c}" for c in wt_num})

# Orders (counts)
orders = files['orders'].copy()
orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
orders_daily = orders.groupby('order_date', as_index=False).agg(
    orders__count=('order_id', 'nunique')
).rename(columns={'order_date': 'Date'})

# Order items (commercial intensity)
oi = files['order_items'].copy()
oi['line_revenue_proxy'] = oi['quantity'] * oi['unit_price'] - oi['discount_amount'].fillna(0)
oi_daily = (
    oi.merge(orders[['order_id', 'order_date']], on='order_id', how='left')
      .assign(order_date=lambda d: pd.to_datetime(d['order_date'], errors='coerce'))
      .groupby('order_date', as_index=False)
      .agg(
          order_items__qty=('quantity', 'sum'),
          order_items__discount=('discount_amount', 'sum'),
          order_items__line_revenue_proxy=('line_revenue_proxy', 'sum')
      )
      .rename(columns={'order_date': 'Date'})
)

# Inventory
inv = files['inventory'].copy()
inv['snapshot_date'] = pd.to_datetime(inv['snapshot_date'], errors='coerce')
inv_num = inv.select_dtypes(include='number').columns.tolist()
inv_daily = inv.groupby('snapshot_date', as_index=False)[inv_num].mean().rename(columns={'snapshot_date': 'Date'})
inv_daily = inv_daily.rename(columns={c: f"inventory__{c}" for c in inv_num})

# Returns
ret = files['returns'].copy()
ret['return_date'] = pd.to_datetime(ret['return_date'], errors='coerce')
ret_daily = ret.groupby('return_date', as_index=False).agg(
    returns__refund_amount=('refund_amount', 'sum'),
    returns__return_qty=('return_quantity', 'sum'),
    returns__count=('return_id', 'nunique')
).rename(columns={'return_date': 'Date'})

# Promotions (active on day, not only start_date)
promo = files['promotions'].copy()
promo['start_date'] = pd.to_datetime(promo['start_date'], errors='coerce')
promo['end_date'] = pd.to_datetime(promo['end_date'], errors='coerce')

calendar = pd.DataFrame({'Date': pd.date_range(target_df['Date'].min(), target_df['Date'].max(), freq='D')})
promo_daily = calendar.copy()
promo_daily['promotions__active_count'] = 0
promo_daily['promotions__active_discount_sum'] = 0.0

for _, r in promo.dropna(subset=['start_date', 'end_date']).iterrows():
    mask = (promo_daily['Date'] >= r['start_date']) & (promo_daily['Date'] <= r['end_date'])
    promo_daily.loc[mask, 'promotions__active_count'] += 1
    promo_daily.loc[mask, 'promotions__active_discount_sum'] += float(r.get('discount_value', 0) or 0)

# 3) Merge everything to target by Date
model_df = target_df.copy()
for d in [wt_daily, orders_daily, oi_daily, inv_daily, ret_daily, promo_daily]:
    model_df = model_df.merge(d, on='Date', how='left')

# 4) Fill missing and inspect correlation to the real target
feat_cols = [c for c in model_df.columns if c not in ['Date', 'Revenue']]
model_df[feat_cols] = model_df[feat_cols].fillna(model_df[feat_cols].median(numeric_only=True))

corr_to_revenue = model_df.drop(columns=['Date']).corr(numeric_only=True)['Revenue'].drop('Revenue')
corr_to_revenue = corr_to_revenue.sort_values(key=lambda s: s.abs(), ascending=False)

print('Top predictors for sales.csv Revenue (daily):')
print(corr_to_revenue.head(15))

# Save for modeling
X = model_df[feat_cols]
y = model_df['Revenue']

# %%
# Remove multicollinearity (>0.75) among predictors, but never drop Revenue
corr_threshold = 0.75
target_col = 'Revenue'

corr_full = model_df.drop(columns=['Date']).corr(numeric_only=True)
abs_corr_full = corr_full.abs()
upper = abs_corr_full.where(np.triu(np.ones(abs_corr_full.shape), k=1).astype(bool))

to_drop_mc = set()
for col in upper.columns:
    high_rows = upper.index[upper[col] > corr_threshold].tolist()
    for row in high_rows:
        # Ignore pairs involving target; never drop based on correlation with target itself
        if col == target_col or row == target_col:
            continue

        col_vs_target = abs_corr_full.loc[col, target_col]
        row_vs_target = abs_corr_full.loc[row, target_col]

        # Drop the one less related to target Revenue
        if col_vs_target < row_vs_target:
            to_drop_mc.add(col)
        else:
            to_drop_mc.add(row)

keep_cols = [c for c in model_df.columns if c not in to_drop_mc and c != 'Date']
pruned_df = model_df[keep_cols].copy()

print(f'Dropped {len(to_drop_mc)} multicollinear features (threshold={corr_threshold}).')
print('Dropped columns:', sorted(to_drop_mc))

corr_pruned = pruned_df.corr(numeric_only=True)
revenue_rank_pruned = corr_pruned[target_col].drop(target_col).sort_values(key=lambda s: s.abs(), ascending=False)

print('\nTop predictors after multicollinearity pruning:')
print(revenue_rank_pruned.head(15))

fig = px.imshow(
    corr_pruned,
    text_auto='.2f',
    aspect='auto',
    color_continuous_scale='RdBu_r',
    zmin=-1, zmax=1,
    title='Pruned Correlation Matrix (Inter-feature |corr| <= 0.75)'
)
fig.update_layout(width=1100, height=900)
fig.show()

# Save pruned modeling set
X_pruned = pruned_df.drop(columns=[target_col])
y_pruned = pruned_df[target_col]


