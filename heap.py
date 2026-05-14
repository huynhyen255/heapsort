import streamlit as st
import graphviz

def draw_heap(arr, n, highlight_idx=-1):
    dot = graphviz.Digraph()
    dot.attr(nodesep='0.5', ranksep='0.5')
    for i in range(n):
        # Tô màu vàng cho nút đang được xét để dễ theo dõi
        color = "#FFD700" if i == highlight_idx else "white"
        dot.node(str(i), f"Index {i}\n({arr[i]})", style="filled", fillcolor=color)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n: dot.edge(str(i), str(left))
        if right < n: dot.edge(str(i), str(right))
    return dot

def heapify(arr, n, i, steps, label="Hiệu chỉnh"):
    # Ghi lại trạng thái bắt đầu xét nút i (Giống bước Hiệu chỉnh đống: i=... trong đề)
    steps.append({
        "type": f"{label}: Đang xét nút i = {i}",
        "array": list(arr),
        "n_current": n,
        "highlight": i
    })
    
    largest = i
    l, r = 2 * i + 1, 2 * i + 2

    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r

    if largest != i:
        val_i, val_largest = arr[i], arr[largest]
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # Ghi lại bước sau khi hoán vị thành công
        steps.append({
            "type": f"-> Hoán vị {val_i} <-> {val_largest} tại i = {i}",
            "array": list(arr),
            "n_current": n,
            "highlight": largest
        })
        heapify(arr, n, largest, steps, label)

def heap_sort_with_steps(arr):
    n = len(arr)
    steps = []
    # 1. Tạo Max-heap (Trang 1 đề thi)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, steps, label=f"Tạo đống (i={i})")

    # 2. Sắp xếp (Trang 2 đề thi)
    for i in range(n - 1, 0, -1):
        val_root, val_last = arr[0], arr[i]
        arr[0], arr[i] = arr[i], arr[0]
        steps.append({
            "type": f"Sắp xếp: Hoán vị gốc {val_root} <-> {val_last}",
            "array": list(arr),
            "n_current": i, # Thu hẹp phạm vi vẽ cây
            "highlight": 0
        })
        heapify(arr, i, 0, steps, label="Hiệu chỉnh lại đống tại gốc")
    return steps

# GIAO DIỆN
st.set_page_config(page_title="Heap Sort Solver", layout="wide")
st.title("📊 Heap Sort ")

# Thay đổi ở đây: Nhập bằng dấu cách
input_str = st.text_input("Nhập mảng số nguyên (cách nhau bằng dấu cách):", "29 40 25 70 27 12 45 19 8 10")

if st.button("Giải chi tiết"):
    try:
        # Xử lý nhập liệu: dùng split() không tham số sẽ tự cắt theo dấu cách/tab/xuống dòng
        arr = [int(x) for x in input_str.split()]
        
        if not arr:
            st.warning("Vui lòng nhập ít nhất một số!")
        else:
            all_steps = heap_sort_with_steps(arr)
            
            for idx, step in enumerate(all_steps):
                with st.expander(f"Bước {idx+1}: {step['type']}"):
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.write(f"Mảng a = `{step['array']}`")
                    with col2:
                        st.graphviz_chart(draw_heap(step['array'], step['n_current'], step['highlight']))
            
            st.success(f"Kết quả cuối cùng: {arr}")
            
    except ValueError:
        st.error("Lỗi: Vui lòng chỉ nhập các số nguyên cách nhau bằng dấu cách!")
