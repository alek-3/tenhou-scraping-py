import bs4
from operator import itemgetter
import datetime
import os

output = []
path = os.path.join('天鳳ランキング_files', 'dummy.html')

with open(path, 'r', encoding='utf-8') as f:
    # ファイルをhtml解析しやすいよう変換
    soup = bs4.BeautifulSoup(f, 'html.parser')

    # 検索プレーヤー名の抽出
    player_name = soup.select('#txtPlayerID')[0].get('value')
    print(player_name)

    # 対戦情報をすべて抽出
    spans = soup.find_all('span')

    count = 1
    for i in spans:
        id_text = i['id']

        # プレーヤー名と一致した項目のidから、順位を見る
        if i.getText() == player_name:
            if 'PLAYER1' in id_text:
                rank = 1
            elif 'PLAYER2' in id_text:
                rank = 2
            elif 'PLAYER3' in id_text:
                rank = 3
            else: # 4位引いたとき
                rank = 4
            # 対戦番号と順位を記録
            result = {
                'No.': count,
                '順位': rank
            }
            output.append(result)

            # 戦績を追加した段階で対戦数を加算
            count += 1 

# 新しい順になっていた戦績を古い順に逆転
output = sorted(output, key=lambda x: x['No.'], reverse=True)

# 取得されたoutputをベースに分析する
analysis = []
num_games = count # このとき対戦数 + 1
count_first = 0
count_second = 0
count_third = 0
count_fourth = 0

for row in output:
    game_num = num_games - row['No.']

    # プレーヤーの順位を取得し、回数に追加する。
    if row['順位'] == 1:
        count_first += 1
    elif row['順位'] == 2:
        count_second += 1
    elif row['順位'] == 3:
        count_third += 1
    else:
        count_fourth += 1

    rank_times = {
        'No.': game_num,
        '1位': count_first,
        '2位': count_second,
        '3位': count_third,
        '4位': count_fourth
    }

    if game_num > 100:
        rank_times_bef100 = analysis[game_num - 100 - 1] # 101ゲーム目の場合、1ゲーム目を取得
        rank_times['直近1位'] = count_first - rank_times_bef100['1位']
        rank_times['直近2位'] = count_second  - rank_times_bef100['2位']
        rank_times['直近3位'] = count_third - rank_times_bef100['3位']
        rank_times['直近4位'] = count_fourth - rank_times_bef100['4位']

    analysis.append(rank_times)

# 分析結果をcsvファイルに出力する。
with open('output.csv', 'w', encoding='utf-8') as f:
    # ヘッダー
    f.write('No.,1位,2位,3位,4位,直近1位,直近2位,直近3位,直近4位\n')

    for row in analysis:
        f.write(str(row['No.']))
        f.write(',')
        f.write(str(row['1位']))
        f.write(',')
        f.write(str(row['2位']))
        f.write(',')
        f.write(str(row['3位']))
        f.write(',')
        f.write(str(row['4位']))
        if(row['No.']) > 100:
            f.write(',')
            f.write(str(row['直近1位']))
            f.write(',')
            f.write(str(row['直近2位']))
            f.write(',')
            f.write(str(row['直近3位']))
            f.write(',')
            f.write(str(row['直近4位']))
        f.write('\n')
