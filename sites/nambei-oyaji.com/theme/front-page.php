<?php get_header(); ?>

<style>
/* ===== Front Page Self-Contained CSS ===== */

/* Section common */
.fp-section, .fp-latest-section, .fp-profile {
    max-width: 1200px;
    margin: 0 auto;
    padding: 80px 24px;
}
.fp-section__label {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6e6e73;
    margin-bottom: 8px;
}
.fp-section__heading {
    font-size: 36px;
    font-weight: 700;
    color: #1d1d1f;
    margin-bottom: 40px;
}

/* Hero */
.fp-hero {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #fff;
    text-align: center;
    padding: 120px 24px 100px;
}
.fp-hero__inner { max-width: 800px; margin: 0 auto; }
.fp-hero__subtitle {
    font-size: 14px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.6);
    margin-bottom: 16px;
}
.fp-hero__title {
    font-size: 42px;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 20px;
    color: #fff;
}
.fp-hero__desc {
    font-size: 17px;
    line-height: 1.8;
    color: rgba(255,255,255,0.8);
    margin-bottom: 32px;
}
.fp-hero__buttons { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.fp-hero__btn {
    display: inline-block;
    padding: 14px 32px;
    border-radius: 50px;
    font-size: 15px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s;
}
.fp-hero__btn--primary {
    background: #fff;
    color: #1d1d1f;
}
.fp-hero__btn--primary:hover { background: #f0f0f0; }
.fp-hero__btn--outline {
    border: 1.5px solid rgba(255,255,255,0.5);
    color: #fff;
}
.fp-hero__btn--outline:hover { border-color: #fff; background: rgba(255,255,255,0.1); }

/* Featured Cards Layout */
.fp-featured-layout {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

/* Card gradients */
.fp-card-grad-1 { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e) !important; }
.fp-card-grad-2 { background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460) !important; }
.fp-card-grad-3 { background: linear-gradient(135deg, #2d1b69, #11998e) !important; }
.fp-card-grad-4 { background: linear-gradient(135deg, #1e3c72, #2a5298) !important; }
.fp-card-grad-5 { background: linear-gradient(135deg, #0a1628, #1a3a5c) !important; }

/* Hero card (1st article) */
.fp-hero-card {
    display: block;
    position: relative;
    min-height: 560px;
    border-radius: 20px;
    overflow: hidden;
    text-decoration: none;
    background-size: cover;
    background-position: center;
    transition: transform 0.3s;
}
.fp-hero-card:hover { transform: scale(1.01); }
.fp-hero-card__overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.1) 60%, transparent 100%);
    border-radius: 20px;
}
.fp-hero-card__body {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 40px;
    z-index: 1;
}
.fp-hero-card__cat {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(8px);
    color: #ffffff;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
}
.fp-hero-card__title {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 12px;
    line-height: 1.4;
}
.fp-hero-card__excerpt {
    font-size: 15px;
    color: rgba(255,255,255,0.85);
    line-height: 1.6;
    margin-bottom: 12px;
    max-width: 600px;
}
.fp-hero-card__date {
    font-size: 13px;
    color: rgba(255,255,255,0.6);
}

/* Sub cards (2nd-5th) */
.fp-sub-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
}
.fp-sub-card {
    display: block;
    position: relative;
    min-height: 480px;
    border-radius: 20px;
    overflow: hidden;
    text-decoration: none;
    background-size: cover;
    background-position: center;
    transition: transform 0.3s;
}
.fp-sub-card:hover { transform: scale(1.02); }
.fp-sub-card__overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.1) 60%, transparent 100%);
    border-radius: 20px;
}
.fp-sub-card__body {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 28px;
    z-index: 1;
}
.fp-sub-card__cat {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(8px);
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
}
.fp-sub-card__title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 8px;
    line-height: 1.4;
}
.fp-sub-card__date {
    font-size: 12px;
    color: rgba(255,255,255,0.6);
}

/* Latest Articles List */
.fp-latest-section {
    background: #ffffff;
}
.fp-latest-inner {
    max-width: 1200px;
    margin: 0 auto;
}
.fp-latest-list {
    list-style: none;
    padding: 0;
    margin: 0;
}
.fp-latest-item {
    display: flex;
    align-items: center;
    gap: 24px;
    padding: 24px 0;
    border-bottom: 1px solid #e5e5e7;
    transition: background 0.2s;
}
.fp-latest-item:hover { background: #f9f9f9; }
.fp-latest-item__num {
    font-size: 36px;
    font-weight: 700;
    color: #d2d2d7;
    min-width: 56px;
    text-align: center;
}
.fp-latest-item__body { flex: 1; }
.fp-latest-item__link {
    text-decoration: none;
    color: inherit;
}
.fp-latest-item__title {
    font-size: 18px;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 6px;
    line-height: 1.5;
}
.fp-latest-item__meta {
    display: flex;
    gap: 12px;
    align-items: center;
    font-size: 13px;
    color: #6e6e73;
}
.fp-latest-item__cat {
    background: #f5f5f7;
    color: #1d1d1f;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}
.fp-latest-item__thumb {
    flex-shrink: 0;
    width: 80px;
    height: 80px;
    border-radius: 12px;
    overflow: hidden;
}
.fp-latest-item__thumb img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Profile */
.fp-profile {
    background: #f5f5f7;
    padding: 80px 24px;
}
.fp-profile__inner {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 40px;
}
.fp-profile__img {
    width: 120px;
    height: 120px;
    border-radius: 50%;
}
.fp-profile__name {
    font-size: 28px;
    font-weight: 700;
    color: #1d1d1f;
    margin-bottom: 8px;
}
.fp-profile__bio {
    font-size: 15px;
    color: #6e6e73;
    line-height: 1.8;
    margin-bottom: 16px;
}
.fp-profile__links {
    display: flex;
    gap: 12px;
}
.fp-profile__link {
    display: inline-block;
    padding: 8px 20px;
    border: 1.5px solid #d2d2d7;
    border-radius: 50px;
    font-size: 13px;
    font-weight: 600;
    color: #1d1d1f;
    text-decoration: none;
    transition: all 0.3s;
}
.fp-profile__link:hover {
    background: #1d1d1f;
    color: #fff;
    border-color: #1d1d1f;
}

/* Empty state */
.fp-empty {
    text-align: center;
    color: #6e6e73;
    font-size: 16px;
    padding: 60px 0;
}

/* Responsive */
@media (max-width: 768px) {
    .fp-hero__title { font-size: 28px; }
    .fp-section__heading { font-size: 28px; }
    .fp-sub-grid { grid-template-columns: 1fr; }
    .fp-hero-card { min-height: 400px; }
    .fp-sub-card { min-height: 360px; }
    .fp-hero-card__title { font-size: 22px; }
    .fp-hero-card__body { padding: 24px; }
    .fp-profile__inner { flex-direction: column; text-align: center; }
    .fp-profile__links { justify-content: center; }
    .fp-latest-item__num { font-size: 28px; min-width: 40px; }
}

.pc-only { display: inline; }
@media (max-width: 768px) { .pc-only { display: none; } }
</style>

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
        $debug_query = new WP_Query([
            'post_type'      => 'post',
            'post_status'    => 'publish',
            'posts_per_page' => 5,
        ]);
        echo '<p style="color:red;font-size:24px;padding:20px;">DEBUG: ' . $debug_query->found_posts . ' posts found</p>';
        wp_reset_postdata();

        $gradients = [
            'fp-card-grad-1',
            'fp-card-grad-2',
            'fp-card-grad-3',
            'fp-card-grad-4',
            'fp-card-grad-5',
        ];

        $featured = new WP_Query([
            'post_type'      => 'post',
            'post_status'    => 'publish',
            'posts_per_page' => 5,
            'orderby'        => 'date',
            'order'          => 'DESC',
        ]);

        if ($featured->have_posts()) :
            $count = 0;
        ?>

        <div class="fp-featured-layout">
            <?php while ($featured->have_posts()) : $featured->the_post(); $count++;
                $grad_class = $gradients[$count - 1] ?? 'fp-card-grad-1';
                $bg_style = '';
                if (has_post_thumbnail()) {
                    $bg_style = 'background-image: url(\'' . esc_url(get_the_post_thumbnail_url(get_the_ID(), ($count === 1 ? 'large' : 'medium_large'))) . '\');';
                }
            ?>

                <?php if ($count === 1) : ?>
                <!-- 1件目：横幅いっぱいの大きなカード -->
                <a href="<?php the_permalink(); ?>" class="fp-hero-card <?php echo $grad_class; ?> scroll-fade"
                   <?php if ($bg_style) : ?>style="<?php echo $bg_style; ?>"<?php endif; ?>
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
                <a href="<?php the_permalink(); ?>" class="fp-sub-card <?php echo $grad_class; ?> scroll-fade"
                   <?php if ($bg_style) : ?>style="<?php echo $bg_style; ?>"<?php endif; ?>
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
