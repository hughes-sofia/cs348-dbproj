from django.db import connection

def raw_today_revenue(shop_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COALESCE(SUM(total_price), 0)
            FROM mainapp_order
            WHERE shop_id = %s AND order_date = CURRENT_DATE
        """, [shop_id])
        row = cursor.fetchone()
    return row[0]