


import random
import streamlit as st
import matplotlib.pyplot as plt

def simulate_case_open(prices_and_chances, num_trials=10000):
    winnings = []
    for _ in range(num_trials):
        roll = random.uniform(0, 100)
        cumulative = 0
        for price, chance in prices_and_chances:
            cumulative += chance
            if roll <= cumulative:
                winnings.append(price)
                break
    return winnings

def simulate_upgrade(current_price, target_price, success_chance, num_trials=10000):
    profits = []
    for _ in range(num_trials):
        roll = random.uniform(0, 100)
        if roll <= success_chance:
            profits.append(target_price - current_price)
        else:
            profits.append(-current_price)
    return profits

st.title("🎮 Симулятор кейсов и апгрейдов Topskin")

st.sidebar.header("🔧 Настройки кейса")
case_price = st.sidebar.number_input("Цена кейса ($)", min_value=0.01, value=2.5, step=0.01)
num_trials = st.sidebar.number_input("Количество симуляций", min_value=100, max_value=100000, value=10000, step=100)

st.sidebar.markdown("### 📦 Предметы в кейсе")
num_items = st.sidebar.slider("Сколько предметов в кейсе?", 2, 10, 5)

prices_and_chances = []
remaining_chance = 100.0

for i in range(num_items):
    st.sidebar.markdown(f"#### Предмет {i+1}")
    price = st.sidebar.number_input(f"Цена {i+1}-го предмета ($)", min_value=0.0, value=float(i + 1), key=f"price_{i}")
    if i < num_items - 1:
        chance = st.sidebar.slider(f"Шанс выпадения (%)", 0.0, remaining_chance, value=remaining_chance / (num_items - i), key=f"chance_{i}")
        remaining_chance -= chance
    else:
        chance = remaining_chance
    prices_and_chances.append((price, chance))

if st.button("🎲 Симулировать кейс"):
    results = simulate_case_open(prices_and_chances, num_trials)
    average_win = sum(results) / len(results)
    profit = average_win - case_price

    st.markdown("### 📊 Результаты кейса")
    st.write(f"Средняя окупаемость: **${average_win:.2f}**")
    st.write(f"Ожидаемая прибыль/убыток: **${profit:.2f}**")

    fig, ax = plt.subplots()
    ax.hist(results, bins=30, color='skyblue', edgecolor='black')
    ax.axvline(case_price, color='red', linestyle='--', label='Цена кейса')
    ax.set_title("Распределение выигрышей")
    ax.set_xlabel("Выигрыш ($)")
    ax.set_ylabel("Частота")
    ax.legend()
    st.pyplot(fig)

st.markdown("---")
st.header("🧩 Симулятор апгрейда")

current_price = st.number_input("Цена текущего предмета ($)", min_value=0.01, value=2.5)
target_price = st.number_input("Цена желаемого предмета ($)", min_value=current_price + 0.01, value=10.0)
success_chance = st.slider("Шанс успешного апгрейда (%)", 1.0, 100.0, 30.0)

if st.button("🎯 Симулировать апгрейд"):
    upgrade_results = simulate_upgrade(current_price, target_price, success_chance, num_trials)
    avg_profit = sum(upgrade_results) / len(upgrade_results)
    success_rate = (sum(1 for r in upgrade_results if r > 0) / len(upgrade_results)) * 100

    st.markdown("### 📈 Результаты апгрейда")
    st.write(f"Средняя прибыль/убыток: **${avg_profit:.2f}**")
    st.write(f"Реальный шанс успеха: **{success_rate:.2f}%**")

    fig2, ax2 = plt.subplots()
    ax2.hist(upgrade_results, bins=30, color='orange', edgecolor='black')
    ax2.axvline(0, color='red', linestyle='--')
    ax2.set_title("Распределение прибыли от апгрейда")
    ax2.set_xlabel("Профит ($)")
    ax2.set_ylabel("Частота")
    st.pyplot(fig2)
