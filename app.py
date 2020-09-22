from checks import run_presets_checks
from reports import report_generator
import json


def prepare_app():
    presets = []
    with open('./settings.json', 'r') as settings_json:
        presetNames = (json.load(settings_json)["presets"])

    for preset in presetNames:
        with open('./presets/{}.json'.format(preset), 'r') as preset:
            presets.append(json.load(preset))

    return presets


def run_checks():
    report_data = {}
    presets = prepare_app()

    for preset in presets:
        report_data[preset['name']] = run_presets_checks(preset)
    return report_data


def app():
    report_generator(run_checks())


if __name__ == '__main__':
    app()




