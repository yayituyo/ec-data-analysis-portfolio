select 
     k.顧客ID,
	 mj.会員ランク,
	 count(kr.注文ID) AS 購入回数,
     coalesce(sum(kr.支払い金額),0) AS 総購入金額 
from 顧客情報 k
left join マイページ登録者情報 mj
on k.システム管理番号 = mj.システム管理番号 
left join 購入履歴 kr
on k.システム管理番号 = kr.システム管理番号
group by k.顧客ID,mj.会員ランク