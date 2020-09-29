# Assignment_Web_Scraping_TripAdivsor

## Steps performed
- Visited the https://www.tripadvisor.com website
- Clicked on Hotels
- Passed New Delhi National Capital Territory of Delhi in Search Bar
- Then moved key down to select best option from Auto-Suggestion Box
- Clicked Hotels button on New Delhi Page
- Reached Top 10 Hotels of New Delhi page

### Data Scraping
  - Scraped all Hotel data cards
  - Navigated to every page by scrolling and clicking Next Button using Selenium
  - Collected all required information as well as handled situation where no data is available for hotel
  - Only image data not collected as many returned as None
  - Stored data in dataframe and later converted to 'output.csv'
  - Also used csv package to create backup as dataframe only after parsing all page be converted to CSV 
  - Backup - 'data/url_req.csv'
 
