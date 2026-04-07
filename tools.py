from langchain_core.tools import tool

# =========================================================
# MOCK DATA – Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# =========================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {
            "name": "Mường Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "Fivitel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Meliá",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "9Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "Cochin Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}


@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    try:
        if not origin or not destination:
            return "Lỗi: Vui lòng cung cấp đầy đủ điểm đi và điểm đến."

        origin_key = str(origin).strip().title()
        dest_key = str(destination).strip().title()

        flights = FLIGHTS_DB.get((origin_key, dest_key))

        def format_price(price: int) -> str:
            return f"{price:,}".replace(",", ".") + "đ"

        if flights:
            sorted_flights = sorted(flights, key=lambda x: x["price"])

            cheapest = sorted_flights[0]
            result = f"💰 Vé rẻ nhất từ {origin_key} đến {dest_key}: {format_price(cheapest['price'])} - {cheapest['airline']} lúc {cheapest['departure']}\n\n"
            result += f"Các chuyến bay từ {origin_key} đến {dest_key} (sắp xếp theo giá):\n"

            for f in sorted_flights:
                result += (
                    f"- Hãng: {f['airline']} | Hạng: {f['class'].title()} | "
                    f"Giờ bay: {f['departure']} - {f['arrival']} | "
                    f"Giá: {format_price(f['price'])}\n"
                )
            return result.strip()
        else:
            reverse_flights = FLIGHTS_DB.get((dest_key, origin_key))
            if reverse_flights:
                return f"Không tìm thấy chuyến bay từ {origin_key} đến {dest_key}, nhưng có chuyến bay chiều ngược lại. Bạn có muốn xem thử không?"
            else:
                return f"Không tìm thấy chuyến bay từ {origin_key} đến {dest_key}."

    except Exception as e:
        return f"Đã xảy ra lỗi hệ thống khi tìm kiếm chuyến bay: {str(e)}"


@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    try:
        if not city:
            return "Lỗi: Vui lòng cung cấp tên thành phố."

        city_key = str(city).strip().title()

        # Đảm bảo max_price_per_night là số nguyên, phòng trường hợp LLM truyền nhầm chuỗi
        try:
            max_price = int(max_price_per_night)
        except ValueError:
            return "Lỗi: Giá tối đa mỗi đêm phải là một số."

        hotels = HOTELS_DB.get(city_key, [])

        def format_price(price: int) -> str:
            return f"{price:,}".replace(",", ".") + "đ"

        filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price]
        if not filtered_hotels:
            if hotels:
                return f"Không tìm thấy khách sạn tại {city_key} với giá dưới {format_price(max_price)}/đêm. Hãy thử tăng ngân sách."
            else:
                return f"Hiện chưa có dữ liệu khách sạn tại {city_key}."

        sorted_hotels = sorted(filtered_hotels, key=lambda x: x["rating"], reverse=True)

        result = f"Danh sách khách sạn tại {city_key} (Ngân sách tối đa: {format_price(max_price)}/đêm):\n"
        for h in sorted_hotels:
            result += (
                f"- {h['name']} ({h['stars']} Sao) | Khu vực: {h['area']} | "
                f"Rating: {h['rating']}⭐ | Giá: {format_price(h['price_per_night'])}/đêm\n"
            )

        return result.strip()

    except Exception as e:
        return f"Đã xảy ra lỗi hệ thống khi tìm kiếm khách sạn: {str(e)}"


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Ép kiểu để bắt lỗi nếu LLM truyền tham số total_budget không phải số
        try:
            budget = int(total_budget)
        except ValueError:
            return "Lỗi: Tổng ngân sách ban đầu phải là một số."

        if not expenses or not str(expenses).strip():
            return "Lỗi: Không có khoản chi phí nào được cung cấp."

        def format_price(price: int) -> str:
            return f"{price:,}".replace(",", ".") + "đ"

        expense_dict = {}
        items = str(expenses).split(",")

        for item in items:
            parts = item.split(":")
            if len(parts) != 2:
                return f"Lỗi định dạng ở khoản: '{item.strip()}'. Cần tuân thủ định dạng 'tên_khoản:số_tiền'."

            name = parts[0].strip()
            amount_str = parts[1].strip()

            if not amount_str.isdigit():
                return f"Lỗi định dạng: Số tiền cho khoản '{name}' phải là số nguyên dương (nhận được: '{amount_str}')."

            clean_name = name.replace("_", " ").capitalize()
            expense_dict[clean_name] = int(amount_str)

        total_expenses = sum(expense_dict.values())
        remaining_budget = budget - total_expenses

        result_lines = ["Bảng chi phí:"]
        for name, amount in expense_dict.items():
            result_lines.append(f"- {name}: {format_price(amount)}")

        result_lines.append("---")
        result_lines.append(f"Tổng chi: {format_price(total_expenses)}")
        result_lines.append(f"Ngân sách: {format_price(budget)}")

        if remaining_budget < 0:
            over_budget = abs(remaining_budget)
            result_lines.append(f"Vượt ngân sách {format_price(over_budget)}! Cần điều chỉnh.")
        else:
            result_lines.append(f"Còn lại: {format_price(remaining_budget)}")

        return "\n".join(result_lines)

    except Exception as e:
        return f"Đã xảy ra lỗi hệ thống khi tính toán ngân sách: {str(e)}"
