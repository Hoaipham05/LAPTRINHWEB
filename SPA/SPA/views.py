from django.shortcuts import render


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
