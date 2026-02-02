
from app import schema, models

def test_vote_on_post(authorized_client, test_posts, session):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id,
                                                      "dir": 1})
    assert response.status_code == 201
    assert response.json() == {"message": "successfully added vote"}
    # verify vote exists in DB
    db_vote = session.query(models.Vote).filter_by(post_id=test_posts[0].id).first()
    assert db_vote is not None
    assert db_vote.post_id == test_posts[0].id

def test_vote_on_post_twice(authorized_client, test_posts):
    # First vote
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id,
                                                      "dir": 1})
    assert response.status_code == 201
    # Second vote on the same post
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id,
                                                      "dir": 1})
    assert response.status_code == 409  # Conflict

def test_remove_vote(authorized_client, test_posts, session):
    # First, vote on the post
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id,
                                                      "dir": 1})
    assert response.status_code == 201
    # Now, remove the vote
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id,
                                                      "dir": 0})
    assert response.status_code == 201
    assert response.json() == {"message": "successfully deleted vote"}
    # verify vote removed from DB
    db_vote = session.query(models.Vote).filter_by(post_id=test_posts[0].id).first()
    assert db_vote is None

def test_remove_nonexistent_vote(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id,
                                                      "dir": 0})
    assert response.status_code == 404  # Not Found

def test_vote_on_nonexistent_post(authorized_client):
    response = authorized_client.post("/vote/", json={"post_id": 9999,
                                                      "dir": 1})
    assert response.status_code == 404  # Not Found

def test_vote_invalid_direction(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id,
                                                      "dir": 2})
    assert response.status_code == 400  # Bad Request

def test_unauthorized_vote(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[0].id,
                                           "dir": 1})
    assert response.status_code == 401  # Unauthorized
    
def test_unauthorized_remove_vote(client, test_posts):
    response = client.post("/vote/", json={"post_id": test_posts[0].id,
                                           "dir": 0})
    assert response.status_code == 401  # Unauthorized


