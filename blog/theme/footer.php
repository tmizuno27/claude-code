<footer class="site-footer">
    <div class="footer-inner">
        <div class="footer-columns">
            <div class="footer-column">
                <h3 class="footer-column__title">カテゴリ</h3>
                <ul>
                    <li><a href="<?php echo esc_url(get_category_link(get_cat_ID('paraguay'))); ?>">パラグアイ生活</a></li>
                    <li><a href="<?php echo esc_url(get_category_link(get_cat_ID('side-business'))); ?>">副業・稼ぎ方</a></li>
                    <li><a href="<?php echo esc_url(get_category_link(get_cat_ID('ijuu-junbi'))); ?>">移住準備</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h3 class="footer-column__title">サイト情報</h3>
                <ul>
                    <li><a href="<?php echo esc_url(home_url('/about')); ?>">運営者について</a></li>
                    <li><a href="<?php echo esc_url(home_url('/privacy-policy')); ?>">プライバシーポリシー</a></li>
                    <li><a href="<?php echo esc_url(home_url('/contact')); ?>">お問い合わせ</a></li>
                </ul>
            </div>
            <div class="footer-column">
                <h3 class="footer-column__title">フォローする</h3>
                <div class="footer-sns">
                    <a href="https://x.com/nambei_oyaji" target="_blank" rel="noopener" aria-label="X">𝕏</a>
                </div>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; <?php echo date('Y'); ?> 南米おやじの海外生活ラボ All Rights Reserved.</p>
        </div>
    </div>
</footer>

<button class="scroll-top" id="js-scroll-top" aria-label="トップへ戻る">↑</button>

<?php wp_footer(); ?>
</body>
</html>
