COMPOSE_FILE := docker-compose-alm.yml
DOCKER_COMPOSE := docker compose -f $(COMPOSE_FILE) --project-directory ..

SERVICE_TRADE := ft-trade
SERVICE_BACKTESTING := ft-backtest
SERVICE_PLOT := ft-plot

USER_DIR := user_data
CONFIG_TRADE := $(USER_DIR)/config.json
CONFIG_BACKTEST := $(USER_DIR)/config_backtest.json
DEFAULT_PAIRS := ETH/USDT BTC/USDT SOL/USDT XRP/USDT

EXCHANGE := binance
#STRATEGY := SampleStrategy
#STRATEGY := SimpleStrategy
#STRATEGY := Strategy002
STRATEGY := SwingHighToSky

# pulling newest image
pull:
	$(DOCKER_COMPOSE) pull

# create or update config file (use defaults, but enable freqUI)
config:
	$(DOCKER_COMPOSE) run --rm ft-trade create-userdir --userdir user_data && docker compose run --rm freqtrade new-config --config user_data/config.json

# -- trade --

# start freqtrade
run:
	$(DOCKER_COMPOSE) up -d

# stop freqtrade
stop:
	$(DOCKER_COMPOSE) down

# -- backtesting --

# example for downloading historic data for ETH/USDT BTC/USDT between 01.01.23 and 01.01.26 (5 min intervals) and drop existing
download-data-fixed:
	$(DOCKER_COMPOSE) run --rm $(SERVICE_BACKTESTING) download-data --pairs $(DEFAULT_PAIRS) --exchange $(EXCHANGE) --timerange 20230101-20260101 --timeframes 5m --erase

download-data-latest:
	$(DOCKER_COMPOSE) run --rm $(SERVICE_BACKTESTING) download-data --pairs $(DEFAULT_PAIRS) --exchange $(EXCHANGE) --days 365 --timeframes 1m 5m 15m 1h --erase

# run backtest for available historic data of ETH/USDT BTC/USDT with the SampleStrategy (5 min steps)
# Note: to run properly, in user_data/config.json modify:
# - pairlists method should be { "method": "StaticPairList" } and delete VolumePairList entry
# - exchange.pair_whitelist should be including the historic data, like: ["ETH/USDT","BTC/USDT"]
run-backtest:
	$(DOCKER_COMPOSE) run --rm $(SERVICE_BACKTESTING) backtesting --config $(CONFIG_BACKTEST) --pairs $(DEFAULT_PAIRS) --strategy $(STRATEGY) --cache none

plot-backtest-results:
	$(DOCKER_COMPOSE) run --rm $(SERVICE_PLOT) plot-dataframe --config $(CONFIG_BACKTEST) --pairs $(DEFAULT_PAIRS) --strategy $(STRATEGY)