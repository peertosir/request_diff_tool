import requests
from deepdiff import diff
import json


def make_diff(url1, url2, method, headers):
    handler_name = ' '.join(url1.split('/')[-2:]).upper()

    if method == 'POST':
        try:
            response1 = requests.post(url1, headers=headers).json()
            response2 = requests.post(url2, headers=headers).json()
        except:
            return {
                "handler": handler_name,
                "error": "Something bad happened"
            }
    elif method == 'GET':
        try:
            response1 = requests.get(url1, headers=headers).json()
            response2 = requests.get(url2, headers=headers).json()
        except:
            return {
                "handler": handler_name,
                "error": "Something bad happened"
            }
    else:
        return {
            "handler": handler_name,
            "error": "Method not supported in script yet"
        }
    diff_result = diff.DeepDiff(response1, response2, ignore_order=True)
    return {
                "handler": handler_name,
                "result": diff_result.to_json() if bool(diff_result.to_dict()) else "NO DIFF"
            }


def run_presets_checks(preset):
    return_value = []
    for handler in preset['handlers']:
        for version in handler['versions']:
            url1 = '{}v{}{}'.format(preset['host1'], version, handler['url'], handler['queryParams'])
            url2 = '{}v{}{}'.format(preset['host2'], version, handler['url'], handler['queryParams'])
            try:
                result = make_diff(url1, url2, handler['method'], handler['headers'])
                print(result)
            except:
                result = {
                    "handler": '{} {}'.format(version, handler["url"]),
                    "error": "Diff error. Maybe bad response was get"
                }
            return_value.append(result)
    return return_value

