# -- installing (docker) --

# pulling newest image
pull:
	docker compose pull

# create or update config file (use defaults, but enable freqUI)
config:
	docker compose run --rm freqtrade create-userdir --userdir user_data && docker compose run --rm freqtrade new-config --config user_data/config.json

# -- operation --

# start freqtrade
run:
	docker compose up -d

# stop freqtrade
stop:
	docker compose down

# -- backtesting --

# example for downloading historic data for ETH/USDT BTC/USDT between 01.01.20 and 01.01.23 (5 min intervals)
download-data-example:
	docker compose run --rm freqtrade download-data --pairs ETH/USDT BTC/USDT --exchange binance --timerange 20200101-20230101 -t 5m

# run backtest for available historic data of ETH/USDT BTC/USDT with the SampleStrategy (5 min steps)
# Note: to run properly, in user_data/config.json modify:
# - pairlists method should be { "method": "StaticPairList" } and delete VolumePairList entry
# - exchange.pair_whitelist should be including the historic data, like: ["ETH/USDT","BTC/USDT"]
backtest-data-example:
	docker compose run --rm freqtrade backtesting --config user_data/config.json --pairs ETH/USDT BTC/USDT --strategy AlmStrategy -i 5m
