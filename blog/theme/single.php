<?php get_header(); ?>

<div class="site-content">
    <main>
        <?php while (have_posts()) : the_post(); ?>

        <article class="single-article">
            <div class="single-article__header">
                <?php
                $cats = get_the_category();
                if ($cats) :
                ?>
                <span class="single-article__cat"><?php echo esc_html($cats[0]->name); ?></span>
                <?php endif; ?>

                <h1 class="single-article__title"><?php the_title(); ?></h1>

                <div class="single-article__meta">
                    <time datetime="<?php echo get_the_date('c'); ?>">
                        <?php echo get_the_date('Y.m.d'); ?>
                    </time>
                    <?php if (get_the_modified_date() !== get_the_date()) : ?>
                    <span>（更新: <?php echo get_the_modified_date('Y.m.d'); ?>）</span>
                    <?php endif; ?>
                </div>
            </div>

            <?php if (has_post_thumbnail()) : ?>
            <figure class="single-article__eyecatch">
                <?php the_post_thumbnail('full'); ?>
            </figure>
            <?php endif; ?>

            <div class="single-article__content">
                <?php the_content(); ?>
            </div>

            <!-- シェアボタン -->
            <div class="share-buttons">
                <?php
                $share_url   = urlencode(get_permalink());
                $share_title = urlencode(get_the_title());
                ?>
                <a class="share-btn share-btn--x" href="https://x.com/intent/tweet?url=<?php echo $share_url; ?>&text=<?php echo $share_title; ?>" target="_blank" rel="noopener">𝕏 ポスト</a>
                <a class="share-btn share-btn--fb" href="https://www.facebook.com/sharer/sharer.php?u=<?php echo $share_url; ?>" target="_blank" rel="noopener">Facebook</a>
                <a class="share-btn share-btn--line" href="https://social-plugins.line.me/lineit/share?url=<?php echo $share_url; ?>" target="_blank" rel="noopener">LINE</a>
                <a class="share-btn share-btn--hatena" href="https://b.hatena.ne.jp/entry/s/<?php echo urlencode(str_replace(['https://', 'http://'], '', get_permalink())); ?>" target="_blank" rel="noopener">はてブ</a>
            </div>

            <!-- 著者情報 -->
            <div class="author-box">
                <?php echo get_avatar(get_the_author_meta('ID'), 80, '', '', ['class' => 'author-box__avatar']); ?>
                <div>
                    <p class="author-box__name"><?php the_author(); ?></p>
                    <p class="author-box__bio"><?php the_author_meta('description'); ?></p>
                </div>
            </div>
        </article>

        <!-- 関連記事 -->
        <?php
        $related = nambei_get_related_posts(get_the_ID(), 3);
        if ($related->have_posts()) :
        ?>
        <div class="related-posts">
            <h2 class="related-posts__title">関連記事</h2>
            <div class="related-posts__grid">
                <?php while ($related->have_posts()) : $related->the_post(); ?>
                <a href="<?php the_permalink(); ?>" class="related-card">
                    <div class="related-card__thumb">
                        <?php if (has_post_thumbnail()) : ?>
                            <?php the_post_thumbnail('medium'); ?>
                        <?php endif; ?>
                    </div>
                    <p class="related-card__title"><?php the_title(); ?></p>
                </a>
                <?php endwhile; wp_reset_postdata(); ?>
            </div>
        </div>
        <?php endif; ?>

        <?php endwhile; ?>
    </main>

    <?php get_sidebar(); ?>
</div>

<?php get_footer(); ?>
