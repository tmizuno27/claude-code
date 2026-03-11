<?php get_header(); ?>

<div class="site-content full-width">

    <!-- Hero Section -->
    <section class="fp-hero">
        <div class="fp-hero__inner">
            <p class="fp-hero__subtitle">Paraguay Life & Remote Work</p>
            <h1 class="fp-hero__title">南米パラグアイから届ける<br>リアルな海外生活</h1>
            <p class="fp-hero__desc">
                パラグアイ在住の「南米おやじ」が、移住・生活費・子育て・海外からの働き方まで、<br>
                実体験ベースで発信する海外生活メディア
            </p>
            <a href="#fp-latest" class="fp-hero__btn">記事を読む</a>
        </div>
    </section>

    <!-- Latest Articles -->
    <section class="fp-section scroll-fade" id="fp-latest">
        <p class="fp-section__label">Latest Articles</p>
        <h2 class="fp-section__heading">最新の記事</h2>
        <div class="fp-featured-grid">
            <?php
            $latest = new WP_Query(['posts_per_page' => 6, 'post_status' => 'publish']);
            while ($latest->have_posts()) : $latest->the_post();
            ?>
            <a href="<?php the_permalink(); ?>" class="fp-featured-card scroll-fade">
                <div class="fp-featured-card__thumb">
                    <?php if (has_post_thumbnail()) : ?>
                        <?php the_post_thumbnail('medium_large'); ?>
                    <?php endif; ?>
                </div>
                <div class="fp-featured-card__body">
                    <?php $cats = get_the_category(); if ($cats) : ?>
                    <span class="fp-featured-card__cat"><?php echo esc_html($cats[0]->name); ?></span>
                    <?php endif; ?>
                    <h3 class="fp-featured-card__title"><?php the_title(); ?></h3>
                    <p class="fp-featured-card__excerpt"><?php echo get_the_excerpt(); ?></p>
                </div>
            </a>
            <?php endwhile; wp_reset_postdata(); ?>
        </div>
    </section>

    <!-- Category Pillars -->
    <section class="fp-pillars">
        <div class="fp-pillars__inner scroll-fade">
            <p class="fp-section__label">Categories</p>
            <h2 class="fp-section__heading">コンテンツの柱</h2>
            <div class="fp-pillars-grid">
                <div class="fp-pillar-card scroll-fade">
                    <div class="fp-pillar-card__icon">🇵🇾</div>
                    <h3 class="fp-pillar-card__title">パラグアイ生活</h3>
                    <p class="fp-pillar-card__desc">
                        生活費、治安、子育て、永住権、食文化まで。<br>
                        在住者だから書ける一次情報をお届けします。
                    </p>
                </div>
                <div class="fp-pillar-card scroll-fade">
                    <div class="fp-pillar-card__icon">💼</div>
                    <h3 class="fp-pillar-card__title">海外からの働き方</h3>
                    <p class="fp-pillar-card__desc">
                        リモートワーク、副業、フリーランス。<br>
                        海外に住みながら日本円を稼ぐ方法を実践レポート。
                    </p>
                </div>
                <div class="fp-pillar-card scroll-fade">
                    <div class="fp-pillar-card__icon">✈️</div>
                    <h3 class="fp-pillar-card__title">移住準備</h3>
                    <p class="fp-pillar-card__desc">
                        ビザ、引っ越し、海外送金、保険。<br>
                        移住前に知っておきたいことを完全ガイド。
                    </p>
                </div>
                <div class="fp-pillar-card scroll-fade">
                    <div class="fp-pillar-card__icon">🌎</div>
                    <h3 class="fp-pillar-card__title">南米おやじの日常</h3>
                    <p class="fp-pillar-card__desc">
                        アサード、サッカー、家族の日々。<br>
                        リアルな南米ライフをお届け。
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- Popular Articles -->
    <section class="fp-section scroll-fade">
        <p class="fp-section__label">Popular</p>
        <h2 class="fp-section__heading">人気の記事</h2>
        <div class="fp-featured-grid">
            <?php
            $popular = nambei_get_popular_posts(3);
            while ($popular->have_posts()) : $popular->the_post();
            ?>
            <a href="<?php the_permalink(); ?>" class="fp-featured-card scroll-fade">
                <div class="fp-featured-card__thumb">
                    <?php if (has_post_thumbnail()) : ?>
                        <?php the_post_thumbnail('medium_large'); ?>
                    <?php endif; ?>
                </div>
                <div class="fp-featured-card__body">
                    <?php $cats = get_the_category(); if ($cats) : ?>
                    <span class="fp-featured-card__cat"><?php echo esc_html($cats[0]->name); ?></span>
                    <?php endif; ?>
                    <h3 class="fp-featured-card__title"><?php the_title(); ?></h3>
                    <p class="fp-featured-card__excerpt"><?php echo get_the_excerpt(); ?></p>
                </div>
            </a>
            <?php endwhile; wp_reset_postdata(); ?>
        </div>
    </section>

</div>

<?php get_footer(); ?>
