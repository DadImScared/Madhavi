
import config
import models


def main():
    models.initialize()

    user = models.User.create_user(
        username=config.ADMIN_NAME,
        password=config.ADMIN_PASS
    )
    models.Post.create_post(
        user=user,
        content="about",
        page_name="about",
        page_display="About",
        page_order=0
    )
    models.Post.create_post(
        user=user,
        content="faq",
        page_name="faq",
        page_display="Faq",
        page_order=1
    )
    models.Post.create_post(
        user=user,
        content="testimonials",
        page_name="testimonials",
        page_display="Testimonials",
        page_order=2
    )


if __name__ == '__main__':
    main()
