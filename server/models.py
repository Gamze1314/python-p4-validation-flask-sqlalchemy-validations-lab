from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import func
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValueError("Name cannot be empty")

        # Check if the name already exists (case-insensitive)
        existing_author = self.query.filter(
            func.lower(Author.name) == func.lower(value)).first()

        if existing_author and existing_author.id != self.id:
            raise ValueError("An author with this name already exists")

        return value

    @validates("phone_number")
    def validate_phone_number(self, key, phone_number):
        # Remove all whitespace
        cleaned_number = ''.join(phone_number.split())

        # Check if the cleaned number contains only digits
        if not cleaned_number.isdigit():
            raise ValueError("Phone number can only contain digits")

        # Check if the number is exactly 10 digits long
        if len(cleaned_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits long")

        # If all checks pass, return the cleaned number
        return cleaned_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators

    @validates("content")
    def validate_content(self, key, value):
        # the content is at least 250 characters long
        # remove white spaces.
        value = value.replace(" ", "")
        if len(value) < 250:
            raise ValueError("Content must be at least 250 characters long")
        else:
            return value

    # Post summary is a maximum of 250 characters
    @validates("summary")
    def validate_summary(self, key, value):
        # remove whitespaces
        value = value.replace(" ", "")
        # the summary is at most 250 characters long
        if len(value) > 250:
            raise ValueError("Summary must be at most 250 characters long")
        else:
            return value

    # category is fiction or non-fiction

    @validates("category")
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either Fiction or Non-Fiction")
        else:
            return value

    # post title is sufficently clickbait-y and must contain one of the following:
    # Won't Believe
    # Secret
    # Top
    # Guess

    @validates("title")
    def validate_title(self, key, value):
        # Title must contain one of the following: Won't Believe, Secret, Top, Guess
        if not value:
            raise ValueError("Title cannot be empty")
        if not any(word in value for word in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError(
                "Title must contain one of the following: Won't Believe, Secret, Top, Guess")
        else:
            return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
