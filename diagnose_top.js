const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 10000));

    // Diagnose all sections
    const diag = await pg.evaluate(() => {
        const results = {};

        // Check if page is using "page" template or "front-page"
        results.bodyClasses = document.body.className;

        // Check entry-content
        const ec = document.querySelector('.entry-content');
        results.entryContentExists = !!ec;
        results.entryContentHeight = ec ? ec.getBoundingClientRect().height : 0;

        // Check for key sections
        const sections = ['nao-hero', 'nao-latest', 'nao-value-props', 'nao-stats', 'nao-pillars', 'nao-topics', 'nao-about', 'nao-experiment', 'nao-cta'];
        sections.forEach(s => {
            const el = document.querySelector('.' + s);
            if (el) {
                const rect = el.getBoundingClientRect();
                const style = getComputedStyle(el);
                results[s] = {
                    exists: true,
                    visible: style.display !== 'none' && style.visibility !== 'hidden',
                    height: rect.height,
                    width: rect.width,
                    display: style.display,
                    bgColor: style.backgroundColor
                };
            } else {
                results[s] = {exists: false};
            }
        });

        // Check style tag
        const styleTags = document.querySelectorAll('.entry-content style');
        results.inlineStyleTags = styleTags.length;
        if (styleTags.length > 0) {
            results.styleTagContent = styleTags[0].textContent.substring(0, 200);
        }

        // Check if article-header is hidden
        const header = document.querySelector('.article-header');
        if (header) {
            results.articleHeader = {
                display: getComputedStyle(header).display,
                visible: getComputedStyle(header).display !== 'none'
            };
        }

        // Check sidebar
        const sidebar = document.querySelector('#sidebar');
        results.sidebarDisplay = sidebar ? getComputedStyle(sidebar).display : 'no-sidebar';

        // Check images
        const imgs = document.querySelectorAll('.entry-content img');
        results.imageCount = imgs.length;
        const brokenImgs = [];
        imgs.forEach((img, i) => {
            if (img.naturalWidth === 0 || !img.complete) {
                brokenImgs.push({src: img.src.substring(0, 80), index: i});
            }
        });
        results.brokenImages = brokenImgs;

        return results;
    });

    console.log(JSON.stringify(diag, null, 2));

    // Take screenshot of hero area
    await pg.screenshot({path:'c:/Users/tmizu/diag-top-hero.png', fullPage:false});

    // Scroll down to check other sections
    await pg.evaluate(() => window.scrollTo(0, 900));
    await new Promise(r => setTimeout(r, 1000));
    await pg.screenshot({path:'c:/Users/tmizu/diag-top-mid1.png', fullPage:false});

    await pg.evaluate(() => window.scrollTo(0, 2000));
    await new Promise(r => setTimeout(r, 1000));
    await pg.screenshot({path:'c:/Users/tmizu/diag-top-mid2.png', fullPage:false});

    await pg.evaluate(() => window.scrollTo(0, 3500));
    await new Promise(r => setTimeout(r, 1000));
    await pg.screenshot({path:'c:/Users/tmizu/diag-top-mid3.png', fullPage:false});

    await pg.evaluate(() => window.scrollTo(0, 5000));
    await new Promise(r => setTimeout(r, 1000));
    await pg.screenshot({path:'c:/Users/tmizu/diag-top-bottom.png', fullPage:false});

    await b.close();
})();
