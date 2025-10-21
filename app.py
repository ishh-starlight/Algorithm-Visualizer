import streamlit as st
import random
import matplotlib.pyplot as plt
import time

# --- Streamlit Setup ---
st.set_page_config(page_title="Sorting Visualizer", layout="wide")
st.title("🎨 Sorting Algorithm Visualizer")

# --- Sidebar Controls ---
algo = st.sidebar.selectbox(
    "Select Sorting Algorithm",
    ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
)
size = st.sidebar.slider("Array Size", 5, 30, 10)
speed_option = st.sidebar.selectbox("Select Speed", ["🐢 Slow", "⚙️ Medium", "⚡ Fast"])

# --- Speed delay ---
if "Slow" in speed_option:
    delay = 3.0
elif "Medium" in speed_option:
    delay = 2.0
else:
    delay = 1.0

arr = [random.randint(10, 100) for _ in range(size)]
start_btn = st.sidebar.button("Start Visualization")

# --- Layout: side-by-side columns ---
col1, col2 = st.columns([2, 1])  # chart 2x wider than log

plot_placeholder = col1.empty()
log_placeholder = col2.empty()

# --- Plot Function ---
def plot_array(arr, color_positions=None):
    fig, ax = plt.subplots(figsize=(6, 3))  # smaller figure size
    bars = ax.bar(range(len(arr)), arr, color="skyblue")

    if color_positions:
        for i in color_positions:
            bars[i].set_color("red")

    # Show values above bars
    for i, val in enumerate(arr):
        ax.text(i, val + 1, str(val), ha='center', va='bottom', fontsize=9)

    ax.set_xticks([])
    ax.set_yticks([])
    plot_placeholder.pyplot(fig, use_container_width=True)
    plt.close(fig)

# --- Sorting Algorithms ---
def bubble_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                steps.append(f"Swapped {arr[j]} and {arr[j+1]}")
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, [j, j + 1], steps.copy()

def selection_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(f"Swapped {arr[i]} with {arr[min_idx]}")
        yield arr, [i, min_idx], steps.copy()

def insertion_sort(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            steps.append(f"Moved {arr[j]} after {key}")
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, [j + 1, i], steps.copy()
        arr[j + 1] = key
        yield arr, [j + 1, i], steps.copy()

def merge_sort(arr, l=0, r=None, steps=None):
    if steps is None: steps = []
    if r is None: r = len(arr)
    if r - l > 1:
        m = (l + r) // 2
        yield from merge_sort(arr, l, m, steps)
        yield from merge_sort(arr, m, r, steps)
        left, right = arr[l:m], arr[m:r]
        i = j = 0
        for k in range(l, r):
            if j >= len(right) or (i < len(left) and left[i] < right[j]):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            steps.append(f"Inserted {arr[k]} at position {k}")
            yield arr, [k], steps.copy()

def quick_sort(arr, low=0, high=None, steps=None):
    if steps is None: steps = []
    if high is None: high = len(arr) - 1

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append(f"Swapped {arr[i]} and {arr[j]} (pivot {pivot})")
                yield arr, [i, j], steps.copy()
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append(f"Placed pivot {arr[i+1]} at correct position")
        yield arr, [i + 1, high], steps.copy()

    if low < high:
        gen = partition(low, high)
        for arr, pos, s in gen:
            yield arr, pos, s
        yield from quick_sort(arr, low, high - 1, steps)

# --- Main Logic ---
if start_btn:
    working_arr = arr.copy()
    log_lines = []
    plot_array(working_arr)

    if algo == "Bubble Sort":
        gen = bubble_sort(working_arr)
    elif algo == "Selection Sort":
        gen = selection_sort(working_arr)
    elif algo == "Insertion Sort":
        gen = insertion_sort(working_arr)
    elif algo == "Merge Sort":
        gen = merge_sort(working_arr)
    else:
        gen = quick_sort(working_arr)

    for updated_arr, color_pos, steps in gen:
        plot_array(updated_arr, color_pos)
        log_lines = steps
        log_placeholder.text_area("Algorithm Steps Log", "\n".join(log_lines), height=400)
        time.sleep(delay)

    st.success("✅ Sorting Complete!")
    st.info(f"Final Sorted Array: {working_arr}")
