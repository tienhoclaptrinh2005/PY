"""Câu 2 - Giao diện GUI quản lý điểm học tập bằng Tkinter."""

import tkinter as tk
from tkinter import messagebox, ttk

from cau1 import tao_du_lieu_mau, them_ban_ghi, tim_kiem_theo_ten


class QuanLyDiemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý điểm học tập")
        self.root.geometry("850x570")
        self.root.minsize(760, 500)

        self.danh_sach = tao_du_lieu_mau()
        self.tao_giao_dien()
        self.hien_thi_danh_sach(self.danh_sach)

    def tao_giao_dien(self):
        style = ttk.Style()
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        tieu_de = ttk.Label(
            self.root,
            text="QUẢN LÝ ĐIỂM HỌC TẬP",
            font=("Segoe UI", 18, "bold"),
        )
        tieu_de.pack(pady=(14, 8))

        khung_nhap = ttk.LabelFrame(self.root, text="Thông tin môn học", padding=12)
        khung_nhap.pack(fill="x", padx=16, pady=6)
        khung_nhap.columnconfigure(1, weight=1)
        khung_nhap.columnconfigure(3, weight=1)

        self.ma_var = tk.StringVar()
        self.ten_var = tk.StringVar()
        self.diem_var = tk.StringVar()
        self.tin_chi_var = tk.StringVar()

        ttk.Label(khung_nhap, text="Mã môn:").grid(row=0, column=0, sticky="w", padx=5, pady=6)
        self.ma_entry = ttk.Entry(khung_nhap, textvariable=self.ma_var)
        self.ma_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=6)

        ttk.Label(khung_nhap, text="Tên môn:").grid(row=0, column=2, sticky="w", padx=5, pady=6)
        ttk.Entry(khung_nhap, textvariable=self.ten_var).grid(
            row=0, column=3, sticky="ew", padx=5, pady=6
        )

        ttk.Label(khung_nhap, text="Điểm môn học:").grid(
            row=1, column=0, sticky="w", padx=5, pady=6
        )
        ttk.Entry(khung_nhap, textvariable=self.diem_var).grid(
            row=1, column=1, sticky="ew", padx=5, pady=6
        )

        ttk.Label(khung_nhap, text="Số tín chỉ:").grid(
            row=1, column=2, sticky="w", padx=5, pady=6
        )
        ttk.Entry(khung_nhap, textvariable=self.tin_chi_var).grid(
            row=1, column=3, sticky="ew", padx=5, pady=6
        )

        ttk.Button(khung_nhap, text="Thêm", command=self.them).grid(
            row=2, column=0, columnspan=4, pady=(9, 2), ipadx=28
        )

        khung_tim = ttk.LabelFrame(self.root, text="Tìm kiếm theo tên môn", padding=10)
        khung_tim.pack(fill="x", padx=16, pady=6)
        khung_tim.columnconfigure(0, weight=1)

        self.tu_khoa_var = tk.StringVar()
        tu_khoa_entry = ttk.Entry(khung_tim, textvariable=self.tu_khoa_var)
        tu_khoa_entry.grid(row=0, column=0, sticky="ew", padx=(2, 8))
        tu_khoa_entry.bind("<Return>", lambda _event: self.tim_kiem())
        ttk.Button(khung_tim, text="Tìm kiếm", command=self.tim_kiem).grid(row=0, column=1, padx=4)
        ttk.Button(khung_tim, text="Hiển thị tất cả", command=self.hien_thi_tat_ca).grid(
            row=0, column=2, padx=4
        )

        khung_bang = ttk.Frame(self.root)
        khung_bang.pack(fill="both", expand=True, padx=16, pady=(6, 12))

        cot = ("MaMon", "TenMon", "Diem", "SoTinChi")
        self.bang = ttk.Treeview(khung_bang, columns=cot, show="headings")
        self.bang.heading("MaMon", text="Mã môn")
        self.bang.heading("TenMon", text="Tên môn")
        self.bang.heading("Diem", text="Điểm")
        self.bang.heading("SoTinChi", text="Số tín chỉ")
        self.bang.column("MaMon", width=110, anchor="center")
        self.bang.column("TenMon", width=350, anchor="w")
        self.bang.column("Diem", width=150, anchor="e")
        self.bang.column("SoTinChi", width=110, anchor="center")

        thanh_cuon = ttk.Scrollbar(khung_bang, orient="vertical", command=self.bang.yview)
        self.bang.configure(yscrollcommand=thanh_cuon.set)
        self.bang.pack(side="left", fill="both", expand=True)
        thanh_cuon.pack(side="right", fill="y")

        self.trang_thai_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.trang_thai_var, anchor="w").pack(
            fill="x", padx=18, pady=(0, 8)
        )

        self.ma_entry.focus_set()

    @staticmethod
    def dinh_dang_diem(diem):
        diem = float(diem)
        return str(int(diem)) if diem.is_integer() else f"{diem:.2f}"

    def hien_thi_danh_sach(self, danh_sach):
        # Xóa kết quả cũ trước khi hiển thị kết quả mới.
        for item in self.bang.get_children():
            self.bang.delete(item)

        for ban_ghi in danh_sach:
            self.bang.insert(
                "",
                "end",
                values=(
                    ban_ghi["MaMon"],
                    ban_ghi["TenMon"],
                    self.dinh_dang_diem(ban_ghi["Diem"]),
                    ban_ghi["SoTinChi"],
                ),
            )
        self.trang_thai_var.set(f"Đang hiển thị {len(danh_sach)} bản ghi")

    def them(self):
        ma = self.ma_var.get().strip()
        ten = self.ten_var.get().strip()
        diem_text = self.diem_var.get().strip()
        tin_chi_text = self.tin_chi_var.get().strip()

        if not ma or not ten:
            messagebox.showerror("Dữ liệu không hợp lệ", "Mã môn và tên môn không được để trống.")
            return

        try:
            diem = float(diem_text)
            so_tin_chi = int(tin_chi_text)
            if diem < 0 or so_tin_chi <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Dữ liệu không hợp lệ",
                "Điểm phải là số không âm và số tín chỉ phải là số nguyên dương.",
            )
            return

        ban_ghi = them_ban_ghi(self.danh_sach, ma, ten, diem, so_tin_chi)
        self.hien_thi_danh_sach(self.danh_sach)
        self.bang.selection_set(self.bang.get_children()[-1])
        self.bang.see(self.bang.get_children()[-1])

        self.ma_var.set("")
        self.ten_var.set("")
        self.diem_var.set("")
        self.tin_chi_var.set("")
        self.ma_entry.focus_set()
        messagebox.showinfo("Thành công", f"Đã thêm môn {ban_ghi['TenMon']}.")

    def tim_kiem(self):
        ket_qua = tim_kiem_theo_ten(self.danh_sach, self.tu_khoa_var.get())
        self.hien_thi_danh_sach(ket_qua)

    def hien_thi_tat_ca(self):
        self.tu_khoa_var.set("")
        self.hien_thi_danh_sach(self.danh_sach)


def main():
    root = tk.Tk()
    QuanLyDiemApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
