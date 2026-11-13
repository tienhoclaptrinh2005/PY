"""Câu 3 - Đọc, thống kê, vẽ biểu đồ và lọc dữ liệu CSV."""

from pathlib import Path
import sys

import matplotlib

# Dùng backend không cần cửa sổ vì đề chỉ yêu cầu lưu biểu đồ ra file.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


THU_MUC = Path(__file__).resolve().parent
FILE_DU_LIEU = THU_MUC / "du_lieu_09.csv"
FILE_BIEU_DO = THU_MUC / "bieudo.png"
FILE_CANH_BAO = THU_MUC / "canh_bao.csv"


def doc_du_lieu(duong_dan=FILE_DU_LIEU):
    """Đọc CSV và giữ MaMon ở dạng chuỗi để không mất số 0 đầu."""
    return pd.read_csv(duong_dan, dtype={"MaMon": str})


def in_thong_ke(du_lieu):
    """In số bản ghi, tổng/điểm trung bình và môn có điểm cao nhất."""
    if du_lieu.empty:
        print("File không có bản ghi nào.")
        return

    tong_ban_ghi = len(du_lieu)
    tong_diem = du_lieu["Diem"].sum()
    diem_trung_binh = du_lieu["Diem"].mean()
    mon_cao_nhat = du_lieu.loc[du_lieu["Diem"].idxmax()]

    print(f"Tổng số bản ghi: {tong_ban_ghi}")
    print(f"Tổng điểm môn học: {tong_diem:g}")
    print(f"Điểm môn học trung bình: {diem_trung_binh:g}")
    print(
        "Môn có điểm cao nhất: "
        f"{mon_cao_nhat['TenMon']} ({mon_cao_nhat['MaMon']}) - {mon_cao_nhat['Diem']:g}"
    )


def ve_bieu_do(du_lieu, duong_dan=FILE_BIEU_DO):
    """Vẽ biểu đồ cột số tín chỉ theo tên môn và lưu thành PNG."""
    fig, ax = plt.subplots(figsize=(10, 6))
    cot = ax.bar(du_lieu["TenMon"], du_lieu["SoTinChi"], color="#377eb8")
    ax.set_title("Số tín chỉ của từng môn học", fontsize=15, fontweight="bold")
    ax.set_xlabel("Tên môn")
    ax.set_ylabel("Số tín chỉ")
    ax.bar_label(cot, padding=3)
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    fig.tight_layout()
    fig.savefig(duong_dan, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Đã lưu biểu đồ: {duong_dan.name}")


def xuat_canh_bao(du_lieu, duong_dan=FILE_CANH_BAO):
    """Lọc các môn có SoTinChi < 10 và xuất ra CSV."""
    canh_bao = du_lieu[du_lieu["SoTinChi"] < 10].copy()
    canh_bao.to_csv(duong_dan, index=False, encoding="utf-8-sig")
    print(f"Đã xuất {len(canh_bao)} bản ghi cảnh báo: {duong_dan.name}")
    return canh_bao


def main():
    # Bảo đảm chữ Việt hiển thị đúng cả khi stdout bị chuyển hướng trên Windows.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        du_lieu = doc_du_lieu()
    except FileNotFoundError:
        print(f"Không tìm thấy file dữ liệu: {FILE_DU_LIEU}")
        return
    except (ValueError, pd.errors.ParserError) as loi:
        print(f"Không thể đọc dữ liệu CSV: {loi}")
        return

    print("Dữ liệu đã đọc:")
    print(du_lieu.to_string(index=False))
    print()
    in_thong_ke(du_lieu)
    ve_bieu_do(du_lieu)
    xuat_canh_bao(du_lieu)


if __name__ == "__main__":
    main()
