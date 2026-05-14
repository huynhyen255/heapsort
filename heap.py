import streamlit as st
import graphviz

def draw_heap(arr, n, highlight_idx=-1):
    dot = graphviz.Digraph()
    dot.attr(nodesep='0.5', ranksep='0.5')
    for i in range(n):
        # Tô màu nút đang được hiệu chỉnh để giống đề thi
        color = "#FFD700" if i == highlight_idx else "white"
        dot.node(str(i), f"Index {i}\n({arr[i]})", style="filled", fillcolor=color)
    for i in range(n):
        left, right = 2 * i + 1, 2 * i + 2
        if left < n: dot.edge(str(i), str(left))
        if right < n: dot.edge(str(i), str(right))
    return dot

def heapify(arr, n, i, steps, label="Hiệu chỉnh"):
    # Ghi lại trạng thái trước khi so sánh (giống bước "Hiệu chỉnh đống: i=..." trong đề)
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
        arr[i], arr[largest] = arr[largest], arr[i]
        steps.append({
            "type": f"-> Hoán vị {arr[largest]} <-> {arr[i]} tại i = {i}",
            "array": list(arr),
            "n_current": n,
            "highlight": largest
        })
        heapify(arr, n, largest, steps, label)

def heap_sort_with_steps(arr):
    n = len(arr)
    steps = []
    # 1. Tạo Max-heap (Giai đoạn xây dựng đống ban đầu)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, steps, label=f"Tạo đống (i={i})")

    # 2. Sắp xếp (Giai đoạn hoán vị gốc và thu hẹp đống)
    for i in range(n - 1, 0, -1):
        val_root, val_last = arr[0], arr[i]
        arr[0], arr[i] = arr[i], arr[0]
        steps.append({
            "type": f"Sắp xếp: Hoán vị gốc {val_root} <-> {val_last} (Đưa {val_root} về cuối)",
            "array": list(arr),
            "n_current": i, # Thu hẹp đống
            "highlight": 0
        })
        heapify(arr, i, 0, steps, label="Hiệu chỉnh lại đống tại gốc")
    return steps

st.set_page_config(page_title="Heap Sort Solver", layout="wide")
st.title("📊 Heap Sort Step-by-Step")

input_str = st.text_input("Nhập mảng:", "29, 40, 25, 70, 27, 12, 45, 19, 8, 10")
if st.button("Giải chi tiết"):
    arr = [int(x.strip()) for x in input_str.split(",")]
    all_steps = heap_sort_with_steps(arr)
    for idx, step in enumerate(all_steps):
        with st.expander(f"Bước {idx+1}: {step['type']}"):
            st.write(f"Mảng hiện tại: `{step['array']}`")
            st.graphviz_chart(draw_heap(step['array'], step['n_current'], step['highlight']))
