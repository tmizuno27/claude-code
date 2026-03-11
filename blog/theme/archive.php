<?php get_header(); ?>

<div class="site-content">
    <main>
        <div class="archive-header">
            <?php if (is_category()) : ?>
                <h1 class="archive-header__title"><?php single_cat_title(); ?></h1>
                <?php if (category_description()) : ?>
                    <p class="archive-header__desc"><?php echo category_description(); ?></p>
                <?php endif; ?>
            <?php elseif (is_tag()) : ?>
                <h1 class="archive-header__title">#<?php single_tag_title(); ?></h1>
            <?php elseif (is_search()) : ?>
                <h1 class="archive-header__title">「<?php echo get_search_query(); ?>」の検索結果</h1>
                <p class="archive-header__desc"><?php echo $wp_query->found_posts; ?>件の記事が見つかりました</p>
            <?php else : ?>
                <h1 class="archive-header__title"><?php the_archive_title(); ?></h1>
            <?php endif; ?>
        </div>

        <div class="article-grid">
            <?php if (have_posts()) : while (have_posts()) : the_post(); ?>

            <a href="<?php the_permalink(); ?>" class="article-card">
                <div class="article-card__thumb">
                    <?php if (has_post_thumbnail()) : ?>
                        <?php the_post_thumbnail('medium_large'); ?>
                    <?php endif; ?>
                </div>
                <div class="article-card__body">
                    <?php
                    $cats = get_the_category();
                    if ($cats) :
                    ?>
                    <span class="article-card__cat"><?php echo esc_html($cats[0]->name); ?></span>
                    <?php endif; ?>
                    <h2 class="article-card__title"><?php the_title(); ?></h2>
                    <div class="article-card__meta">
                        <time datetime="<?php echo get_the_date('c'); ?>"><?php echo get_the_date('Y.m.d'); ?></time>
                    </div>
                </div>
            </a>

            <?php endwhile; else : ?>
                <p>記事が見つかりませんでした。</p>
            <?php endif; ?>
        </div>

        <div class="pagination">
            <?php
            the_posts_pagination([
                'mid_size'  => 2,
                'prev_text' => '&laquo;',
                'next_text' => '&raquo;',
            ]);
            ?>
        </div>
    </main>

    <?php get_sidebar(); ?>
</div>

<?php get_footer(); ?>
