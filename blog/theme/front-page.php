<?php get_header(); ?>

<div class="site-content full-width">

    <!-- Hero Section -->
    <section class="fp-hero">
        <div class="fp-hero__inner">
            <p class="fp-hero__subtitle">Paraguay Life & Remote Work</p>
            <h1 class="fp-hero__title">自由に生きる。<br>海外から発信する。</h1>
            <p class="fp-hero__desc">
                南米パラグアイから、海外生活・副業・家族のリアルをお届け。<br>
                場所にとらわれない生き方のヒント。
            </p>
            <div class="fp-hero__buttons">
                <a href="#fp-featured" class="fp-hero__btn fp-hero__btn--primary">記事を読む</a>
                <a href="<?php echo esc_url(home_url('/about')); ?>" class="fp-hero__btn fp-hero__btn--outline">プロフィール</a>
            </div>
        </div>
    </section>

    <!-- Featured Articles (Latest 5) -->
    <section class="fp-section scroll-fade" id="fp-featured">
        <p class="fp-section__label">Featured</p>
        <h2 class="fp-section__heading">注目の記事</h2>

        <?php
        // デバッグ用（確認後削除）
        $test = new WP_Query(['post_type' => 'post', 'post_status' => 'publish', 'posts_per_page' => 5]);
        echo '<!-- DEBUG: found ' . $test->found_posts . ' posts -->';
        wp_reset_postdata();

        $featured = new WP_Query([
            'post_type'      => 'post',
            'posts_per_page' => 5,
            'post_status'    => 'publish',
            'orderby'        => 'date',
            'order'          => 'DESC',
        ]);

        if ($featured->have_posts()) :
            $count = 0;
        ?>

        <div class="fp-featured-layout">
            <?php while ($featured->have_posts()) : $featured->the_post(); $count++; ?>

                <?php if ($count === 1) : ?>
                <!-- 1件目：横幅いっぱいの大きなカード -->
                <a href="<?php the_permalink(); ?>" class="fp-hero-card scroll-fade"
                   <?php if (has_post_thumbnail()) : ?>
                   style="background-image: url('<?php echo esc_url(get_the_post_thumbnail_url(get_the_ID(), 'large')); ?>');"
                   <?php endif; ?>
                >
                    <div class="fp-hero-card__overlay"></div>
                    <div class="fp-hero-card__body">
                        <?php $cats = get_the_category(); if ($cats) : ?>
                        <span class="fp-hero-card__cat"><?php echo esc_html($cats[0]->name); ?></span>
                        <?php endif; ?>
                        <h3 class="fp-hero-card__title"><?php the_title(); ?></h3>
                        <p class="fp-hero-card__excerpt"><?php echo get_the_excerpt(); ?></p>
                        <span class="fp-hero-card__date"><?php echo get_the_date('Y.m.d'); ?></span>
                    </div>
                </a>
                <?php else : ?>

                <?php if ($count === 2) : ?>
                <div class="fp-sub-grid">
                <?php endif; ?>

                <!-- 2-5件目：2列グリッド -->
                <a href="<?php the_permalink(); ?>" class="fp-sub-card scroll-fade"
                   <?php if (has_post_thumbnail()) : ?>
                   style="background-image: url('<?php echo esc_url(get_the_post_thumbnail_url(get_the_ID(), 'medium_large')); ?>');"
                   <?php endif; ?>
                >
                    <div class="fp-sub-card__overlay"></div>
                    <div class="fp-sub-card__body">
                        <?php $cats = get_the_category(); if ($cats) : ?>
                        <span class="fp-sub-card__cat"><?php echo esc_html($cats[0]->name); ?></span>
                        <?php endif; ?>
                        <h3 class="fp-sub-card__title"><?php the_title(); ?></h3>
                        <span class="fp-sub-card__date"><?php echo get_the_date('Y.m.d'); ?></span>
                    </div>
                </a>
                <?php endif; ?>

            <?php endwhile; ?>

            <?php if ($count > 1) : ?>
            </div><!-- .fp-sub-grid -->
            <?php endif; ?>
        </div><!-- .fp-featured-layout -->

        <?php else : ?>
        <p class="fp-empty">記事がまだありません</p>
        <?php endif; wp_reset_postdata(); ?>
    </section>

    <!-- Latest Articles (6件目以降、番号付きリスト) -->
    <?php
    $latest = new WP_Query([
        'post_type'      => 'post',
        'posts_per_page' => 10,
        'post_status'    => 'publish',
        'offset'         => 5,
        'orderby'        => 'date',
        'order'          => 'DESC',
    ]);

    if ($latest->have_posts()) :
    ?>
    <section class="fp-latest-section scroll-fade">
        <div class="fp-latest-inner">
            <p class="fp-section__label">Latest</p>
            <h2 class="fp-section__heading">最新の記事</h2>
            <ol class="fp-latest-list">
                <?php $num = 6; while ($latest->have_posts()) : $latest->the_post(); ?>
                <li class="fp-latest-item scroll-fade">
                    <span class="fp-latest-item__num"><?php echo str_pad($num, 2, '0', STR_PAD_LEFT); ?></span>
                    <div class="fp-latest-item__body">
                        <a href="<?php the_permalink(); ?>" class="fp-latest-item__link">
                            <h3 class="fp-latest-item__title"><?php the_title(); ?></h3>
                        </a>
                        <div class="fp-latest-item__meta">
                            <?php $cats = get_the_category(); if ($cats) : ?>
                            <span class="fp-latest-item__cat"><?php echo esc_html($cats[0]->name); ?></span>
                            <?php endif; ?>
                            <time datetime="<?php echo get_the_date('c'); ?>"><?php echo get_the_date('Y.m.d'); ?></time>
                        </div>
                    </div>
                    <?php if (has_post_thumbnail()) : ?>
                    <a href="<?php the_permalink(); ?>" class="fp-latest-item__thumb">
                        <?php the_post_thumbnail('thumbnail'); ?>
                    </a>
                    <?php endif; ?>
                </li>
                <?php $num++; endwhile; ?>
            </ol>
        </div>
    </section>
    <?php endif; wp_reset_postdata(); ?>

    <!-- Profile Section -->
    <section class="fp-profile">
        <div class="fp-profile__inner scroll-fade">
            <div class="fp-profile__avatar">
                <?php
                // Gravatar or fallback
                $admin = get_user_by('email', get_option('admin_email'));
                if ($admin) {
                    echo get_avatar($admin->ID, 120, '', '南米おやじ', ['class' => 'fp-profile__img']);
                }
                ?>
            </div>
            <div class="fp-profile__content">
                <p class="fp-section__label">About</p>
                <h2 class="fp-profile__name">南米おやじ</h2>
                <p class="fp-profile__bio">
                    南米パラグアイ在住のフリーランサー。海外生活、副業、家族、投資、<br class="pc-only">
                    フィットネスなど場所に縛られない生き方をリアルに発信。
                </p>
                <div class="fp-profile__links">
                    <a href="<?php echo esc_url(home_url('/')); ?>" class="fp-profile__link">
                        <span>ブログ</span>
                    </a>
                    <a href="https://x.com/nambei_oyaji" target="_blank" rel="noopener" class="fp-profile__link fp-profile__link--x">
                        <span>𝕏 Twitter</span>
                    </a>
                </div>
            </div>
        </div>
    </section>

</div>

<?php get_footer(); ?>
