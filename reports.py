from datetime import date
import json


def get_report_header(report_date):
    return '<h2>Report from {}</h2>'.format(report_date)


def get_preset_header(preset):
    return '<h2>{}</h2>'.format(preset)


def get_diff_report(check):
    return '<table><tr><td>{}</td><td><pre>{}<pre></td></tr></table>'\
        .format(check["handler"], check['result'])


def get_error_report(check):
    return '<tr><td>{}</td><td>{}</td></tr>' \
        .format(check["handler"], check['error'])


def report_generator(presets_results):
    with open('./reports/report_header.html', 'r') as template_header:
        report_data = template_header.read()

    report_date = date.today()
    with open('checks_report_{}.html'.format(report_date), 'w') as report:
        report_data += get_report_header(report_date)
        for preset in presets_results.keys():
            report_data += get_preset_header(preset)
            report_data += '<table>'
            for check in presets_results[preset]:
                if "error" in check.keys():
                    report_data += get_error_report(check)
                else:
                    report_data += get_diff_report(check)
            report_data += '</table><hr>'
        report_data += '</body></html>'
        report.write(report_data)

