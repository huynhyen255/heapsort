import streamlit as st
import graphviz

# Cấu hình vẽ cây nhị phân tối giản giống đề thi
def draw_heap(arr, n, highlight_idx=-1):
    dot = graphviz.Digraph()
    dot.attr(nodesep='0.2', ranksep='0.3')
    # Set font và size nhỏ lại để vừa với ô lưới
    dot.attr('node', shape='circle', fontsize='10', width='0.4', height='0.4')
    
    for i in range(n):
        # Nút đang được hiệu chỉnh sẽ có màu xám đậm hơn giống đề
        color = "#aaaaaa" if i == highlight_idx else "white"
        # Hiển thị chỉ số bên trên và giá trị bên dưới giống ảnh 3
        dot.node(str(i), f"{i}\n({arr[i]})", style="filled", fillcolor=color)
        
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n: dot.edge(str(i), str(left))
        if right < n: dot.edge(str(i), str(right))
    return dot

def heapify(arr, n, i, steps):
    largest = i
    l, r = 2 * i + 1, 2 * i + 2
    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Sau mỗi lần hoán vị trong heapify, ghi lại trạng thái cây
        steps.append({
            "label": "Hiệu chỉnh đống:",
            "array": list(arr),
            "n": n,
            "highlight": largest
        })
        heapify(arr, n, largest, steps)

def solve_heap_sort(arr):
    n = len(arr)
    all_steps = []
    
    # BƯỚC 1: CÂY BAN ĐẦU
    all_steps.append({
        "is_section": True, 
        "content": f"**Câu 1: (2.0 điểm)**\n\n**Cây ban đầu cho mảng a:**\n`a = {arr}`, n = {n}"
    })
    all_steps.append({"label": "Cây ban đầu:", "array": list(arr), "n": n, "highlight": -1})

    # BƯỚC 2: TẠO MAX-HEAP
    all_steps.append({"is_section": True, "content": "### **Tạo max-heap:**"})
    temp_arr = list(arr)
    for i in range(n // 2 - 1, -1, -1):
        all_steps.append({
            "label": f"Hiệu chỉnh đống: i = {i}", 
            "array": list(temp_arr), 
            "n": n, 
            "highlight": i
        })
        heapify(temp_arr, n, i, all_steps)

    # BƯỚC 3: SẮP XẾP
    all_steps.append({"is_section": True, "content": "### **Sắp xếp:**"})
    for i in range(n - 1, 0, -1):
        v_root, v_last = temp_arr[0], temp_arr[i]
        temp_arr[0], temp_arr[i] = temp_arr[i], temp_arr[0]
        
        # Ghi lại bước hoán vị giống ảnh 1
        all_steps.append({
            "label": f"Hoán vị {v_root} <-> {v_last}", 
            "array": list(temp_arr), 
            "n": i, 
            "highlight": 0,
            "footer": f"Mảng a = {list(temp_arr[i:])}"
        })
        
        all_steps.append({"label": "Hiệu chỉnh đống:", "array": list(temp_arr), "n": i, "highlight": 0})
        heapify(temp_arr, i, 0, all_steps)
        
    all_steps.append({"is_section": True, "content": f"**Kết quả sắp xếp: a = {temp_arr}**"})
    return all_steps

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Đáp án Heap Sort", layout="wide")
st.markdown("<h2 style='text-align: center;'>TRƯỜNG ĐẠI HỌC TIỀN GIANG</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>ĐÁP ÁN ĐỀ THI SỐ: 01</h3>", unsafe_allow_html=True)

input_str = st.text_input("Nhập dãy số (cách nhau bởi dấu cách):", "29 40 25 70 27 12 45 19 8 10")

if st.button("XEM ĐÁP ÁN CHI TIẾT"):
    data = [int(x) for x in input_str.split()]
    steps = solve_heap_sort(data)
    
    # Dùng columns để tạo lưới 3 cột giống trong tờ đề
    cols = st.columns(3)
    col_idx = 0
    
    for step in steps:
        if "is_section" in step:
            st.markdown(step["content"])
            st.divider()
            col_idx = 0 # Reset lưới khi sang phần mới
        else:
            with cols[col_idx % 3]:
                # Tạo một khung viền bao quanh mỗi bước giống bảng trong đề
                with st.container(border=True):
                    st.caption(step["label"])
                    st.graphviz_chart(draw_heap(step["array"], step["n"], step["highlight"]))
                    if "footer" in step:
                        st.write(f"*{step['footer']}*")
            col_idx += 1
