from logging import getLogger
from src.core.logger import operations as logger_opertations
import pandas as pd


run_id = pd.Timestamp("now").strftime("%Y%m%d_%H%M%S")
logger = logger_opertations.configure_logger(getLogger(), log_dir="logs", suffix=run_id)