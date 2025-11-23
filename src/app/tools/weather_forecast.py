"""
Math related tools.
"""
from app.main import mcp

@mcp.tool()
def get_weather_forecast(location: str) -> str:
    """
    天気予報を取得します。
    例えば、"東京の天気を教えて" のように使用します。
    """
    # ここに天気予報を取得するロジックを実装します
    return f"{location}の天気予報は晴れです。"