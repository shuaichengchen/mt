import math
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt

# =========================
# Matplotlib 中文字体修复
# =========================
matplotlib.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "SimSun",
    "KaiTi",
    "FangSong",
    "Noto Sans CJK SC",
    "Arial Unicode MS",
    "DejaVu Sans"
]
matplotlib.rcParams["axes.unicode_minus"] = False
matplotlib.rcParams["font.family"] = "sans-serif"

st.set_page_config(
    page_title="基于 Python 的平抛运动虚拟实验与学习反馈系统",
    page_icon="📘",
    layout="wide"
)

# =========================
# 页面美化 CSS
# =========================
def inject_custom_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f6f9ff 0%, #eef3ff 45%, #f8fbff 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eef4ff 0%, #f7faff 100%);
        border-right: 1px solid rgba(80, 120, 200, 0.15);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-title {
        font-size: 2.65rem;
        font-weight: 900;
        color: #1f2a44;
        margin-bottom: 0.35rem;
        letter-spacing: 0.3px;
    }

    .subtitle-text {
        font-size: 1.05rem;
        color: #4b587c;
        line-height: 1.9;
        margin-bottom: 1.2rem;
    }

    .hero-box {
        background: rgba(255, 255, 255, 0.84);
        border: 1px solid rgba(90, 120, 200, 0.12);
        border-radius: 24px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 10px 30px rgba(31, 42, 68, 0.08);
        backdrop-filter: blur(8px);
        margin-bottom: 1.2rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.94);
        border: 1px solid rgba(90, 120, 200, 0.12);
        border-radius: 20px;
        padding: 1rem 1.2rem;
        box-shadow: 0 8px 24px rgba(31, 42, 68, 0.08);
        transition: all 0.25s ease;
        height: 100%;
        min-height: 120px;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px rgba(31, 42, 68, 0.12);
    }

    .metric-label {
        font-size: 0.95rem;
        color: #64739a;
        margin-bottom: 0.45rem;
        font-weight: 600;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #1f2a44;
        line-height: 1.1;
    }

    .section-card {
        background: rgba(255,255,255,0.9);
        border: 1px solid rgba(90, 120, 200, 0.12);
        border-radius: 22px;
        padding: 1.2rem 1.3rem;
        box-shadow: 0 8px 24px rgba(31, 42, 68, 0.07);
        margin-bottom: 1rem;
    }

    .mini-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #233457;
        margin-bottom: 0.7rem;
    }

    .soft-note {
        background: linear-gradient(135deg, #eef5ff 0%, #f8fbff 100%);
        border-left: 4px solid #5b8def;
        border-radius: 14px;
        padding: 0.9rem 1rem;
        color: #35507d;
        line-height: 1.8;
        margin-top: 0.6rem;
        margin-bottom: 0.6rem;
    }

    .result-box {
        background: linear-gradient(135deg, #ffffff 0%, #f7faff 100%);
        border: 1px solid rgba(90, 120, 200, 0.12);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        box-shadow: 0 8px 20px rgba(31, 42, 68, 0.06);
        margin-bottom: 1rem;
    }

    .sidebar-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #21304f;
        margin-bottom: 1rem;
    }

    div[data-testid="stTabs"] button {
        font-weight: 700;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
    }

    .footer-note {
        text-align: center;
        color: #6f7fa6;
        font-size: 0.92rem;
        margin-top: 1rem;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 700;
        border: none;
        padding: 0.55rem 1.1rem;
        box-shadow: 0 6px 18px rgba(91, 141, 239, 0.20);
    }

    .stDownloadButton > button {
        border-radius: 12px;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)


inject_custom_css()

# =========================
# 工具函数
# =========================
def metric_card(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_open(title):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="mini-title">{title}</div>
        """,
        unsafe_allow_html=True
    )


def section_close():
    st.markdown("</div>", unsafe_allow_html=True)


def simulate_ideal(v0, h, g, dt):
    total_time = math.sqrt(2 * h / g)
    t = np.arange(0, total_time + dt, dt)
    x = v0 * t
    y = h - 0.5 * g * t**2
    y = np.maximum(y, 0)

    vx = np.full_like(t, v0)
    vy = -g * t
    speed = np.sqrt(vx**2 + vy**2)

    df = pd.DataFrame({
        "时间(s)": t,
        "水平位移x(m)": x,
        "竖直高度y(m)": y,
        "水平速度vx(m/s)": vx,
        "竖直速度vy(m/s)": vy,
        "合速度v(m/s)": speed
    })

    return {
        "df": df,
        "total_time": float(total_time),
        "range": float(v0 * total_time),
        "final_speed": float(math.sqrt(v0**2 + (g * total_time)**2))
    }


def simulate_drag(v0, h, g, dt, k):
    t_list = [0.0]
    x_list = [0.0]
    y_list = [h]
    vx_list = [v0]
    vy_list = [0.0]

    x = 0.0
    y = h
    vx = v0
    vy = 0.0
    t = 0.0

    max_steps = 100000

    for _ in range(max_steps):
        ax = -k * vx
        ay = -g - k * vy

        vx = vx + ax * dt
        vy = vy + ay * dt

        x = x + vx * dt
        y = y + vy * dt
        t = t + dt

        if y < 0:
            y = 0

        t_list.append(t)
        x_list.append(x)
        y_list.append(y)
        vx_list.append(vx)
        vy_list.append(vy)

        if y <= 0:
            break

    t_arr = np.array(t_list)
    x_arr = np.array(x_list)
    y_arr = np.array(y_list)
    vx_arr = np.array(vx_list)
    vy_arr = np.array(vy_list)
    speed_arr = np.sqrt(vx_arr**2 + vy_arr**2)

    df = pd.DataFrame({
        "时间(s)": t_arr,
        "水平位移x(m)": x_arr,
        "竖直高度y(m)": y_arr,
        "水平速度vx(m/s)": vx_arr,
        "竖直速度vy(m/s)": vy_arr,
        "合速度v(m/s)": speed_arr
    })

    return {
        "df": df,
        "total_time": float(t_arr[-1]),
        "range": float(x_arr[-1]),
        "final_speed": float(speed_arr[-1])
    }


def get_frame_data(df, progress):
    idx = int(progress * (len(df) - 1))
    idx = max(0, min(idx, len(df) - 1))
    return idx, df.iloc[idx]


def plot_trajectory(df, h, title="平抛轨迹图"):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["水平位移x(m)"], df["竖直高度y(m)"], linewidth=2.5, label="运动轨迹")
    ax.scatter(df["水平位移x(m)"].iloc[0], df["竖直高度y(m)"].iloc[0], s=70, label="起点")
    ax.scatter(df["水平位移x(m)"].iloc[-1], df["竖直高度y(m)"].iloc[-1], s=70, label="落点")
    ax.set_title(title, fontsize=16, fontweight="bold")
    ax.set_xlabel("水平位移 x / m", fontsize=13)
    ax.set_ylabel("高度 y / m", fontsize=13)
    ax.set_ylim(bottom=0, top=max(h * 1.1, 1))
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_displacement(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["时间(s)"], df["水平位移x(m)"], label="x-t 图", linewidth=2.2)
    ax.plot(df["时间(s)"], df["竖直高度y(m)"], label="y-t 图", linewidth=2.2)
    ax.set_title("位移—时间图像", fontsize=16, fontweight="bold")
    ax.set_xlabel("时间 t / s", fontsize=13)
    ax.set_ylabel("位移 / 高度", fontsize=13)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_velocity(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["时间(s)"], df["水平速度vx(m/s)"], label="vx-t 图", linewidth=2.2)
    ax.plot(df["时间(s)"], df["竖直速度vy(m/s)"], label="vy-t 图", linewidth=2.2)
    ax.plot(df["时间(s)"], df["合速度v(m/s)"], label="v-t 图", linewidth=2.2)
    ax.set_title("速度—时间图像", fontsize=16, fontweight="bold")
    ax.set_xlabel("时间 t / s", fontsize=13)
    ax.set_ylabel("速度 / (m/s)", fontsize=13)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_compare(df1, df2, label1="理想模型", label2="空气阻力模型"):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df1["水平位移x(m)"], df1["竖直高度y(m)"], label=label1, linewidth=2.4)
    ax.plot(df2["水平位移x(m)"], df2["竖直高度y(m)"], label=label2, linewidth=2.4)
    ax.set_title("不同模型轨迹对比", fontsize=16, fontweight="bold")
    ax.set_xlabel("水平位移 x / m", fontsize=13)
    ax.set_ylabel("高度 y / m", fontsize=13)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    return fig


def dataframe_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def build_feedback(score, answers):
    advice = []
    wrong_points = []

    std = {
        "q1": "匀速直线运动",
        "q2": "自由落体运动",
        "q3": "无关",
        "q4": "变大",
        "q5": "抛物线"
    }

    if answers["q1"] != std["q1"]:
        wrong_points.append("对水平方向运动性质理解不准确")
        advice.append("平抛运动忽略空气阻力时，水平方向不受力，因此做匀速直线运动。")

    if answers["q2"] != std["q2"]:
        wrong_points.append("对竖直方向运动性质理解不准确")
        advice.append("竖直方向只受重力作用，因此属于自由落体运动。")

    if answers["q3"] != std["q3"]:
        wrong_points.append("对飞行时间影响因素理解不准确")
        advice.append("飞行时间由高度和重力加速度决定，与水平初速度无关。")

    if answers["q4"] != std["q4"]:
        wrong_points.append("对射程与初速度关系理解不准确")
        advice.append("在高度不变时，飞行时间不变，初速度越大，水平射程越大。")

    if answers["q5"] != std["q5"]:
        wrong_points.append("对轨迹形状理解不准确")
        advice.append("平抛运动由水平方向匀速和竖直方向自由落体合成，因此轨迹是抛物线。")

    if score == 5:
        summary = "你对平抛运动的核心规律掌握很好，已经能够准确理解运动分解、飞行时间和射程变化。"
    elif score >= 3:
        summary = "你已掌握平抛运动的大部分基础规律，但仍有部分概念需要进一步巩固。"
    else:
        summary = "你目前对平抛运动的核心概念掌握还不够牢固，建议结合轨迹图和分运动分析重新学习。"

    return summary, wrong_points, advice


# =========================
# 侧边栏
# =========================
st.sidebar.markdown('<div class="sidebar-title">实验参数设置</div>', unsafe_allow_html=True)

model_type = st.sidebar.radio(
    "选择实验模型",
    ["理想模型（忽略空气阻力）", "空气阻力模型（线性阻力）"]
)

v0 = st.sidebar.slider("水平初速度 v₀（m/s）", 1.0, 30.0, 10.0, 0.5)
h = st.sidebar.slider("抛出高度 h（m）", 0.5, 50.0, 10.0, 0.5)
g = st.sidebar.slider("重力加速度 g（m/s²）", 1.0, 20.0, 9.8, 0.1)
dt = st.sidebar.slider("时间步长 dt（s）", 0.001, 0.1, 0.01, 0.001)

k = 0.0
if "空气阻力" in model_type:
    k = st.sidebar.slider("空气阻力系数 k", 0.0, 2.0, 0.15, 0.01)

show_trace = st.sidebar.checkbox("显示轨迹", value=True)
show_data = st.sidebar.checkbox("显示数据表", value=True)
show_charts = st.sidebar.checkbox("显示图像分析", value=True)
show_compare = st.sidebar.checkbox("显示理想/阻力模型对比", value=True)

# =========================
# 仿真
# =========================
if "理想模型" in model_type:
    result = simulate_ideal(v0, h, g, dt)
else:
    result = simulate_drag(v0, h, g, dt, k)

df = result["df"]
ideal_result = simulate_ideal(v0, h, g, dt)
ideal_df = ideal_result["df"]

# =========================
# 顶部介绍
# =========================
st.markdown(
    """
    <div class="hero-box">
        <div class="main-title">基于 Python 的平抛运动虚拟实验与学习反馈系统</div>
        <div class="subtitle-text">
            本系统面向中学物理教学，支持平抛运动的虚拟实验、数据分析、图像展示、参数探究与学习反馈。<br>
            可直接用于课程设计、毕业设计、论文展示、课堂演示与教学答辩。
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# 顶部指标卡
# =========================
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("飞行时间", f"{result['total_time']:.3f} s")
with m2:
    metric_card("水平射程", f"{result['range']:.3f} m")
with m3:
    metric_card("落地速度", f"{result['final_speed']:.3f} m/s")
with m4:
    metric_card("采样点数", f"{len(df)}")

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# Tabs
# =========================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "虚拟实验",
    "图像分析",
    "参数探究",
    "学习反馈",
    "教学说明"
])

# =========================
# Tab1 虚拟实验
# =========================
with tab1:
    section_open("平抛运动虚拟实验区")

    left, right = st.columns([1.45, 1])

    with left:
        progress = st.slider("拖动查看运动过程", 0.0, 1.0, 0.0, 0.01)
        idx, row = get_frame_data(df, progress)

        fig, ax = plt.subplots(figsize=(9, 5))
        if show_trace:
            ax.plot(
                df["水平位移x(m)"][:idx+1],
                df["竖直高度y(m)"][:idx+1],
                linewidth=2.5,
                label="运动轨迹"
            )

        ax.scatter(
            df["水平位移x(m)"].iloc[idx],
            df["竖直高度y(m)"].iloc[idx],
            s=130,
            label="当前位置"
        )

        ax.axhline(0, linestyle="--", alpha=0.7)
        ax.set_xlim(0, max(df["水平位移x(m)"].max() * 1.1, 1))
        ax.set_ylim(0, max(h * 1.15, 1))
        ax.set_xlabel("水平位移 x / m", fontsize=13)
        ax.set_ylabel("高度 y / m", fontsize=13)
        ax.set_title("平抛运动过程演示", fontsize=16, fontweight="bold")
        ax.grid(True, alpha=0.25)
        ax.legend()
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)

    with right:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### 当前状态")
        st.write(f"**当前时刻：** {row['时间(s)']:.3f} s")
        st.write(f"**水平位移：** {row['水平位移x(m)']:.3f} m")
        st.write(f"**当前高度：** {row['竖直高度y(m)']:.3f} m")
        st.write(f"**水平速度：** {row['水平速度vx(m/s)']:.3f} m/s")
        st.write(f"**竖直速度：** {row['竖直速度vy(m/s)']:.3f} m/s")
        st.write(f"**合速度：** {row['合速度v(m/s)']:.3f} m/s")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="soft-note">
                <b>物理解释：</b><br>
                平抛运动可分解为两个互不影响的分运动：<br>
                1. 水平方向做匀速直线运动；<br>
                2. 竖直方向做自由落体运动。
            </div>
            """,
            unsafe_allow_html=True
        )

        if "空气阻力" in model_type:
            st.warning("当前采用空气阻力模型，水平方向速度会逐渐减小，轨迹与理想模型不同。")
        else:
            st.success("当前采用理想模型，忽略空气阻力。")

    if show_data:
        st.markdown("### 实验数据表")
        st.dataframe(df, use_container_width=True, height=320)
        st.download_button(
            "下载实验数据 CSV",
            data=dataframe_to_csv_bytes(df),
            file_name="平抛运动实验数据.csv",
            mime="text/csv"
        )

    section_close()

# =========================
# Tab2 图像分析
# =========================
with tab2:
    section_open("图像分析与模型对比")

    if show_charts:
        c1, c2 = st.columns(2)
        with c1:
            st.pyplot(plot_trajectory(df, h, "当前模型轨迹图"), use_container_width=True)
        with c2:
            st.pyplot(plot_displacement(df), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.pyplot(plot_velocity(df), use_container_width=True)
        with c4:
            if show_compare:
                if "空气阻力" in model_type:
                    st.pyplot(plot_compare(ideal_df, df), use_container_width=True)
                else:
                    drag_result = simulate_drag(v0, h, g, dt, 0.15)
                    st.pyplot(
                        plot_compare(df, drag_result["df"], "理想模型", "阻力模型(k=0.15)"),
                        use_container_width=True
                    )

    st.markdown(
        """
        <div class="soft-note">
            <b>图像规律总结：</b><br>
            1. 在理想模型中，水平速度 vx 保持不变。<br>
            2. 竖直速度 vy 随时间线性变化。<br>
            3. 轨迹为抛物线。<br>
            4. 存在空气阻力时，水平速度逐渐减小，射程减小，轨迹更短、更陡。
        </div>
        """,
        unsafe_allow_html=True
    )

    section_close()

# =========================
# Tab3 参数探究
# =========================
with tab3:
    section_open("参数探究实验")

    st.markdown("### 1. 改变初速度，探究水平射程变化")
    v_list = np.linspace(max(1, v0 - 6), v0 + 6, 7)
    ranges_v = []
    for vv in v_list:
        if "理想模型" in model_type:
            rr = simulate_ideal(float(vv), h, g, dt)["range"]
        else:
            rr = simulate_drag(float(vv), h, g, dt, k)["range"]
        ranges_v.append(rr)

    df_v = pd.DataFrame({
        "初速度 v0(m/s)": np.round(v_list, 3),
        "水平射程 L(m)": np.round(ranges_v, 3)
    })
    st.dataframe(df_v, use_container_width=True)

    fig_v, ax_v = plt.subplots(figsize=(8, 4))
    ax_v.plot(df_v["初速度 v0(m/s)"], df_v["水平射程 L(m)"], marker="o", linewidth=2.2)
    ax_v.set_title("初速度与水平射程关系", fontsize=16, fontweight="bold")
    ax_v.set_xlabel("初速度 v0 / (m/s)", fontsize=13)
    ax_v.set_ylabel("水平射程 L / m", fontsize=13)
    ax_v.grid(True, alpha=0.25)
    fig_v.tight_layout()
    st.pyplot(fig_v, use_container_width=True)

    st.markdown("### 2. 改变高度，探究飞行时间变化")
    h_list = np.linspace(max(0.5, h - 6), h + 6, 7)
    times_h = []
    for hh in h_list:
        if "理想模型" in model_type:
            tt = simulate_ideal(v0, float(hh), g, dt)["total_time"]
        else:
            tt = simulate_drag(v0, float(hh), g, dt, k)["total_time"]
        times_h.append(tt)

    df_h = pd.DataFrame({
        "高度 h(m)": np.round(h_list, 3),
        "飞行时间 t(s)": np.round(times_h, 3)
    })
    st.dataframe(df_h, use_container_width=True)

    fig_h, ax_h = plt.subplots(figsize=(8, 4))
    ax_h.plot(df_h["高度 h(m)"], df_h["飞行时间 t(s)"], marker="o", linewidth=2.2)
    ax_h.set_title("高度与飞行时间关系", fontsize=16, fontweight="bold")
    ax_h.set_xlabel("高度 h / m", fontsize=13)
    ax_h.set_ylabel("飞行时间 t / s", fontsize=13)
    ax_h.grid(True, alpha=0.25)
    fig_h.tight_layout()
    st.pyplot(fig_h, use_container_width=True)

    st.success(
        "实验结论：在其他条件不变时，初速度增大，水平射程增大；抛出高度增大，飞行时间增大。理想模型中飞行时间与初速度无关。"
    )

    section_close()

# =========================
# Tab4 学习反馈
# =========================
with tab4:
    section_open("学习反馈与知识诊断")

    st.markdown("请完成下面 5 道题，系统会自动评分并给出反馈。")

    q1 = st.radio(
        "1. 平抛运动在水平方向做什么运动？",
        ["匀速直线运动", "匀加速直线运动", "自由落体运动"],
        key="q1"
    )

    q2 = st.radio(
        "2. 平抛运动在竖直方向做什么运动？",
        ["匀速直线运动", "自由落体运动", "匀减速直线运动"],
        key="q2"
    )

    q3 = st.radio(
        "3. 忽略空气阻力时，平抛运动的飞行时间与初速度的关系是？",
        ["有关", "无关"],
        key="q3"
    )

    q4 = st.radio(
        "4. 在抛出高度不变时，初速度增大，水平射程会怎样？",
        ["变小", "不变", "变大"],
        key="q4"
    )

    q5 = st.radio(
        "5. 平抛运动的轨迹是什么形状？",
        ["直线", "圆弧", "抛物线"],
        key="q5"
    )

    if st.button("提交并生成学习反馈"):
        answers = {
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "q4": q4,
            "q5": q5
        }

        std = {
            "q1": "匀速直线运动",
            "q2": "自由落体运动",
            "q3": "无关",
            "q4": "变大",
            "q5": "抛物线"
        }

        score = sum(1 for kq in std if answers[kq] == std[kq])
        summary, wrong_points, advice = build_feedback(score, answers)

        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("得分", f"{score} / 5")
        with c2:
            st.info(summary)

        st.markdown("### 知识薄弱点")
        if wrong_points:
            for p in wrong_points:
                st.write(f"- {p}")
        else:
            st.write("- 暂无明显薄弱点，掌握较好。")

        st.markdown("### 个性化建议")
        if advice:
            for a in advice:
                st.write(f"- {a}")
        else:
            st.write("- 建议进一步尝试改变参数，观察图像变化，加深理解。")

        st.success("平抛运动的核心在于运动分解：水平方向匀速，竖直方向自由落体，两者合成形成抛物线轨迹。")

    section_close()

# =========================
# Tab5 教学说明
# =========================
with tab5:
    section_open("系统教学说明与落地应用")

    st.markdown("""
### 一、项目定位
本系统是一个面向中学物理教学的虚拟实验平台，适用于：
- 高中物理《平抛运动》课堂演示
- 学生自主探究学习
- 课程设计与毕业设计项目
- 教学比赛、说课展示、论文成果展示

### 二、功能亮点
1. 支持理想模型与空气阻力模型切换  
2. 支持参数调节与过程观察  
3. 自动生成位移、速度与轨迹图像  
4. 支持参数探究实验  
5. 内置学习反馈系统，可自动评分与知识诊断  

### 三、课堂应用建议
- 课前预习：让学生先观察不同参数下的轨迹变化  
- 课中实验：边调参边讨论“飞行时间与谁有关”“射程与谁有关”  
- 课后巩固：通过反馈题检测概念掌握情况  

### 四、可继续拓展的方向
- 增加自动播放动画
- 增加多球同屏对比
- 增加实验报告自动生成
- 增加错题记录与学习档案
- 增加 AI 问答助手模块
- 增加桌面端 tkinter / pygame 版本
""")

    st.markdown("### 五、核心公式")
    st.latex(r"x = v_0 t")
    st.latex(r"y = h - \frac{1}{2}gt^2")
    st.latex(r"t = \sqrt{\frac{2h}{g}}")
    st.latex(r"L = v_0 \sqrt{\frac{2h}{g}}")
    st.latex(r"y = h - \frac{g}{2v_0^2}x^2")

    section_close()

st.markdown(
    '<div class="footer-note">开发说明：本系统使用 Python + Streamlit + NumPy + Pandas + Matplotlib 实现。</div>',
    unsafe_allow_html=True
)
