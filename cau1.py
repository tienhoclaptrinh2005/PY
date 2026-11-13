"""Câu 1 - Quản lý điểm học tập bằng giao diện console."""

import sys


def them_ban_ghi(danh_sach, ma, ten, diem, sotinchi):
    """Thêm một bản ghi môn học vào danh_sach và trả về bản ghi vừa thêm."""
    ban_ghi = {
        "MaMon": str(ma).strip(),
        "TenMon": str(ten).strip(),
        "Diem": float(diem),
        "SoTinChi": int(sotinchi),
    }
    danh_sach.append(ban_ghi)
    return ban_ghi


def tim_kiem_theo_ten(danh_sach, tu_khoa):
    """Tìm các môn có TenMon chứa từ khóa, không phân biệt hoa/thường."""
    tu_khoa = str(tu_khoa).strip().casefold()
    return [
        ban_ghi
        for ban_ghi in danh_sach
        if tu_khoa in str(ban_ghi["TenMon"]).casefold()
    ]


def tinh_tong_gia_tri(danh_sach):
    """Tính tổng Diem * SoTinChi của tất cả bản ghi."""
    return sum(
        float(ban_ghi["Diem"]) * int(ban_ghi["SoTinChi"])
        for ban_ghi in danh_sach
    )


def tao_du_lieu_mau():
    """Trả về dữ liệu mẫu của đề thi."""
    return [
        {"MaMon": "0901", "TenMon": "điểm học tập A", "Diem": 40000.0, "SoTinChi": 15},
        {"MaMon": "0902", "TenMon": "điểm học tập B", "Diem": 96000.0, "SoTinChi": 8},
        {"MaMon": "0903", "TenMon": "điểm học tập C", "Diem": 25000.0, "SoTinChi": 20},
        {"MaMon": "0904", "TenMon": "điểm học tập D", "Diem": 47500.0, "SoTinChi": 5},
        {"MaMon": "0905", "TenMon": "điểm học tập E", "Diem": 17000.0, "SoTinChi": 60},
    ]


def dinh_dang_so(gia_tri):
    """Hiển thị số nguyên gọn, số thực giữ tối đa hai chữ số thập phân."""
    gia_tri = float(gia_tri)
    if gia_tri.is_integer():
        return f"{int(gia_tri):,}"
    return f"{gia_tri:,.2f}"


def hien_thi_danh_sach(danh_sach):
    """In danh sách môn học dạng bảng."""
    if not danh_sach:
        print("Không tìm thấy bản ghi phù hợp.")
        return

    print(f"{'MaMon':<10}{'TenMon':<30}{'Diem':>15}{'SoTinChi':>12}")
    print("-" * 67)
    for ban_ghi in danh_sach:
        print(
            f"{ban_ghi['MaMon']:<10}"
            f"{ban_ghi['TenMon']:<30}"
            f"{dinh_dang_so(ban_ghi['Diem']):>15}"
            f"{ban_ghi['SoTinChi']:>12}"
        )


def nhap_ban_ghi(danh_sach):
    """Nhập, kiểm tra và thêm một môn học từ bàn phím."""
    ma = input("Nhập mã môn: ").strip()
    ten = input("Nhập tên môn: ").strip()

    if not ma or not ten:
        print("Lỗi: Mã môn và tên môn không được để trống.")
        return

    try:
        diem = float(input("Nhập điểm môn học: ").strip())
        so_tin_chi_text = input("Nhập số tín chỉ: ").strip()
        so_tin_chi = int(so_tin_chi_text)
        if diem < 0 or so_tin_chi <= 0:
            raise ValueError
    except ValueError:
        print("Lỗi: Điểm phải là số không âm và số tín chỉ phải là số nguyên dương.")
        return

    ban_ghi = them_ban_ghi(danh_sach, ma, ten, diem, so_tin_chi)
    print("Đã thêm bản ghi:")
    hien_thi_danh_sach([ban_ghi])


def main():
    # Bảo đảm chữ Việt hiển thị đúng cả khi stdout bị chuyển hướng trên Windows.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    danh_sach = tao_du_lieu_mau()

    while True:
        print("\n===== QUẢN LÝ ĐIỂM HỌC TẬP =====")
        print("1. Thêm bản ghi")
        print("2. Tìm kiếm theo tên")
        print("3. Xem tổng giá trị")
        print("4. Thoát")
        lua_chon = input("Chọn chức năng (1-4): ").strip()

        if lua_chon == "1":
            nhap_ban_ghi(danh_sach)
        elif lua_chon == "2":
            tu_khoa = input("Nhập từ khóa tên môn: ")
            ket_qua = tim_kiem_theo_ten(danh_sach, tu_khoa)
            print(f"Tìm thấy {len(ket_qua)} bản ghi:")
            hien_thi_danh_sach(ket_qua)
        elif lua_chon == "3":
            tong = tinh_tong_gia_tri(danh_sach)
            print(f"Tổng giá trị (Điểm x Số tín chỉ): {dinh_dang_so(tong)}")
        elif lua_chon == "4":
            print("Đã thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 4.")


if __name__ == "__main__":
    main()
