# test/functional/test_post_detail.py
from app.models import User
from test.factories import PostFactory


long_content = """Im baby taiyaki ennui taxidermy jianbing YOLO venmo,
knausgaard ugh palo santo readymade hella swag scenester. Post - ironic
taxidermy mixtape activated charcoal, chambray freegan tacos man braid bespoke
occupy whatever typewriter fam godard. Street art photo booth shaman bicycle
rights, flexitarian sustainable twee small batch messenger bag swag hella VHS.
Yr pour - over try-hard, franzen scenester post - ironic hot chicken copper
mug. Direct trade artisan celiac raw denim schlitz blue bottle poke chambray
pug humblebrag. Chicharrones health goth selfies, ethical tousled truffaut
everyday carry blue bottle freegan glossier tilde.

Ennui echo park la croix cold - pressed coloring book bushwick pabst.
Scenester chicharrones YOLO ethical unicorn normcore farm - to - table shaman
raw denim. Crucifix retro vape kitsch, try-hard celiac normcore four loko
tumblr roof party echo park lyft craft beer flexitarian. Small batch 90s pork
belly selfies fixie fingerstache."""


def test_post_shortening(test_client, db_init, insert_user):
    """
    GIVEN one inserted user, and one inserted long post
    WHEN index is hit
    THEN a "Read more" link, linking to the the inserted post's detail
            template is present in the response
    WHEN the post's detail is hit
    THEN the whole post's content is rendered
    """
    author = User.query.first()
    post = PostFactory.create(
        content=long_content,
        user=author,
        user_id=author.id)

    response = test_client.get("/")
    assert bytes(
        f'<a href="/post/{post.id}">Read more</a>',
        encoding="utf-8"
    ) in response.data

    response_detail = test_client.get(f"/post/{post.id}")
    assert response_detail.status_code == 200
    assert long_content in response_detail.data.decode('utf-8')


def test_unexisting_post_detail_returns_404_template(test_client, db_init):
    """
    GIVEN test_client and db init
    WHEN post detail is hit with unexisting post id
    THEN - Response status code is 404
         - 404.j2.html is rendered
    """
    resp = test_client.get("/post/999")
    assert resp.status_code == 404
    assert b"404" in resp.data
    assert b"Not found" in resp.data
    assert b'Let&apos;s head back to <a href="/">the index</a>.' in resp.data
