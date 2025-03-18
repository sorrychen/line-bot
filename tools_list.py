tools_list = [
    {"type": "file_search"},
    {
        "type": "function",
        "function": {
            'name': 'get_today_date',
            'description': '當使用扯詢問今日日期時，回傳今日日期',
        }
    },
    {
    "type": "function",
    "function": {
        "name": "get_opening_hours",
        "description": "根據顧客詢問的日期，提供對應的咖啡廳營業時間",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "當顧客詢問營業時間，回傳營業時間"
                }
            },
            "required": []
            }
        }
    }

]