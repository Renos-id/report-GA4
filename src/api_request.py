from google.analytics.data_v1beta import types

def run_report(client, property_id, dimensions, metrics, date_ranges):
    request = types.RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=dimensions,
        metrics=metrics,
        date_ranges=date_ranges
    )
    response = client.run_report(request)
    return response