const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});

    const pages = [
        ['home', 'https://nambei-oyaji.com/'],
        ['article-1065', 'https://nambei-oyaji.com/?p=1065'],
        ['category', 'https://nambei-oyaji.com/category/paraguay/'],
    ];

    for (const [name, url] of pages) {
        await pg.goto(url, {waitUntil:'domcontentloaded',timeout:30000});
        await new Promise(r => setTimeout(r, 10000));
        await pg.screenshot({path: 'c:/Users/tmizu/final-' + name + '.png', fullPage: false});

        const info = await pg.evaluate(() => ({
            title: document.title.substring(0, 60),
            sidebarDisplay: document.getElementById('sidebar') ? getComputedStyle(document.getElementById('sidebar')).display : 'none',
            sidebarSections: document.querySelectorAll('.nambei-sidebar-section').length,
            tocVisible: document.querySelector('.toc') ? getComputedStyle(document.querySelector('.toc')).display : 'none',
            hasHeader: document.querySelector('.nambei-header') !== null || document.querySelector('.nambei-nav') !== null
        }));
        console.log(name + ':', JSON.stringify(info));
    }

    await b.close();
})();
