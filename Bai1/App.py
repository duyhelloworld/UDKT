from datetime import datetime
from Const import *

class Vehicle:
    def __init__(self, vehicle_type, check_in_time, license_plate, ticket_id):
        self.vehicle_type = vehicle_type
        self.check_in_time = check_in_time
        # None for bicycles
        self.license_plate = license_plate  
        self.ticket_id = ticket_id

    def calculate_fee(self, check_out_time, lost_ticket):
        pass

    def __str__(self):
        return f"""
            Loại xe: {"Xe đạp " if self.vehicle_type == 0 else "Xe máy " if self.vehicle_type == 1 else "Không xác định"},
            Thời gian đậu: {self.check_in_time},
            Biển số xe: {self.license_plate if self.license_plate else "Không có"},
            Mã vé: {self.ticket_id}"""

class Bicycle(Vehicle):
    def __init__(self, check_in_time, ticket_id):
        super().__init__(BICYCLE_CODE, check_in_time, None, ticket_id)

    def calculate_fee(self, check_out_time, lost_ticket):
        fee = 0
        if lost_ticket:
            fee += BICYCLE_LOST_TICKET_FINE
        else:
            if START_WORK_HOUR <= check_out_time.hour < 18:
                fee += BICYCLE_DAY_FEE
            elif 18 <= check_out_time.hour < END_WORK_HOUR:
                fee += BICYCLE_NIGHT_FEE
            else:
                fee += BICYCLE_OVERNIGHT_FEE
        return fee

class Motorcycle(Vehicle):
    def __init__(self, check_in_time, license_plate, ticket_id):
        super().__init__(MOTORCYCLE_CODE, check_in_time, license_plate, ticket_id)

    def calculate_fee(self, check_out_time, lost_ticket):
        fee = 0
        if lost_ticket:
            fee += MOTORCYCLE_LOST_TICKET_FINE
            
        else:
            if START_WORK_HOUR <= check_out_time.hour < 18:
                fee += MOTORCYCLE_DAY_FEE
            elif 18 <= check_out_time.hour < END_WORK_HOUR:
                fee += MOTORCYCLE_NIGHT_FEE
            else:
                fee += MOTORCYCLE_OVERNIGHT_FEE
        return fee

# Parking lot management
class ParkingLot:
    def __init__(self):
        self.vehicles = []
        # Lost ticket vehicles list
        self.lost_ticket_vehicles = [] 
        # List of vehicles that need alert
        self.alert_list = []  
        # List of vehicles for daily statistics
        self.daily_vehicles = []  

        # Ví dụ mẫu
        # Bicycle
        # xedapsang = Bicycle(datetime(2024, 2, 23, 10, 0), "xedapsang")
        # self.vehicles.append(xedapsang)

        # xedaptoi = Bicycle(datetime(2024, 2, 23, 20, 0), "xedaptoi")
        # self.vehicles.append(xedaptoi)

        # xedaphomqua = Bicycle(datetime(2024, 2, 22, 11, 0), "xedaphomqua")
        # self.vehicles.append(xedaphomqua)

        # xedapcanhbao = Bicycle(datetime(2024, 2, 20, 11, 0), "xedapcanhbao")
        # self.vehicles.append(xedapcanhbao)

        # Xe máy
        # xemay1 = Motorcycle(datetime(2024, 2, 23, 9, 0), "123", "xemaysang")
        # self.vehicles.append(xemay1) 
        # self.daily_vehicles.append(xemay1) 

        # xemay2 = Motorcycle(datetime(2024, 2, 23, 21, 0), "456", "xemaytoi")
        # self.vehicles.append(xemay2)
        # self.daily_vehicles.append(xemay2)

        # xemay3 = Motorcycle(datetime(2024, 2, 22, 9, 0), "789", "xemayhomqua")
        # self.vehicles.append(xemay3)
        # self.daily_vehicles.append(xemay3)

        # xemay4 = Motorcycle(datetime(2024, 2, 17, 9, 0), "1122", "xemaycanhbao")
        # self.vehicles.append(xemay4)
        # self.daily_vehicles.append(xemay4)

    def __add_lost_ticket_vehicle__(self, vehicle):
        self.lost_ticket_vehicles.append(vehicle)

    def add_daily_vehicle(self, vehicle):
        self.daily_vehicles.append(vehicle)

    def __is_in_lost_ticket_list__(self, vehicle):
        return vehicle in self.lost_ticket_vehicles

    def find_vehicle_by_ticket_id(self, ticket_id):
        if ticket_id is None:
            return None
        for vehicle in self.vehicles:
            if vehicle.ticket_id == str(ticket_id) or vehicle.ticket_id == int(ticket_id):
                return vehicle
        return None

    def __load_alert_vehicles__(self):
        current_time = datetime.now()
        for vehicle in self.vehicles:
            entry_time = vehicle.check_in_time
            if isinstance(vehicle, Bicycle) and (current_time - entry_time).days >= 3:
                # In thông tin xe đạp cần cảnh báo
                self.alert_list.append(vehicle)
            elif isinstance(vehicle, Motorcycle) and (current_time - entry_time).days >= 5:
                # In thông tin xe máy cần cảnh báo
                self.alert_list.append(vehicle)

    def add_vehicle(self, vehicle):
        if self.find_vehicle_by_ticket_id(vehicle.ticket_id) is not None:
            print("\n=====================================\n")
            print(f"Đã tồn tại xe có mã {vehicle.ticket_id} trong hệ thống. Không thể thêm phương tiện mới.")
            return
        if vehicle.ticket_id is None:
            vehicle.ticket_id = len(self.vehicles) + 1
        self.vehicles.append(vehicle)
        print("\n=====================================\n")
        print("Thêm phương tiện đậu vào thành công.")
        print(f"Mã vé xe : {vehicle.ticket_id}")

    def remove_vehicle(self, ticket_id, has_paid_fee=None, has_ticket=None, license_plate=None):
        # Tìm kiếm phương tiện với mã vé
        found_vehicle = self.find_vehicle_by_ticket_id(ticket_id)
        if found_vehicle is None:
            print("\n=====================================\n")
            print("Không tìm thấy phương tiện với mã vé đã nhập.")
            return
        
        # Kiểm tra loại phương tiện có khớp không
        if has_ticket:
            if isinstance(found_vehicle, Bicycle):
                print("\n=====================================\n")
                print(f"Vé {found_vehicle.ticket_id} không phải cho xe máy. Không thể lấy ra.")
                return
            elif isinstance(found_vehicle, Motorcycle):
                print("\n=====================================\n")
                print(f"Vé {found_vehicle.ticket_id} không phải cho xe đạp. Không thể lấy ra.")
                return
            
        # Kiểm tra biển số xe (nếu có)
        if license_plate is not None and license_plate != found_vehicle.license_plate:
            print("\n=====================================\n")
            print("Biển số xe không khớp với dữ liệu trong hệ thống. Không thể lấy phương tiện ra.")
            return

        # Tính toán phí nếu cần thiết và hiển thị thông tin
        fee = found_vehicle.calculate_fee(datetime.now(), False) if has_ticket else found_vehicle.calculate_fee(datetime.now(), True)
        # In chi phí trước khi xác nhận đã nộp tiền phí
        print("Chi phí:", fee) 

        # Xác nhận việc lấy xe ra và xóa nó khỏi danh sách nếu đã nộp phí
        if has_paid_fee is None:
            # Yêu cầu xác nhận đã nộp phí
            # Mở rộng sẽ là chụp bill chuyển khoản / thu tiền mặt
            confirm_fee = input("Đã nộp tiền phí (Y/N): ").upper()
            if confirm_fee not in SELECT_CHOICE:
                print("\n=====================================\n")
                print("Lựa chọn không hợp lệ.")
                return
            has_paid_fee = confirm_fee == 'Y'  
        if has_paid_fee:
            print("\n=====================================\n")
            print("Phương tiện đã được lấy ra thành công.")
            self.vehicles.remove(found_vehicle)
        else:
            print("\n=====================================\n")
            print("Phương tiện không được phép lấy ra. Hãy nộp phí trước khi lấy phương tiện ra.")

    def display_sorted_vehicles(self, type_vehicle=None, is_asc=None):
        sorted_list = []
        if type_vehicle is not None:
            sorted_list = sorted(self.vehicles, 
                key=lambda v: v.type_vehicle,
                reverse=is_asc)
        if is_asc is not None:
            sorted_list = sorted(self.vehicles,
                key=lambda v: v.check_in_time,
                reverse=is_asc)
        for vehicle in sorted_list:
            print("\n=====================================\n")
            print(vehicle)

    # Tính doanh thu hàng ngày các xe gửi  
    def calculate_daily_revenue(self):
        total_revenue_bicycle = 0
        total_revenue_motorbicycle = 0
        current_date = datetime.now().date()
        for vehicle in self.vehicles:
            if START_WORK_HOUR <= vehicle.check_in_time.hour <= END_WORK_HOUR and current_date > vehicle.check_in_time.date() and not self.__is_in_lost_ticket_list__(vehicle):  
                if isinstance(vehicle, Motorcycle):
                    fee = vehicle.calculate_fee(datetime.now(), False )
                    total_revenue_bicycle += fee
                elif isinstance(vehicle, Bicycle):
                    fee = vehicle.calculate_fee(datetime.now(), False )
                    total_revenue_motorbicycle += fee
        print("\n=====================================\n")
        print("Doanh thu của ngày hiện tại:", total_revenue_bicycle + total_revenue_motorbicycle)
        print("- Doanh thu từ xe đạp:", total_revenue_bicycle)
        print("- Doanh thu từ xe máy:", total_revenue_motorbicycle)

    def get_alert_list(self):
        alert_list = []
        current_date = datetime.now().date()
        for vehicle in self.vehicles:
            entry_date = vehicle.check_in_time.date()
            if isinstance(vehicle, Bicycle):
                if (current_date - entry_date).days >= 3:
                    alert_list.append(vehicle)
            elif isinstance(vehicle, Motorcycle):
                if (current_date - entry_date).days >= 5:
                    alert_list.append(vehicle)
        return alert_list

    def get_lost_ticket_vehicles(self):
        lost_ticket_vehicles = []
        for vehicle in self.vehicles:
            entry_hour = vehicle.check_in_time.hour
            if entry_hour >= START_WORK_HOUR and entry_hour <= END_WORK_HOUR:
                if vehicle.ticket_id == "":
                    lost_ticket_vehicles.append(vehicle)
        return lost_ticket_vehicles

    def get_motorcycles_with_multiple_entries(self):
        motorcycle_counts = {}
        for vehicle in self.vehicles:
            if isinstance(vehicle, Motorcycle):
                entry_date = vehicle.check_in_time.date()
                if entry_date == datetime.now().date():
                    license_plate = vehicle.license_plate
                    if license_plate in motorcycle_counts:
                        motorcycle_counts[license_plate] += 1
                    else:
                        motorcycle_counts[license_plate] = 1
        multiple_entry_motorcycles = [vehicle for vehicle, count in motorcycle_counts.items() if count >= 2]
        return [vehicle for vehicle in self.vehicles if vehicle.license_plate in multiple_entry_motorcycles]

    def get_motorcycles_with_multiple_entries_today(self):
        motorcycle_counts = {}
        for vehicle in self.vehicles:
            if isinstance(vehicle, Motorcycle):
                entry_date = vehicle.check_in_time.date()
                if entry_date == datetime.now().date():
                    license_plate = vehicle.license_plate
                    if license_plate in motorcycle_counts:
                        motorcycle_counts[license_plate] += 1
                    else:
                        motorcycle_counts[license_plate] = 1
        multiple_entry_motorcycles = [license_plate for license_plate, count in motorcycle_counts.items() if count >= 2]
        return [vehicle for vehicle in self.vehicles if isinstance(vehicle, Motorcycle) and vehicle.license_plate in multiple_entry_motorcycles]

    def display_daily_vehicles(self, daily_vehicles):
        print("\n=====================================\n")
        print("\nDanh sách thống kê lượt gửi xe trong ngày:")
        for vehicle in daily_vehicles:
            print("\n=====================================\n")
            print(vehicle)

# Test
vehicle_manager = ParkingLot()
choice = ''
while choice != '0':
    print("\n=====================================\n")
    print("\nChọn chức năng:")
    print("1. Thêm phương tiện đậu vào")
    print("2. Lấy phương tiện ra")
    print("3. Hiển thị số lượng phương tiện đang đậu")
    print("4. Hiển thị danh sách phương tiện đang đậu")
    print("5. Tính doanh thu của ngày hiện tại")
    print("6. Hiển thị danh sách phương tiện cần cảnh báo")
    print("7. Hiển thị danh sách phương tiện bị mất vé trong ngày")
    print("8. Hiển thị danh sách xe máy có lượt gửi từ 2 lần trong ngày hiện tại")
    print("9. Hiển thị danh sách thống kê lượt gửi xe trong ngày")
    print("0. Thoát")
    choice = input("Nhập lựa chọn của bạn: ")

    if choice == '1':
        vehicle_type = input("Nhập loại phương tiện (1: Xe đạp, 2: Xe máy): ")
        if vehicle_type not in ['1', '2']:
            print("Lựa chọn không hợp lệ!")
            continue

        if vehicle_type == '2':
            license_plate = input("Nhập biển số xe: ")
            if not license_plate:
                print("Vui lòng nhập biển số xe!")
                continue

        ticket_id = None
        if vehicle_type == '1':
            bicycle = Bicycle(datetime.now(), ticket_id)
            vehicle_manager.add_vehicle(bicycle)
            # vehicle_manager.add_daily_vehicle(bicycle)
        elif vehicle_type == '2':
            check_in_time = datetime.now()
            motorcycle = Motorcycle(check_in_time, license_plate, ticket_id)
            vehicle_manager.add_vehicle(motorcycle)
            # Thêm xe máy vào danh sách thống kê
            vehicle_manager.add_daily_vehicle(motorcycle)

    elif choice == '2':
        vehicle_type = input("Nhập loại phương tiện (1: Xe đạp, 2: Xe máy): ")
        if vehicle_type not in ['1', '2']:
            print("Lựa chọn không hợp lệ!")
            continue

        ticket_id = input("Nhập mã vé: ")

        # Tìm kiếm phương tiện với mã vé
        vehicle_to_remove = vehicle_manager.find_vehicle_by_ticket_id(ticket_id)

        if vehicle_to_remove is None:
            print("\n=====================================\n")
            print("Không tìm thấy phương tiện với mã vé đã nhập.")
        else:
            if (vehicle_type == '1' and isinstance(vehicle_to_remove, Bicycle)) or \
            (vehicle_type == '2' and isinstance(vehicle_to_remove, Motorcycle)):
                if vehicle_type == '2':
                    license_plate = input("Nhập biển số xe: ")
                    if license_plate != vehicle_to_remove.license_plate:
                        print("\n=====================================\n")
                        print("Biển số xe không khớp với dữ liệu trong hệ thống. Không thể lấy phương tiện ra.")
                        continue

                # Kiểm tra có vé hay không
                input_has_ticket = input("Có vé (Y/N): ").upper()
                if input_has_ticket not in SELECT_CHOICE:
                    print("\n=====================================\n")
                    print("Lựa chọn không hợp lệ.")
                    continue

                has_ticket = input_has_ticket == 'Y'
                # In chi phí trước khi xác nhận đã nộp tiền phí nếu có vé
                fee = vehicle_to_remove.calculate_fee(datetime.now(), False)
                print("Chi phí:", fee)
                if has_ticket:
                    # Xác nhận đã nộp phí nếu có vé
                    input_has_paid_fee = input("Xác nhận người gửi xe đã nộp phí (Y/N): ").upper()
                    if input_has_paid_fee not in SELECT_CHOICE:
                        print("\n=====================================\n")
                        print("Lựa chọn không hợp lệ.")
                        continue

                    has_paid_fee = input_has_paid_fee == 'Y'
                    if has_paid_fee:
                        print("\n=====================================\n")
                        print("Phương tiện đã được lấy ra thành công.")
                        vehicle_manager.vehicles.remove(vehicle_to_remove)
                    else:
                        print("\n=====================================\n")
                        print("Phương tiện Không được phép lấy.")
                else:
                    # Xác nhận đã nộp phí và biên bản nếu không có vé
                    input_has_signed_document = input("Xác nhận người gửi xe đã ký biên bản (Y/N): ").upper()
                    if input_has_signed_document not in SELECT_CHOICE:
                        print("\n=====================================\n")
                        print("Lựa chọn không hợp lệ.")
                        continue
                    has_signed_document = input_has_signed_document.upper() == 'Y'
                    if has_signed_document:
                        print("\n=====================================\n")
                        print("Phương tiện đã được lấy ra thành công.")
                        vehicle_manager.vehicles.remove(vehicle_to_remove)
                    else:
                        print("\n=====================================\n")
                        print("Phương tiện Không được phép lấy ra.")
            else:
                print("\n=====================================\n")
                print("Loại phương tiện không khớp với dữ liệu trong hệ thống.")

    elif choice == '3':
        print("\n=====================================\n")
        print("\nSố lượng phương tiện đang đậu:", len(vehicle_manager.vehicles))

    elif choice == '4':
        print("\n=====================================\n")
        print("1. Chỉ xe máy ")
        print("2. Chỉ xe đạp ")
        print("3. Sắp xếp theo thời gian đậu (tăng dần) ")
        print("4. Sắp xếp theo thời gian đậu (giảm dần) ")
        by = input()
        if by == '1':
            vehicle_manager.display_sorted_vehicles(type_vehicle='1')
        elif by == '2':
            vehicle_manager.display_sorted_vehicles(type_vehicle='2')
        elif by == '3':
            vehicle_manager.display_sorted_vehicles(is_asc=True)
        elif by == '3':
            vehicle_manager.display_sorted_vehicles(is_asc=False)
        else:
            print("Lựa chọn không hợp lệ")
            print("=====================")
            continue
    elif choice == '5':
        vehicle_manager.calculate_daily_revenue()

    elif choice == '6':
        print("Danh sách phương tiện cần cảnh báo:")
        vehicle_manager.add_alert_vehicles()


    elif choice == '7':
        lost_ticket_vehicles = vehicle_manager.lost_ticket_vehicles
        print("\n=====================================\n")
        print("\nDanh sách phương tiện bị mất vé trong ngày:")
        for vehicle in lost_ticket_vehicles:
            print("\n=====================================\n")
            print(vehicle)

    elif choice == '8':
        # Tạo một từ điển để đếm số lần xuất hiện của mỗi biển số xe
        motorcycle_counts = {}
        today = datetime.now().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        for motorcycle in vehicle_manager.daily_vehicles:
            if isinstance(motorcycle, Motorcycle):
                entry_time = motorcycle.check_in_time
                if start_of_day <= entry_time <= end_of_day:
                    license_plate = motorcycle.license_plate
                    if license_plate in motorcycle_counts:
                        motorcycle_counts[license_plate] += 1
                    else:
                        motorcycle_counts[license_plate] = 1

        # Lọc ra các xe máy đã gửi từ 2 lần trở lên
        motorcycles_multiple_entries = [license_plate for license_plate, count in motorcycle_counts.items() if count >= 2]

        # In ra thông tin của các xe máy đã gửi từ 2 lần trở lên
        print("\n=====================================\n")
        print("\nDanh sách xe máy đã gửi từ 2 lần trở lên trong ngày:")
        for license_plate in motorcycles_multiple_entries:
            count = motorcycle_counts[license_plate]
            print("\n=====================================\n")
            print(f"Biển số xe: {license_plate}  số lần: {count}")


    elif choice == '9':
        print("\n=====================================\n")
        print("\nDanh sách thống kê lượt gửi xe trong ngày:")
        for vehicle in vehicle_manager.daily_vehicles:
            print("\n=====================================\n")
            print(vehicle)

    elif choice == '0':
        print("Thoát")
    else:
        print("\n=====================================\n")
        print("Lựa chọn không hợp lệ!")
