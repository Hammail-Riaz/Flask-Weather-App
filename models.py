from app import database

class Blog_posts(database.Model):
    __tablename__ = "Blogs_Posts_data"
    
    s_no = database.Column(database.Integer, primary_key= True)
    name = database.Column(database.Text, nullable=False)
    post_title = database.Column(database.Text, nullable=False)
    post_content = database.Column(database.Text, nullable=False)
    date_and_time = database.Column(database.Text, nullable=False)
    post_token = database.Column(database.Text, nullable=False)
    
    
    def __repr__(self):
        return f"{self.s_no} {self.name} {self.post_content} {self.post_content} {self.date_and_time} {self.post_token}"