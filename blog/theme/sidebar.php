<aside class="sidebar">

    <!-- 検索 -->
    <div class="sidebar-widget">
        <h3 class="sidebar-widget__title">検索</h3>
        <form class="search-form" role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
            <input type="search" name="s" placeholder="キーワードで検索" value="<?php echo get_search_query(); ?>">
            <button type="submit">🔍</button>
        </form>
    </div>

    <!-- 新着 / 人気 タブ -->
    <div class="sidebar-widget">
        <div class="tab-nav">
            <button class="tab-nav__btn active" data-tab="tab-new">新着記事</button>
            <button class="tab-nav__btn" data-tab="tab-popular">人気記事</button>
        </div>

        <!-- 新着 -->
        <div class="tab-panel active" id="tab-new">
            <ul class="sidebar-post-list">
                <?php
                $recent = new WP_Query(['posts_per_page' => 5, 'post_status' => 'publish']);
                while ($recent->have_posts()) : $recent->the_post();
                ?>
                <li class="sidebar-post-item">
                    <a href="<?php the_permalink(); ?>" class="sidebar-post-item__thumb">
                        <?php if (has_post_thumbnail()) : ?>
                            <?php the_post_thumbnail('thumbnail'); ?>
                        <?php else : ?>
                            <img src="<?php echo esc_url(get_stylesheet_directory_uri()); ?>/assets/img/no-image.png" alt="No Image">
                        <?php endif; ?>
                    </a>
                    <a href="<?php the_permalink(); ?>" class="sidebar-post-item__title"><?php the_title(); ?></a>
                </li>
                <?php endwhile; wp_reset_postdata(); ?>
            </ul>
        </div>

        <!-- 人気 -->
        <div class="tab-panel" id="tab-popular">
            <ul class="sidebar-post-list">
                <?php
                $popular = nambei_get_popular_posts(5);
                while ($popular->have_posts()) : $popular->the_post();
                ?>
                <li class="sidebar-post-item">
                    <a href="<?php the_permalink(); ?>" class="sidebar-post-item__thumb">
                        <?php if (has_post_thumbnail()) : ?>
                            <?php the_post_thumbnail('thumbnail'); ?>
                        <?php else : ?>
                            <img src="<?php echo esc_url(get_stylesheet_directory_uri()); ?>/assets/img/no-image.png" alt="No Image">
                        <?php endif; ?>
                    </a>
                    <a href="<?php the_permalink(); ?>" class="sidebar-post-item__title"><?php the_title(); ?></a>
                </li>
                <?php endwhile; wp_reset_postdata(); ?>
            </ul>
        </div>
    </div>

    <!-- カテゴリ -->
    <div class="sidebar-widget">
        <h3 class="sidebar-widget__title">カテゴリ</h3>
        <ul class="category-list">
            <?php
            $categories = get_categories(['hide_empty' => true]);
            foreach ($categories as $cat) :
            ?>
            <li>
                <a href="<?php echo esc_url(get_category_link($cat->term_id)); ?>">
                    <?php echo esc_html($cat->name); ?>
                    <span class="count"><?php echo $cat->count; ?></span>
                </a>
            </li>
            <?php endforeach; ?>
        </ul>
    </div>

</aside>
