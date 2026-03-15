const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 12000));

    // Force trigger animations for screenshot purposes
    await pg.evaluate(() => {
        document.querySelectorAll('.nao-anim').forEach(el => el.classList.add('nao-visible'));
    });
    await new Promise(r => setTimeout(r, 1000));

    const state = await pg.evaluate(() => ({
        sidebarDisplay: document.getElementById('sidebar') ? getComputedStyle(document.getElementById('sidebar')).display : 'none',
        latestPosts: document.querySelectorAll('.nao-post-card a, a.nao-post-card').length,
        popularPosts: document.querySelectorAll('.nao-popular-item').length,
        naoVisibleCount: document.querySelectorAll('.nao-visible').length,
        heroExists: document.querySelector('.nao-hero') !== null,
        themesExists: document.querySelector('.nao-themes') !== null,
        ctaExists: document.querySelector('.nao-cta') !== null,
        footerExists: document.querySelector('.nao-footer') !== null,
    }));
    console.log(JSON.stringify(state, null, 2));

    // Screenshots of each section
    await pg.screenshot({path: 'c:/Users/tmizu/v-hero.png'});

    await pg.evaluate(() => window.scrollTo(0, 800));
    await new Promise(r => setTimeout(r, 500));
    await pg.screenshot({path: 'c:/Users/tmizu/v-themes.png'});

    await pg.evaluate(() => window.scrollTo(0, 1500));
    await new Promise(r => setTimeout(r, 500));
    await pg.screenshot({path: 'c:/Users/tmizu/v-latest.png'});

    await pg.evaluate(() => window.scrollTo(0, 2300));
    await new Promise(r => setTimeout(r, 500));
    await pg.screenshot({path: 'c:/Users/tmizu/v-popular.png'});

    await pg.evaluate(() => window.scrollTo(0, 3200));
    await new Promise(r => setTimeout(r, 500));
    await pg.screenshot({path: 'c:/Users/tmizu/v-topics.png'});

    await pg.evaluate(() => window.scrollTo(0, 3800));
    await new Promise(r => setTimeout(r, 500));
    await pg.screenshot({path: 'c:/Users/tmizu/v-author.png'});

    await pg.evaluate(() => window.scrollTo(0, 4500));
    await new Promise(r => setTimeout(r, 500));
    await pg.screenshot({path: 'c:/Users/tmizu/v-cta.png'});

    await pg.evaluate(() => document.querySelector('.nao-footer').scrollIntoView());
    await new Promise(r => setTimeout(r, 500));
    await pg.screenshot({path: 'c:/Users/tmizu/v-footer.png'});

    await b.close();
})();
