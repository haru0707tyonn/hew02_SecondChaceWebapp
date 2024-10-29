from flask import Flask, render_template, request, url_for, redirect, flash, session
from random import sample
import os
import mysql.connector
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def conn_db():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="P@ssw0rd",
        db="secondchance"
    )
    return conn

# ログインページ
@app.route("/", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']
        
        conn = conn_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user WHERE Email = %s AND Password = %s', (Email, Password))

        user = cursor.fetchone()

        if user:
            session['flag'] = True
            session['Email'] = Email
            session['user_id'] = user[0]  # ここでユーザーIDをセッションに追加
            print("ログイン成功")
            print("現在ログイン中のユーザー" ,user)
            # flash('ログイン成功！', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for("top"))
        else:
            flash('メールアドレスまたはパスワードが異なります', 'error')
            print("ログイン失敗")
        cursor.close()
        conn.close()
        
    return render_template('index.html')


# ユーザーIDを取得する例
def get_current_user_id():
    return session.get('user_id')

# ログアウト
# @app.route('/logout')
# def logout():
#     # セッションからユーザーIDを削除
#     session.pop('user_id', None)
#     return redirect(url_for("index"))

# アカウント作成ページ
@app.route("/create/", methods=['GET', 'POST'])
def create():
    
    if request.method == "POST":
       
        Real_Name = request.form["Real_Name"]
        User_Name = request.form["User_Name"]
        Email = request.form["Email"]
        Password = request.form["Password"]
        BrithDate = request.form["BrithDate"]
        Post_Code = request.form["Post_Code"]
        Address = request.form["Address"]
        Tel = request.form["Tel"]
        
        conn = conn_db()
        cursor = conn.cursor()
        

        try:
            # Goods_ID カラムに値 1 を含めた SQL ステートメントの変更
            sql = "INSERT INTO user (Real_Name, User_Name, Email, Password, BrithDate, Post_Code, Address, Tel, Rank_ID, Total__Amount, Picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (Real_Name, User_Name, Email, Password, BrithDate, Post_Code, Address, Tel, 1, 0, 'Default.jpg'))

            conn.commit()
            print("会員登録できた")
            print("会員登録情報", Real_Name, User_Name, Email, Password, BrithDate, Post_Code, Address, Tel)
            return redirect(url_for("hello"))

        except mysql.connector.IntegrityError as e:
            print(e)
        
        finally:
            cursor.close()
            conn.close()

    return render_template("create.html")


# アカウント作成完了
@app.route("/hello/")
def hello():

    return render_template("hello.html")

# トップページ
@app.route("/top/", methods=['GET'])
def top():
        if 'flag' in session and session['flag']:
            conn = conn_db()
            cursor = conn.cursor()
            
            #　新着商品
            sql = "SELECT Goods_Name, Price, Picture, Goods_ID FROM Goods WHERE Sold_out IS NULL AND Request_Goods IS NULL;"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            
            # おすすめ
            sql = "SELECT Goods_Name, Price, Picture, Goods_ID FROM Goods WHERE Sold_out IS NULL AND Request_Goods IS NULL;"
            cursor.execute(sql)
            result_1 = cursor.fetchall()
            random_records = sample(result_1, min(6, len(result_1)))

            # 人気の商品
            sql = "SELECT Goods_Name, Price, Picture, Goods_ID FROM Goods WHERE Sold_out IS NULL AND Request_Goods IS NULL;"
            cursor.execute(sql)
            result_2 = cursor.fetchall()
            random_records_1 = sample(result_2, min(6, len(result_2)))
            
            # リクエスト
            sql = "SELECT Goods_Name, Price, Picture, Goods_ID FROM Goods WHERE Sold_out IS NULL AND Request_Goods = 1;"
            cursor.execute(sql)
            result_3 = cursor.fetchall()

            return render_template('top.html', email=session['Email'], records=result, random_records=random_records, random_records_1=random_records_1, result_3=result_3)
        else:
            return redirect(url_for("index"))



#　検索結果
@app.route("/kennsaku/", methods=['POST'])
def search_results():
    
    try:
        search_query = request.form.get('search_query')
        # フォームから送信されたカテゴリの値を取得
        selected_category = request.args.get('category')
        
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)

        # ここで適切なクエリを実行してデータを取得します
        query = "SELECT Goods_Name, Price, Picture, Goods_ID FROM goods WHERE Goods_Name = %s"
        cursor.execute(query, (search_query,))
        search_results = cursor.fetchall()
        
        query = "SELECT Goods_Name, Price, Picture, Goods_ID FROM goods WHERE Genre_ID = %s"
        cursor.execute(query, (selected_category,))
        search_results_1 = cursor.fetchall()
        
        query = "SELECT Genre_Name FROM Genre WHERE Genre_ID = %s"
        cursor.execute(query, (selected_category,))
        search_results_2 = cursor.fetchall()

        return render_template('kennsaku.html', search_query=search_query, search_results=search_results, selected_category=selected_category,search_results_1=search_results_1, )

    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


    
#　検索結果(ジャンル)
@app.route("/kennsaku_1/", methods=['POST',"GET"])
def kennsaku_1():
    
    try:

        # フォームから送信されたカテゴリの値を取得
        selected_category = request.args.get('category')
        
        conn = conn_db()
        cursor = conn.cursor(dictionary=True)

        # ここで適切なクエリを実行してデータを取得します
        query = "SELECT Goods_Name, Price, Picture, Goods_ID FROM goods WHERE Genre_ID = %s"
        cursor.execute(query, (selected_category,))
        search_results_1 = cursor.fetchall()
        print(search_results_1)
        
        query = "SELECT Genre_Name FROM Genre WHERE Genre_ID = %s"
        cursor.execute(query, (selected_category,))
        search_results_2= cursor.fetchall()
        search_results_3 = [result['Genre_Name'] for result in search_results_2]
        

        return render_template('kennsaku_1.html', selected_category=selected_category,search_results_1=search_results_1, search_results_2=search_results_2, search_results_3=search_results_3)

    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()



# 商品詳細
@app.route("/syousai/<int:Goods_ID>/", methods=['GET', 'POST'])
def syousai(Goods_ID):
    try:
        # カテゴリの一覧を取得
        Genre = get_categories()
        
        #ユーザー情報の取得
        current_user_id = get_current_user_id()


        # データベース接続
        conn = conn_db()
        cursor = conn.cursor()

        # 商品情報を取得
        sql = "SELECT Goods_Name, Price, Picture, Genre_ID, Cond_Goods, Shipping_Method, Shipping_Days, Appraiser, Explanation, User_ID FROM Goods WHERE Goods_ID = %s"
        cursor.execute(sql, (Goods_ID,))
        record = cursor.fetchone()
        sql_1 = "SELECT Genre_Name FROM Genre WHERE Genre_ID = %s"
        cursor.execute(sql_1, (record[3],))
        record_1 = cursor.fetchone()
        sql_2 = "SELECT User_Name, Picture FROM User WHERE User_ID = %s"
        cursor.execute(sql_2, (record[9],))
        record_2 = cursor.fetchone()
        print("record_2の値:", record_2)

        
        # コメント一覧を取得(昇順で)
        cursor.execute("SELECT Content, Comment_Date, User_Name, Picture  FROM Comment JOIN User ON Comment.User_ID = User.User_ID WHERE Goods_ID = %s ORDER BY Comment_Date ASC;", (Goods_ID,))
        comment = cursor.fetchall()

        # POSTリクエストの場合はコメントを保存
        if request.method == 'POST':
            comment_text = request.form['content']
            user_id = session.get('user_id')
            cursor.execute("INSERT INTO Comment (Goods_ID, User_ID, Content, Comment_Date) VALUES (%s, %s, %s, CURRENT_TIMESTAMP);", (Goods_ID, user_id, comment_text))
            conn.commit()
            # コメントを保存した後、再度コメント一覧を取得(昇順で表示する)
            cursor.execute("SELECT Content, Comment_Date, User_Name, Picture FROM Comment JOIN User ON Comment.User_ID = User.User_ID WHERE Goods_ID = %s ORDER BY Comment_Date ASC;", (Goods_ID,))
            comment = cursor.fetchall()
            # sql_3 = "SELECT User_Name FROM User WHERE User_ID = %s"
            # cursor.execute(sql_3, (comments[2],))
            # record_3 = cursor.fetchone()

        # セッションにGoods_IDを保存
        session['Goods_ID'] = Goods_ID
        
        # おすすめの表示
        sql = "SELECT Picture, Goods_ID FROM Goods;"
        cursor.execute(sql)
        result = cursor.fetchall()

        # ランダムに6つの商品を選択
        if len(result) >= 6:
            random_records = sample(result, 6)
        else:
            # リストの要素数が6未満の場合は全ての要素を使うか、適切な処理を行う
            random_records = result


        # 商品情報をテンプレートに渡して render_template を呼び出す
        return render_template("syousai.html", record=record, Genre=Genre, record_1=record_1, record_2=record_2, comment=comment, random_records=random_records)
    
    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}
    
    finally:
        # 接続をクローズする
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

            
# リクエスト商品詳細
@app.route("/request_syousai/<int:Goods_ID>/", methods=['GET', 'POST'])
def request_syousai(Goods_ID):
    try:
        # カテゴリの一覧を取得
        Genre = get_categories()
        
        #ユーザー情報の取得
        current_user_id = get_current_user_id()

        # データベース接続
        conn = conn_db()
        cursor = conn.cursor()

        # 商品情報を取得
        sql = "SELECT Goods_Name, Price, Picture, Genre_ID, Cond_Goods, Shipping_Method, Shipping_Days, Appraiser, Explanation, User_ID FROM Goods WHERE Goods_ID = %s"
        cursor.execute(sql, (Goods_ID,))
        record = cursor.fetchone()
        sql_1 = "SELECT Genre_Name FROM Genre WHERE Genre_ID = %s"
        cursor.execute(sql_1, (record[3],))
        record_1 = cursor.fetchone()
        sql_2 = "SELECT User_Name, Picture FROM User WHERE User_ID = %s"
        cursor.execute(sql_2, (record[9],))
        record_2 = cursor.fetchone()
        print("record_2の値:", record_2)

        
        # コメント一覧を取得(昇順で)
        cursor.execute("SELECT Content, Comment_Date, User_Name  FROM Comment JOIN User ON Comment.User_ID = User.User_ID WHERE Goods_ID = %s ORDER BY Comment_Date ASC;", (Goods_ID,))
        comment = cursor.fetchall()

        # POSTリクエストの場合はコメントを保存
        if request.method == 'POST':
            comment_text = request.form['content']
            user_id = session.get('user_id')
            cursor.execute("INSERT INTO Comment (Goods_ID, User_ID, Content, Comment_Date) VALUES (%s, %s, %s, CURRENT_TIMESTAMP);", (Goods_ID, user_id, comment_text))
            conn.commit()
            # コメントを保存した後、再度コメント一覧を取得(昇順で表示する)
            cursor.execute("SELECT Content, Comment_Date, User_Name, Picture FROM Comment JOIN User ON Comment.User_ID = User.User_ID WHERE Goods_ID = %s ORDER BY Comment_Date ASC;", (Goods_ID,))
            comment = cursor.fetchall()
            # sql_3 = "SELECT User_Name FROM User WHERE User_ID = %s"
            # cursor.execute(sql_3, (comments[2],))
            # record_3 = cursor.fetchone()

        # セッションにGoods_IDを保存
        session['Goods_ID'] = Goods_ID
        
        # おすすめの表示
        sql = "SELECT Picture, Goods_ID FROM Goods;"
        cursor.execute(sql)
        result = cursor.fetchall()

        # ランダムに6つの商品を選択
        if len(result) >= 6:
            random_records = sample(result, 6)
        else:
            # リストの要素数が6未満の場合は全ての要素を使うか、適切な処理を行う
            random_records = result


        # 商品情報をテンプレートに渡して render_template を呼び出す
        return render_template("request_syousai.html", record=record, Genre=Genre, record_1=record_1, record_2=record_2, comment=comment, random_records=random_records)
    
    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}
    
    finally:
        # 接続をクローズする
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


# カテゴリの一覧を取得する関数
def get_categories():
    conn = conn_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Genre")
    Genres = cursor.fetchall()
    cursor.close()
    conn.close()
    return Genres

#　出品ページ
@app.route("/syuppin/", methods=['GET', 'POST'])
def syuppin():
    
    new_filename = None  # 初期化
    current_user_id = get_current_user_id()

    if 'flag' in session and session['flag']:
        if request.method == 'POST':
            # POST リクエストからフォームデータを取得
            Cond_Goods = request.form['Cond_Goods']
            Genre_ID = request.form['Genre_ID']
            Shipping_Method = request.form['Shipping_Method']
            Shipping_Days = request.form['Shipping_Days']
            Appraiser = request.form['Appraiser']
            Goods_Name = request.form['Goods_Name']
            Price = request.form['Price']
            Explanation = request.form['Explanation']
            

            # 複数の画像ファイルを処理
            pictures = request.files.getlist("Pictures[]")
            picture_filenames = []

            for i, picture in enumerate(pictures):
                new_filename = str(uuid.uuid4()) + "_" + picture.filename
                picture_path = os.path.join("./static/img", new_filename)
                picture.save(picture_path)
                picture_filenames.append(new_filename)

                print(f"Saved picture {i + 1} to {picture_path}")


            # データベースに出品情報を保存
            conn = conn_db()
            cursor = conn.cursor()
          
            try:
                sql = """
                    INSERT INTO goods (
                        User_ID, Cond_Goods, Genre_ID, Shipping_Method, Shipping_Days, Appraiser, Goods_Name, Price, Explanation, Picture
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    current_user_id, Cond_Goods, Genre_ID, Shipping_Method, Shipping_Days, Appraiser, Goods_Name, Price, Explanation, ','.join(picture_filenames)
                ))
                
                conn.commit()
                flash('出品が完了しました！', 'success')
                print("出品できた")
                print("出品情報",current_user_id, Cond_Goods, Genre_ID, Shipping_Method, Shipping_Days, Appraiser, Goods_Name, Price, Explanation, new_filename)

                return redirect(url_for("syuppinok"))
            except mysql.connector.Error as e:
                print(e)
                flash('出品に失敗しました。', 'error')
            finally:
                cursor.close()
                conn.close()

        # カテゴリの一覧を取得
        Genre = get_categories()

        return render_template('syuppin.html', Genre=Genre, filename=new_filename)
    else:
        return redirect(url_for("syuppinok"))


# 出品完了
@app.route("/syuppinok/")
def syuppinok():

    return render_template("syuppinok.html")

# リクエスト出品
@app.route("/request_syuppin/", methods=['GET', 'POST'])
def request_syuppin():
    new_filename = None  # 初期化
    current_user_id = get_current_user_id()

    if 'flag' in session and session['flag']:
        if request.method == 'POST':
            # POST リクエストからフォームデータを取得
            Cond_Goods = request.form['Cond_Goods']
            Genre_ID = request.form['Genre_ID']
            Shipping_Method = request.form['Shipping_Method']
            Shipping_Days = request.form['Shipping_Days']
            Appraiser = request.form['Appraiser']
            Goods_Name = request.form['Goods_Name']
            Price = request.form['Price']
            Explanation = request.form['Explanation']
            

            # 複数の画像ファイルを処理
            pictures = request.files.getlist("Pictures[]")
            picture_filenames = []

            for i, picture in enumerate(pictures):
                new_filename = str(uuid.uuid4()) + "_" + picture.filename
                picture_path = os.path.join("./static/img", new_filename)
                picture.save(picture_path)
                picture_filenames.append(new_filename)

                print(f"Saved picture {i + 1} to {picture_path}")


            # データベースにリクエスト情報を保存
            conn = conn_db()
            cursor = conn.cursor()
          
            try:
                sql = """
                    INSERT INTO goods (
                        User_ID, Cond_Goods, Genre_ID, Shipping_Method, Shipping_Days, Appraiser, Goods_Name, Price, Explanation, Picture, Request_Goods
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    current_user_id, Cond_Goods, Genre_ID, Shipping_Method, Shipping_Days, Appraiser, Goods_Name, Price, Explanation, ','.join(picture_filenames),1
                ))
                
                conn.commit()
                
                print("リクエストできた")
                print("リクエスト情報",current_user_id, Cond_Goods, Genre_ID, Shipping_Method, Shipping_Days, Appraiser, Goods_Name, Price, Explanation, new_filename)

                return redirect(url_for("requestok"))
            except mysql.connector.Error as e:
                print(e)
            finally:
                cursor.close()
                conn.close()

        # カテゴリの一覧を取得
        Genre = get_categories()

        return render_template('request_form.html', Genre=Genre, filename=new_filename)
    else:
        return redirect(url_for("requestok"))

# リクエスト完了
@app.route("/requestok/")
def requestok():

    return render_template("requestok.html")


# ユーザーIDを取得する例
def get_current_Goods_ID():
    return session.get('Goods_ID')

# ユーザーIDを取得する例
def get_current_Price():
    return session.get('Price')




# # 決済(1ページ目)
# @app.route('/kessai1/',  methods=['GET', 'POST'])
# def kessai1():
    
    
#     try:
        
#         if request.method == "POST":
            
#             current_user_id = get_current_user_id()
#             current_Goods_ID = get_current_Goods_ID()
#             print(current_Goods_ID)
    
#             Real_Name = request.form["Real_Name"]
#             Post_Code = request.form["Post_Code"]
#             Address = request.form["Address"]
#             Tel = request.form["Tel"]
#             Email = request.form["Email"]
#             Payment = request.form["Payment"]

#             conn = conn_db()
#             cursor = conn.cursor()
            

#             try:
                
#                 # 注文をデータベースに挿入
#                 sql = "INSERT INTO `order` (Goods_ID ,User_ID, Real_Name, Email, Post_Code, Address, Tel, Payment) VALUES (%s ,%s ,%s, %s, %s, %s, %s, %s)"
#                 cursor.execute(sql, (current_Goods_ID,current_user_id,Real_Name, Email, Post_Code, Address, Tel, Payment))
#                 conn.commit()
                
#                 # 購入した商品の値段を取得
#                 cursor.execute('SELECT Price FROM Goods WHERE Goods_ID = %s;', (current_Goods_ID,))
#                 price = cursor.fetchone()[0]
                
#                 # 購入した商品の値段をユーザーのTotal__Amountに加算
#                 cursor.execute('UPDATE user SET Total__Amount = Total__Amount + %s WHERE user_id = %s;', (price, current_user_id))
#                 conn.commit()
                
#                 # 商品を非表示に
#                 # 数字の 1 を挿入する
#                 cursor.execute('UPDATE Goods SET Sold_out = 1 WHERE Goods_ID = %s;', (current_Goods_ID,))
#                 conn.commit()
#                 print("決済できた")
#                 print("決済情報", current_Goods_ID, current_user_id, Real_Name, Email, Post_Code, Address, Tel, Payment)
#                 return redirect(url_for("kessai3"))

#             except mysql.connector.IntegrityError as e:
#                 print(e)
            
#             finally:
#                 cursor.close()
#                 conn.close()
            
#         # セッションからユーザーIDを取得
#         user_id = session.get('user_id')

#         # データベースからユーザー情報を取得する関数を呼び出す
#         conn = conn_db()
#         cursor = conn.cursor()

#         # データベース
#         cursor.execute('SELECT Real_Name, Post_Code, Address, Tel, Email FROM user WHERE user_id = %s;', (user_id,))
#         record = cursor.fetchone()
#         # ユーザー情報を取得できた場合
#         if record:
#             return render_template('kessai1.html', record=record)
  
#     except mysql.connector.Error as err:
#         # エラーが発生した場合の処理
#         print(f"Error: {err}")
#         return {'error': str(err)}
 
#     finally:
#         # 接続をクローズする
#         if 'conn' in locals() and conn.is_connected():
#             cursor.close()
#             conn.close()
            
            
# # 決済(2ページ目)
# @app.route("/kessai2/")
# def kessai2():
 

#     return render_template("kessai2.html")


# 決済(1ページ目)
@app.route('/kessai1/', methods=['GET', 'POST'])
def kessai1():
    conn = None
    cursor = None
    
    try:
        if request.method == "POST":
            current_user_id = get_current_user_id()
            current_Goods_ID = get_current_Goods_ID()

    
            Real_Name = request.form["Real_Name"]
            Post_Code = request.form["Post_Code"]
            Address = request.form["Address"]
            Tel = request.form["Tel"]
            Email = request.form["Email"]
            Payment = request.form["Payment"]

            try:
                conn = conn_db()
                cursor = conn.cursor()

                # 決済情報をセッションに保存
                session['kessai_info'] = {
                    'current_Goods_ID': current_Goods_ID,
                    'current_user_id': current_user_id,
                    'Real_Name': Real_Name,
                    'Email': Email,
                    'Post_Code': Post_Code,
                    'Address': Address,
                    'Tel': Tel,
                    'Payment': Payment
                }

                return redirect(url_for("kessai2"))

            except mysql.connector.IntegrityError as e:
                print(e)
            
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

        user_id = session.get('user_id')

        conn = conn_db()
        cursor = conn.cursor()

        cursor.execute('SELECT Real_Name, Post_Code, Address, Tel, Email FROM user WHERE user_id = %s;', (user_id,))
        record = cursor.fetchone()

        if record:
            return render_template('kessai1.html', record=record)
  
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {'error': str(err)}
 
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
          

# 決済(2ページ目)
@app.route("/kessai2/", methods=['GET', 'POST'])
def kessai2():
    kessai_info = session.get('kessai_info')
    price = 0  # 商品の値段の初期化
    result = None  # result変数の初期化

    # データベースにリクエスト情報を保存
    conn = conn_db()
    cursor = conn.cursor()
    goods_id = session.get('goods_id')
    
    current_user_id = get_current_user_id()
    current_Goods_ID = get_current_Goods_ID()
    print(current_Goods_ID)
    
    # 購入した商品の値段を取得
    cursor.execute('SELECT Price, Goods_Name, Picture FROM Goods WHERE Goods_ID = %s;', (current_Goods_ID,))
    result = cursor.fetchone()
    print("kessai2_table にデータを保存しました")
    if result:
        price = result[0]

    if not kessai_info:
        return redirect(url_for("kessai1"))

    if request.method == 'POST':
        try:
            print(current_Goods_ID)
            # データベースに保存 (kessai2_table に保存)
            sql_kessai2 = "INSERT INTO `order` (Goods_ID, User_ID, Real_Name, Email, Post_Code, Address, Tel, Payment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_kessai2, (
                current_Goods_ID,
                current_user_id,
                kessai_info['Real_Name'],
                kessai_info['Email'],
                kessai_info['Post_Code'],
                kessai_info['Address'],
                kessai_info['Tel'],
                kessai_info['Payment']
            ))

            # 購入した商品の値段をユーザーのTotal__Amountに加算
            cursor.execute('UPDATE user SET Total__Amount = Total__Amount + %s WHERE user_id = %s;', (price, current_user_id,))
            conn.commit()

            # 商品を非表示に
            cursor.execute('UPDATE Goods SET Sold_out = 1 WHERE Goods_ID = %s;', (current_Goods_ID,))
            conn.commit()
            print("商品を非表示にしました")

        except mysql.connector.Error as e:
            print("データベースエラー:", e)

        finally:
            # セッションに price を保存
            session['price'] = price
            session.pop('kessai_info', None)
            return redirect(url_for("kessai3"))

    return render_template("kessai2.html", kessai_info=kessai_info, price=price, result=result)

# 決済(3ページ目)
@app.route("/kessai3/")
def kessai3():
    try:
        
        current_Goods_ID = get_current_Goods_ID()

        
        # データベース接続
        conn = conn_db()
        cursor = conn.cursor()

        # 商品情報を取得
        cursor.execute('SELECT Price FROM goods WHERE Goods_ID = %s;', (current_Goods_ID,))
        record = cursor.fetchone()



        # 商品情報をテンプレートに渡して render_template を呼び出す
        return render_template("kessai3.html", record=record)
    
    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}
    
    finally:
        # 接続をクローズする
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def get_user_rank(total_amount):
    gauge_ranges = [
        { 'max': 10000, 'color': '#3498db', 'image': 'rank1.png', 'name': 'ブロンズ' },
        { 'max': 30000, 'color': '#2ecc71', 'image': 'rank2.png', 'name': 'シルバー' },
        { 'max': 50000, 'color': '#f39c12', 'image': 'rank3.png', 'name': 'ゴールド' },
        { 'max': 100000, 'color': '#e74c3c', 'image': 'rank4.png', 'name': 'プラチナ' },
    ]

    for i, rank in enumerate(gauge_ranges):
        if total_amount <= rank['max']:
            return i



# リクエスト決済(1ページ目)
@app.route('/request_kessai1/', methods=['GET', 'POST'])
def request_kessai1():
    conn = None
    cursor = None
    
    try:
        if request.method == "POST":
            current_user_id = get_current_user_id()
            current_Goods_ID = get_current_Goods_ID()

    
            Real_Name = request.form["Real_Name"]
            Post_Code = request.form["Post_Code"]
            Address = request.form["Address"]
            Tel = request.form["Tel"]
            Email = request.form["Email"]

            try:
                conn = conn_db()
                cursor = conn.cursor()

                # 決済情報をセッションに保存
                session['kessai_info'] = {
                    'current_Goods_ID': current_Goods_ID,
                    'current_user_id': current_user_id,
                    'Real_Name': Real_Name,
                    'Email': Email,
                    'Post_Code': Post_Code,
                    'Address': Address,
                    'Tel': Tel,
                }

                return redirect(url_for("request_kessai2"))

            except mysql.connector.IntegrityError as e:
                print(e)
            
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

        user_id = session.get('user_id')

        conn = conn_db()
        cursor = conn.cursor()

        cursor.execute('SELECT Real_Name, Post_Code, Address, Tel, Email FROM user WHERE user_id = %s;', (user_id,))
        record = cursor.fetchone()

        if record:
            return render_template('request_kessai1.html', record=record)
  
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {'error': str(err)}
 
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
          

# リクエスト決済(2ページ目)
@app.route("/request_kessai2/", methods=['GET', 'POST'])
def request_kessai2():
    kessai_info = session.get('kessai_info')
    price = 0  # 商品の値段の初期化
    result = None  # result変数の初期化

    # データベースにリクエスト情報を保存
    conn = conn_db()
    cursor = conn.cursor()
    goods_id = session.get('goods_id')
    
    current_user_id = get_current_user_id()
    current_Goods_ID = get_current_Goods_ID()
    print(current_Goods_ID)
    
    # 購入した商品の値段を取得
    cursor.execute('SELECT Price, Goods_Name, Picture FROM Goods WHERE Goods_ID = %s;', (current_Goods_ID,))
    result = cursor.fetchone()
    print("kessai2_table にデータを保存しました")
    if result:
        price = result[0]

    if not kessai_info:
        return redirect(url_for("request_kessai1"))

    if request.method == 'POST':
        try:
            print(current_Goods_ID)
            # データベースに保存 (kessai2_table に保存)
            sql_kessai2 = "INSERT INTO `order` (Goods_ID, User_ID, Real_Name, Email, Post_Code, Address, Tel) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_kessai2, (
                current_Goods_ID,
                current_user_id,
                kessai_info['Real_Name'],
                kessai_info['Email'],
                kessai_info['Post_Code'],
                kessai_info['Address'],
                kessai_info['Tel'],
            ))

            # 購入した商品の値段をユーザーのTotal__Amountに加算
            cursor.execute('UPDATE user SET Total__Amount = Total__Amount + %s WHERE user_id = %s;', (price, current_user_id,))
            conn.commit()

            # 商品を非表示に
            cursor.execute('UPDATE Goods SET Sold_out = 1 WHERE Goods_ID = %s;', (current_Goods_ID,))
            conn.commit()
            print("商品を非表示にしました")

        except mysql.connector.Error as e:
            print("データベースエラー:", e)

        finally:
            # セッションに price を保存
            session['price'] = price
            session.pop('kessai_info', None)
            return redirect(url_for("request_kessai3"))

    return render_template("request_kessai2.html", kessai_info=kessai_info, price=price, result=result)


# リクエスト決済(3ページ目)
@app.route("/request_kessai3/")
def request_kessai3():
    try:
        
        current_Goods_ID = get_current_Goods_ID()

        
        # データベース接続
        conn = conn_db()
        cursor = conn.cursor()

        # 商品情報を取得
        cursor.execute('SELECT Price FROM goods WHERE Goods_ID = %s;', (current_Goods_ID,))
        record = cursor.fetchone()



        # 商品情報をテンプレートに渡して render_template を呼び出す
        return render_template("request_kessai3.html", record=record)
    
    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}
    
    finally:
        # 接続をクローズする
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()



# マイページ 
@app.route("/mypage/", methods=["GET", "POST"])
def mypage():
    try:
        # セッションからユーザーIDを取得
        user_id = session.get('user_id')

        if request.method == "POST":

            # データベースからユーザー情報を取得
            conn = conn_db()
            cursor = conn.cursor()


            # フォーム1: Real_NameおよびBrithDateの更新
            if "Real_Name" in request.form and "BrithDate" in request.form:
                Real_Name = request.form["Real_Name"]
                BrithDate = request.form["BrithDate"]
                sql = "UPDATE user SET Real_Name=%s, BrithDate=%s WHERE user_id=%s"
                cursor.execute(sql, (Real_Name, BrithDate, user_id))
                conn.commit()

            # フォーム2: AddressおよびPost_Codeの更新
            if "Address" in request.form and "Post_Code" in request.form:
                Address = request.form["Address"]
                Post_Code = request.form["Post_Code"]
                sql_1 = "UPDATE user SET Address=%s, Post_Code=%s WHERE user_id=%s"
                cursor.execute(sql_1, (Address, Post_Code, user_id))
                conn.commit()
                
            # フォーム3: Telの更新
            if "Tel" in request.form:
                Tel = request.form["Tel"]
                sql_2 = "UPDATE user SET Tel=%s WHERE user_id=%s"
                cursor.execute(sql_2, (Tel, user_id))
                conn.commit()
                
            # フォーム4: PictureおよびUser_Nameの更新
            if "User_Name" in request.form and "Picture" in request.files:
                Picture = request.files["Picture"]
                User_Name = request.form["User_Name"]

                # UUIDを使用してファイル名を生成
                filename = str(uuid.uuid4()) + "_" + Picture.filename

                # 画像を 'static/img' フォルダに保存
                img_path = os.path.join("./static/img", filename)
                Picture.save(img_path)

                # データベースを新しい情報で更新
                sql_3 = "UPDATE user SET Picture=%s, User_Name=%s WHERE user_id=%s"
                cursor.execute(sql_3, (filename, User_Name, user_id))
                conn.commit()             

            cursor.close()

        # データベースからユーザー情報を再度取得
        conn = conn_db()
        cursor = conn.cursor()
        
        # デバッグ用に record を表示
        cursor.execute('SELECT User_Name, Real_Name, BrithDate, Post_Code, Address, Tel, Total__Amount, Picture FROM user WHERE user_id = %s;', (user_id,))
        record = cursor.fetchone()
        cursor.execute('SELECT COUNT(Goods_ID) FROM goods WHERE user_id = %s AND Sold_out IS NULL;', (user_id,))
        record_1 = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(Goods_ID) FROM goods WHERE user_id = %s AND Sold_out = 1;', (user_id,))
        record_2 = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(order_id) FROM `order` WHERE user_id = %s;', (user_id,))
        record_3 = cursor.fetchone()[0]

        # ユーザー情報を取得できた場合
        if record:
            # ユーザーの合計金額を取得
            total_amount = record[6]
            print(record)
            # ユーザーランクを計算
            user_rank = get_user_rank(total_amount)
            
            # ランクの情報を定義
            gauge_ranges = [
                { 'max': 10000, 'color': '#3498db', 'image': 'rank1.png', 'name': 'ブロンズ' },
                { 'max': 30000, 'color': '#2ecc71', 'image': 'rank2.png', 'name': 'シルバー' },
                { 'max': 50000, 'color': '#f39c12', 'image': 'rank3.png', 'name': 'ゴールド' },
                { 'max': 100000000, 'color': '#e74c3c', 'image': 'rank4.png', 'name': 'プラチナ' },
            ]

            # 次のランクまでの残り購入金額を計算
            remaining_to_next_rank = gauge_ranges[user_rank + 1]['max'] - total_amount if user_rank is not None and user_rank < len(gauge_ranges) - 1 else 0


        return render_template('mypage.html', record=record, record_1=record_1, record_2=record_2, record_3=record_3,user_rank=user_rank, remaining_to_next_rank=remaining_to_next_rank, gauge_ranges=gauge_ranges)


    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {'error': str(err)}
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

#　出品中・リクエスト中ページ
@app.route("/syuppintyuu/")
def syuppintyuu():
    try:
        
        # セッションからユーザーIDを取得
        user_id = session.get('user_id')

        conn = conn_db()
        cursor = conn.cursor(dictionary=True)

        # ここで適切なクエリを実行してデータを取得します
        cursor.execute('SELECT Goods_Name, Price, Picture FROM goods WHERE user_id = %s AND Sold_out IS NULL;', (user_id,))
        result = cursor.fetchall()
        
        return render_template('syuppintyuu.html', result=result )

    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


#　取引完了ページ
@app.route("/torihikikan/")
def torihikikan():
    try:
        
        # セッションからユーザーIDを取得
        user_id = session.get('user_id')

        conn = conn_db()
        cursor = conn.cursor(dictionary=True)

        # ここで適切なクエリを実行してデータを取得します
        cursor.execute('SELECT Goods_Name, Price, Picture FROM goods WHERE user_id = %s AND Sold_out=1;', (user_id,))
        result = cursor.fetchall()
        
        return render_template('torihikikan.html', result=result )

    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    

#　購入履歴
@app.route("/rireki/")
def rireki():
    try:
        
        # セッションからユーザーIDを取得
        user_id = session.get('user_id')

        conn = conn_db()
        cursor = conn.cursor(dictionary=True)

        # ここで適切なクエリを実行してデータを取得します
        cursor.execute('SELECT Goods_Name, Price, Picture FROM `order` JOIN Goods ON `order`.User_ID = Goods.User_ID WHERE `order`.user_id = %s;', (user_id,))


        result = cursor.fetchall()
                
        return render_template('rireki.html', result=result )

    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error: {err}")
        return {'error': str(err)}

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
   




# # マイページ
# @app.route("/mypage/")
# def mypage():
    
#     try:
#         # セッションからユーザーIDを取得
#         user_id = session.get('user_id')
 
#         # データベースからユーザー情報を取得する関数を呼び出す
#         conn = conn_db()
#         cursor = conn.cursor()
 
#         # ユーザー情報を表示
#         cursor.execute('SELECT User_Name, Real_Name, BrithDate, Post_Code, Address, Tel, Total_Amount FROM user WHERE user_id = %s;', (user_id,))
#         record = cursor.fetchone()
#         cursor.execute('SELECT COUNT(Goods_ID) FROM goods WHERE user_id = %s;', (user_id,))
#         record_1 = cursor.fetchone()[0]
#         cursor.execute('SELECT COUNT(order_id) FROM `order` WHERE user_id = %s;', (user_id,))
#         record_2 = cursor.fetchone()[0]
#         # ユーザー情報を取得できた場合
#         if record:
#             return render_template('mypage.html', record=record, record_1=record_1, record_2=record_2)
        
    
#     except mysql.connector.Error as err:
#         # エラーが発生した場合の処理
#         print(f"Error: {err}")
#         return {'error': str(err)}
 
#     finally:
#         # 接続をクローズする
#         if 'conn' in locals() and conn.is_connected():
#             cursor.close()
#             conn.close()
            
#     try:
#         # 複数の画像ファイルを処理
#         pictures = request.files.getlist("Pictures[]")
#         picture_filenames = []

#         for i, picture in enumerate(pictures):
#             new_filename = str(uuid.uuid4()) + "_" + picture.filename
#             picture_path = os.path.join("./static/img", new_filename)
#             picture.save(picture_path)
#             picture_filenames.append(new_filename)

#             print(f"Saved picture {i + 1} to {picture_path}")

#         # データベースに出品情報を保存
#         conn = conn_db()
#         cursor = conn.cursor()

#         try:
#             sql = """
#                 INSERT INTO goods (
#                     Picture
#                 ) VALUES (%s,)
#             """
#             cursor.execute(sql, (
#                 ','.join(picture_filenames)
#             ))

#             conn.commit()
#             flash('出品が完了しました！', 'success')
#             print("出品できた")
#             print("出品情報", new_filename)

#             return render_template('mypage.html', filename=new_filename)
#         except mysql.connector.Error as e:
#             print(e)
#             flash('出品に失敗しました。', 'error')
#         finally:
#             cursor.close()
#             conn.close()

#         return redirect(url_for("mypage"))
    
#     except Exception as e:
#         print(f"Error: {e}")
#         flash('画像の処理中にエラーが発生しました。', 'error')
#         return redirect(url_for("mypage"))

    


# ログアウトのルート
@app.route("/logout/")
def logout():
    # セッションデータをクリア
    session.pop('flag', None)
    session.pop('Email', None)
    session.pop('user_id', None)

    # 'index' エンドポイントにリダイレクト
    return redirect(url_for("login"))

# 退会ページ
@app.route("/quit/", methods=['GET', 'POST'])
def quit():
    if request.method == 'POST':
        current_user_id = get_current_user_id()
        
        conn = conn_db()
        cursor = conn.cursor()

        try:
            cursor.execute('DELETE FROM User WHERE User_ID = %s;', (current_user_id,))
            conn.commit()
            
            # ユーザーを削除した後、セッションもクリアする
            session.clear()

            return redirect(url_for("login"))

        except mysql.connector.IntegrityError as e:
            print(e)

        finally:
            cursor.close()
            conn.close()

    return render_template("quit.html")


#================================================================================================================================================================================================
# お問い合わせフォーム
@app.route('/otoiawase/', methods=['GET', 'POST'])
def otoiawase():
    conn = conn_db()
    cursor = conn.cursor()

    # ジャンルの選択肢をデータベースから取得
    cursor.execute("SELECT Genre_ID, Genre_Name FROM Genre")
    genres = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        genre_id = request.form['genre']
        inquiry = request.form['inquiry']

        cursor.execute("INSERT INTO Inquiries (Name, Email, Genre, inquiry) VALUES (%s, %s, %s, %s)",
                       (name, email, genre_id, inquiry))
        conn.commit()

        return redirect(url_for('otoiawaseok'))

    # お問い合わせ情報とそれに紐づくジャンル名を取得
    cursor.execute("""
    SELECT i.name, i.email, i.inquiry, g.Genre_Name
    FROM Inquiries i
    JOIN Genre g ON i.genre = g.Genre_Name
    """)
    inquiries_with_genre = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('otoiawase.html', genres=genres, inquiries=inquiries_with_genre)

# お問い合わせ完了ページ
@app.route('/otoiawaseok/')
def otoiawaseok():
    return render_template('otoiawaseok.html')

# お問い合わせ内容の一覧表示
@app.route('/admin_otoiawase/')
def admin_otoiawase():
    conn = conn_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inquiries")
    inquiries = cursor.fetchall()  # 変数名を `otoiawases` から `inquiries` に変更
    cursor.close()
    conn.close()
    return render_template('admin_otoiawase.html', inquiries=inquiries)  # 変数名を変更




@app.route('/submit/', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    inquiry = request.form['inquiry']
    genre = request.form['genre']
    
    conn = conn_db()
    cursor = conn.cursor()
    query = "INSERT INTO inquiries (name, email, inquiry, genre) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, inquiry, genre))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('top')) # お問い合わせ完了ページへリダイレクトするか、適切な応答を返します



#================================================================================================================================================================================================

#==================================================================================================
# お知らせ
@app.route("/osirase/")
def osirase():
    conn = conn_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute('SELECT * FROM Announcements ORDER BY created_at DESC')
    announcements = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("osirase.html", announcements=announcements)
#==================================================================================================

# ー　「管理者関係」　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー

# 管理者のログインページ
@app.route("/bosslogin/")
def bosslogin():

    return render_template("bosslogin.html")

# マスターメンテナンスページ
@app.route("/master/")
def master():

    return render_template("master.html")

# 管理者トップページ
@app.route("/admin/")
def admin():

    return render_template("admin.html")

#=================================================================================================
@app.route("/admin_osirase/", methods=["POST","GET"])
def admin_osirase():
    # 管理者かどうかを確認するロジックをここに追加
    # 例: if not session.get('is_admin'): return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = conn_db()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO Announcements (title, content) VALUES (%s, %s)', (title, content))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('admin'))

    return render_template('admin_osirase.html')
#==================================================================================================


# テーブルメンテナンスページ

#「ジャンルテーブル」
@app.route("/Genre/")
def table():
    conn = conn_db()
    cursor = conn.cursor()
    sql = "SELECT Genre_ID, Genre_Name FROM Genre;"
    cursor.execute(sql)
    result = cursor.fetchall()

    return render_template("table.html", records=result)

#「ジャンルテーブルの削除」
@app.route("/table_sakujo/")
def table_sakujo():
    conn = None
    cursor = None
    
    try:
        id = request.args.get("Genre_ID", "")
        conn = conn_db()
        cursor = conn.cursor()
        
        sql = "DELETE FROM Genre WHERE Genre_ID = %s"
        cursor.execute(sql, (id,))
        conn.commit()

    except mysql.connector.ProgrammingError as e:
        print(e)
        # conn.rollback()  # エラー時にロールバックする場合はこの行のコメントを外してください

    finally:
        if cursor is not None:
            cursor.close()
        
        if conn is not None:
            conn.close()

    return redirect(url_for("table"))

# アカウント削除設定ページ
@app.route("/sakujo/")
def sakujo():
    conn = conn_db()
    cursor = conn.cursor()
    sql = "SELECT Email, Real_Name, User_Name FROM user;"
    cursor.execute(sql)
    result = cursor.fetchall()
    return render_template("sakujo.html", records=result)

# アカウント削除設定ページ
@app.route("/sakujo_/", methods=["GET"])
def sakujo_():
    conn = None
    cursor = None
    
    try:
        id = request.args.get("User_Name", "")
        conn = conn_db()
        cursor = conn.cursor()
        
        sql = "DELETE FROM user WHERE User_Name = %s"
        cursor.execute(sql, (id,))
        conn.commit()

    except mysql.connector.ProgrammingError as e:
        print(e)
        # conn.rollback()  # エラー時にロールバックする場合はこの行のコメントを外してください

    finally:
        if cursor is not None:
            cursor.close()
        
        if conn is not None:
            conn.close()

    return redirect(url_for("sakujo"))

# ユーザーメンテナンスページ
@app.route("/user/")
def user():

    conn = conn_db()
    cursor = conn.cursor()
    sql = "SELECT Email, Real_Name, User_Name FROM user;"
    cursor.execute(sql)
    result = cursor.fetchall()

    return render_template("user.html", records=result)


#　ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー 

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    # app.run(debug=True)