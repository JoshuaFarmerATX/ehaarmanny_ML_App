import requests
import json
from pprint import pprint

def apiData(call):

    response = json.loads(requests.get(f'https://api-pc6dbtrtla-uc.a.run.app/API/{call}').text)
    cases = int(response[0].get('Cases'))
    recoveries = int(response[0].get('Recovered'))
    deaths = int(response[0].get('Deaths'))

    return {
        'cases': cases,
        'recoveries': recoveries,
        'deaths': deaths
    }

def apiDataCallMulti(call, region):
    responses = json.loads(requests.get(f'https://api-pc6dbtrtla-uc.a.run.app/API/{call}').text)
    dict = []
    for i in range(len(responses) - 1):
        if region == 'State':
            dict.append({
                'region': responses[i - 1].get(region),
                'date': responses[i - 1].get('Last Update'),
                'cases': int(responses[i - 1].get('Cases')),
                'deaths': int(responses[i - 1].get('Deaths'))

            })
        else:
            dict.append({
                'region': responses[i - 1].get(region),
                'date': responses[i - 1].get('Last Update'),
                'cases': int(responses[i - 1].get('Cases')),
                'cases': int(responses[i - 1].get('Recovered')),
                'deaths': int(responses[i - 1].get('Deaths'))
            })

    return dict

def apiDataCallTimeSeries(call, region):
    responses = json.loads(requests.get(f'https://api-pc6dbtrtla-uc.a.run.app/API/{call}').text)
    pprint(responses)
    dict = []
    for i in range(len(responses) - 1):
        if region == 'State':
            dict.append({
                'state': responses[i - 1].get(region),
                'date': responses[i - 1].get('Totals as of Date'),
                'cases': int(responses[i - 1].get('Cases')),
                'deaths': int(responses[i - 1].get('Deaths'))

            })
        else:
            dict.append({
                'region': responses[i - 1].get(region),
                'date': responses[i - 1].get('Total Results as of Date'),
                'cases': int(responses[i - 1].get('Cases')),
                'cases': int(responses[i - 1].get('Recovered')),
                'deaths': int(responses[i - 1].get('Deaths'))
            })
    dict[:] = [d for d in dict if d.get('date') >= '2020-03-01']

    return dict

# datadict = apiData('global_totals/most_recent')
# print(datadict)

# multiDict = apiDataCallMulti('us/most_recent', 'State')
# pprint(multiDict)

# multiDictTS = apiDataCallTimeSeries('timeseries/USA', 'Country')
# pprint(multiDictTS)