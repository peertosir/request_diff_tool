import json

import requests
from deepdiff import diff


def make_diff(url1, url2, method, headers, body=None):
    handler_name = ' '.join(url1.split('/')[-2:]).upper()
    try:
        if method == 'POST':
            response1 = requests.post(url1, data=json.dumps(body), headers=headers, verify=False)
            response2 = requests.post(url2, data=json.dumps(body), headers=headers, verify=False)
        elif method == 'GET':
            response1 = requests.get(url1, headers=headers, verify=False)
            response2 = requests.get(url2, headers=headers, verify=False)
        else:
            return {
                "handler": handler_name,
                "error": "Method not supported in script yet"
            }
    except:
        return {
            "handler": handler_name,
            "error": "Error during request occured"
        }
    diff_result = diff.DeepDiff(response1.json(), response2.json(), ignore_order=True)
    return {
        "handler": handler_name,
        "status_code": response1.status_code,
        "result": diff_result.to_json() if bool(diff_result.to_dict()) else "NO DIFF"
    }


def run_presets_checks(preset):
    return_value = []
    for handler in preset['handlers']:
        for version in handler['versions']:
            url1 = '{}v{}{}{}'.format(preset['host1'], version, handler['url'], handler['queryParams'])
            url2 = '{}v{}{}{}'.format(preset['host2'], version, handler['url'], handler['queryParams'])
            try:
                body = None
                if 'body' in handler.keys():
                    body = handler['body']
                result = make_diff(url1, url2, handler['method'], handler['headers'], body)
            except:
                result = {
                    "handler": '{} {}'.format(version, handler["url"]),
                    "error": "Diff error. Maybe bad response was sent"
                }
            return_value.append(result)
    return return_value

