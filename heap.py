import streamlit as st
import graphviz

# Vẽ cây nhị phân với chỉ số và giá trị riêng biệt
def draw_heap(arr, n, highlight_idx=-1):
    dot = graphviz.Digraph()
    dot.attr(nodesep='0.2', ranksep='0.3')
    dot.attr('node', shape='circle', fontsize='10', width='0.4', height='0.4')
    
    for i in range(n):
        # Nút đang hiệu chỉnh có màu xám giống đề thi
        color = "#aaaaaa" if i == highlight_idx else "white"
        # Index trên, giá trị trong ngoặc dưới
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
    
    # --- PHẦN 1: CÂY BAN ĐẦU ---
    all_steps.append({"is_section": True, "content": f"### **Cây ban đầu cho mảng a:**\n`a = {arr}`, n = {n}"})
    all_steps.append({"label": "Cây ban đầu:", "array": list(arr), "n": n, "highlight": -1})

    # --- PHẦN 2: TẠO MAX-HEAP ---
    all_steps.append({"is_section": True, "content": "### **Tạo max-heap:**"})
    temp_arr = list(arr)
    for i in range(n // 2 - 1, -1, -1):
        all_steps.append({"label": f"Hiệu chỉnh đống: i = {i}", "array": list(temp_arr), "n": n, "highlight": i})
        heapify(temp_arr, n, i, all_steps)

    # --- PHẦN 3: SẮP XẾP ---
    all_steps.append({"is_section": True, "content": "### **Sắp xếp:**"})
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
        
        all_steps.append({"label": "Hiệu chỉnh đống:", "array": list(temp_arr), "n": i, "highlight": 0})
        heapify(temp_arr, i, 0, all_steps)
        
    return all_steps

# Giao diện chính
st.set_page_config(page_title="Đáp án Heap Sort", layout="wide")
st.markdown("<h2 style='text-align: center;'>TRƯỜNG ĐẠI HỌC TIỀN GIANG</h2>", unsafe_allow_html=True)

input_str = st.text_input("Nhập dãy số (cách nhau bởi dấu cách):", "29 40 25 70 27 12 45 19 8 10")

if st.button("XEM ĐÁP ÁN CHI TIẾT"):
    data = [int(x) for x in input_str.split()]
    steps = solve_heap_sort(data)
    
    cols = st.columns(3)
    step_counter = 1 # Biến đếm số bước toàn cục
    
    for step in steps:
        if "is_section" in step:
            st.markdown(step["content"])
            st.divider()
            # Không reset step_counter ở đây để số thứ tự chạy liên tục từ đầu đến cuối
        else:
            with cols[(step_counter - 1) % 3]:
                # Sử dụng border=True để tạo khung ô lưới giống tờ đề
                with st.container(border=True):
                    # Đánh dấu số bước ở góc trái ngay con chuột bạn chỉ
                    st.markdown(f"**Bước {step_counter}**") 
                    st.caption(step["label"])
                    st.graphviz_chart(draw_heap(step["array"], step["n"], step["highlight"]))
                    if "footer" in step:
                        st.write(f"*{step['footer']}*")
            step_counter += 1
