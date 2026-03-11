<?php
/**
 * 南米おやじ Child Theme - functions.php
 */

// 親テーマ + 子テーマ スタイル読み込み
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('generatepress-style', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('nambei-child-style', get_stylesheet_uri(), ['generatepress-style'], wp_get_theme()->get('Version'));
    wp_enqueue_style('google-fonts', 'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap', [], null);
    wp_enqueue_script('nambei-custom', get_stylesheet_directory_uri() . '/assets/js/custom.js', [], '1.0.0', true);
});

// ナビゲーションメニュー登録
register_nav_menus([
    'primary'  => 'メインメニュー',
    'footer'   => 'フッターメニュー',
]);

// ============================================
// 目次自動生成（h2/h3 → TOC）
// ============================================
function nambei_generate_toc($content) {
    if (!is_single()) return $content;

    preg_match_all('/<h([23])[^>]*>(.*?)<\/h[23]>/i', $content, $matches, PREG_SET_ORDER);
    if (count($matches) < 3) return $content;

    $toc = '<div class="toc-wrap"><p class="toc-wrap__title">目次</p><ol>';
    $counter = 0;

    foreach ($matches as $m) {
        $level = $m[1];
        $text  = strip_tags($m[2]);
        $id    = 'toc-' . (++$counter);

        // 見出しにIDを付与
        $content = preg_replace(
            '/' . preg_quote($m[0], '/') . '/',
            sprintf('<h%s id="%s">%s</h%s>', $level, $id, $m[2], $level),
            $content,
            1
        );

        $indent = $level === '3' ? ' style="margin-left:20px;list-style-type:circle;"' : '';
        $toc .= sprintf('<li%s><a href="#%s">%s</a></li>', $indent, $id, $text);
    }

    $toc .= '</ol></div>';

    // 最初のh2の直前に目次を挿入
    $content = preg_replace('/<h2/', $toc . '<h2', $content, 1);

    return $content;
}
add_filter('the_content', 'nambei_generate_toc', 10);

// ============================================
// 人気記事カウント（post_views カスタムフィールド）
// ============================================
function nambei_count_post_views() {
    if (is_single() && !is_admin()) {
        $post_id = get_the_ID();
        $views   = (int) get_post_meta($post_id, 'post_views', true);
        update_post_meta($post_id, 'post_views', $views + 1);
    }
}
add_action('wp_head', 'nambei_count_post_views');

function nambei_get_popular_posts($count = 5) {
    return new WP_Query([
        'posts_per_page' => $count,
        'meta_key'       => 'post_views',
        'orderby'        => 'meta_value_num',
        'order'          => 'DESC',
        'post_status'    => 'publish',
    ]);
}

// ============================================
// 抜粋文字数
// ============================================
add_filter('excerpt_length', function () { return 60; });
add_filter('excerpt_more', function () { return '…'; });

// ============================================
// パンくずリスト
// ============================================
function nambei_breadcrumb() {
    if (is_front_page()) return;

    echo '<nav class="breadcrumb" aria-label="パンくず">';
    echo '<a href="' . esc_url(home_url('/')) . '">ホーム</a>';
    echo '<span class="separator">›</span>';

    if (is_single()) {
        $cats = get_the_category();
        if ($cats) {
            echo '<a href="' . esc_url(get_category_link($cats[0]->term_id)) . '">' . esc_html($cats[0]->name) . '</a>';
            echo '<span class="separator">›</span>';
        }
        echo '<span>' . get_the_title() . '</span>';
    } elseif (is_category()) {
        echo '<span>' . single_cat_title('', false) . '</span>';
    } elseif (is_tag()) {
        echo '<span>' . single_tag_title('', false) . '</span>';
    } elseif (is_search()) {
        echo '<span>「' . get_search_query() . '」の検索結果</span>';
    } elseif (is_archive()) {
        echo '<span>' . get_the_archive_title() . '</span>';
    }

    echo '</nav>';
}

// ============================================
// 関連記事取得
// ============================================
function nambei_get_related_posts($post_id, $count = 3) {
    $cats    = get_the_category($post_id);
    $cat_ids = $cats ? wp_list_pluck($cats, 'term_id') : [];

    return new WP_Query([
        'posts_per_page' => $count,
        'post__not_in'   => [$post_id],
        'category__in'   => $cat_ids,
        'post_status'    => 'publish',
        'orderby'        => 'rand',
    ]);
}
