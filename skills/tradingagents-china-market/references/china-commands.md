# China Market Query Commands

## Market data
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
result = mgr.get_market_data('600519.SH', '2024-05-01', '2024-06-01')
print(result)
"
```

## Company info
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
result = mgr.get_company_info('600519.SH')
print(result)
"
```

## Financial data
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
result = mgr.get_financial_info('600519.SH')
print(result)
"
```

## News and events
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
result = mgr.get_news_events('600519.SH', '2024-05-01', '2024-06-01', limit=10)
print(result)
"
```

## Technical indicators
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
result = mgr.get_indicators('600519.SH', 'SMA_20', '2024-06-01', look_back_days=30)
print(result)
"
```
