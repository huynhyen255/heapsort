import streamlit as st
import graphviz

# Hàm vẽ cây nhị phân từ mảng (giống trong ảnh đề thi)
def draw_heap(arr, n, highlight_idx=-1):
    dot = graphviz.Digraph()
    dot.attr(nodesep='0.5', ranksep='0.5')
    
    for i in range(n):
        color = "lightblue" if i == highlight_idx else "white"
        dot.node(str(i), f"Index {i}\n({arr[i]})", style="filled", fillcolor=color)
        
    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n:
            dot.edge(str(i), str(left))
        if right < n:
            dot.edge(str(i), str(right))
    return dot

def heapify(arr, n, i, steps):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l
    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        val_i, val_largest = arr[i], arr[largest]
        arr[i], arr[largest] = arr[largest], arr[i]
        
        # Ghi lại bước hiệu chỉnh đống (Hiệu chỉnh đống: i=...)
        steps.append({
            "type": f"Hiệu chỉnh đống: Hoán vị {val_i} <-> {val_largest}",
            "array": list(arr),
            "n_current": n
        })
        heapify(arr, n, largest, steps)

def heap_sort_with_steps(arr):
    n = len(arr)
    steps = []
    
    # Bước ban đầu
    steps.append({"type": "Mảng ban đầu", "array": list(arr), "n_current": n})

    # 1. Tạo Max-heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, steps)
        steps.append({"type": f"Tạo Max-heap (i={i})", "array": list(arr), "n_current": n})

    # 2. Sắp xếp (Hoán vị và Hiệu chỉnh)
    for i in range(n - 1, 0, -1):
        val_root, val_last = arr[0], arr[i]
        arr[0], arr[i] = arr[i], arr[0]
        steps.append({"type": f"Sắp xếp: Hoán vị {val_root} <-> {val_last}", "array": list(arr), "n_current": i})
        heapify(arr, i, 0, steps)
        
    return steps

# GIAO DIỆN STREAMLIT
st.set_page_config(page_title="Heap Sort Solver", layout="wide")
st.title("🗂️ Heap Sort Step-by-Step Solver")
st.write("Giải bài tập Cấu trúc dữ liệu & Giải thuật giống định dạng đề thi")

input_str = st.text_input("Nhập mảng số nguyên (cách nhau bằng dấu phẩy):", "29, 40, 25, 70, 27, 12, 45, 19, 8, 10")

if st.button("Giải ngay"):
    try:
        arr = [int(x.strip()) for x in input_str.split(",")]
        original_arr = list(arr)
        
        all_steps = heap_sort_with_steps(arr)
        
        # Hiển thị từng bước
        for idx, step in enumerate(all_steps):
            with st.expander(f"Bước {idx}: {step['type']}"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(f"**Mảng a =** `{step['array']}`")
                    if "Sắp xếp" in step['type']:
                        st.info(f"Phần tử đã cố định ở cuối: {original_arr[step['n_current']:]}")
                with col2:
                    st.graphviz_chart(draw_heap(step['array'], step['n_current']))
                    
        st.success(f"Kết quả cuối cùng: {arr}")
        
    except ValueError:
        st.error("Vui lòng nhập đúng định dạng số nguyên!")
