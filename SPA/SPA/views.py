from datetime import date, timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomerProfileForm, LoginForm, RegisterForm
from services.models import CustomerProfile, Service


def redirect_by_role(request):
    if not request.user.is_authenticated:
        return redirect("about_page")
    if request.user.is_staff:
        return redirect("service_dashboard")
    return redirect("customer_account")


def manager_required(view_func):
    @login_required(login_url="user_login")
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.warning(request, "Trang nay chi danh cho quan ly.")
            return redirect("customer_account")
        return view_func(request, *args, **kwargs)

    return wrapped


def customer_required(view_func):
    @login_required(login_url="user_login")
    def wrapped(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect("service_dashboard")
        return view_func(request, *args, **kwargs)

    return wrapped


def home_entry(request):
    return redirect_by_role(request)


def format_service_price(value):
    return f"{value:,}".replace(",", ".")


def category_label(category):
    labels = {
        Service.CATEGORY_FACE: "Da mat",
        Service.CATEGORY_BODY: "Body",
        Service.CATEGORY_HAIR: "Triet long",
    }
    return labels.get(category, category)


def serialize_service(service):
    return {
        "id": service.id,
        "name": service.name,
        "slug": service.slug,
        "short_description": service.short_description,
        "description": service.description,
        "category": service.category,
        "category_label": category_label(service.category),
        "duration_minutes": service.duration_minutes,
        "price": service.price,
        "price_label": format_service_price(service.price),
        "rating": service.rating,
        "image_url": service.image_url,
        "status": service.status,
    }


def build_customer_history():
    return [
        {
            "date": "12/03/2026",
            "service": "Cham soc da mat Collagen",
            "status": "Hoan thanh",
            "price": "1.200.000d",
        },
        {
            "date": "27/02/2026",
            "service": "Massage body thu gian",
            "status": "Hoan thanh",
            "price": "500.000d",
        },
        {
            "date": "08/02/2026",
            "service": "Tri mun chuyen sau",
            "status": "Hoan thanh",
            "price": "800.000d",
        },
    ]


def get_public_reviews():
    return [
        {
            "name": "Nguyễn Hà My",
            "time": "2 ngày trước",
            "rating": 5,
            "service": "Chăm sóc da mặt chuyên sâu",
            "content": "Không gian spa sang và thoáng. Kỹ thuật viên soi da kỹ, làm rất nhẹ tay và tư vấn routine sau liệu trình rõ ràng. Da mình đều màu và mềm hơn chỉ sau một buổi.",
            "image_urls": [
                "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=900&q=80",
                "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=900&q=80",
            ],
        },
        {
            "name": "Trần Khánh Linh",
            "time": "5 ngày trước",
            "rating": 5,
            "service": "Gội đầu dưỡng sinh",
            "content": "Mùi tinh dầu dễ chịu, phòng làm việc sạch và yên tĩnh. Phần massage đầu vai gáy rất đã, đúng kiểu dịch vụ để quay lại sau những ngày làm việc căng thẳng.",
            "image_urls": [],
        },
        {
            "name": "Lê Bảo Ngọc",
            "time": "1 tuần trước",
            "rating": 4,
            "service": "Post-Acne Recovery Therapy",
            "content": "Liệu trình phục hồi sau mụn làm mình hài lòng. Độ đỏ giảm rõ, da được hướng dẫn chăm sóc tại nhà khá chi tiết. Nếu có thêm gói combo thì sẽ rất hợp lý.",
            "image_urls": [
                "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=900&q=80",
            ],
        },
        {
            "name": "Phạm Thu Hằng",
            "time": "2 tuần trước",
            "rating": 5,
            "service": "Massage body thư giãn",
            "content": "Phòng hương nhẹ, nhạc vừa đủ và thao tác rất chuyên nghiệp. Sau 60 phút massage mình thấy cơ thể được thả lỏng hoàn toàn. Trải nghiệm đồng đều từ lúc check-in đến lúc ra về.",
            "image_urls": [],
        },
        {
            "name": "Võ Minh Anh",
            "time": "3 tuần trước",
            "rating": 4,
            "service": "Triệt lông công nghệ Diode",
            "content": "Máy móc mới, nhân viên giải thích quy trình kỹ và nhắc lịch tái khám đầy đủ. Lần đầu hơi hồi hộp nhưng làm xong thấy yên tâm. Hiệu quả cần thêm vài buổi nữa để đánh giá trọn vẹn.",
            "image_urls": [
                "https://images.unsplash.com/photo-1519415943484-9fa1873496d4?auto=format&fit=crop&w=900&q=80",
                "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=900&q=80",
                "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80",
            ],
        },
        {
            "name": "Đoàn Ngọc Thảo",
            "time": "1 tháng trước",
            "rating": 5,
            "service": "Acne Detox Therapy",
            "content": "Mình đánh giá cao cách spa theo dõi da trước và sau buổi trị liệu. Phong cách phục vụ lịch sự, sạch sẽ và không bị tạo cảm giác bán hàng quá đà. Sẽ giới thiệu thêm bạn bè.",
            "image_urls": [],
        },
    ]


def user_login(request):
    """Xử lý đăng nhập người dùng"""
    if request.user.is_authenticated:
        return redirect_by_role(request)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)

                if user is not None:
                    login(request, user)
                    messages.success(request, f'Chào mừng {user.first_name or user.username}!')
                    # Nếu là admin/staff, vào service_dashboard
                    if user.is_staff:
                        return redirect('service_dashboard')
                    # Nếu là người dùng thường, vào customer_dashboard
                    return redirect('customer_account')
                else:
                    messages.error(request, 'Mật khẩu không chính xác.')
            except User.DoesNotExist:
                messages.error(request, 'Email này không tồn tại.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def user_register(request):
    """Xử lý đăng ký tài khoản người dùng"""
    if request.user.is_authenticated:
        return redirect_by_role(request)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('email')
            user.save()
            CustomerProfile.objects.get_or_create(
                user=user,
                defaults={
                    "full_name": f"{user.last_name} {user.first_name}".strip(),
                    "member_since": user.date_joined.date(),
                    "loyalty_points": 120,
                    "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80",
                },
            )

            messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
            return redirect('user_login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_logout(request):
    """Xử lý đăng xuất"""
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất thành công!')
    return redirect('user_login')


@manager_required
def service_dashboard(request):
    services = [
        {
            "name": "Chăm sóc da mặt cao cấp",
            "description": "Liệu trình chăm sóc chuyên sâu với công nghệ Hàn Quốc",
            "price": "1.000.000",
            "status": "Hoạt động",
            "image_class": "peach",
            "image_url": "https://tourdanangcity.vn/wp-content/uploads/2024/06/review-spa-hoi-an.jpg",
        },
        {
            "name": "Massage body thư giãn",
            "description": "Massage toàn thân với tinh dầu thiên nhiên",
            "price": "800.000",
            "status": "Hoạt động",
            "image_class": "amber",
            "image_url": "https://dynamic-media-cdn.tripadvisor.com/media/photo-o/12/63/9f/04/sakura-massage-spa.jpg?w=900&h=500&s=1",
        },
        {
            "name": "Triệt lông công nghệ Diode",
            "description": "Công nghệ triệt lông vĩnh viễn an toàn",
            "price": "800.000",
            "status": "Hoạt động",
            "image_class": "sun",
            "image_url": "https://images.virginexperiencedays.co.uk/images/product/large/mychocolate-chocoholic-workshop-with-29145629.jpg?auto=compress%2Cformat&w=1440&q=80&fit=max",
        },
        {
            "name": "Gội đầu dưỡng sinh",
            "description": "Liệu trình chăm sóc tóc và da đầu",
            "price": "300.000",
            "status": "Hoạt động",
            "image_class": "sea",
            "image_url": "https://static.vinwonders.com/production/2025/09/spa-ha-noi-topbanner.jpg",
        },
        {
            "name": "Trị mụn chuyên sâu",
            "description": "Làm sạch, lấy nhân mụn, phục hồi da",
            "price": "800.000",
            "status": "Hoạt động",
            "image_class": "rose",
            "image_url": "https://static.hotdeal.vn/images/1535/1534508/60x60/349662-dang-cap-massage-bau-5-thu-gian-toan-than-cho-me-khoe-be-thong-minh-tai-bloomy-spa.jpg",
        },
        {
            "name": "Acne Detox Therapy",
            "description": "Thanh lọc da mụn, làm sạch sâu lỗ chân lông",
            "price": "950.000",
            "status": "Hoạt động",
            "image_class": "mint",
            "image_url": "https://file.hstatic.net/200000827051/article/facial_treatment_f73cebb667794301afd01348897774e7.jpg",
        },
        {
            "name": "Post-Acne Recovery Therapy",
            "description": "Phục hồi da sau mụn, giảm thâm sẹo",
            "price": "1.200.000",
            "status": "Hoạt động",
            "image_class": "violet",
            "image_url": "https://hd1.hotdeal.vn/images/uploads/2016/Thang%208/31/285824/285824-dung-spa-body%20%289%29.jpg",
        },
    ]
    return render(request, "service_dashboard.html", {"services": services})


@manager_required
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
        {
            "id": 8,
            "customer": "Trần Thị Yến",
            "phone": "0912345678",
            "service": "Chăm sóc da mặt cao cấp",
            "date": "15/02/2026",
            "time": "10:00",
            "status": "Đang Tiến Hành",
            "status_class": "green",
            "note": "Khách sử dụng voucher giảm 20%",
        },
        {
            "id": 9,
            "customer": "Lương Thị Nhà",
            "phone": "0923456789",
            "service": "Massage body thư giãn",
            "date": "14/02/2026",
            "time": "14:30",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Khách thanh toán bằng thẻ",
        },
        {
            "id": 10,
            "customer": "Ngô Hồng Duyên",
            "phone": "0934567890",
            "service": "Triệt lông công nghệ Diode",
            "date": "13/02/2026",
            "time": "11:00",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Liệu trình 5 buổi, hoàn tất buổi thứ 3",
        },
        {
            "id": 11,
            "customer": "Bùi Thị Mỹ",
            "phone": "0945678901",
            "service": "Gội đầu dưỡng sinh",
            "date": "16/02/2026",
            "time": "15:00",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Khách mua thêm tinh dầu",
        },
        {
            "id": 12,
            "customer": "Đỗ Quỳnh Anh",
            "phone": "0956789012",
            "service": "Post-Acne Recovery Therapy",
            "date": "17/02/2026",
            "time": "9:30",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Khách yêu cầu tư vấn thêm",
        },
        {
            "id": 13,
            "customer": "Vũ Thị Hương",
            "phone": "0967890123",
            "service": "Acne Detox Therapy",
            "date": "18/02/2026",
            "time": "16:00",
            "status": "Đang Tiến Hành",
            "status_class": "green",
            "note": "Khách lần đầu đến",
        },
        {
            "id": 14,
            "customer": "Trịnh Thị Loan",
            "phone": "0978901234",
            "service": "Chăm sóc da mặt cao cấp",
            "date": "19/02/2026",
            "time": "13:00",
            "status": "Đã Hủy",
            "status_class": "red",
            "note": "Khách hủy 1 giờ trước",
        },
        {
            "id": 15,
            "customer": "Phan Thị Thảo",
            "phone": "0989012345",
            "service": "Massage body thư giãn",
            "date": "20/02/2026",
            "time": "10:30",
            "status": "Hoàn Thành",
            "status_class": "blue",
            "note": "Khách đặt lịch tiếp tục",
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


@manager_required
def customer_dashboard(request):
    customers = [
        {
            "id": 1, 
            "name": "Nguyễn Thị Lan", 
            "gender": "Nữ", 
            "age": "32",
            "phone": "0901234567", 
            "points": "500 điểm",
            "email": "nguyen.lan@email.com",
            "address": "Mỹ An, Ngũ Hành Sơn, TP Đà Nẵng",
            "history": [
                {"date": "30/01/2026", "service": "Chăm sóc da mặt cao cấp", "status": "Hoàn Thành", "price": "1.000.000"},
                {"date": "15/02/2026", "service": "Post-Acne Recovery Therapy", "status": "Hoàn Thành", "price": "1.200.000"},
            ]
        },
        {
            "id": 2, 
            "name": "Phạm Thị Hoài", 
            "gender": "Nữ", 
            "age": "28",
            "phone": "0905050323", 
            "points": "200 điểm",
            "email": "pham.hoai@email.com",
            "address": "Thanh Khê, TP Đà Nẵng",
            "history": [
                {"date": "10/02/2026", "service": "Triệt lông công nghệ Diode", "status": "Hoàn Thành", "price": "800.000"},
            ]
        },
        {
            "id": 3, 
            "name": "Võ Bích Hợp", 
            "gender": "Nữ", 
            "age": "35",
            "phone": "0328775385", 
            "points": "1.000 điểm",
            "email": "vo.bich@email.com",
            "address": "Hải Châu, TP Đà Nẵng",
            "history": [
                {"date": "10/02/2026", "service": "Gội đầu dưỡng sinh", "status": "Hoàn Thành", "price": "300.000"},
                {"date": "20/02/2026", "service": "Massage body thư giãn", "status": "Hoàn Thành", "price": "800.000"},
            ]
        },
        {
            "id": 4, 
            "name": "Nguyễn Thị Hoa", 
            "gender": "Nữ", 
            "age": "26",
            "phone": "0384726564", 
            "points": "300 điểm",
            "email": "nguyen.hoa@email.com",
            "address": "Sơn Trà, TP Đà Nẵng",
            "history": [
                {"date": "11/02/2026", "service": "Post-Acne Recovery Therapy", "status": "Hoàn Thành", "price": "1.200.000"},
            ]
        },
        {
            "id": 5, 
            "name": "Lê Thị Bé Như", 
            "gender": "Nữ", 
            "age": "30",
            "phone": "0376258537", 
            "points": "600 điểm",
            "email": "le.be.nhu@email.com",
            "address": "Liên Chiểu, TP Đà Nẵng",
            "history": [
                {"date": "05/02/2026", "service": "Acne Detox Therapy", "status": "Hoàn Thành", "price": "950.000"},
                {"date": "12/02/2026", "service": "Chăm sóc da mặt cao cấp", "status": "Hoàn Thành", "price": "1.000.000"},
            ]
        },
        {
            "id": 6, 
            "name": "Nguyễn Cao Sang", 
            "gender": "Nam", 
            "age": "29",
            "phone": "0387642458", 
            "points": "100 điểm",
            "email": "nguyen.sang@email.com",
            "address": "Cẩm Lệ, TP Đà Nẵng",
            "history": [
                {"date": "12/02/2026", "service": "Acne Detox Therapy", "status": "Hoàn Thành", "price": "950.000"},
            ]
        },
        {
            "id": 7, 
            "name": "Đoàn Thanh Nhã", 
            "gender": "Nam", 
            "age": "27",
            "phone": "0927462684", 
            "points": "100 điểm",
            "email": "doan.nha@email.com",
            "address": "Ngũ Hành Sơn, TP Đà Nẵng",
            "history": [
                {"date": "02/02/2026", "service": "Chăm sóc da mặt cao cấp", "status": "Hoàn Thành", "price": "1.000.000"},
            ]
        },
        {
            "id": 8, 
            "name": "Trần Thị Yến", 
            "gender": "Nữ", 
            "age": "31",
            "phone": "0912345678", 
            "points": "750 điểm",
            "email": "tran.yen@email.com",
            "address": "Thanh Khê, TP Đà Nẵng",
            "history": [
                {"date": "15/02/2026", "service": "Chăm sóc da mặt cao cấp", "status": "Hoàn Thành", "price": "1.000.000"},
                {"date": "18/02/2026", "service": "Acne Detox Therapy", "status": "Hoàn Thành", "price": "950.000"},
            ]
        },
        {
            "id": 9, 
            "name": "Lương Thị Nhà", 
            "gender": "Nữ", 
            "age": "24",
            "phone": "0923456789", 
            "points": "450 điểm",
            "email": "luong.nha@email.com",
            "address": "Hải Châu, TP Đà Nẵng",
            "history": [
                {"date": "14/02/2026", "service": "Massage body thư giãn", "status": "Hoàn Thành", "price": "800.000"},
            ]
        },
        {
            "id": 10, 
            "name": "Ngô Hồng Duyên", 
            "gender": "Nữ", 
            "age": "33",
            "phone": "0934567890", 
            "points": "900 điểm",
            "email": "ngo.duyen@email.com",
            "address": "Sơn Trà, TP Đà Nẵng",
            "history": [
                {"date": "13/02/2026", "service": "Triệt lông công nghệ Diode", "status": "Hoàn Thành", "price": "800.000"},
                {"date": "20/02/2026", "service": "Triệt lông công nghệ Diode", "status": "Hoàn Thành", "price": "800.000"},
            ]
        },
        {
            "id": 11, 
            "name": "Bùi Thị Mỹ", 
            "gender": "Nữ", 
            "age": "25",
            "phone": "0945678901", 
            "points": "350 điểm",
            "email": "bui.my@email.com",
            "address": "Liên Chiểu, TP Đà Nẵng",
            "history": [
                {"date": "16/02/2026", "service": "Gội đầu dưỡng sinh", "status": "Hoàn Thành", "price": "300.000"},
            ]
        },
        {
            "id": 12, 
            "name": "Đỗ Quỳnh Anh", 
            "gender": "Nữ", 
            "age": "29",
            "phone": "0956789012", 
            "points": "550 điểm",
            "email": "do.anh@email.com",
            "address": "Cẩm Lệ, TP Đà Nẵng",
            "history": [
                {"date": "17/02/2026", "service": "Post-Acne Recovery Therapy", "status": "Hoàn Thành", "price": "1.200.000"},
            ]
        },
        {
            "id": 13, 
            "name": "Vũ Thị Hương", 
            "gender": "Nữ", 
            "age": "27",
            "phone": "0967890123", 
            "points": "250 điểm",
            "email": "vu.huong@email.com",
            "address": "Thanh Khê, TP Đà Nẵng",
            "history": [
                {"date": "18/02/2026", "service": "Acne Detox Therapy", "status": "Hoàn Thành", "price": "950.000"},
            ]
        },
        {
            "id": 14, 
            "name": "Trịnh Thị Loan", 
            "gender": "Nữ", 
            "age": "34",
            "phone": "0978901234", 
            "points": "150 điểm",
            "email": "trinh.loan@email.com",
            "address": "Hải Châu, TP Đà Nẵng",
            "history": [
                {"date": "08/02/2026", "service": "Gội đầu dưỡng sinh", "status": "Hoàn Thành", "price": "300.000"},
                {"date": "15/02/2026", "service": "Triệt lông công nghệ Diode", "status": "Hoàn Thành", "price": "800.000"},
            ]
        },
        {
            "id": 15, 
            "name": "Phan Thị Thảo", 
            "gender": "Nữ", 
            "age": "28",
            "phone": "0989012345", 
            "points": "800 điểm",
            "email": "phan.thao@email.com",
            "address": "Sơn Trà, TP Đà Nẵng",
            "history": [
                {"date": "20/02/2026", "service": "Massage body thư giãn", "status": "Hoàn Thành", "price": "800.000"},
                {"date": "25/02/2026", "service": "Chăm sóc da mặt cao cấp", "status": "Hoàn Thành", "price": "1.000.000"},
            ]
        },
        {
            "id": 16, 
            "name": "Nguyễn Thanh Huyền", 
            "gender": "Nữ", 
            "age": "30",
            "phone": "0990123456", 
            "points": "420 điểm",
            "email": "nguyen.huyen@email.com",
            "address": "Liên Chiểu, TP Đà Nẵng",
            "history": [
                {"date": "14/02/2026", "service": "Acne Detox Therapy", "status": "Hoàn Thành", "price": "950.000"},
            ]
        },
        {
            "id": 17, 
            "name": "Hoàng Thị Linh", 
            "gender": "Nữ", 
            "age": "26",
            "phone": "0901111111", 
            "points": "680 điểm",
            "email": "hoang.linh@email.com",
            "address": "Cẩm Lệ, TP Đà Nẵng",
            "history": [
                {"date": "13/02/2026", "service": "Gội đầu dưỡng sinh", "status": "Hoàn Thành", "price": "300.000"},
                {"date": "19/02/2026", "service": "Triệt lông công nghệ Diode", "status": "Hoàn Thành", "price": "800.000"},
            ]
        },
        {
            "id": 18, 
            "name": "Phạm Minh Châu", 
            "gender": "Nữ", 
            "age": "32",
            "phone": "0902222222", 
            "points": "520 điểm",
            "email": "pham.chau@email.com",
            "address": "Ngũ Hành Sơn, TP Đà Nẵng",
            "history": [
                {"date": "16/02/2026", "service": "Post-Acne Recovery Therapy", "status": "Hoàn Thành", "price": "1.200.000"},
            ]
        },
        {
            "id": 19, 
            "name": "Cao Thị Phương", 
            "gender": "Nữ", 
            "age": "29",
            "phone": "0903333333", 
            "points": "380 điểm",
            "email": "cao.phuong@email.com",
            "address": "Thanh Khê, TP Đà Nẵng",
            "history": [
                {"date": "17/02/2026", "service": "Chăm sóc da mặt cao cấp", "status": "Hoàn Thành", "price": "1.000.000"},
            ]
        },
        {
            "id": 20, 
            "name": "Lê Minh Hiền", 
            "gender": "Nữ", 
            "age": "27",
            "phone": "0904444444", 
            "points": "620 điểm",
            "email": "le.hien@email.com",
            "address": "Hải Châu, TP Đà Nẵng",
            "history": [
                {"date": "18/02/2026", "service": "Massage body thư giãn", "status": "Hoàn Thành", "price": "800.000"},
                {"date": "22/02/2026", "service": "Acne Detox Therapy", "status": "Hoàn Thành", "price": "950.000"},
            ]
        },
    ]
    return render(request, "customer_dashboard.html", {"customers": customers})


@manager_required
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


@manager_required
def feedback_dashboard(request):
    # Dữ liệu mẫu cho các đánh giá
    names = [
        "Hương Nguyễn", "Luyện Đặng", "Tuyết Sương", "Linh Phương", "Quỳnh Anh",
        "Minh Hoa", "Trúc Nhan", "Thanh Vân", "Khuê Ngôn", "Hà Linh",
        "Tú Anh", "Xuân Hương", "Diệp Chi", "Vân Anh", "Hồng Nhân",
        "Thảo Vy", "Bảo Anh", "Phương Thảo", "Khánh Linh", "Minh Châu",
        "Anh Tuấn", "Bảo Ngân", "Châu Giang", "Đức Minh", "Gia Hân",
        "Hải Yến", "Ích Nhân", "Khắc Quân", "Liêu Phương", "Minh Tú",
        "Ngân Hà", "Oanh Lê", "Phúc Lâm", "Quốc Trung", "Rin Shimizu",
        "Sơn Tùng", "Trâm Anh", "Uyên Thy", "Việt Anh", "Vy Kiều",
        "Thanh Xuân", "Hương Giang", "Mỹ Duyên", "Ngọc Trinh", "Phương Oanh",
        "Quỳnh Như", "Thủy Tiên", "Vy Oanh", "Xuan Hương", "Yến Nhi"
    ]
    
    services = [
        "Chăm sóc da mặt cao cấp",
        "Massage body thư giãn",
        "Triệt lông công nghệ Diode",
        "Gội đầu dưỡng sinh",
        "Trị mụn chuyên sâu",
        "Acne Detox Therapy",
        "Post-Acne Recovery Therapy",
        "Chăm sóc da mặt Collagen",
        "Triệt lông Laser Diode",
    ]
    
    contents = [
        "Dịch vụ tuyệt vời! Nhân viên rất chuyên nghiệp và tận tâm. Kết quả vượt mong đợi. Sẽ quay lại nhiều lần nữa!",
        "Rất hài lòng với dịch vụ. Mình cảm thấy thư giãn và thoải mái. Giá cả hợp lý, nhân viên thân thiện.",
        "Liệu trình rất hiệu quả. Sau vài buổi, tôi đã thấy kết quả rõ rệt. Chắc chắn sẽ tiếp tục sử dụng.",
        "Không gian sạch sẽ, thoáng mát. Nhân viên tư vấn kỹ lưỡng. Dịch vụ chất lượng cao, đáng giá tiền.",
        "Trải nghiệm tuyệt vời! Cảm thấy được chăm sóc kỹ lưỡng. Sẽ giới thiệu cho bạn bè.",
        "Khá tốt, tuy nhiên cần cải thiện một chút về thái độ phục vụ.",
        "Dịch vụ bình thường, không có gì nổi bật. Kết quả tạm được.",
        "Không hài lòng với kết quả. Dù giá khá mắc nhưng hiệu quả không như mong đợi.",
        "Nhân viên rất chu đáo. Tôi cảm thấy được chúc mừng bởi sự tử tế của họ.",
        "Liệu trình phục hồi da rất tốt. Làn da tôi sáng mịn hơn rất nhiều.",
    ]
    
    times = [
        "1 giờ trước", "3 giờ trước", "5 giờ trước", "1 ngày trước", "2 ngày trước",
        "3 ngày trước", "5 ngày trước", "1 tuần trước", "2 tuần trước", "3 tuần trước",
        "1 tháng trước", "1.5 tháng trước", "2 tháng trước", "2.5 tháng trước", "3 tháng trước",
    ]
    
    avatar_classes = ["avatar-peach", "avatar-neutral", "avatar-rose", "avatar-sun", "avatar-sea"]
    
    # Tạo 120 đánh giá
    feedbacks = []
    ratings = [5.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 3.0, 2.0, 1.0]  # Tỷ lệ: 40% 5-star, 30% 4-star, 10% 3-star, 10% 2-star, 10% 1-star
    statuses = ["Đã phản hồi", "Chưa phản hồi"]
    
    for i in range(1, 121):
        rating = float(ratings[(i - 1) % len(ratings)])
        status = statuses[(i - 1) % len(statuses)]
        status_class = "green" if status == "Đã phản hồi" else "yellow"
        
        feedbacks.append({
            "id": i,
            "name": names[(i - 1) % len(names)],
            "time": times[(i - 1) % len(times)],
            "service": services[(i - 1) % len(services)],
            "rating": f"{rating}",
            "status": status,
            "status_class": status_class,
            "content": contents[(i - 1) % len(contents)] + f" (Đánh giá #{i})",
            "avatar_class": avatar_classes[(i - 1) % len(avatar_classes)],
        })
    
    # Tính toán phân phối sao
    total_reviews = len(feedbacks)
    star_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    total_rating = 0
    
    for feedback in feedbacks:
        rating = int(float(feedback["rating"]))
        star_distribution[rating] += 1
        total_rating += float(feedback["rating"])
    
    average_rating = round(total_rating / total_reviews, 1) if total_reviews > 0 else 0
    
    # Chuẩn bị dữ liệu phân phối sao cho template
    star_stats = []
    for star_num in [5, 4, 3, 2, 1]:
        count = star_distribution[star_num]
        percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
        star_stats.append({
            "star": star_num,
            "count": count,
            "percentage": int(percentage)
        })
    
    return render(request, "feedback_dashboard.html", {
        "feedbacks": feedbacks,
        "average_rating": average_rating,
        "total_reviews": total_reviews,
        "star_stats": star_stats
    })


def get_consultation_data():
    return {
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
                {"side": "left", "text": "Shop ơi tư vấn này giúp e với .....", "time": "23/01/2026"},
            ],
        },
        4: {
            "id": 4,
            "name": "Lê Thư Ý",
            "avatar_class": "chat-avatar-three",
            "messages": [
                {"divider": "23/01/2026"},
                {"side": "left", "text": "Shop ơi", "time": ""},
                {
                    "side": "right",
                    "text": "Dạ em chào chị, chị cần bên em tư vấn dịch vụ nào ạ?",
                    "time": "09:03",
                },
                {"side": "left", "text": "Mình muốn đặt lịch gội đầu dưỡng sinh vào cuối tuần này", "time": ""},
                {
                    "side": "right",
                    "text": "Dạ cuối tuần bên em còn slot 15:00 và 17:00, chị chọn giờ nào để em giữ lịch nhé.",
                    "time": "09:05",
                },
            ],
        },
        5: {
            "id": 5,
            "name": "Lê Trà Thư",
            "avatar_class": "avatar-neutral",
            "messages": [
                {"divider": "23/01/2026"},
                {"side": "left", "text": "Ngày mai nha", "time": ""},
                {
                    "side": "right",
                    "text": "Dạ em đã note lịch ngày mai cho chị rồi ạ.",
                    "time": "21:40",
                },
                {"side": "left", "text": "Khoảng 10h chị qua được không em?", "time": ""},
                {
                    "side": "right",
                    "text": "Dạ được chị nha, em giữ lịch 10:00 và sẽ nhắn xác nhận trước 30 phút ạ.",
                    "time": "21:42",
                },
            ],
        },
    }


@manager_required
def consultation_dashboard(request):
    conversation_data = get_consultation_data()
    conversations = []

    for item in conversation_data.values():
        messages = item["messages"]
        latest_message = next((msg for msg in reversed(messages) if "text" in msg), None)

        conversations.append(
            {
                "id": item["id"],
                "name": item["name"],
                "avatar_class": item["avatar_class"],
                "preview": latest_message["text"] if latest_message else "",
                "time": latest_message.get("time", "") if latest_message else "",
            }
        )

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


@manager_required
def consultation_detail(request, conversation_id):
    conversations = get_consultation_data()
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


@manager_required
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


def customer_consultation_page(request):
    faq_items = [
        {
            "question": "Da nhay cam co the lam lieu trinh massage hoac cham soc mat khong?",
            "answer": "Chung toi co cac lieu trinh danh rieng cho da nhay cam, su dung san pham diu nhe va nhan vien se tu van ky truoc khi thuc hien.",
        },
        {
            "question": "Lieu trinh lam trang da co an toan cho da nhay cam khong?",
            "answer": "Spa su dung san pham chuyen dung cho da nhay cam va ky thuat vien duoc dao tao de giam nguy co kich ung truoc khi tien hanh toan bo lieu trinh.",
        },
        {
            "question": "Sau khi lan kim hoac peel da, toi can bao lau de da phuc hoi hoan toan?",
            "answer": "Thoi gian phuc hoi tuy vao co dia va do sau cua lieu trinh, thong thuong tu 3 den 7 ngay neu cham soc dung cach tai nha.",
        },
    ]
    chat_messages = [
        {
            "side": "right",
            "text": "Shop oi tu van nay giup em voi ve goi cham da voi",
            "time": "10:48",
        },
        {
            "side": "left",
            "text": "Chao mung ban den voi dich vu Mai Tram, ban vui long doi mot chut se co nhan vien tu van ngay.",
            "time": "10:50",
        },
        {
            "side": "right",
            "text": "Shop oi tu van a",
            "time": "10:50",
        },
        {
            "side": "left",
            "text": "Em day a",
            "time": "10:52",
        },
    ]
    return render(
        request,
        "customer_consultation.html",
        {
            "faq_items": faq_items,
            "chat_messages": chat_messages,
        },
    )


def about_page(request):
    return render(request, 'about.html')


def public_review_page(request):
    reviews = get_public_reviews()
    average_rating = round(sum(item["rating"] for item in reviews) / len(reviews), 1) if reviews else 0
    total_reviews = 120
    with_images = sum(1 for item in reviews if item["image_urls"])
    highlighted_reviews = reviews[:3]

    context = {
        "reviews": reviews,
        "highlighted_reviews": highlighted_reviews,
        "average_rating": average_rating,
        "total_reviews": total_reviews,
        "with_images": with_images,
    }
    return render(request, "public_reviews.html", context)


@customer_required
def customer_account(request):
    profile, _ = CustomerProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": f"{request.user.last_name} {request.user.first_name}".strip() or request.user.username,
            "member_since": request.user.date_joined.date(),
            "loyalty_points": 320,
            "avatar_url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=400&q=80",
        },
    )

    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            request.user.first_name = form.cleaned_data["full_name"]
            request.user.save(update_fields=["first_name"])
            messages.success(request, "Thong tin tai khoan da duoc cap nhat.")
            return redirect("customer_account")
    else:
        form = CustomerProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
        "history_items": build_customer_history(),
        "active_tab": request.GET.get("tab", "profile"),
        "member_since_label": profile.member_since.strftime("%m/%Y") if profile.member_since else "",
        "display_name": profile.display_name,
    }
    return render(request, "customer_account.html", context)


def build_booking_calendar(days=14):
    today = date.today()
    items = []
    for offset in range(days):
        current = today + timedelta(days=offset)
        items.append(
            {
                "day": current.day,
                "iso": current.isoformat(),
                "disabled": False,
                "is_today": offset == 0,
            }
        )
    return items


@customer_required
def booking_page(request):
    if request.method == "POST":
        messages.success(request, "Dat lich thanh cong. Spa se lien he xac nhan som.")
        return redirect("booking")

    services = [
        {
            "id": 1,
            "name": "Cham soc da mat Collagen",
            "description": "Lam sach sau, duong am va tai tao da",
            "duration": "60 phut",
            "rating": "4.9",
            "price": "1.200.000d",
            "tone": "peach",
            "image_url": "https://images.unsplash.com/photo-1515377905703-c4788e51af15?auto=format&fit=crop&w=900&q=80",
        },
        {
            "id": 2,
            "name": "Tri mun chuyen sau",
            "description": "Dieu tri mun an toan, hieu qua",
            "duration": "60 phut",
            "rating": "4.8",
            "price": "800.000d",
            "tone": "rose",
            "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=900&q=80",
        },
        {
            "id": 3,
            "name": "Massage body thu gian",
            "description": "Massage toan than thong co va giam cang thang",
            "duration": "60 phut",
            "rating": "4.8",
            "price": "500.000d",
            "tone": "sea",
            "image_url": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=900&q=80",
        },
        {
            "id": 4,
            "name": "Triet long vinh vien bang laser IPL",
            "description": "Cong nghe triet long hien dai va an toan",
            "duration": "90 phut",
            "rating": "4.7",
            "price": "2.000.000d",
            "tone": "mint",
            "image_url": "https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?auto=format&fit=crop&w=900&q=80",
        },
    ]

    package_catalog = [
        {
            "id": "basic",
            "name": "Goi co ban",
            "sessions": "1-2",
            "price": "Tu 800.000d",
            "result": "Phu hop cho lan dau trai nghiem",
            "benefits": [
                "Lam sach co ban",
                "Massage mat thu gian",
                "Dap mat na Collagen",
                "Duong am nhanh",
            ],
        },
        {
            "id": "standard",
            "name": "Goi tieu chuan",
            "sessions": "3-5",
            "price": "Tu 1.300.000d",
            "result": "Hieu qua ro ret sau 1 thang",
            "benefits": [
                "Tat ca quyen loi goi co ban",
                "Tay te bao chet chuyen sau",
                "Serum duong da cao cap",
                "Tu van cham soc tai nha",
            ],
        },
        {
            "id": "advanced",
            "name": "Goi cao cap",
            "sessions": "8-10",
            "price": "Tu 2.500.000d",
            "result": "Cham soc toan dien, hieu qua lau dai",
            "benefits": [
                "Tat ca quyen loi goi tieu chuan",
                "Cong nghe dieu tri tien tien",
                "Massage vai gay mien phi",
                "Tang bo skincare mini",
            ],
        },
        {
            "id": "vip",
            "name": "Goi VIP",
            "sessions": "12-15",
            "price": "Tu 3.500.000d",
            "result": "Trai nghiem dang cap 5 sao",
            "benefits": [
                "Tat ca quyen loi goi cao cap",
                "Phong rieng VIP sang trong",
                "Thu cong nghe tri lieu moi",
                "Tang bo skincare cao cap",
            ],
            "theme": "vip",
        },
    ]

    packages_by_service = {
        str(service["id"]): [dict(item) for item in package_catalog]
        for service in services
    }
    today_iso = date.today().isoformat()
    time_slots_by_date = {
        today_iso: ["09:00", "10:30", "14:00", "16:00"],
    }
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)

    context = {
        "services": services,
        "packages_by_service": packages_by_service,
        "time_slots_by_date": time_slots_by_date,
        "calendar_days": build_booking_calendar(),
        "current_month_label": date.today().strftime("%m/%Y"),
        "customer_info": {
            "full_name": profile.display_name,
            "phone": profile.phone or "Chua cap nhat",
            "email": request.user.email,
        },
        "history": build_customer_history(),
    }
    return render(request, "booking.html", context)


def see_service(request):
    services = [
        serialize_service(service)
        for service in Service.objects.filter(status=Service.STATUS_ACTIVE)
    ]
    return render(request, "see_service.html", {"services": services})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, status=Service.STATUS_ACTIVE)
    related_services = [
        serialize_service(item)
        for item in Service.objects.filter(status=Service.STATUS_ACTIVE, category=service.category)
        .exclude(pk=service.pk)[:3]
    ]
    return render(
        request,
        "service_detail.html",
        {
            "service": serialize_service(service),
            "related_services": related_services,
        },
    )
