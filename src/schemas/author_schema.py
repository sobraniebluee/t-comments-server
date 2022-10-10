from src.schemas.user_schema import UserSchema

AuthorSchema = UserSchema(many=False, only=("id", "username",))

