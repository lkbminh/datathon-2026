# VinTelligence Datathon 2026

This repository contains the working files for a daily forecasting project built for VinTelligence Datathon 2026. The goal is to predict `Revenue` and `COGS` for the competition test period using historical sales, order, promotion, and calendar signals.

Competition details: `kaggle.com/competitions/datathon-2026-round-1/overview`

## Repository Layout

- `model.py` - end-to-end training and submission script
- `baseline.ipynb` - baseline notebook
- `eda.ipynb` - exploratory data analysis notebook
- `analysis.html` - exported analysis report
- `overview.md` - detailed dataset profiling notes
- `dataset/` - competition CSV files

## Problem Overview

The model is trained on historical data from 2012 to 2022 and produces daily forecasts for the competition test horizon. The script uses sales history, order volume, and promotion activity to build a recursive time-series forecasting pipeline.

The reported test window in the project is 1 January 2023 to 1 July 2024, covering 548 daily predictions.

## Data Files

The `dataset/` folder includes the main competition tables used by the project:

- `sales.csv`
- `orders.csv`
- `promotions.csv`
- `sample_submission.csv`
- supporting tables such as `customers.csv`, `geography.csv`, `inventory.csv`, `order_items.csv`, `payments.csv`, `products.csv`, `returns.csv`, `reviews.csv`, `shipments.csv`, and `web_traffic.csv`


## Requirements

- Python 3.8 or newer
- `numpy`
- `pandas`
- `scikit-learn`

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install numpy pandas scikit-learn
```

If you already have the dependencies installed, you can skip the environment setup and run the script directly.

## How To Run

From the root folder, run:

```bash
python model.py
```

Before running, make sure the path in `DATA_DIR` inside `model.py` matches your local data location.

## Modeling Approach

`model.py` follows a time-series forecasting pipeline built around the observation that the revenue distribution is more stable in the 2019-2022 period than in the earlier years.

The main workflow is:

1. Load sales, order, promotion, and submission data.
2. Aggregate daily order counts.
3. Build calendar, holiday, promotion, lag, rolling, and year-over-year features.
4. Train a `HistGradientBoostingRegressor` and a `Ridge` model on log-transformed revenue.
5. Blend the two revenue models with a weighted ensemble.
6. Estimate `COGS` from predicted revenue using historical cost ratios.
7. Retrain on the full historical period and generate recursive day-by-day predictions for the test period.
8. Save the final output to `submission.csv`.

The script uses a fixed random seed for reproducibility.

The strongest signals in the pipeline are year-ago lags, rolling averages, seasonality terms, order volume, and the rolling `COGS`-to-`Revenue` ratio.

## Feature Engineering

Key features in the pipeline include:

- day-of-week, month, quarter, and year trend features
- weekend and month-end indicators
- Vietnamese holiday flags
- weekly and yearly sine/cosine seasonality terms
- short and long lag features for revenue, orders, and COGS
- rolling means and rolling standard deviations
- year-over-year ratios
- promotion flags and promotion discount features

## Reported Validation Results

The project README previously documented the following out-of-sample validation results for 2022:

| Metric | Revenue | COGS |
| --- | ---: | ---: |
| MAE | 325,442 | 327,730 |
| RMSE | 443,696 | 453,653 |
| R² | 0.9297 | 0.9033 |

These numbers reflect the model configuration used in the repository and are included here for continuity.

Compared with simple baselines, the proposed approach was reported to reduce revenue MAE substantially while preserving strong out-of-sample $R^2$.

## Output

Running `model.py` generates `submission.csv` with the columns:

- `Date`
- `Revenue`
- `COGS`

The file follows the format expected by `sample_submission.csv`, contains 548 daily rows for the test period, and is written in UTF-8 encoding.

## Troubleshooting

- If you see `FileNotFoundError` for `sales.csv`, check that `DATA_DIR` points to the folder containing the CSV files.
- If `sklearn` is missing, install the dependencies with `pip install numpy pandas scikit-learn`.
- If memory usage is high, reduce `max_iter` in `HGB_PARAMS` inside `model.py`.

## Notes

- `model.py` suppresses warnings at startup.
- The prediction step is recursive, so each predicted day can influence later days.
- `overview.md` contains a detailed profile of each dataset in this repository.

## Author

- Phạm Đình Nhật Minh
- Lê Khánh Bảo Minh
- Nguyễn Thành Vinh
- Lê Nguyễn Thái Sơn
