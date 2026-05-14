import streamlit as st
import graphviz

# Vẽ cây nhị phân tối giản
def draw_heap(arr, n, highlight_idx=-1):
    dot = graphviz.Digraph()
    dot.attr(nodesep='0.2', ranksep='0.3')
    dot.attr('node', shape='circle', fontsize='10', width='0.4', height='0.4')
    for i in range(n):
        color = "#aaaaaa" if i == highlight_idx else "white"
        dot.node(str(i), f"{i}\n({arr[i]})", style="filled", fillcolor=color)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n: dot.edge(str(i), str(left))
        if right < n: dot.edge(str(i), str(right))
    return dot

def heapify(arr, n, i, steps, label_prefix="Hiệu chỉnh đống"):
    largest = i
    l, r = 2 * i + 1, 2 * i + 2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r

    if largest != i:
        val_i, val_lg = arr[i], arr[largest]
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # Ghi lại bước hoán vị CHI TIẾT ngay dưới tiêu đề i = ...
        steps.append({
            "label": f"{label_prefix}: Hoán vị {val_i} ↔ {val_lg}",
            "array": list(arr),
            "n": n,
            "highlight": largest
        })
        # Tiếp tục đệ quy hiệu chỉnh xuống các nhánh dưới
        heapify(arr, n, largest, steps, label_prefix)

def solve_heap_sort(arr):
    n = len(arr)
    all_steps = []
    all_steps.append({"is_section": True, "content": "### **1. Tạo max-heap (Vun đống)**"})

    temp_arr = list(arr)
    # Duyệt từ i = n/2 - 1 về 0 theo đúng đề thi
    for i in range(n // 2 - 1, -1, -1):
        # Ghi bước bắt đầu xét i
        all_steps.append({
            "label": f"Hiệu chỉnh đống: i = {i}", 
            "array": list(temp_arr), 
            "n": n, 
            "highlight": i
        })
        # Gọi heapify để tìm các hoán vị con bên trong i đó
        heapify(temp_arr, n, i, all_steps, label_prefix=f"Hiệu chỉnh đống i={i}")

    all_steps.append({"is_section": True, "content": "### **2. Sắp xếp (Trích xuất)**"})
    # ... (Phần code sắp xếp tương tự nhưng dùng label "Sắp xếp")
    for i in range(n - 1, 0, -1):
        v_root, v_last = temp_arr[0], temp_arr[i]
        temp_arr[0], temp_arr[i] = temp_arr[i], temp_arr[0]
        all_steps.append({"label": f"Hoán vị {v_root} ↔ {v_last}", "array": list(temp_arr), "n": i, "highlight": 0, "footer": f"Mảng a = {list(temp_arr[i:])}"})
        all_steps.append({"label": "Hiệu chỉnh đống:", "array": list(temp_arr), "n": i, "highlight": 0})
        heapify(temp_arr, i, 0, all_steps)
        
    return all_steps

# GIAO DIỆN
st.set_page_config(page_title="Đáp án Heap Sort chuẩn", layout="wide")
st.markdown("<h2 style='text-align: center;'>TRƯỜNG ĐẠI HỌC TIỀN GIANG</h2>", unsafe_allow_html=True)

input_str = st.text_input("Nhập dãy số:", "29 40 25 70 27 12 45 19 8 10")

if st.button("XEM ĐÁP ÁN"):
    data = [int(x) for x in input_str.split()]
    steps = solve_heap_sort(data)
    cols = st.columns(3)
    for idx, step in enumerate([s for s in steps if "is_section" not in s]):
        with cols[idx % 3]:
            with st.container(border=True):
                st.markdown(f"**Bước {idx + 1}**")
                st.caption(step["label"]) # Sẽ hiện "Hiệu chỉnh đống: i = 4" hoặc "Hoán vị..."
                st.graphviz_chart(draw_heap(step["array"], step["n"], step["highlight"]))
                if "footer" in step: st.write(step["footer"])
