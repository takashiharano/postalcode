# Copyright 2022 Takashi Harano
# Released under the MIT license
# Create: 20221020
# Update: 20250119

import os
import sys

ROOT_DIR = '../../'
sys.path.append(os.path.join(os.path.dirname(__file__), ROOT_DIR + 'libs'))
import util

# The data file is available at the following URLs.
DATA_PATH = './postalcode/KEN_ALL.CSV'
JIGYOSYO_DATA_PATH = './postalcode/JIGYOSYO.CSV'

# https://www.post.japanpost.jp/zipcode/dl/kogaki-zip.html
#
#  1. 全国地方公共団体コード（JIS X0401、X0402）………　半角数字
#  2. （旧）郵便番号（5桁）………………………………………　半角数字
#  3. 郵便番号（7桁）………………………………………　半角数字
#  4. 都道府県名　…………　半角カタカナ（コード順に掲載）　（注1）
#  5. 市区町村名　…………　半角カタカナ（コード順に掲載）　（注1）
#  6. 町域名　………………　半角カタカナ（五十音順に掲載）　（注1）
#  7. 都道府県名　…………　漢字（コード順に掲載）　（注1,2）
#  8. 市区町村名　…………　漢字（コード順に掲載）　（注1,2）
#  9. 町域名　………………　漢字（五十音順に掲載）　（注1,2）
# 10. 一町域が二以上の郵便番号で表される場合の表示　（注3）　（「1」は該当、「0」は該当せず）
# 11. 小字毎に番地が起番されている町域の表示　（注4）　（「1」は該当、「0」は該当せず）
# 12. 丁目を有する町域の場合の表示　（「1」は該当、「0」は該当せず）
# 13. 一つの郵便番号で二以上の町域を表す場合の表示　（注5）　（「1」は該当、「0」は該当せず）
# 14. 更新の表示（注6）（「0」は変更なし、「1」は変更あり、「2」廃止（廃止データのみ使用））
# 15. 変更理由　（「0」は変更なし、「1」市政・区政・町政・分区・政令指定都市施行、「2」住居表示の実施、「3」区画整理、「4」郵便区調整等、「5」訂正、「6」廃止（廃止データのみ使用））
# ※1 文字コードには、MS漢字コード（SHIFT JIS）を使用しています。
# ※2 文字セットとして、JIS X0208-1983を使用し、規定されていない文字はひらがなで表記しています。
# ※3 「一町域が二以上の郵便番号で表される場合の表示」とは、町域のみでは郵便番号が特定できず、丁目、番地、小字などにより番号が異なる町域のことです。
# ※4 「小字毎に番地が起番されている町域の表示」とは、郵便番号を設定した町域（大字）が複数の小字を有しており、各小字毎に番地が起番されているため、町域（郵便番号）と番地だけでは住所が特定できない町域のことです。
# ※5 「一つの郵便番号で二以上の町域を表す場合の表示」とは、一つの郵便番号で複数の町域をまとめて表しており、郵便番号と番地だけでは住所が特定できないことを示すものです。
# ※6 「変更あり」とは追加および修正により更新されたデータを示すものです。
# ※7 全角となっている町域名の文字数が38文字を超える場合、また、半角カタカナとなっている町域名のフリガナが76文字を越える場合には、複数レコードに分割しています。
#
# 13111,"144  ","1440041","ﾄｳｷｮｳﾄ","ｵｵﾀｸ","ﾊﾈﾀﾞｸｳｺｳ","東京都","大田区","羽田空港",0,0,1,0,0,0
#----------------------------------------------------------

# https://www.post.japanpost.jp/zipcode/dl/jigyosyo/index-zip.html
#
# 大口事業所個別番号データ
# ※1 大口事業所の所在地のJISコード（5バイト）
# ※2 大口事業所名（カナ）（100バイト）
# ※3 大口事業所名（漢字）（160バイト）
# ※4 都道府県名（漢字）（8バイト）
# ※5 市区町村名（漢字）（24バイト）
# ※6 町域名（漢字）（24バイト）
# ※7 小字名、丁目、番地等（漢字）（124バイト）
# ※8 大口事業所個別番号（7バイト）
# ※9 旧郵便番号（5バイト）
# ※10 取扱局（漢字）（40バイト）
# ※11 個別番号の種別の表示（1バイト）
# 「0」大口事業所
# 「1」私書箱
# ※12 複数番号の有無（1バイト）
# 「0」複数番号無し
# 「1」複数番号を設定している場合の個別番号の1
# 「2」複数番号を設定している場合の個別番号の2
# 「3」複数番号を設定している場合の個別番号の3
# 一つの事業所が同一種別の個別番号を複数持つ場合に複数番号を設定しているものとします。
# 
# 従って、一つの事業所で大口事業所、私書箱の個別番号をそれぞれ一つづつ設定している場合は 12）は「0」となります。
# 
# ※13 修正コード（1バイト）
# 「0」修正なし
# 「1」新規追加
# 「5」廃止
#
# 13113,"ﾆﾎﾝｼｽﾃﾑｳｴｱ ｶﾌﾞｼｷｶﾞｲｼﾔ","日本システムウエア　株式会社","東京都","渋谷区","桜丘町","３１－１１ＮＳＷビル","1508577","150  ","渋谷",0,0,0

#----------------------------------------------------------
def from_code5(code5):
    code5 = normalize_postalcode(code5)

    data_list = util.read_csv(DATA_PATH);

    matched_list = []
    for i in range(len(data_list)):
        record = data_list[i]
        data = csv_to_dict(record)

        if code5 == data['code5']:
            data = convert_result_dict(data)
            matched_list.append(data)

    if len(matched_list) == 0:
        return None
    elif len(matched_list) == 1:
        return matched_list[0]

    return matched_list

#----------------------------------------------------------
def from_code7(code7):
    code7 = normalize_postalcode(code7)

    data_list = util.read_csv(JIGYOSYO_DATA_PATH);
    for i in range(len(data_list)):
        record = data_list[i]
        data = csv_to_dict_jigyosyo(record)
        if code7 == data['code7']:
            data = convert_result_dict(data)
            return data

    data_list = util.read_csv(DATA_PATH);
    matched_list = []
    for i in range(len(data_list)):
        record = data_list[i]
        data = csv_to_dict(record)

        if code7 == data['code7']:
            data = convert_result_dict(data)
            return data
        elif util.match(data['code7'], '^' + code7):
            data = convert_result_dict(data)
            matched_list.append(data)

    if len(matched_list) == 0:
        return None

    return matched_list

#----------------------------------------------------------
def from_addr(addr):
    addr = normalize_address(addr)

    data_list = util.read_csv(JIGYOSYO_DATA_PATH);
    for i in range(len(data_list)):
        record = data_list[i]
        data = csv_to_dict_jigyosyo(record)
        address = data['pref_kanji'] + data['city_kanji'] + data['town_kanji'] + data['street_address']
        address = normalize_address(address)

        if address == addr:
            data = convert_result_dict(data)
            return data

    data_list = util.read_csv(DATA_PATH);

    matched_list = []
    for i in range(len(data_list)):
        record = data_list[i]
        data = csv_to_dict(record)
        address = data['pref_kanji'] + data['city_kanji'] + data['town_kanji']

        if util.match(addr, address):
            data = convert_result_dict(data)
            return data
        elif util.match(address, addr):
            data = convert_result_dict(data)
            matched_list.append(data)

    if len(matched_list) == 0:
        return None

    return matched_list

#----------------------------------------------------------
def csv_to_dict(record):
    data = {
        'lpb_code': record[0],
        'code5': record[1].strip(),
        'code7': record[2],
        'pref_kana': record[3],
        'city_kana': record[4],
        'town_kana': record[5],
        'pref_kanji': record[6],
        'city_kanji': record[7],
        'town_kanji': record[8]
    }
    return data

#----------------------------------------------------------
def csv_to_dict_jigyosyo(record):
    data = {
        'lpb_code': record[0],
        'office_name_kana': record[1],
        'office_name_kanji': record[2],
        'pref_kanji': record[3],
        'city_kanji': record[4],
        'town_kanji': record[5],
        'street_address': record[6],
        'code7': record[7],
        'code5': record[8].strip()
    }
    return data


#----------------------------------------------------------
def convert_result_dict(src_dict):
    data = {
        'lpb_code': src_dict['lpb_code'],
        'code5': src_dict['code5'],
        'code7': src_dict['code7'],
        'pref': src_dict['pref_kanji'],
        'city': src_dict['city_kanji'],
        'town': src_dict['town_kanji']
    }

    if 'street_address' in src_dict:
        data['street_address'] = util.to_half_width(src_dict['street_address'])

    if 'office_name_kanji' in src_dict:
        data['office_name'] = normalize_office_name(src_dict['office_name_kanji'])

    return data

#----------------------------------------------------------
def normalize_postalcode(code):
    code = code.strip()
    code = code.replace('-', '')
    return code

#----------------------------------------------------------
def normalize_address(addr):
    addr = util.to_half_width(addr)
    addr = addr.replace(' ', '')
    addr = addr.replace('番地', '')
    addr = addr.replace('丁目', '-')
    addr = addr.replace('番', '-')
    addr = addr.replace('号', '')
    addr = util.replace(addr, '-$', '')
    return addr

#----------------------------------------------------------
def normalize_office_name(name):
    name = util.to_half_width(name)
    name = name.replace(' 株式会社', '株式会社')
    return name

#----------------------------------------------------------
def webmain():
    code5 = util.get_request_param('code5', '');
    code7 = util.get_request_param('code7', '');
    addr = util.get_request_param('addr', '');

    data = main(code5, code7, addr)

    util.send_response(data, 'application/json');

#----------------------------------------------------------
def main(code7, addr='', code5=''):
    if code7 != '':
        data = from_code7(code7)
    elif addr != '':
        data = from_addr(addr)
    elif code5 != '':
        data = from_code5(code5)
    else:
        data = None

    return data
