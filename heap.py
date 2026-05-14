import streamlit as st
import graphviz

# Vẽ cây nhị phân
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

def heapify(arr, n, i, steps, label_prefix, is_sorting=False):
    largest = i
    l, r = 2 * i + 1, 2 * i + 2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r

    if largest != i:
        val_i, val_lg = arr[i], arr[largest]
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # CHỈ THÊM BƯỚC KHI CÓ HOÁN VỊ
        steps.append({
            "label": f"{label_prefix}: Hoán vị {val_i} ↔ {val_lg}",
            "array": list(arr),
            "n": n,
            "highlight": largest
        })
        heapify(arr, n, largest, steps, label_prefix, is_sorting)
    return largest != i # Trả về True nếu có hoán vị

def solve_heap_sort(arr):
    n = len(arr)
    all_steps = []
    
    # 1. Cây ban đầu
    all_steps.append({"label": "Cây ban đầu cho mảng a:", "array": list(arr), "n": n, "highlight": -1, "is_header": True})

    temp_arr = list(arr)
    # 2. Tạo Max-heap
    for i in range(n // 2 - 1, -1, -1):
        # Lưu trạng thái trước khi heapify để kiểm tra xem có biến động không
        has_changed = heapify(temp_arr, n, i, all_steps, label_prefix=f"Hiệu chỉnh đống i={i}")
        # Nếu không có hoán vị nào, ta vẫn thêm 1 bước "Hiệu chỉnh đống: i=..." nếu đó là bước quan trọng hoặc bạn muốn lược bỏ luôn?
        # Ở đây mình sẽ chỉ giữ lại những bước CÓ hoán vị như bạn yêu cầu.

    # 3. Sắp xếp
    for i in range(n - 1, 0, -1):
        v_root, v_last = temp_arr[0], temp_arr[i]
        temp_arr[0], temp_arr[i] = temp_arr[i], temp_arr[0]
        
        all_steps.append({
            "label": f"Hoán vị {v_root} ↔ {v_last}", 
            "array": list(temp_arr), 
            "n": i, 
            "highlight": 0,
            "footer": f"Mảng a = {list(temp_arr[i:])}"
        })
        heapify(temp_arr, i, 0, all_steps, label_prefix="Hiệu chỉnh đống")
        
    return all_steps

# GIAO DIỆN
st.set_page_config(page_title="Heap Sort Chuẩn", layout="wide")
st.markdown("<h2 style='text-align: center;'>ĐÁP ÁN CHI TIẾT HEAP SORT</h2>", unsafe_allow_html=True)

input_str = st.text_input("Nhập dãy số:", "29 40 25 70 27 12 45 19 8 10")

if st.button("XEM ĐÁP ÁN"):
    data = [int(x) for x in input_str.split()]
    steps = solve_heap_sort(data)
    cols = st.columns(3)
    
    display_idx = 0
    for step in steps:
        with cols[display_idx % 3]:
            with st.container(border=True):
                st.markdown(f"**Bước {display_idx + 1}**")
                st.caption(step["label"])
                st.graphviz_chart(draw_heap(step["array"], step["n"], step["highlight"]))
                if "footer" in step: st.write(f"*{step['footer']}*")
        display_idx += 1
