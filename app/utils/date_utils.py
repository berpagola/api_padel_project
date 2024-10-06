from datetime import datetime
import pytz

def parse_and_convert_to_utc(date_str: str, format: str = "%Y-%m-%d %H:%M") -> datetime:
    try:
        local_dt = datetime.strptime(date_str, format)
        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        local_dt = local_tz.localize(local_dt)
        return local_dt.astimezone(pytz.UTC)
    except ValueError:
        return None