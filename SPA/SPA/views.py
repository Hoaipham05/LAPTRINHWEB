from calendar import Calendar
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.utils.dateparse import parse_date, parse_time

from accounts.models import Appointment, ConsultationConversation, ConsultationMessage


BOOKING_SERVICES = [
    {
        "id": "collagen",
        "name": "Chăm sóc da mặt Collagen",
        "description": "Làm sạch sâu, dưỡng ẩm và tái tạo da.",
        "duration": "90 phút",
        "price": "Từ 1,200,000đ",
        "rating": "4.8",
        "tone": "collagen",
        "image": "images/services/collagen.svg",
    },
    {
        "id": "tri-mun",
        "name": "Trị mụn chuyên sâu",
        "description": "Điều trị mụn an toàn, hiệu quả.",
        "duration": "60 phút",
        "price": "Từ 800,000đ",
        "rating": "4.9",
        "tone": "acne",
        "image": "images/services/tri-mun.svg",
    },
    {
        "id": "massage",
        "name": "Massage body thư giãn",
        "description": "Massage toàn thân giúp thư giãn.",
        "duration": "60 phút",
        "price": "Từ 500,000đ",
        "rating": "4.9",
        "tone": "massage",
        "image": "images/services/massage.svg",
    },
    {
        "id": "triet-long",
        "name": "Triệt lông vĩnh viễn bằng laser/IPL",
        "description": "Triệt lông vĩnh viễn bằng laser/IPL.",
        "duration": "90 phút",
        "price": "Từ 2,000,000đ",
        "rating": "4.8",
        "tone": "laser",
        "image": "images/services/triet-long.svg",
    },
    {
        "id": "goi-dau",
        "name": "Trị rụng tóc / gàu",
        "description": "Giúp làm sạch sâu, giảm bã nhờn.",
        "duration": "60 phút",
        "price": "Từ 1,300,000đ",
        "rating": "4.7",
        "tone": "hair",
        "image": "images/services/goi-dau.svg",
    },
    {
        "id": "sauna",
        "name": "Xông hơi sauna",
        "description": "Giãn nở lỗ chân lông, đào thải độc tố.",
        "duration": "90 phút",
        "price": "Từ 700,000đ",
        "rating": "4.9",
        "tone": "sauna",
        "image": "images/services/sauna.svg",
    },
]

BOOKING_PACKAGES = [
    {
        "id": "basic",
        "name": "Gói cơ bản",
        "sessions": "1-2 buổi điều trị",
        "steps": "✓ Làm sạch da cơ bản\n✓ Massage mặt thư giãn\n✓ Đắp mặt nạ Collagen\n✓ Dưỡng ẩm hoàn thiện",
        "price": "Từ 800,000đ",
        "first_time": "Phù hợp cho lần đầu trải nghiệm",
        "result": "Phù hợp cho lần đầu trải nghiệm",
        "accent": "basic",
    },
    {
        "id": "standard",
        "name": "Gói tiêu chuẩn",
        "sessions": "3-5 buổi điều trị",
        "steps": "✓ Tất cả quyền lợi gói cơ bản\n✓ Tẩy tế bào chết chuyên sâu\n✓ Serum dưỡng da cao cấp\n✓ Tư vấn chăm sóc da tại nhà\n✓ Tặng 1 mặt nạ collagen về nhà",
        "price": "Từ 1,300,000đ",
        "first_time": "Hiệu quả rõ rệt sau 1 tháng",
        "result": "Hiệu quả rõ rệt sau 1 tháng",
        "accent": "standard",
    },
    {
        "id": "premium",
        "name": "Gói cao cấp",
        "sessions": "8-10 buổi điều trị",
        "steps": "✓ Tất cả quyền lợi gói tiêu chuẩn\n✓ Công nghệ điều trị tiên tiến\n✓ Massage với đá quý miễn phí\n✓ Tặng bộ skincare mini\n✓ Ưu đãi 10% dịch vụ tiếp theo",
        "price": "Từ 2,500,000đ",
        "first_time": "Chăm sóc toàn diện, hiệu quả lâu dài",
        "result": "Chăm sóc toàn diện, hiệu quả lâu dài",
        "accent": "premium",
    },
    {
        "id": "vip",
        "name": "Gói VIP",
        "sessions": "12-15 buổi điều trị",
        "steps": "✓ Tất cả quyền lợi gói cao cấp\n✓ Phòng riêng VIP sang trọng\n✓ Thức uống & trái cây miễn phí\n✓ Tặng bộ skincare cao cấp\n✓ Ưu đãi 20% mọi dịch vụ",
        "price": "Từ 3,500,000đ",
        "first_time": "Trải nghiệm đẳng cấp 5 sao",
        "result": "Trải nghiệm đẳng cấp 5 sao",
        "accent": "vip",
    },
]

BOOKING_PACKAGES_BY_SERVICE = {
    "collagen": [
        {
            "id": "basic",
            "name": "Gói cơ bản",
            "sessions": "1-2 buổi điều trị",
            "steps": "✓ Làm sạch da cơ bản\n✓ Massage mặt thư giãn\n✓ Đắp mặt nạ Collagen\n✓ Dưỡng ẩm hoàn thiện",
            "price": "Từ 800,000đ",
            "first_time": "Phù hợp cho lần đầu trải nghiệm",
            "result": "Phù hợp cho lần đầu trải nghiệm",
            "accent": "basic",
        },
        {
            "id": "standard",
            "name": "Gói tiêu chuẩn",
            "sessions": "3-5 buổi điều trị",
            "steps": "✓ Tẩy tế bào chết chuyên sâu\n✓ Đi tinh chất Collagen\n✓ Ủ mặt nạ phục hồi\n✓ Tư vấn chăm sóc da tại nhà",
            "price": "Từ 1,300,000đ",
            "first_time": "Hiệu quả rõ rệt sau 1 tháng",
            "result": "Da sáng khỏe và căng mịn hơn sau liệu trình đầu",
            "accent": "standard",
        },
        {
            "id": "premium",
            "name": "Gói cao cấp",
            "sessions": "8-10 buổi điều trị",
            "steps": "✓ Công nghệ điện di Collagen\n✓ Massage đá lạnh se khít lỗ chân lông\n✓ Phục hồi chuyên sâu\n✓ Tặng bộ skincare mini",
            "price": "Từ 2,500,000đ",
            "first_time": "Chăm sóc toàn diện, hiệu quả lâu dài",
            "result": "Da đều màu, căng bóng và giữ ẩm tốt hơn",
            "accent": "premium",
        },
        {
            "id": "vip",
            "name": "Gói VIP",
            "sessions": "12-15 buổi điều trị",
            "steps": "✓ Phác đồ cá nhân hóa\n✓ Phòng riêng cao cấp\n✓ Collagen nhập khẩu\n✓ Chăm sóc sau liệu trình 1:1",
            "price": "Từ 3,500,000đ",
            "first_time": "Trải nghiệm đẳng cấp 5 sao",
            "result": "Tối ưu độ đàn hồi và độ sáng cho da mặt",
            "accent": "vip",
        },
    ],
    "tri-mun": [
        {
            "id": "basic",
            "name": "Gói cơ bản",
            "sessions": "1-2 buổi điều trị",
            "steps": "✓ Soi da\n✓ Làm sạch sâu\n✓ Lấy nhân mụn cơ bản\n✓ Làm dịu da",
            "price": "Từ 800,000đ",
            "first_time": "Phù hợp mụn nhẹ và lần đầu điều trị",
            "result": "Giảm viêm cơ bản, da sạch hơn sau buổi đầu",
            "accent": "basic",
        },
        {
            "id": "standard",
            "name": "Gói tiêu chuẩn",
            "sessions": "3-5 buổi điều trị",
            "steps": "✓ Lấy nhân mụn chuyên sâu\n✓ Đi serum giảm viêm\n✓ Ánh sáng sinh học\n✓ Hướng dẫn skincare tại nhà",
            "price": "Từ 1,300,000đ",
            "first_time": "Phù hợp da dầu mụn cần theo liệu trình",
            "result": "Hiệu quả rõ rệt sau 1 tháng",
            "accent": "standard",
        },
        {
            "id": "premium",
            "name": "Gói cao cấp",
            "sessions": "8-10 buổi điều trị",
            "steps": "✓ Điều trị mụn theo phác đồ\n✓ Peel tái tạo nhẹ\n✓ Phục hồi thâm sau mụn\n✓ Tặng bộ chăm sóc da mini",
            "price": "Từ 2,500,000đ",
            "first_time": "Dành cho da mụn trung bình đến nặng",
            "result": "Cải thiện mụn, thâm và bề mặt da rõ rệt",
            "accent": "premium",
        },
        {
            "id": "vip",
            "name": "Gói VIP",
            "sessions": "12-15 buổi điều trị",
            "steps": "✓ Theo dõi da từng tuần\n✓ Công nghệ ánh sáng cao cấp\n✓ Điều trị thâm sẹo đi kèm\n✓ Ưu tiên lịch riêng",
            "price": "Từ 3,500,000đ",
            "first_time": "Dành cho mục tiêu xử lý mụn chuyên sâu",
            "result": "Kiểm soát mụn lâu dài, giảm tái phát",
            "accent": "vip",
        },
    ],
    "massage": [
        {
            "id": "basic",
            "name": "Gói cơ bản",
            "sessions": "1 buổi thư giãn",
            "steps": "✓ Massage body 60 phút\n✓ Tinh dầu thư giãn\n✓ Chườm vai gáy",
            "price": "Từ 500,000đ",
            "first_time": "Phù hợp khách muốn thư giãn nhanh",
            "result": "Giảm căng cơ và dễ chịu sau một buổi",
            "accent": "basic",
        },
        {
            "id": "standard",
            "name": "Gói tiêu chuẩn",
            "sessions": "3 buổi thư giãn",
            "steps": "✓ Massage body chuyên sâu\n✓ Ấn huyệt giảm mỏi\n✓ Chườm thảo dược\n✓ Tặng ngâm chân",
            "price": "Từ 1,200,000đ",
            "first_time": "Phù hợp dân văn phòng hay đau mỏi",
            "result": "Cơ thể nhẹ hơn, ngủ ngon hơn",
            "accent": "standard",
        },
        {
            "id": "premium",
            "name": "Gói cao cấp",
            "sessions": "5 buổi thư giãn",
            "steps": "✓ Massage đá nóng\n✓ Giảm mỏi cổ vai gáy\n✓ Kỹ thuật viên cố định\n✓ Phòng riêng yên tĩnh",
            "price": "Từ 2,200,000đ",
            "first_time": "Phù hợp khách cần hồi phục thể lực",
            "result": "Giảm đau mỏi tích tụ và thư giãn toàn thân",
            "accent": "premium",
        },
        {
            "id": "vip",
            "name": "Gói VIP",
            "sessions": "8 buổi thư giãn",
            "steps": "✓ Massage body VIP\n✓ Đá nóng + tinh dầu nhập khẩu\n✓ Trà thảo mộc\n✓ Ưu tiên đặt phòng riêng",
            "price": "Từ 3,300,000đ",
            "first_time": "Dành cho khách muốn trải nghiệm cao cấp",
            "result": "Phục hồi năng lượng và giảm stress lâu dài",
            "accent": "vip",
        },
    ],
    "triet-long": [
        {
            "id": "basic",
            "name": "Gói cơ bản",
            "sessions": "2 buổi điều trị",
            "steps": "✓ Soi da vùng triệt\n✓ Triệt IPL cơ bản\n✓ Làm dịu sau triệt",
            "price": "Từ 2,000,000đ",
            "first_time": "Phù hợp vùng nhỏ và lần đầu trải nghiệm",
            "result": "Lông mảnh dần, giảm kích ứng bề mặt da",
            "accent": "basic",
        },
        {
            "id": "standard",
            "name": "Gói tiêu chuẩn",
            "sessions": "4 buổi điều trị",
            "steps": "✓ Triệt vùng vừa\n✓ Thoa gel lạnh phục hồi\n✓ Hướng dẫn chăm sóc sau triệt",
            "price": "Từ 3,400,000đ",
            "first_time": "Phù hợp khách muốn duy trì hiệu quả rõ hơn",
            "result": "Giảm mọc lại sau vài buổi đầu",
            "accent": "standard",
        },
        {
            "id": "premium",
            "name": "Gói cao cấp",
            "sessions": "6-8 buổi điều trị",
            "steps": "✓ Công nghệ laser/IPL nâng cao\n✓ Theo dõi chu kỳ lông\n✓ Gel phục hồi cao cấp",
            "price": "Từ 5,200,000đ",
            "first_time": "Phù hợp vùng lớn và liệu trình dài",
            "result": "Lông thưa rõ rệt và da mịn hơn",
            "accent": "premium",
        },
        {
            "id": "vip",
            "name": "Gói VIP",
            "sessions": "10-12 buổi điều trị",
            "steps": "✓ Phác đồ triệt cá nhân hóa\n✓ Ưu tiên kỹ thuật viên riêng\n✓ Chăm sóc phục hồi sau triệt",
            "price": "Từ 7,500,000đ",
            "first_time": "Dành cho khách muốn tối ưu hiệu quả lâu dài",
            "result": "Hiệu quả triệt ổn định, hạn chế mọc lại",
            "accent": "vip",
        },
    ],
    "goi-dau": [
        {
            "id": "basic",
            "name": "Gói cơ bản",
            "sessions": "1 buổi điều trị",
            "steps": "✓ Làm sạch da đầu\n✓ Gội dưỡng sinh\n✓ Sấy tạo kiểu nhẹ",
            "price": "Từ 1,300,000đ",
            "first_time": "Phù hợp da đầu dầu hoặc gàu nhẹ",
            "result": "Da đầu sạch hơn, tóc nhẹ và bồng hơn",
            "accent": "basic",
        },
        {
            "id": "standard",
            "name": "Gói tiêu chuẩn",
            "sessions": "3 buổi điều trị",
            "steps": "✓ Gội dưỡng sinh chuyên sâu\n✓ Massage da đầu\n✓ Ủ phục hồi chân tóc",
            "price": "Từ 2,100,000đ",
            "first_time": "Phù hợp khách có tóc yếu, dễ rụng",
            "result": "Giảm gàu và hỗ trợ giảm rụng tóc",
            "accent": "standard",
        },
        {
            "id": "premium",
            "name": "Gói cao cấp",
            "sessions": "5 buổi điều trị",
            "steps": "✓ Soi da đầu định kỳ\n✓ Tinh chất mọc tóc\n✓ Ủ nóng phục hồi nang tóc",
            "price": "Từ 3,600,000đ",
            "first_time": "Phù hợp da đầu nhạy cảm cần chăm kỹ",
            "result": "Da đầu khỏe hơn, tóc giảm gãy rụng",
            "accent": "premium",
        },
        {
            "id": "vip",
            "name": "Gói VIP",
            "sessions": "8 buổi điều trị",
            "steps": "✓ Liệu trình cá nhân hóa\n✓ Tinh chất cao cấp\n✓ Theo dõi tiến trình mọc tóc",
            "price": "Từ 5,200,000đ",
            "first_time": "Dành cho khách muốn đầu tư dài hạn",
            "result": "Nuôi dưỡng da đầu và cải thiện chân tóc bền hơn",
            "accent": "vip",
        },
    ],
    "sauna": [
        {
            "id": "basic",
            "name": "Gói cơ bản",
            "sessions": "1 buổi thư giãn",
            "steps": "✓ Xông hơi 30 phút\n✓ Nghỉ thư giãn\n✓ Trà nóng sau buổi",
            "price": "Từ 700,000đ",
            "first_time": "Phù hợp khách muốn thải độc nhẹ nhàng",
            "result": "Cơ thể thư giãn và dễ chịu ngay sau buổi",
            "accent": "basic",
        },
        {
            "id": "standard",
            "name": "Gói tiêu chuẩn",
            "sessions": "3 buổi thư giãn",
            "steps": "✓ Xông hơi thảo dược\n✓ Chăm sóc da sau xông\n✓ Ngâm chân thảo mộc",
            "price": "Từ 1,600,000đ",
            "first_time": "Phù hợp khách hay mệt mỏi, stress",
            "result": "Giảm căng thẳng và ngủ ngon hơn",
            "accent": "standard",
        },
        {
            "id": "premium",
            "name": "Gói cao cấp",
            "sessions": "5 buổi thư giãn",
            "steps": "✓ Sauna + massage vai gáy\n✓ Tinh dầu thư giãn\n✓ Không gian riêng tư",
            "price": "Từ 2,700,000đ",
            "first_time": "Phù hợp khách cần phục hồi thể trạng",
            "result": "Giải tỏa áp lực và phục hồi năng lượng tốt hơn",
            "accent": "premium",
        },
        {
            "id": "vip",
            "name": "Gói VIP",
            "sessions": "8 buổi thư giãn",
            "steps": "✓ Sauna VIP\n✓ Phòng riêng sang trọng\n✓ Chăm sóc cơ thể toàn diện",
            "price": "Từ 4,100,000đ",
            "first_time": "Dành cho khách muốn trải nghiệm cao cấp",
            "result": "Thư giãn sâu và duy trì thể trạng cân bằng",
            "accent": "vip",
        },
    ],
}

BOOKING_BASE_SLOTS = [
    "08:30",
    "09:30",
    "10:30",
    "13:00",
    "14:00",
    "15:30",
    "16:30",
    "18:00",
]

BOOKING_LIMITED_DAYS = {2, 5, 8, 11, 15, 18, 21}


def _get_booking_reference_data():
    services = [dict(item) for item in BOOKING_SERVICES]
    packages_by_service = {
        service_id: [dict(package) for package in package_list]
        for service_id, package_list in BOOKING_PACKAGES_BY_SERVICE.items()
    }
    package_lookup = {
        service_id: {item["id"]: item for item in package_list}
        for service_id, package_list in packages_by_service.items()
    }
    return services, packages_by_service, {item["id"]: item for item in services}, package_lookup


def _build_booking_schedule(today):
    slot_map = {}
    available_dates = set()

    booked_pairs = set(
        Appointment.objects.exclude(status='cancelled')
        .filter(appointment_date__gte=today, appointment_date__lte=today + timedelta(days=21))
        .values_list('appointment_date', 'appointment_time')
    )

    for offset in range(0, 22):
        current_day = today + timedelta(days=offset)
        iso_day = current_day.isoformat()
        is_closed = current_day.weekday() == 6
        slots = []

        for slot in BOOKING_BASE_SLOTS:
            slot_time = parse_time(slot)
            disabled = is_closed or (current_day, slot_time) in booked_pairs
            if offset in BOOKING_LIMITED_DAYS and slot in {"08:30", "18:00"}:
                disabled = True
            slots.append({"label": slot, "disabled": disabled})

        if any(not item["disabled"] for item in slots):
            available_dates.add(iso_day)
        slot_map[iso_day] = slots

    return slot_map, available_dates


def _build_booking_context(request):
    today = date.today()
    calendar_builder = Calendar(firstweekday=0)
    services, packages_by_service, _, _ = _get_booking_reference_data()
    slot_map, available_dates = _build_booking_schedule(today)

    calendar_days = []
    for week in calendar_builder.monthdatescalendar(today.year, today.month):
        for day_item in week:
            iso_day = day_item.isoformat()
            in_month = day_item.month == today.month
            disabled = (not in_month) or day_item < today or iso_day not in available_dates
            calendar_days.append(
                {
                    "iso": iso_day,
                    "day": day_item.day,
                    "disabled": disabled,
                    "is_today": day_item == today,
                }
            )

    profile = getattr(request.user, "profile", None)
    history_queryset = request.user.appointments.order_by('-appointment_date', '-appointment_time')[:6] if request.user.pk else []
    history = [
        {
            "service": item.service_name,
            "schedule": f"{item.appointment_date.strftime('%d/%m/%Y')} - {item.appointment_time.strftime('%H:%M')}",
            "status": {
                'confirmed': 'Đã xác nhận',
                'pending': 'Chờ xác nhận',
                'cancelled': 'Đã hủy',
            }.get(item.status, item.get_status_display()),
        }
        for item in history_queryset
    ]

    return {
        "services": services,
        "packages_by_service": packages_by_service,
        "calendar_days": calendar_days,
        "time_slots_by_date": slot_map,
        "current_month_label": today.strftime("%m/%Y"),
        "history": history,
        "customer_info": {
            "full_name": request.user.get_full_name() or request.user.first_name or request.user.username,
            "email": request.user.email,
            "phone": getattr(profile, "phone", "") or "Chưa cập nhật",
            "address": getattr(profile, "address", "") or "Chưa cập nhật",
            "note": "Thông tin này được lấy từ tài khoản khách hàng hiện tại.",
        },
    }

CONSULTATION_FAQS = [
    {
        "question": "Da nhạy cảm có thể làm liệu trình massage hoặc chăm sóc mặt không?",
        "answer": "Chúng tôi có các liệu trình dành riêng cho da nhạy cảm, sử dụng sản phẩm dịu nhẹ, không gây kích ứng và nhân viên sẽ tư vấn trước khi thực hiện.",
    },
    {
        "question": "Liệu trình làm trắng da có an toàn cho da nhạy cảm không?",
        "answer": "Spa sử dụng sản phẩm chuyên dụng cho da nhạy cảm và kỹ thuật viên được đào tạo để giảm nguy cơ kích ứng. Khách hàng sẽ được thử một vùng nhỏ trước khi tiến hành toàn bộ liệu trình.",
    },
    {
        "question": "Sau khi lăn kim hoặc peel da, tôi cần bao lâu để da phục hồi hoàn toàn?",
        "answer": "Thời gian phục hồi tùy vào cơ địa và độ sâu của liệu trình. Thông thường da sẽ hồi phục từ 3 đến 7 ngày. Nhân viên sẽ hướng dẫn cách chăm sóc tại nhà để da hồi phục nhanh và hiệu quả.",
    },
    {
        "question": "Tôi chưa từng đi spa, nên bắt đầu từ gói nào?",
        "answer": "Nếu bạn mới bắt đầu, nên chọn gói cơ bản hoặc gói tiêu chuẩn để được soi da, tư vấn tình trạng hiện tại và xây dựng liệu trình phù hợp.",
    },
    {
        "question": "Spa có nhận tư vấn điều trị mụn cho nam không?",
        "answer": "Có. Spa tiếp nhận cả khách nam và nữ, đặc biệt với các liệu trình điều trị mụn, chăm sóc da dầu và phục hồi da sau mụn.",
    },
    {
        "question": "Triệt lông có cần theo đúng lịch hẹn không?",
        "answer": "Nên đi đúng lịch để bám theo chu kỳ phát triển của sợi lông. Làm đúng buổi sẽ giúp hiệu quả ổn định và giảm số buổi phát sinh.",
    },
    {
        "question": "Tôi có thể đổi lịch hẹn sau khi đã đặt không?",
        "answer": "Có thể. Bạn nên báo sớm để spa hỗ trợ sắp xếp lại khung giờ phù hợp và giữ trải nghiệm dịch vụ tốt nhất.",
    },
    {
        "question": "Spa có tư vấn chăm sóc da tại nhà sau liệu trình không?",
        "answer": "Có. Sau mỗi liệu trình, kỹ thuật viên sẽ hướng dẫn routine cơ bản tại nhà, cách dùng sản phẩm và các lưu ý để duy trì hiệu quả.",
    },
    {
        "question": "Nếu tôi đang có mụn viêm nặng thì có nên tự chọn dịch vụ không?",
        "answer": "Bạn vẫn có thể gửi tin nhắn trước cho spa. Nhân viên sẽ đánh giá sơ bộ và hướng bạn sang đúng gói trị mụn hoặc lịch soi da phù hợp.",
    },
]


def _get_auto_consultation_reply(message):
    lowered = message.lower()
    if 'mụn' in lowered:
        return "Spa có các gói điều trị mụn từ cơ bản đến chuyên sâu. Bạn có thể cho bên mình biết tình trạng da hiện tại để tư vấn kỹ hơn."
    if 'giá' in lowered or 'bao nhiêu' in lowered:
        return "Mỗi dịch vụ sẽ có nhiều gói giá khác nhau. Bạn có thể nói rõ dịch vụ quan tâm để spa gửi mức giá phù hợp nhất."
    if 'đặt lịch' in lowered or 'lịch' in lowered:
        return "Bạn có thể đặt lịch trực tiếp trên website ở mục Đặt lịch hẹn. Nếu cần, spa cũng có thể hỗ trợ giữ chỗ qua khung chat này."
    if 'triệt lông' in lowered:
        return "Triệt lông bên mình có các gói theo vùng và số buổi. Spa sẽ tư vấn theo vùng cần làm để báo giá và số buổi phù hợp."
    if 'massage' in lowered:
        return "Spa có nhiều gói massage thư giãn và phục hồi. Bạn muốn massage body thư giãn hay tập trung vai gáy để spa gợi ý đúng hơn?"
    return "Chào bạn, Mai Trâm Spa đã nhận được câu hỏi. Nhân viên tư vấn sẽ hỗ trợ bạn chi tiết hơn trong khung chat này."


@login_required(login_url='login')
def service_dashboard(request):
    services = [
        {
            "name": "Chăm sóc da mặt cao cấp",
            "description": "Liệu trình chăm sóc chuyên sâu với công nghệ Hàn Quốc",
            "price": "1.000.000",
            "status": "Hoạt động",
            "image_class": "peach",
        },
        {
            "name": "Massage body thư giãn",
            "description": "Massage toàn thân với tinh dầu thiên nhiên",
            "price": "800.000",
            "status": "Hoạt động",
            "image_class": "amber",
        },
        {
            "name": "Triệt lông công nghệ Diode",
            "description": "Công nghệ triệt lông vĩnh viễn an toàn",
            "price": "800.000",
            "status": "Hoạt động",
            "image_class": "sun",
        },
        {
            "name": "Gội đầu dưỡng sinh",
            "description": "Liệu trình chăm sóc tóc và da đầu",
            "price": "300.000",
            "status": "Hoạt động",
            "image_class": "sea",
        },
        {
            "name": "Trị mụn chuyên sâu",
            "description": "Làm sạch, lấy nhân mụn, phục hồi da",
            "price": "800.000",
            "status": "Hoạt động",
            "image_class": "rose",
        },
        {
            "name": "Acne Detox Therapy",
            "description": "Thanh lọc da mụn, làm sạch sâu lỗ chân lông",
            "price": "950.000",
            "status": "Hoạt động",
            "image_class": "mint",
        },
        {
            "name": "Post-Acne Recovery Therapy",
            "description": "Phục hồi da sau mụn, giảm thâm sẹo",
            "price": "1.200.000",
            "status": "Hoạt động",
            "image_class": "violet",
        },
    ]
    return render(request, "service_dashboard.html", {"services": services})


@login_required(login_url='login')
def appointment_dashboard(request):
    appointments = [
        {
            "id": 1,
            "customer": "Nguyễn Thị Trà My",
            "phone": "0901234567",
            "service": "Trị mụn chuyên sâu",
            "date": "25/02/2026",
            "time": "16:00",
            "status": "Đang Tiến Hành",
            "status_class": "green",
            "note": "Khách yêu cầu phòng riêng",
        },
        {
            "id": 2,
            "customer": "Phạm Thị Hoài",
            "phone": "0905050323",
            "service": "Triệt lông công nghệ Diode",
            "date": "10/02/2026",
            "time": "9:00",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Đã hoàn tất liệu trình theo lịch đặt",
        },
        {
            "id": 3,
            "customer": "Võ Bích Hợp",
            "phone": "0328775385",
            "service": "Gội đầu dưỡng sinh",
            "date": "10/02/2026",
            "time": "13:00",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Khách thanh toán tại quầy",
        },
        {
            "id": 4,
            "customer": "Nguyễn Thị Hoa",
            "phone": "0384726564",
            "service": "Post-Acne Recovery Therapy",
            "date": "11/02/2026",
            "time": "9:00",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Khách đặt lại lịch tái khám",
        },
        {
            "id": 5,
            "customer": "Lê Thị Bé Như",
            "phone": "0376258537",
            "service": "Acne Detox Therapy",
            "date": "11/02/2026",
            "time": "13:00",
            "status": "Đã Hủy",
            "status_class": "red",
            "note": "Khách báo hủy trước 2 giờ",
        },
        {
            "id": 6,
            "customer": "Nguyễn Cao Sang",
            "phone": "0387642458",
            "service": "Acne Detox Therapy",
            "date": "12/02/2026",
            "time": "13:00",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Khách yêu cầu xuất hóa đơn",
        },
        {
            "id": 7,
            "customer": "Đoàn Thanh Nhã",
            "phone": "0927462684",
            "service": "Post-Acne Recovery Therapy",
            "date": "9/02/2026",
            "time": "7:00",
            "status": "Đã Hủy",
            "status_class": "red",
            "note": "Khách đến trễ nên lịch bị hủy",
        },
    ]
    modal_state = request.GET.get("modal", "")
    return render(
        request,
        "appointment_dashboard.html",
        {
            "appointments": appointments,
            "modal_state": modal_state,
        },
    )


@login_required(login_url='login')
def customer_dashboard(request):
    customers = [
        {"id": 1, "name": "Nguyễn Thị Lan", "gender": "Nữ", "phone": "0901234567", "points": "500 điểm"},
        {"id": 2, "name": "Phạm Thị Hoài", "gender": "Nữ", "phone": "0905050323", "points": "200 điểm"},
        {"id": 3, "name": "Võ Bích Hợp", "gender": "Nữ", "phone": "0328775385", "points": "1.000 điểm"},
        {"id": 4, "name": "Nguyễn Thị Hoa", "gender": "Nữ", "phone": "0384726564", "points": "300 điểm"},
        {"id": 5, "name": "Lê Thị Bé Như", "gender": "Nữ", "phone": "0376258537", "points": "600 điểm"},
        {"id": 6, "name": "Nguyễn Cao Sang", "gender": "Nam", "phone": "0387642458", "points": "100 điểm"},
        {"id": 7, "name": "Đoàn Thanh Nhã", "gender": "Nam", "phone": "0927462684", "points": "100 điểm"},
    ]
    return render(request, "customer_dashboard.html", {"customers": customers})


@login_required(login_url='login')
def customer_detail(request, customer_id):
    customer = {
        "id": customer_id,
        "name": "Nguyễn Thị Lan",
        "gender": "Nữ",
        "age": "32",
        "email": "nguyenlanvn@gmail.com",
        "address": "Mỹ An, Ngũ Hành Sơn, TP Đà Nẵng",
        "history": [
            {
                "date": "30/01/2026",
                "service": "Chăm sóc da mặt cao cấp",
                "status": "Hoàn Thành",
                "price": "1.000.000",
            },
            {
                "date": "11/02/2026",
                "service": "Post-Acne Recovery Therapy",
                "status": "Hoàn Thành",
                "price": "1.200.000",
            },
        ],
    }
    return render(request, "customer_detail.html", {"customer": customer})


@login_required(login_url='login')
def feedback_dashboard(request):
    feedbacks = [
        {
            "id": 1,
            "name": "Hương Nguyễn",
            "time": "3 ngày trước",
            "service": "Chăm sóc da mặt Collagen",
            "rating": "5.0",
            "status": "Đã phản hồi",
            "status_class": "green",
            "content": "Mình rất hài lòng với dịch vụ chăm sóc da tại Mai Trâm! Chuyên viên tư vấn rất tận tình, quy trình làm chuyên nghiệp. Da mình sau liệu trình sáng mịn hơn, mụn cũng giảm đáng kể. Không gian cũng rất sang trọng và thư giãn. Chắc chắn sẽ quay lại!",
            "avatar_class": "avatar-peach",
        },
        {
            "id": 2,
            "name": "Luyện Đặng",
            "time": "19/01/2025",
            "service": "Massage body thư giãn",
            "rating": "4.0",
            "status": "Chưa phản hồi",
            "status_class": "yellow",
            "content": "Dịch vụ massage rất tốt! Nhân viên massage chuyên nghiệp, lực tay vừa phải. Tinh dầu thơm nhẹ nhàng không gây kích ứng. Sau 60 phút massage, cơ thể mình thư giãn hẳn, giảm đau mỏi vai gáy rất nhiều. Giá cả hợp lý, spa sạch sẽ thoáng mát.",
            "avatar_class": "avatar-neutral",
        },
        {
            "id": 3,
            "name": "Tuyết Sương",
            "time": "1 năm trước",
            "service": "Triệt lông Laser Diode",
            "rating": "4.0",
            "status": "Đã phản hồi",
            "status_class": "green",
            "content": "Dịch vụ triệt lông ổn, máy móc hiện đại. Nhân viên tư vấn kỹ về quy trình và số buổi cần thiết. Có điều mình thấy thời gian chờ hơi lâu một chút. Nhưng nhìn chung thì dịch vụ tốt, sau 3 buổi thấy lông mọc thưa hơn hẳn.",
            "avatar_class": "avatar-rose",
        },
    ]
    return render(request, "feedback_dashboard.html", {"feedbacks": feedbacks})


@login_required(login_url='login')
def consultation_page(request):
    profile = getattr(request.user, 'profile', None)
    if profile and profile.role == 'staff':
        return redirect('consultation_dashboard')

    conversation, _ = ConsultationConversation.objects.get_or_create(
        user=request.user,
        status='open',
        defaults={'subject': 'Tư vấn dịch vụ Mai Trâm'},
    )

    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        if not content:
            messages.error(request, 'Vui lòng nhập nội dung trước khi gửi tư vấn.')
        else:
            ConsultationMessage.objects.create(
                conversation=conversation,
                sender='customer',
                content=content,
            )
            ConsultationMessage.objects.create(
                conversation=conversation,
                sender='spa',
                content=_get_auto_consultation_reply(content),
            )
            return redirect(f"{request.path}?chat=1")

    chat_messages = list(conversation.messages.all())
    context = {
        "faqs": CONSULTATION_FAQS,
        "chat_messages": chat_messages,
        "chat_open": request.GET.get('chat') == '1' or bool(chat_messages),
    }
    return render(request, "consultation.html", context)


@login_required(login_url='login')
def consultation_dashboard(request):
    conversations = [
        {
            "id": 1,
            "name": "Mai Hồng Ngọc",
            "avatar_class": "chat-avatar-one",
            "preview": "Cho em hỏi về dịch vụ bên mình bao nhiêu......",
            "time": "19:30",
        },
        {
            "id": 2,
            "name": "Trần Thiên Hà",
            "avatar_class": "avatar-neutral",
            "preview": "Shop ơi tư vấn này giúp e với .....",
            "time": "Hôm qua",
        },
        {
            "id": 3,
            "name": "Ngô Thanh Vân",
            "avatar_class": "chat-avatar-two",
            "preview": "Shop ơi tư vấn này giúp e với .....",
            "time": "23/01/2026",
        },
        {
            "id": 4,
            "name": "Lê Thư Ý",
            "avatar_class": "chat-avatar-three",
            "preview": "Shop ơi",
            "time": "23/01/2026",
        },
        {
            "id": 5,
            "name": "Lê Trà Thư",
            "avatar_class": "avatar-neutral",
            "preview": "Ngày mai nha",
            "time": "23/01/2026",
        },
    ]
    search = request.GET.get("q", "").strip()
    empty_state = request.GET.get("empty", "") == "1"
    if search:
        lowered = search.lower()
        conversations = [item for item in conversations if lowered in item["name"].lower()]
    if empty_state:
        conversations = []
    return render(
        request,
        "consultation_dashboard.html",
        {
            "conversations": conversations,
            "search": search,
        },
    )


@login_required(login_url='login')
def consultation_detail(request, conversation_id):
    conversations = {
        1: {
            "id": 1,
            "name": "Mai Hồng Ngọc",
            "avatar_class": "chat-avatar-one",
            "messages": [
                {"side": "left", "text": "Cho em hỏi về dịch vụ bên mình bao nhiêu......", "time": "19:30"},
            ],
        },
        2: {
            "id": 2,
            "name": "Trần Thiên Hà",
            "avatar_class": "avatar-neutral",
            "messages": [
                {"side": "left", "text": "Shop ơi tư vấn này giúp e với .....", "time": "Hôm qua"},
            ],
        },
        3: {
            "id": 3,
            "name": "Ngô Thanh Vân",
            "avatar_class": "chat-avatar-two",
            "messages": [
                {"divider": "Hôm qua 19:45"},
                {"side": "left", "text": "Shop ơi tư vấn này giúp e với về gói chăm da với", "time": ""},
                {
                    "side": "right",
                    "text": "Chào mừng bạn đến với dịch vụ Mai Trâm, bạn vui lòng đợi một chút sẽ có nhân viên tư vấn cho bạn ạ!",
                    "time": "19:45",
                },
                {"divider": "10:50"},
                {"side": "left", "text": "Shop ơi tư vấn ạ", "time": ""},
                {"side": "right", "text": "Em đây ạ", "time": "10:52"},
            ],
        },
        4: {
            "id": 4,
            "name": "Lê Thư Ý",
            "avatar_class": "chat-avatar-three",
            "messages": [
                {"side": "left", "text": "Shop ơi", "time": "23/01/2026"},
            ],
        },
        5: {
            "id": 5,
            "name": "Lê Trà Thư",
            "avatar_class": "avatar-neutral",
            "messages": [
                {"side": "left", "text": "Ngày mai nha", "time": "23/01/2026"},
            ],
        },
    }
    conversation = conversations.get(conversation_id, conversations[3])
    modal_state = request.GET.get("modal", "")
    return render(
        request,
        "consultation_detail.html",
        {
            "conversation": conversation,
            "modal_state": modal_state,
        },
    )


@login_required(login_url='login')
def feedback_detail(request, feedback_id):
    feedback = {
        "id": feedback_id,
        "name": "Luyện Đặng",
        "date": "19/01/2025",
        "service": "Massage body thư giãn",
        "rating": "4.0",
        "status": "Chưa phản hồi",
        "content": "Dịch vụ massage rất tốt! Nhân viên massage chuyên nghiệp, lực tay vừa phải. Tinh dầu thơm nhẹ nhàng không gây kích ứng. Sau 60 phút massage, cơ thể mình thư giãn hẳn, giảm đau mỏi vai gáy rất nhiều. Giá cả hợp lý, spa sạch sẽ thoáng mát.",
    }
    return render(request, "feedback_detail.html", {"feedback": feedback})


@login_required(login_url='login')
def booking(request):
    profile = getattr(request.user, 'profile', None)
    if profile and profile.role == 'staff':
        return redirect('appointment_dashboard')

    services, packages_by_service, service_lookup, package_lookup = _get_booking_reference_data()
    if request.method == 'POST':
        service_id = request.POST.get('service_id', '').strip()
        package_id = request.POST.get('package_id', '').strip()
        date_value = parse_date(request.POST.get('appointment_date', '').strip())
        time_value = parse_time(request.POST.get('appointment_time', '').strip())

        selected_service = service_lookup.get(service_id)
        selected_package = package_lookup.get(service_id, {}).get(package_id)
        slot_map, available_dates = _build_booking_schedule(date.today())
        selected_date_key = date_value.isoformat() if date_value else ''
        available_slots = {item['label'] for item in slot_map.get(selected_date_key, []) if not item['disabled']}

        if not selected_service or not selected_package:
            messages.error(request, 'Vui lòng chọn đầy đủ dịch vụ và gói điều trị.')
        elif not date_value or not time_value:
            messages.error(request, 'Vui lòng chọn ngày và giờ hẹn hợp lệ.')
        elif date_value < date.today() or selected_date_key not in available_dates:
            messages.error(request, 'Ngày hẹn này không còn khả dụng.')
        elif time_value.strftime('%H:%M') not in available_slots:
            messages.error(request, 'Khung giờ này đã được đặt hoặc không khả dụng.')
        else:
            try:
                Appointment.objects.create(
                    user=request.user,
                    service_id=selected_service['id'],
                    service_name=selected_service['name'],
                    package_id=selected_package['id'],
                    package_name=selected_package['name'],
                    package_sessions=selected_package['sessions'],
                    package_price=selected_package['price'],
                    package_result=selected_package['result'],
                    appointment_date=date_value,
                    appointment_time=time_value,
                    status='confirmed',
                )
            except IntegrityError:
                messages.error(request, 'Khung giờ vừa được người khác đặt mất. Vui lòng chọn lại.')
            else:
                messages.success(request, 'Đặt lịch thành công. Hệ thống đã lưu lịch hẹn của bạn.')
                return redirect('booking')

    context = _build_booking_context(request)
    context['services'] = services
    context['packages_by_service'] = packages_by_service
    return render(request, 'booking.html', context)
