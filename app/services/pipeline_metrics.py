pipeline_metrics = {

    "jobs_fetched": 0,

    "jobs_filtered": 0,

    "duplicates_skipped": 0,

    "jobs_inserted": 0,

    "alerts_sent": 0,

    "scraper_failures": 0
}

def reset_metrics():
    global pipeline_metrics
    pipeline_metrics = {
        "jobs_fetched": 0,

        "jobs_filtered": 0,

        "duplicates_skipped": 0,

        "jobs_inserted": 0,

        "alerts_sent": 0,

        "scraper_failures": 0
    }
    
def increment_metric(metric_name, count=1):
    if metric_name in pipeline_metrics:
        pipeline_metrics[metric_name] += count

def get_metrics():
    return pipeline_metrics