import requests

other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=financialData%2CsummaryDetail&corsDomain=finance.yahoo.com".format(
    "NVR")
summary_json_response = requests.get(other_details_json_link)

print(summary_json_response)

# JSON error:  could not convert string to float: '3,517.80'  for ticker:  NVR