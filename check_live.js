const puppeteer = require('puppeteer');
(async () => {
    const b = await puppeteer.launch({headless:'new'});
    const pg = await b.newPage();
    await pg.setViewport({width:1280,height:800});
    await pg.goto('https://nambei-oyaji.com/?p=1065', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 8000));
    const checks = await pg.evaluate(() => {
        return {
            hasCustomHeader: document.querySelector('.nambei-header') !== null,
            navRight: document.querySelector('.nambei-nav') !== null,
            sidebarSections: document.querySelectorAll('.nambei-sidebar-section').length,
            colorMarkers: document.querySelectorAll('span[style*="linear-gradient"]').length,
            snsHidden: !document.querySelector('.sns-share') || getComputedStyle(document.querySelector('.sns-share')).display === 'none',
            title: document.title.substring(0,60)
        };
    });
    console.log(JSON.stringify(checks, null, 2));
    await pg.screenshot({path:'c:/Users/tmizu/live-check-article.png', fullPage:false});

    // Also check category page
    await pg.goto('https://nambei-oyaji.com/category/paraguay/', {waitUntil:'domcontentloaded',timeout:30000});
    await new Promise(r => setTimeout(r, 8000));
    const cat = await pg.evaluate(() => {
        return {
            hasCustomHeader: document.querySelector('.nambei-header') !== null,
            sidebarSections: document.querySelectorAll('.nambei-sidebar-section').length,
            sidebarVisible: document.querySelector('#sidebar') ? getComputedStyle(document.querySelector('#sidebar')).display : 'no-sidebar',
            title: document.title.substring(0,60)
        };
    });
    console.log(JSON.stringify(cat, null, 2));
    await pg.screenshot({path:'c:/Users/tmizu/live-check-category.png', fullPage:false});

    await b.close();
})();
