<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="site-header">
    <div class="header-inner">
        <div class="site-logo">
            <a href="<?php echo esc_url(home_url('/')); ?>">
                <span class="logo-accent">南米おやじ</span>
            </a>
        </div>

        <button class="hamburger" id="js-hamburger" aria-label="メニュー">
            <span></span><span></span><span></span>
        </button>

        <nav class="nav-primary" id="js-nav">
            <?php
            wp_nav_menu([
                'theme_location' => 'primary',
                'container'      => false,
                'fallback_cb'    => false,
            ]);
            ?>
        </nav>
    </div>
</header>

<?php nambei_breadcrumb(); ?>
