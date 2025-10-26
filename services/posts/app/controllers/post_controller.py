from flask import Blueprint, request, jsonify , current_app
from app.models.post import Post
from app.schemas.post import PostSchema
from app.db import db
from flask_jwt_extended import get_jwt_identity,jwt_required
from app.lib.s3 import s3_client
from app.config import Config
from uuid import uuid4
from sqlalchemy import insert,delete
from app.models.post import likes , ImageKey 
from sqlalchemy import select, exists
from app.schemas.user import UserSchema

post_blueprint = Blueprint('post', __name__)
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
user_schema = UserSchema()

@post_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    post = Post(
        description=data['description'],
        owner_id=user_id
    )
    db.session.add(post)
    db.session.commit()
    images_keys = map(lambda image: ImageKey(key=image,post_id=post.id), data.get('image_keys', []))
    db.session.add_all(images_keys)
    current_app.rabbit_channel.basic_publish(exchange='',
                      routing_key=Config.CREATED_POSTS_QUEUE_NAME,
                      body=str(post.id))


    return "Post created",201



@post_blueprint.route('/', methods=['GET'])
def get_posts():

    is_liked_subquery = (
        select(likes.c.post_id)
        .where(
            (likes.c.post_id == Post.id)
            & (likes.c.user_id == 1)
        )
        .exists()
    )

    like_count_subquery = (
        select(db.func.count(likes.c.post_id))
        .where(likes.c.post_id == Post.id)
        
    )

    stmt = (
        select(
            Post,
            is_liked_subquery.label("is_liked"),
            like_count_subquery.label("likes_count")
        )
        .offset(0)
        .limit(10)
        .order_by(Post.created_at.desc())
    )

    result = db.session.execute(stmt).unique().all()
    posts_data = []
    for post, is_liked, likes_count in result:
        posts_data.append({
            "id":post.id,
            "description":post.description,
            "image_urls":[],
            "created_at":post.created_at,
            "user": user_schema.dump(post.owner),
            "likes_count":likes_count,
            "is_liked":is_liked,
            "is_owner":post.owner_id == 1

        })


    return jsonify({
        "pages":5,
        "posts":posts_data
    })



@post_blueprint.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    user_id = get_jwt_identity()

    post = db.session.execute(select(Post).where(Post.id == post_id)).scalar_one_or_none()

    if not post:
        return '', 404
    
    if post.owner_id != user_id:
        return '', 403

    db.session.delete(post)
    db.session.commit()
    return '', 204



@post_blueprint.route('/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id, user_id):
    user_id = get_jwt_identity()
    stmt = insert(likes).values(user_id=user_id, post_id=post_id)
    db.session.execute(stmt)
    db.session.commit()
    return '', 201

@post_blueprint.route('/<int:post_id>/unlike', methods=['POST'])
@jwt_required()
def unlike_post(post_id, user_id):
    user_id = get_jwt_identity()
    stmt = delete(likes).where(
        likes.c.user_id == user_id,
        likes.c.post_id == post_id
    )
    db.session.execute(stmt)
    db.session.commit()
    return '', 204



@post_blueprint.route('/get-signed-url', methods=['GET'])
def get_signed_url():
    file_name = request.args.get('file_name')
    file_type = request.args.get('file_type')

    if not file_name or not file_type:
        return jsonify({'error': 'file_name and file_type are required'}), 400

   
    key = f'{uuid4().hex}-{file_name}'
    presigned_url = s3_client.generate_presigned_url('put_object',
                                                        Params={'Bucket': Config.POST_IMAGES_BUCKET,
                                                                'Key': key,
                                                                'ContentType': file_type},
                                                        ExpiresIn=3600)
    return jsonify({'url': presigned_url}), 200
