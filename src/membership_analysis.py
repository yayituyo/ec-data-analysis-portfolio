"""
会員ランクと購買行動の関係分析
・顧客単位で購買データを集計
・ランク別平均値算出
・箱ひげ図作成
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from db_connect import get_engine

# =========================
# 出力フォルダ作成
# =========================
os.makedirs("output", exist_ok=True)

# 日本語フォント設定（Windows想定）
plt.rcParams['font.family'] = 'MS Gothic'

# =========================
# DB接続
# =========================
engine = get_engine()

# =========================
# SQL実行
# =========================
sql = """
SELECT 
     k.顧客ID,
     mj.会員ランク,
     COUNT(kr.注文ID) AS 購入回数,
     COALESCE(SUM(kr.支払い金額),0) AS 総購入金額 
FROM 顧客情報 k
LEFT JOIN マイページ登録者情報 mj
  ON k.システム管理番号 = mj.システム管理番号 
LEFT JOIN 購入履歴 kr
  ON k.システム管理番号 = kr.システム管理番号
GROUP BY k.顧客ID, mj.会員ランク
"""

df = pd.read_sql(sql, engine)

# =========================
# 前処理
# =========================
df["会員ランク"] = df["会員ランク"].fillna("ランクなし")

# =========================
# ランク別集計
# =========================
rank_summary = df.groupby("会員ランク").agg(
    平均購入回数=("購入回数", "mean"),
    平均総購入金額=("総購入金額", "mean"),
    顧客数=("顧客ID", "count")
).sort_values("平均総購入金額", ascending=False)

print(rank_summary)

# =========================
# ファイル保存
# =========================
df.to_csv("output/customer_summary.csv", encoding="utf-8-sig", index=False)
rank_summary.to_csv("output/rank_summary.csv", encoding="utf-8-sig")

# =========================
# 箱ひげ図作成
# =========================
df.boxplot(column="総購入金額", by="会員ランク")
plt.title("会員ランク別 総購入金額分布")
plt.suptitle("")
plt.xlabel("会員ランク")
plt.ylabel("総購入金額")
plt.savefig("output/rank_sales_boxplot.png")
plt.close()