from app import schema
import pytest
def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200
    def validate(post):
        return schema.Postresponse(**post)
    # print(list(posts_map))
    assert len(response.json()) == len(test_posts)  

def unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 200
    post = schema.Postresponse(**response.json())
    assert post.id == test_posts[0].id

def test_get_one_post_not_found(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/9999")
    assert response.status_code == 404
@pytest.mark.parametrize("title, content, published", [
    ("Test Post 1", "Content 1", True),
    ("Test Post 2", "Content 2", False),
    ("Test Post 3", "Content 3", True)
])

def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts/", json={"title": title,
                                                       "content": content,
                                                       "published": published})
    assert response.status_code == 201
    post = schema.Postresponse(**response.json())
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user):
    response = authorized_client.post("/posts/", json={"title": "New Post",
                                                       "content": "New Post Content"})
    assert response.status_code == 201
    post = schema.Postresponse(**response.json())
    assert post.published == True

def test_get_all_posts(unauthorized_client, test_posts):
    response = unauthorized_client.get("/posts/all")
    assert response.status_code == 200
    def validate(post):
        return schema.Postresponse(**post)
    assert len(response.json()) == len(test_posts)

def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_not_found(authorized_client):
    response = authorized_client.delete(f"/posts/9999")
    assert response.status_code == 404

def test_delete_post_unauthorized_user(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_forbidden(authorized_client, test_posts, test_user):
    # Create a new user
    new_user_response = authorized_client.post("/users/", json={"email": "newuser@example.com", "password": "password123"})
    assert new_user_response.status_code == 201
    new_user = new_user_response.json()
    response = authorized_client.delete(f"/posts/{test_posts[2].id}",headers={"Authorization": f"Bearer {new_user['token']}"})
    assert response.status_code == 403
