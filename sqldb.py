# contains code for sql database connectivity and for user authentication

import mysql.connector as connection
import video_info

class mysqlconnector:
    def __init__(self):
        try:
            self.conn=connection.connect(host="localhost", user="root", database="ytsummariser", password="root")
            self.cur=self.conn.cursor()
        except:
            print("Could not connect to SQL")
    
    # user authentication

    def user_signup(self,username,email,password):
        self.cur.execute(f"insert into users(username,email,password) values('{username}','{email}','{password}');")
        self.conn.commit()
        self.cur.execute(f"select * from users where username='{username}' and password='{password}';")
        res=self.cur.fetchall()
        print(res)
        return res
    
    def user_exists_signup(self,email):
        self.cur.execute(f"select * from users where email='{email}';")
        res=self.cur.fetchall()
        print(res)
        return res
    
    def user_login(self,email,password):
        self.cur.execute(f"select * from users where email='{email}' and password='{password}';")
        res=self.cur.fetchall()
        print(res)
        return res
    
    # storing video information

    def check_video_info(self, user_id, video_id):
        self.cur.execute(f"select * from videos where u_id={user_id} and vid_id='{video_id}';")
        res=self.cur.fetchall()
        return res
    
    def insert_video_info(self,video_id,session_id):
        res=self.check_video_info(session_id, video_id)
        video_title=""
        if len(res)==0:
            video_title+=video_info.get_video_title(video_id)
            print("Request generated for -->", video_title)
            self.cur.execute(f"insert into videos values({session_id}, '{video_id}', '{video_title}', curdate(), curtime());")
            self.conn.commit()
        else:
            video_title+=res[0][2]
            print("User already searched for -->", video_title)
            self.cur.execute(f"insert into videos values({session_id}, '{video_id}', '{video_title}', curdate(), curtime());")
            self.conn.commit()
        return video_title
