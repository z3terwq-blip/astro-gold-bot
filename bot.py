import requests
from datetime import datetime
import time
import math

# إعدادات التليجرام
BOT_TOKEN = '8288347690:AAErOP-qfjyVUkUXs2ch0ovcLEsJdRb45Rw'
CHAT_ID = '-1002086107811'

# آخر درجة تم إرسالها
last_degree = None

def calculate_sun_degree():
    """حساب درجة الشمس الفلكية"""
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    day_of_year = (now - start_of_year).days
    
    # حساب الدرجة (معدلة للدقة)
    degree = ((day_of_year * 0.9856) + 278) % 360
    return round(degree)

def degree_to_price(degree):
    """تحويل درجة الشمس إلى سعر"""
    return 2374 + (degree % 360)

def calculate_main_levels(degree, base_price):
    """حساب المستويات نيو سن"""
    jump = round(degree / 2)
    levels = []
    current_price = base_price
    level_number = 1
    
    for _ in range(25):
        if current_price >= 3500:
            levels.append({
                'level': level_number,
                'price': current_price,
                'type': 'نيو سن'
            })
            level_number += 1
        current_price += jump
    
    return levels

def calculate_fib_levels(main_levels):
    """حساب مستويات فيبوناتشي 0.618"""
    fib_levels = []
    
    for i in range(len(main_levels) - 1):
        level1 = main_levels[i]['price']
        level2 = main_levels[i + 1]['price']
        fib_price = round(level1 + ((level2 - level1) * 0.618))
        
        if fib_price >= 3500:
            fib_levels.append({
                'level': f"{i+1}-{i+2}",
                'price': fib_price,
                'type': 'فيبوناتشي 0.618'
            })
    
    return fib_levels

def send_to_telegram(degree, main_levels, fib_levels):
    """إرسال المستويات للتليجرام"""
    message = f"🌞 *تحديث استراتيجية الشمس الفلكية*\n\n"
    message += f"📅 التاريخ: {datetime.now().strftime('%Y-%m-%d')}\n"
    message += f"🔢 درجة الشمس: *{degree}°*\n"
    message += f"💰 AST Forex\n\n"
    
    message += f"📊 *المستويات نيو سن:*\n"
    for level in main_levels[:10]:
        message += f"{level['level']}. {level['price']}\n"
    
    message += f"\n🎯 *مستويات فيبوناتشي 0.618:*\n"
    for level in fib_levels[:8]:
        message += f"• {level['level']}: {level['price']}\n"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"✅ تم إرسال المستويات بنجاح - درجة الشمس: {degree}°")
        else:
            print(f"⚠️ خطأ في الإرسال: {response.status_code}")
    except Exception as e:
        print(f"❌ خطأ: {e}")

def main():
    """الدالة الرئيسية"""
    global last_degree
    
    print("🌟 بدء نظام استراتيجية الشمس الفلكية...")
    
    # حساب درجة الشمس
    degree = calculate_sun_degree()
    print(f"🌞 درجة الشمس الحالية: {degree}°")
    
    # التحقق من التغيير
    if last_degree is None or degree != last_degree:
        print("🔄 تم رصد تغيير في درجة الشمس...")
        
        # حساب السعر والمستويات
        base_price = degree_to_price(degree)
        main_levels = calculate_main_levels(degree, base_price)
        fib_levels = calculate_fib_levels(main_levels)
        
        # إرسال للتليجرام
        send_to_telegram(degree, main_levels, fib_levels)
        
        # تحديث آخر درجة
        last_degree = degree
    else:
        print("⏳ لا يوجد تغيير في درجة الشمس")

if __name__ == "__main__":
    main()
