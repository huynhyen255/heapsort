import streamlit as st
import graphviz

# Cấu hình vẽ cây nhị phân giống sơ đồ trong đề
def draw_heap(arr, n, highlight_idx=-1):
    dot = graphviz.Digraph()
    dot.attr(nodesep='0.5', ranksep='0.5')
    for i in range(n):
        # Tô màu xám nhạt cho nút đang xét giống như trong ảnh đề thi
        color = "#e0e0e0" if i == highlight_idx else "white"
        dot.node(str(i), f"{i}\n({arr[i]})", style="filled", fillcolor=color, shape="circle")
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n: dot.edge(str(i), str(left))
        if right < n: dot.edge(str(i), str(right))
    return dot

def heapify(arr, n, i, steps, label="Hiệu chỉnh đống"):
    largest = i
    l, r = 2 * i + 1, 2 * i + 2

    if l < n and arr[l] > arr[largest]: largest = l
    if r < n and arr[r] > arr[largest]: largest = r

    if largest != i:
        v_i, v_l = arr[i], arr[largest]
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # Ghi lại bước hoán vị giống format: Hoán vị 29 <-> 10
        steps.append({
            "header": f"Hoán vị {v_i} <-> {v_l}",
            "array": list(arr),
            "n_current": n,
            "highlight": largest,
            "footer": f"Mảng a = {list(arr)}"
        })
        heapify(arr, n, largest, steps, label)

def heap_sort_with_steps(arr):
    n = len(arr)
    steps = []
    
    # Bước ban đầu: Cây ban đầu cho mảng a
    steps.append({
        "header": "Cây ban đầu cho mảng a:",
        "array": list(arr),
        "n_current": n,
        "highlight": -1,
        "footer": f"int [] a = {list(arr)}, n = {n}"
    })

    # 1. TẠO MAX-HEAP (Trang 1 của đề)
    steps.append({"is_title": True, "title": "Tạo max-heap:"})
    for i in range(n // 2 - 1, -1, -1):
        steps.append({
            "header": f"Hiệu chỉnh đống: i = {i}",
            "array": list(arr),
            "n_current": n,
            "highlight": i,
            "footer": ""
        })
        heapify(arr, n, i, steps)

    # 2. SẮP XẾP (Trang 2 của đề)
    steps.append({"is_title": True, "title": "Sắp xếp:"})
    for i in range(n - 1, 0, -1):
        v_root, v_last = arr[0], arr[i]
        arr[0], arr[i] = arr[i], arr[0]
        
        steps.append({
            "header": f"Hoán vị {v_root} <-> {arr[i]}",
            "array": list(arr),
            "n_current": i,
            "highlight": 0,
            "footer": f"Mảng a = {list(arr[i:])}"
        })
        
        steps.append({
            "header": "Hiệu chỉnh đống:",
            "array": list(arr),
            "n_current": i,
            "highlight": 0,
            "footer": ""
        })
        heapify(arr, i, 0, steps)
        
    steps.append({"header": "Dừng:", "array": list(arr), "n_current": 1, "highlight": -1, "footer": f"Kết quả sắp xếp: {arr}"})
    return steps

# GIAO DIỆN STREAMLIT
st.set_page_config(page_title="DS&A Heap Sort Solver", layout="centered")
st.title("Trường Đại học Tiền Giang")
st.subheader("Khoa Kỹ thuật Công nghệ - Đáp án Heap Sort")

input_str = st.text_input("Nhập mảng số nguyên (cách nhau bởi dấu cách):", "29 40 25 70 27 12 45 19 8 10")

if st.button("Xử lý giống đề thi"):
    arr = [int(x) for x in input_str.split()]
    all_steps = heap_sort_with_steps(arr)
    
    for step in all_steps:
        if "is_title" in step:
            st.markdown(f"### **{step['title']}**")
            st.divider()
        else:
            # Tạo khung hiển thị giống các ô trong tờ giấy thi
            with st.container():
                st.write(f"**{step['header']}**")
                st.graphviz_chart(draw_heap(step['array'], step['n_current'], step['highlight']))
                if step['footer']:
                    st.write(f"*{step['footer']}*")
                st.markdown("---")
