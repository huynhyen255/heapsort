import streamlit as st
import graphviz

# 1. Hàm vẽ cây nhị phân (Tối ưu kích thước nhỏ gọn cho mobile)
def draw_heap(arr, n, highlight_idx=-1):
    dot = graphviz.Digraph()
    dot.attr(nodesep='0.15', ranksep='0.2')
    # Giảm size node một chút để không bị tràn màn hình điện thoại
    dot.attr('node', shape='circle', fontsize='9', width='0.35', height='0.35')
    for i in range(n):
        color = "#aaaaaa" if i == highlight_idx else "white"
        dot.node(str(i), f"{i}\n({arr[i]})", style="filled", fillcolor=color)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n: dot.edge(str(i), str(left))
        if right < n: dot.edge(str(i), str(right))
    return dot

# 2. Thuật toán Heapify
def heapify(arr, n, i, steps, label_prefix):
    largest = i
    l, r = 2 * i + 1, 2 * i + 2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r
    if largest != i:
        val_i, val_lg = arr[i], arr[largest]
        arr[i], arr[largest] = arr[largest], arr[i]
        steps.append({
            "label": f"{label_prefix}: Hoán vị {val_i} ↔ {val_lg}",
            "array": list(arr),
            "n": n,
            "highlight": largest
        })
        heapify(arr, n, largest, steps, label_prefix)

# 3. Giải Heap Sort
def solve_heap_sort(arr):
    n = len(arr)
    all_steps = []
    all_steps.append({"label": "Cây ban đầu cho mảng a:", "array": list(arr), "n": n, "highlight": -1})
    temp_arr = list(arr)
    for i in range(n // 2 - 1, -1, -1):
        all_steps.append({"label": f"Hiệu chỉnh đống: i = {i}", "array": list(temp_arr), "n": n, "highlight": i})
        heapify(temp_arr, n, i, all_steps, label_prefix=f"Hiệu chỉnh đống i={i}")
    for i in range(n - 1, 0, -1):
        v_root, v_last = temp_arr[0], temp_arr[i]
        temp_arr[0], temp_arr[i] = temp_arr[i], temp_arr[0]
        all_steps.append({"label": f"Hoán vị {v_root} ↔ {v_last}", "array": list(temp_arr), "n": i, "highlight": 0, "footer": f"Mảng a = {list(temp_arr[i:])}"})
        all_steps.append({"label": "Hiệu chỉnh đống:", "array": list(temp_arr), "n": i, "highlight": 0})
        heapify(temp_arr, i, 0, all_steps, label_prefix="Hiệu chỉnh đống")
    return all_steps

# --- GIAO DIỆN STREAMLIT ---
st.set_page_config(page_title="Heap Sort Chuẩn Tiền Giang", layout="wide")

# CSS MỚI: Bỏ min-height cứng, dùng padding và căn chỉnh linh hoạt
st.markdown("""
    <style>
    /* Làm container gọn hơn trên Mobile */
    [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    /* Căn giữa biểu đồ và giới hạn chiều rộng tối đa */
    .stGraphvizChart {
        display: flex;
        justify-content: center;
        max-width: 100%;
        overflow-x: auto;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-size: 1.5rem;'>ĐÁP ÁN CHI TIẾT HEAP SORT</h2>", unsafe_allow_html=True)

input_str = st.text_input("Nhập dãy số:", "29 40 25 70 27 12 45 19 8 10")

if st.button("XEM ĐÁP ÁN"):
    data = [int(x) for x in input_str.split()]
    steps = solve_heap_sort(data)
    
    # Sử dụng columns nhưng Streamlit sẽ tự động stack (chồng lên nhau) khi xem trên mobile
    cols = st.columns(3)
    
    for idx, step in enumerate(steps):
        with cols[idx % 3]:
            # Dùng border=True giúp tạo khung bao quanh từng bước
            with st.container(border=True):
                st.markdown(f"**Bước {idx + 1}**")
                # Hiển thị text gọn gàng, không ép height quá lớn
                st.info(step['label']) 
                st.graphviz_chart(draw_heap(step["array"], step["n"], step["highlight"]), use_container_width=True)
                if "footer" in step:
                    st.caption(f"_{step['footer']}_")
