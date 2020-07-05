# https://www.scrapehero.com/scrape-yahoo-finance-stock-market-data/
# https://gist.github.com/scrapehero-code/6d87e1e1369ee701dcea8880b4b620e9

import requests
import json
import os
import glob
import time

# 173 companies in food industry
# files = ['beverage_and_alcohol', 'beverage_brewers', 'farm_products', 'food_distribution', 'grocery_stores', 'packaged_foods', 'restaurants']


def retrieve_industry_companies(folder):
    companies = []
    path = "/Users/izadi/Downloads/Scrape Stocks/" + folder
    for filename in glob.glob(os.path.join(path, '*.txt')):
        if 'finviz_links.txt' not in filename:
            with open(filename, 'r') as f:
                for i in f:
                    companies.append(i.strip("\n"))

    return companies

def parse(ticker):
    """ commented code below includes recommendation on Yahoo Finance and other trends """
    # EXTREMELY USEFUL DATA USING THE COMMENTED LINK BELOW
    # other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents%2CsummaryDetail&corsDomain=finance.yahoo.com".format(
    #     ticker)
    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=financialData%2CsummaryDetail&corsDomain=finance.yahoo.com".format(
        ticker)
    summary_json_response = requests.get(other_details_json_link)

    company_data = {}
    try:
        """ DATA RETRIEVAL """
        json_loaded_summary = json.loads(summary_json_response.text)
        summary = json_loaded_summary["quoteSummary"]["result"][0]
        summary_detail_module = summary['summaryDetail']
        financial_data_module = summary['financialData']

        company_data['ticker_code'] = ticker
        company_data['current_price'] = float(financial_data_module['currentPrice']['fmt'].replace(",", ""))
        company_data['market_cap'] = summary_detail_module['marketCap']['fmt']
        company_data['profit_margin'] = float(financial_data_module['profitMargins']['fmt'][:-1].replace(",", ""))
        # company_data['debt_to_equity'] = float(financial_data_module['debtToEquity']['fmt'].replace(",", ""))
        company_data['fifty_two_week_low'] = float(summary_detail_module['fiftyTwoWeekLow']['fmt'].replace(",", ""))

        # print(summary)
        # print(company_data['ticker_code'])
        # print(company_data['current_price'])
        # print(company_data['market_cap'])
        # print(company_data['profit_margin'])
        # print(company_data['debt_to_equity'])
        # print(company_data['fifty_two_week_low'])

        try:
            company_data['price_target'] = float(financial_data_module['targetMeanPrice']['fmt'])
            # print(company_data['price_target'])
        except KeyError:
            company_data['price_target'] = None
            # print('No target price for: ', ticker)

        return company_data

    except KeyError:
        # print("No fmt")
        # print(summary)
        return None

    except Exception as e:
        print(e)

    # except ValueError:
    #     print("Failed to parse json response for: ", ticker)
    #     return None
    # except:
    #     print("Unhandled error for: ", ticker)
    #     return None

def filter(dataset):

    if dataset != None:
        pass_filter = {}

        if dataset['market_cap'][-1] == "B" or dataset['market_cap'][-1] == "T":
            pass_filter['market_cap'] = True
        else:
            pass_filter['market_cap'] = False

        if dataset['profit_margin'] >= 2:
            pass_filter['profit_margin'] = True
        else:
            pass_filter['profit_margin'] = False

        # if dataset['debt_to_equity'] < 100:
        #     pass_filter['debt_to_equity'] = True
        # else:
        #     pass_filter['debt_to_equity'] = False

        lower_bound = dataset['fifty_two_week_low'] - (dataset['fifty_two_week_low']*0.1)
        upper_bound = dataset['fifty_two_week_low'] + (dataset['fifty_two_week_low']*0.1)

        # print(lower_bound)
        # print(upper_bound)

        if dataset['current_price'] >= lower_bound and dataset['current_price'] <= upper_bound:
            pass_filter['pricing_range'] = True
        else:
            pass_filter['pricing_range'] = False


        price_target = dataset['current_price']*1.1
        # print(price_target)
        if dataset['price_target'] != None:
            if dataset['price_target'] >= price_target:
                pass_filter['price_target'] = True
            else:
                pass_filter['price_target'] = False

            for i in pass_filter:
                if pass_filter[i] == False:
                    return None

            return dataset
        else:
            return None


def main():
    companies = retrieve_industry_companies("Food Industry Tickers")
    print(companies)
    buy = []

    start = time.time()
    for i in companies:
        company = parse(i)
        # if company != None:
        #     filtered = filter(company)
        #     if filtered != None:
        #         buy.append(filtered['ticker_code'])

    end = time.time()
    timetaken = end - start
    print("Time taken : ", timetaken)

    if len(buy) > 0:
        for company in buy:
            print("BUY : ", company)

main()

# lol = parse('3182.KL')
# loll = filter(lol)
# print(lol['market_cap'])