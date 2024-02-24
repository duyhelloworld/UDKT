import datetime

from Const import *

# Class phương tiện
class Vehicle:
    def __init__(self, vehicle_type, check_in_time, license_plate, ticket_id):
        self.vehicle_type = vehicle_type
        self.check_in_time = check_in_time
        # None for bicycles
        self.license_plate = license_plate 
        self.ticket_id = ticket_id

    def __str__(self):
        return f"""Loại xe: {self.vehicle_type},
            Thời gian đậu: {self.check_in_time.strftime("%H:%M:%S %d-%m-%Y")},
            Biển số xe: {self.license_plate 
                if self.license_plate else 'Không'}, 
            Mã vé: {self.ticket_id}"""

# Class phương tiện con
class Bicycle(Vehicle):
    def __init__(self, check_in_time, ticket_id):
        super().__init__('Xe đạp', check_in_time, None, ticket_id)

    def calculate_fee(self, check_out_time, lost_ticket):
        fee = 0
        if lost_ticket:
            fee += BICYCLE_LOST_TICKET_FINE
        if check_out_time.hour < 18:
            fee += BICYCLE_DAY_FEE
        elif 18 <= check_out_time.hour < 22:
            fee += BICYCLE_NIGHT_FEE
        if check_out_time.hour >= 22 or check_out_time.hour < 8:
            fee += BICYCLE_OVERNIGHT_FEE
        return fee

class Motorcycle(Vehicle):
    def __init__(self, check_in_time, license_plate, ticket_id):
        super().__init__('Xe máy', check_in_time, license_plate, ticket_id)

    def calculate_fee(self, check_out_time, lost_ticket):
        fee = 0
        if lost_ticket:
            fee += MOTORCYCLE_LOST_TICKET_FINE
        if check_out_time.hour < 18:
            fee += MOTORCYCLE_DAY_FEE
        elif 18 <= check_out_time.hour < 22:
            fee += MOTORCYCLE_NIGHT_FEE
        if check_out_time.hour >= 22 or check_out_time.hour < 8:
            fee += MOTORCYCLE_OVERNIGHT_FEE
        return fee

# Quản lý bãi đậu xe
class ParkingLot:
    def __init__(self):
        self.vehicles = []
        self.lost_ticket_vehicles = []  # Danh sách phương tiện bị mất vé
        self.alert_list = []  # Danh sách phương tiện cần cảnh báo

    def add_lost_ticket_vehicle(self, vehicle):
        self.lost_ticket_vehicles.append(vehicle)

    def add_alert_vehicle(self, vehicle):
        self.alert_list.append(vehicle)

    def add_vehicle(self, vehicle):
        # Kiểm tra xem mã vé đã tồn tại cho bất kỳ loại phương tiện nào chưa
        if any(existing_vehicle.ticket_id == vehicle.ticket_id for existing_vehicle in self.vehicles):
            print("\n=====================================\n")
            print("Mã vé đã tồn tại trong hệ thống. Không thể thêm phương tiện mới.")
            return
        if vehicle.vehicle_type == "Xe máy":
            if any(existing_vehicle.license_plate == vehicle.license_plate for existing_vehicle in self.vehicles):
                print("\n=====================================\n")
                print("Biển số xe đã tồn tại trong hệ thống. Không thể thêm phương tiện mới.")
                return
        # Nếu mã vé chưa tồn tại cho bất kỳ loại phương tiện nào, thêm phương tiện vào danh sách
        self.vehicles.append(vehicle)
        print("\n=====================================\n")
        print("Thêm phương tiện đậu vào thành công.")

    def remove_vehicle(self, ticket_id, has_paid_fee, has_ticket, license_plate=None):
        for vehicle in self.vehicles:
            if vehicle.ticket_id == ticket_id:
                if vehicle.vehicle_type == "Xe máy" and license_plate != vehicle.license_plate:
                    print("\n=====================================\n")
                    print("\nBiển số xe không khớp với dữ liệu trong hệ thống. Không thể lấy phương tiện ra.")
                    return None
                if has_ticket:
                    if has_paid_fee:
                        print("\n=====================================\n")
                        print("Phương tiện đã được lấy ra thành công.")
                        self.vehicles.remove(vehicle)
                    else:
                        print("\n=====================================\n")
                        print("Phương tiện không được phép lấy.")
                else:
                    signed_document = input("Xác nhận người gửi xe đã nộp phí và biên bản báo cáo mất vé : (Y/N): ").upper()
                    if signed_document not in ['Y', 'N']:
                        print("Lựa chọn không hợp lệ! Hãy chỉ chọn Y hoặc N.")
                        return
                    has_signed_document = signed_document == 'Y'
                    if has_signed_document:
                        print("\n=====================================\n")
                        print("Phương tiện đã được lấy ra thành công.")
                        self.vehicles.remove(vehicle)
                        # Thêm phương tiện vào danh sách phương tiện bị mất vé nếu không có vé xe
                        self.add_lost_ticket_vehicle(vehicle)
                    else:
                        print("\n=====================================\n")
                        print("Phương tiện Không được phép lấy.")
                        # Thêm phương tiện vào danh sách cảnh báo nếu không xác nhận đã nộp phí và biên bản
                        self.add_alert_vehicle(vehicle)
                return vehicle
        print("\n=====================================\n")
        print("Không tìm thấy phương tiện với mã vé đã nhập.")
        return None
    
    # def buy_ticket(self, ticket_id):
    #     try:
    #         for vehicle in self.vehicles:
    #             if vehicle.ticket_id == ticket_id:
    #                 # Custom billing
    #                 is_paid = input("Nhập mã bill: ")
    #                 return is_paid.isalnum()
    #         return False
    #     except:
    #         print("Lựa chọn không hợp lệ!")


    def display_sorted_vehicles(self, sort_by_entry_time=True, sort_ascending=True, filter_vehicle_type=None):
        sorted_list = sorted(self.vehicles, key=lambda x: x.check_in_time, reverse=not sort_ascending) if sort_by_entry_time else self.vehicles
        if filter_vehicle_type:
            sorted_list = [vehicle for vehicle in sorted_list if vehicle.vehicle_type == filter_vehicle_type]
        for vehicle in sorted_list:
            print("\n=====================================\n")
            print(vehicle)

    # Các phương pháp bổ sung cho thống kê, tính toán thanh toán, vv sẽ được thêm ở đây
    def calculate_daily_revenue(self):
        total_revenue = 0
        current_time = datetime.datetime.now().time().hour
        if 8 <= current_time <= 22:
            for vehicle in self.vehicles:
                entry_hour = vehicle.check_in_time.hour
                if entry_hour >= 8 and entry_hour <= 22:
                    # Giả sử không có vé bị mất
                    lost_ticket = False 
                    fee = vehicle.calculate_fee(datetime.datetime.now(), lost_ticket)
                    total_revenue += fee
            print("\n=====================================\n")
            print("Doanh thu của ngày hiện tại:", total_revenue)
        else:
            print("Ngoài khung giờ tính doanh thu (8h-22h)")

    def get_alert_list(self):
        alert_list = []
        current_date = datetime.datetime.now().date()
        for vehicle in self.vehicles:
            entry_date = vehicle.check_in_time.date()
            if vehicle.vehicle_type == "Xe đạp":
                if (current_date - entry_date).days >= 3:
                    alert_list.append(vehicle)
            elif vehicle.vehicle_type == "Xe máy":
                if (current_date - entry_date).days >= 5:
                    alert_list.append(vehicle)
        return alert_list

    def get_lost_ticket_vehicles(self):
        lost_ticket_vehicles = []
        current_date = datetime.datetime.now().date()
        for vehicle in self.vehicles:
            entry_hour = vehicle.check_in_time.hour
            if entry_hour >= 8 and entry_hour <= 22:
                if vehicle.ticket_id == "":
                    lost_ticket_vehicles.append(vehicle)
        return lost_ticket_vehicles

    def get_motorcycles_with_multiple_entries(self):
        motorcycle_counts = {}
        for vehicle in self.vehicles:
            if vehicle.vehicle_type == "Xe máy":
                entry_date = vehicle.check_in_time.date()
                if entry_date == datetime.datetime.now().date():
                    license_plate = vehicle.license_plate
                    if license_plate in motorcycle_counts:
                        motorcycle_counts[license_plate] += 1
                    else:
                        motorcycle_counts[license_plate] = 1
        multiple_entry_motorcycles = [vehicle for vehicle, count in motorcycle_counts.items() if count >= 2]
        return [vehicle for vehicle in self.vehicles if vehicle.license_plate in multiple_entry_motorcycles]
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
    print("0. Thoát")
    choice = input("Nhập lựa chọn của bạn: ")

    if choice == '1':
        vehicle_type = int(input("Nhập loại phương tiện (1: Xe đạp, 2: Xe máy): "))
        if vehicle_type == 1:
            ticket_id = input("Nhập mã vé: ")
            bicycle = Bicycle(datetime.datetime.now(), ticket_id)
            vehicle_manager.add_vehicle(bicycle)
        elif vehicle_type == 2:
            ticket_id = input("Nhập mã vé: ")
            license_plate = input("Nhập biển số xe: ")
            motorcycle = Motorcycle(datetime.datetime.now(), license_plate, ticket_id)
            vehicle_manager.add_vehicle(motorcycle)
        else:
            print("Lựa chọn không hợp lệ!")

    elif choice == '2':
        vehicle_type = int(input("Nhập loại phương tiện (1: Xe đạp, 2: Xe máy): "))
        ticket_id = input("Nhập mã vé: ")
        if vehicle_type == 1:
            license_plate = None  # Không cần biển số xe cho xe đạp
        elif vehicle_type == 2:
            license_plate = input("Nhập biển số xe: ")
        else:
            print("Lựa chọn không hợp lệ!")
            # Quay lại menu chính
            continue  
        paid_fee_choice = input("Đã nộp tiền phí (Y/N): ").upper()
        ticket = input("Có vé xe (Y/N): ").upper()
        if paid_fee_choice.upper() not in ['Y', 'N'] or ticket.upper() not in ['Y', 'N']:
            print("Lựa chọn không hợp lệ! Hãy chỉ chọn Y hoặc N.")
            # Quay lại menu chính
            continue  
        has_paid_fee = paid_fee_choice == 'Y'
        has_ticket = ticket == 'Y'

        if vehicle_type in [1, 2]:
            if vehicle_type == 1:
                vehicle_manager.remove_vehicle(ticket_id, has_paid_fee, has_ticket)
            else:
                vehicle_manager.remove_vehicle(ticket_id, has_paid_fee, has_ticket, license_plate)
        else:
            print("Lựa chọn không hợp lệ!")




    elif choice == '3':
        print("\n=====================================\n")
        print("\nSố lượng phương tiện đang đậu:", len(vehicle_manager.vehicles))

    elif choice == '4':
        vehicle_manager.display_sorted_vehicles()

    elif choice == '5':
        vehicle_manager.calculate_daily_revenue()

    elif choice == '6':
        alert_list = vehicle_manager.alert_list
        print("\nDanh sách phương tiện cần cảnh báo:")
        for vehicle in alert_list:
            print("\n=====================================\n")
            print(vehicle)

    elif choice == '7':
        lost_ticket_vehicles = vehicle_manager.lost_ticket_vehicles
        print("\n=====================================\n")
        print("\nDanh sách phương tiện bị mất vé trong ngày:")
        for vehicle in lost_ticket_vehicles:
            print("\n=====================================\n")
            print(vehicle)

    elif choice == '8':
        motorcycles_multiple_entries = vehicle_manager.get_motorcycles_with_multiple_entries()
        print("\n=====================================\n")
        print("\nDanh sách xe máy có lượt gửi từ 2 lần trong ngày hiện tại:")
        for vehicle in motorcycles_multiple_entries:
            print("\n=====================================\n")
            print(vehicle)

    elif choice == '0':
        print("Thoát")
    else:
        print("\n=====================================\n")
        print("Lựa chọn không hợp lệ!")
